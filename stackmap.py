# -*- coding: utf-8 -*-
"""StackMap class."""
from collections.abc import Mapping, MutableMapping
from reprlib import recursive_repr

# pylint: disable=too-many-ancestors

# see:
# https://github.com/python/cpython/blob/f393b2c588559162dc2e77f8079a42e48558870a/Lib/collections/__init__.py


class StackMap(MutableMapping):
    """
    Adapted from collections.ChainMap.
    StackMap groups multiple dicts (or other mappings) together
    to create a single, updateable view.
    The underlying mappings are stored in a list.
    That list can be accessed or updated using the *maps* property.
    Lookups search the underlying mappings starting from the last mapping
    in the *maps* until a key is found.
    Updates and deletions only operate on the **last** mapping in *maps*.
    """
    def __init__(self, *maps):
        '''Initialize a StackMap by setting *_maps* to the given mappings
        in reversed order. If no mappings are provided,
        a single empty dictionary is used.
        '''
        self._maps = list(reversed(maps)) or [{}]  # always at least one map

    @property
    def maps(self):
        """Ordered mappings."""
        return self._maps[::-1]

    def __missing__(self, key):
        raise KeyError(key)

    def __getitem__(self, key):
        for mapping in self._maps:
            try:
                # can't use 'key in mapping' with defaultdict
                return mapping[key]
            except KeyError:
                pass
        # support subclasses that define __missing__
        return self.__missing__(key)

    def get(self, key, default=None):
        return self[key] if key in self else default

    def __len__(self):
        # reuses stored hash values if possible
        return len(set().union(*self._maps))

    def __iter__(self):
        d = {}
        for mapping in reversed(self._maps):
            d.update(mapping)  # reuses stored hash values if possible
        return iter(d)

    def __contains__(self, key):
        return any(key in m for m in self._maps)

    def __bool__(self):
        return any(self._maps)

    @recursive_repr()
    def __repr__(self):
        return f'{self.__class__.__name__}({", ".join(map(repr, self.maps))})'

    @classmethod
    def fromkeys(cls, iterable, *args):
        'Create a StackMap with a single dict created from the iterable.'
        return cls(dict.fromkeys(iterable, *args))

    def copy(self):
        """
        New StackMap or subclass with a new copy of maps[-1] and
        refs to maps[:-1]
        """
        return self.__class__(*self.maps[:-1], self.maps[-1].copy())

    __copy__ = copy

    def push(self, m=None, left=False):
        """
        Append a new map to the the `maps` list.
        If no map is provided, an empty dict is used.
        In-place version of `new` method.
        If left, append a new map as the first mapping, to the left side of the
        `maps` list.
        """
        if m is None:
            m = {}
        if left:
            self._maps.append(m)
        else:
            self._maps.insert(0, m)

    def new(self, m=None, left=False):
        """
        New StackMap with a new map appended to the previous maps.
        If no map is provided, an empty dict is used.
        Like ChainSave new_child() and Django's Context.push()
        If left, append a new map as the first mapping, to the left side of the
        `maps` list.
        """
        if m is None:
            m = {}
        if left:
            return self.__class__(m, *self.maps)
        return self.__class__(*self.maps, m)

    @property
    def parents(self):  # like Django's Context.pop()
        'New StackMap from maps[:-1].'
        return self.__class__(*self.maps[:-1])

    def __setitem__(self, key, value):
        """Set item on last map."""
        self._maps[0][key] = value

    def __delitem__(self, key):
        """Delete item on last map."""
        try:
            del self._maps[0][key]
        except KeyError:
            raise KeyError(
                'Key not found in the last mapping: {!r}'.format(key))

    def popitem(self):
        """Remove and return an item pair from maps[-1].
        Raise KeyError is maps[-1] is empty."""
        try:
            return self._maps[0].popitem()
        except KeyError:
            raise KeyError('No keys found in the last mapping.')

    def pop(self, key, *args):  # pylint: disable=arguments-differ
        """Remove *key* from maps[-1] and return its value.
        Raise KeyError if *key* not in maps[-1]."""
        try:
            return self._maps[0].pop(key, *args)
        except KeyError:
            raise KeyError(
                'Key not found in the last mapping: {!r}'.format(key))

    def clear(self):
        'Clear maps[-1], leaving previous maps[:-1] intact.'
        self._maps[0].clear()

    def __ior__(self, other):
        # inplace update last mapping with other
        self._maps[0] |= other
        return self

    def __or__(self, other):
        # update last mapping with other
        # return new StackMap object
        if isinstance(other, Mapping):
            m = self._maps[0].copy()
            m.update(other)
            return self.__class__(*self.maps[:-1], m)
        return NotImplemented

    def __ror__(self, other):
        # update other using the mappings from the first to the last
        # return new mapping
        if isinstance(other, Mapping):
            m = dict(other)
            for child in reversed(self._maps):
                m.update(child)
            return self.__class__(m)
        return NotImplemented
