#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.

The tests verify that access_nested_map returns the correct values for
various nested mapping inputs and paths.
"""

import unittest
from typing import Any
from parameterized import parameterized
from utils import access_nested_map  # This is the function to be tested


class TestAccessNestedMap(unittest.TestCase):
    """TestCase grouping tests for the access_nested_map utility function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Ensure access_nested_map returns
        the expected value for each input.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
