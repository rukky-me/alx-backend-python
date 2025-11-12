#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py.
Tests that the org property correctly fetches and returns
organization data using get_json without making real HTTP calls.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


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
