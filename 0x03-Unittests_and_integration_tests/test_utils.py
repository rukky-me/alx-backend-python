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
from client import GithubOrgClient
from utils import get_json
from utils import memoize


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


"""
Unit tests for utils.memoize decorator.
This test verifies that the memoize decorator correctly caches a method’s
result so that subsequent calls do not re-execute the original method.
"""


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches method results properly."""

        class TestClass:
            """Simple test class to verify memoization behavior."""

            def a_method(self) -> int:
                """A dummy method that returns a fixed number."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Method decorated with memoize that calls a_method."""
                return self.a_method()

        # Patch a_method to track how many times it is called
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # First call - should execute a_method once
            result1 = obj.a_property()
            # Second call - should use cached result, no new call to a_method
            result2 = obj.a_property()

            # Assert both results are the same
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was called only once
            mock_method.assert_called_once()


"""
Unit tests for the GithubOrgClient class in client.py.
Tests that the org property correctly fetches and returns
organization data using get_json without making real HTTP calls.
"""


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, expected_payload: dict, mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns expected data and that
        get_json is called once with the correct URL.
        """
        # Arrange: Mock get_json to return expected_payload
        mock_get_json.return_value = expected_payload

        # Act: Create client instance and access .org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json called correctly and result matches
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)


if __name__ == '__main__':
    unittest.main()
