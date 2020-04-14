# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
"""Tests module."""

from collections import ChainMap

import pytest

from stackmap import StackMap


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
    assert StackMap(*maps) == ChainMap(*maps[::-1])


def test_maps(maps):
    assert StackMap(*maps).maps == tuple(ChainMap(*maps[::-1]).maps[::-1])


def test_append(maps):
    sm = StackMap(*maps[:-1])
    sm.append(maps[-1])
    assert sm == StackMap(*maps)


def test_insert(maps):
    n = len(maps)
    sm = StackMap(*maps[:-1])
    sm.insert(n, maps[-1])
    assert sm == StackMap(*maps)


def test_delete(maps):
    sm = StackMap(*maps)
    sm.delete(-1)
    assert sm == StackMap(*maps[:-1])


def test_new(maps):
    assert StackMap(*maps).new() == ChainMap(*maps[::-1]).new_child()


def test_clear(maps):
    assert StackMap(*maps).clear() == ChainMap(*maps[::-1]).clear()
