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


"""
Unit tests for the utils.access_nested_map function.

The tests verify that access_nested_map returns the correct values for
various nested mapping inputs and paths.
"""


class TestAccessNestedMap(unittest.TestCase):
    """TestCase grouping tests for the access_nested_map utility function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: Any) -> None:
        """Ensure access_nested_map returns the expected value for each input."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple) -> None:
        """
        Ensure access_nested_map raises KeyError for missing keys.
        """
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)

        # The missing key should be the last one in the path tuple
        self.assertEqual(str(error.exception), f"'{path[-1]}'")


if __name__ == '__main__':
    unittest.main()
