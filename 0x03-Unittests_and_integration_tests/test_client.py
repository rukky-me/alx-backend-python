#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class in client.py.
Tests that the org property correctly fetches and returns
organization data using get_json without making real HTTP calls.
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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


"""
Unit tests for the GithubOrgClient._public_repos_url property.
"""


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient._public_repos_url property."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL."""
        # Create a fake payload/dictionary that mimics or looks like what GitHub would return for an organization.
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch GithubOrgClient.org property so it returns the fake payload
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload

            # Instantiate the client and access _public_repos_url
            client = GithubOrgClient("google")
            result = client._public_repos_url

            # Assert that the value returned is what we expect
            self.assertEqual(result, payload["repos_url"])

            # Also assert that the org property was accessed exactly once
            mock_org.assert_called_once()


"""
Unit tests for the GithubOrgClient.public_repos method.
"""


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.public_repos method."""

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns a list of repository names."""
        # Step 1: Define fake payload returned by get_json
        fake_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        # Step 2: Set up mock for get_json
        mock_get_json.return_value = fake_repos_payload

        # Step 3: Define a fake URL for the _public_repos_url property
        fake_url = "https://api.github.com/orgs/google/repos"

        # Step 4: Patch the _public_repos_url property
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_url:
            mock_public_url.return_value = fake_url

            # Step 5: Create instance and call public_repos()
            client = GithubOrgClient("google")
            result = client.public_repos()

            # Step 6: Verify result matches expected list of repo names
            expected_result = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_result)

            # Step 7: Ensure mocks were called exactly once
            mock_get_json.assert_called_once_with(fake_url)
            mock_public_url.assert_called_once()


"""
Unit tests for the GithubOrgClient.has_license method.
"""


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.has_license method."""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True if the repo has the correct license,
        otherwise False.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


"""
Integration tests for GithubOrgClient.public_repos.
This ensures the client works correctly end-to-end while mocking
only external HTTP requests.
"""


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up the test class by patching requests.get."""
        # Patch 'requests.get' globally in the 'client' module
        cls.get_patcher = patch('requests.get')

        # Start the patcher and get the mock
        mock_get = cls.get_patcher.start()

        # Configure the side effect: depending on the URL, return different payloads
        def side_effect(url):
            """Return different fake responses depending on URL."""
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                return Mock(json=lambda: cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return Mock(json=lambda: cls.repos_payload)

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected list of repo names."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license using has_license."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
