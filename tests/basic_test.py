# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
"""Tests module."""

from collections import ChainMap
from types import MappingProxyType

import pytest

from listmap import ListMap


@pytest.fixture
def maps():
    return [
        {
            1: 2,
            3: 4,
            5: 6
        },
        {
            5: 7,
            6: 8,
            7: 9
        },
        {
            7: 10,
            8: 11,
            9: 12
        },
    ]


def test_init(maps):
    assert ListMap(*maps) == ChainMap(*maps[::-1])


def test_maps(maps):
    assert ListMap(*maps).maps == tuple(ChainMap(*maps[::-1]).maps[::-1])


def test_append(maps):
    sm = ListMap(*maps[:-1])
    sm.append(maps[-1])
    assert sm == ListMap(*maps)


def test_new_child(maps):
    assert ListMap(*maps).new_child() == ChainMap(*maps[::-1]).new_child()


def test_clear(maps):
    assert ListMap(*maps).clear() == ChainMap(*maps[::-1]).clear()


def test_extend(maps):
    sm = ListMap(*maps)
    sm.extend(maps)
    assert sm == ListMap(*maps, *maps)


def test_add_map(maps):
    m = {1: 100}
    sm = ListMap(*maps)
    assert sm + m == ListMap(*maps, m)


def test_add_stackmap(maps):
    sm = ListMap(*maps)
    assert sm + ListMap(*maps) == ListMap(*maps, *maps)


def test_iadd_map(maps):
    m = {1: 100}
    sm = ListMap(*maps)
    sm += m
    assert sm == ListMap(*maps, m)


def test_iadd_stackmap(maps):
    sm = ListMap(*maps)
    sm += ListMap(*maps)
    assert sm == ListMap(*maps, *maps)


def test_init_mapper(maps):
    assert ListMap(*maps, mapper=MappingProxyType) == ChainMap(*maps[::-1])


def test_append_mapper(maps):
    sm = ListMap(*maps[:-1], mapper=MappingProxyType)
    sm.append(maps[-1])
    assert sm == ListMap(*maps)


def test_extend_mapper(maps):
    sm = ListMap(*maps, mapper=MappingProxyType)
    sm.extend(maps)
    assert sm == ListMap(*maps, *maps)
