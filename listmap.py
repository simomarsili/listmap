# -*- coding: utf-8 -*-
"""ListMap class."""
from collections.abc import Mapping, MutableMapping
from reprlib import recursive_repr


class ListMap(MutableMapping):
    """
    Adapted from the ``ChainMap`` class. A ``ListMap`` creates a single,
    updateable view of a stack of dicts or other mappings.

    The underlying list of mappings can be accessed and modified
    using the``maps`` property, and the ``append`` method.

    Main differences with ``ChainMap`` objects:

    * Lookups search the underlying mappings starting from the **last**
      mapping and going backward in the list of mappings until a key is
      found.
    * Updates and deletions of keys operate on the **last** mapping in the list
    * The ``append(m)`` method appends a new mapping ``m`` to the list
    * The ``extend(iterable)`` method extends the mappings by appending
      mappings from `iterable`

    Parameters
    ----------

    *maps : Mapping objects
    mapper : callable or None
        Apply the callable ``mapper`` to each of the original mappings.

    Notes
    -----
    ChainMap code:

    https://github.com/python/cpython/blob/3.8/Lib/collections/__init__.py

    """
    def __init__(self, *maps, mapper=None):
        """
        Initialize a ListMap by setting *_maps* to the given mappings
        in reversed order. If no mappings are provided,
        a single empty dictionary is used.
        """
        # TODO: func a generic callable
        # TODO: document `mapper` optional kwarg
        self.mapper = mapper
        if mapper is None:
            self._maps = list(reversed(maps)) or [{}]  # at least one map
        else:
            self._maps = list(reversed([mapper(m)
                                        for m in maps])) or [mapper()]

    @property
    def maps(self):
        """Ordered mappings."""
        return tuple(self._maps[::-1])

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
        'Create a ListMap with a single dict created from the iterable.'
        return cls(dict.fromkeys(iterable, *args))

    def copy(self):
        """
        New ListMap or subclass with a new copy of maps[-1] and
        refs to maps[:-1]
        """
        return self.__class__(*self.maps[:-1], self.maps[-1].copy())

    __copy__ = copy

    def append(self, m=None):
        """
        Append a new map to the the `maps` list.
        If no map is provided, an empty dict is used.
        In-place version of `new` method.
        """
        if m is None:
            m = {}
        if self.mapper is not None:
            m = self.mapper(m)
        self._maps.insert(0, m)

    def new_child(self, m=None):
        """
        New ListMap with a new map appended to the previous maps.
        If no map is provided, an empty dict is used.
        Like ChainSave new_child() and Django's Context.push()
        """
        if m is None:
            m = {}
        if self.mapper is not None:
            m = self.mapper(m)
        return self.__class__(*self.maps, m)

    @property
    def parents(self):  # like Django's Context.pop()
        'New ListMap from maps[:-1].'
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
        # return new ListMap object
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

    def __add__(self, other):
        if isinstance(other, Mapping):
            if isinstance(other, self.__class__):
                return self.__class__(*self.maps, *other.maps)
            if self.mapper is not None:
                other = self.mapper(other)
            return self.__class__(*self.maps, other)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Mapping):
            if isinstance(other, self.__class__):
                self.extend(other)
            else:
                self.append(other)
            return self
        raise NotImplementedError

    def extend(self, mappings):
        """Extend sequence of mappings by appending mappings from iterable."""
        if isinstance(mappings, self.__class__):
            mappings = mappings.maps
        for m in mappings:
            if self.mapper is not None:
                m = self.mapper(m)
            self.append(m)
