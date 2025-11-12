#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.

The tests verify that access_nested_map returns the correct values for
various nested mapping inputs and paths.
"""

import unittest
from typing import Any
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map  # This is the function to be tested
from utils import get_json


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


"""
Unit tests for utils.get_json function.
This module verifies that get_json correctly fetches and returns JSON data
from a provided URL, while avoiding real network requests by mocking them.
"""


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url: str, test_payload: dict, mock_get: Mock) -> None:
        """
        This test that get_json returns expected JSON data and that
        requests.get is called once with the correct URL.
        """
        # Create a mock response object with json() returning our payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()
