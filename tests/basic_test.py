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
