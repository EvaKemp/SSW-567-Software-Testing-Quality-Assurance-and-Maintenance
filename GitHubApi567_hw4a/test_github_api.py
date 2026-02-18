import unittest
from unittest.mock import patch, Mock

from github_api import (
    list_repos_and_commits,
    get_user_repos,
    get_commit_count,
    format_output,
    GitHubApiError,
)


def _mock_response(status_code=200, json_data=None, text="", headers=None):
    """Helper to build a mocked requests.Response-like object."""
    resp = Mock()
    resp.status_code = status_code
    resp.text = text
    resp.headers = headers or {}
    resp.json.return_value = json_data
    return resp


class TestGitHubApiMocking(unittest.TestCase):

    @patch("github_api.requests.Session.get")
    def test_get_user_repos_happy_path(self, mock_get):
        mock_get.return_value = _mock_response(
            200, json_data=[{"name": "Triangle567"}, {"name": "Square567"}]
        )

        repos = get_user_repos("testuser")  # no session passed; uses requests.Session internally
        self.assertEqual(repos, ["Triangle567", "Square567"])

        # Optional: verify correct endpoint was called
        called_url = mock_get.call_args[0][0]
        self.assertIn("https://api.github.com/users/testuser/repos", called_url)

    @patch("github_api.requests.Session.get")
    def test_get_commit_count_with_link_header_last_page(self, mock_get):
        mock_get.return_value = _mock_response(
            200,
            json_data=[{"sha": "abc"}],
            headers={
                "Link": '<https://api.github.com/repos/testuser/Triangle567/commits?per_page=1&page=34>; rel="last"'
            },
        )

        count = get_commit_count("testuser", "Triangle567")
        self.assertEqual(count, 34)

    @patch("github_api.requests.Session.get")
    def test_get_commit_count_no_link_header_0_commits(self, mock_get):
        mock_get.return_value = _mock_response(200, json_data=[], headers={})

        count = get_commit_count("testuser", "EmptyRepo")
        self.assertEqual(count, 0)

    @patch("github_api.requests.Session.get")
    def test_list_repos_and_commits_integration_using_mocks(self, mock_get):
        """
        list_repos_and_commits makes 1 call to /users/<id>/repos and then
        1 call per repo to /repos/<id>/<repo>/commits?per_page=1
        We'll return different mocked responses depending on the requested URL.
        """

        def side_effect(url, *args, **kwargs):
            if url.startswith("https://api.github.com/users/testuser/repos"):
                return _mock_response(200, json_data=[{"name": "Triangle567"}, {"name": "Square567"}])

            if url.startswith("https://api.github.com/repos/testuser/Triangle567/commits?per_page=1"):
                return _mock_response(200, json_data=[{"sha": "a"}], headers={"Link": '<x?page=10>; rel="last"'})

            if url.startswith("https://api.github.com/repos/testuser/Square567/commits?per_page=1"):
                return _mock_response(200, json_data=[{"sha": "b"}], headers={"Link": '<x?page=27>; rel="last"'})

            return _mock_response(404, json_data={"message": "Not Found"}, text="Not Found")

        mock_get.side_effect = side_effect

        items = list_repos_and_commits("testuser")
        self.assertEqual([(i.name, i.commits) for i in items], [("Triangle567", 10), ("Square567", 27)])

        out = format_output(items)
        self.assertIn("Repo: Triangle567 Number of commits: 10", out)
        self.assertIn("Repo: Square567 Number of commits: 27", out)

    @patch("github_api.requests.Session.get")
    def test_user_not_found(self, mock_get):
        mock_get.return_value = _mock_response(
            404, json_data={"message": "Not Found"}, text="Not Found"
        )

        with self.assertRaises(GitHubApiError):
            get_user_repos("nobody")

    @patch("github_api.requests.Session.get")
    def test_rate_limit_error(self, mock_get):
        mock_get.return_value = _mock_response(
            403,
            json_data={"message": "API rate limit exceeded"},
            text="API rate limit exceeded",
        )

        with self.assertRaises(GitHubApiError):
            get_user_repos("testuser")


if __name__ == "__main__":
    unittest.main()
    