import unittest

from github_api import (
    list_repos_and_commits,
    get_user_repos,
    get_commit_count,
    format_output,
    GitHubApiError,
)


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text="", headers=None):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._json_data


class FakeSession:
    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def get(self, url, timeout=None, headers=None):
        self.calls.append(url)
        for prefix, response in self.routes.items():
            if url.startswith(prefix):
                return response
        return FakeResponse(status_code=404, json_data={"message": "Not Found"}, text="Not Found")


class TestGitHubApi(unittest.TestCase):
    def test_get_user_repos_happy_path(self):
        routes = {
            "https://api.github.com/users/testuser/repos": FakeResponse(
                200, json_data=[{"name": "Triangle567"}, {"name": "Square567"}]
            )
        }
        session = FakeSession(routes)
        repos = get_user_repos("testuser", session=session)
        self.assertEqual(repos, ["Triangle567", "Square567"])

    def test_get_commit_count_with_link_header_last_page(self):
        routes = {
            "https://api.github.com/repos/testuser/Triangle567/commits?per_page=1": FakeResponse(
                200,
                json_data=[{"sha": "abc"}],
                headers={
                    "Link": '<https://api.github.com/repos/testuser/Triangle567/commits?per_page=1&page=34>; rel="last"'
                },
            )
        }
        session = FakeSession(routes)
        count = get_commit_count("testuser", "Triangle567", session=session)
        self.assertEqual(count, 34)

    def test_get_commit_count_no_link_header_0_commits(self):
        routes = {
            "https://api.github.com/repos/testuser/EmptyRepo/commits?per_page=1": FakeResponse(
                200, json_data=[], headers={}
            )
        }
        session = FakeSession(routes)
        count = get_commit_count("testuser", "EmptyRepo", session=session)
        self.assertEqual(count, 0)

    def test_list_repos_and_commits_integration_using_fakes(self):
        routes = {
            "https://api.github.com/users/testuser/repos": FakeResponse(
                200, json_data=[{"name": "Triangle567"}, {"name": "Square567"}]
            ),
            "https://api.github.com/repos/testuser/Triangle567/commits?per_page=1": FakeResponse(
                200, json_data=[{"sha": "a"}], headers={"Link": '<x?page=10>; rel="last"'}
            ),
            "https://api.github.com/repos/testuser/Square567/commits?per_page=1": FakeResponse(
                200, json_data=[{"sha": "b"}], headers={"Link": '<x?page=27>; rel="last"'}
            ),
        }
        session = FakeSession(routes)
        items = list_repos_and_commits("testuser", session=session)
        self.assertEqual([(i.name, i.commits) for i in items], [("Triangle567", 10), ("Square567", 27)])

        out = format_output(items)
        self.assertIn("Repo: Triangle567 Number of commits: 10", out)
        self.assertIn("Repo: Square567 Number of commits: 27", out)

    def test_user_not_found(self):
        routes = {
            "https://api.github.com/users/nobody/repos": FakeResponse(
                404, json_data={"message": "Not Found"}, text="Not Found"
            )
        }
        session = FakeSession(routes)
        with self.assertRaises(GitHubApiError):
            get_user_repos("nobody", session=session)

    def test_rate_limit_error(self):
        routes = {
            "https://api.github.com/users/testuser/repos": FakeResponse(
                403, json_data={"message": "API rate limit exceeded"}, text="API rate limit exceeded"
            )
        }
        session = FakeSession(routes)
        with self.assertRaises(GitHubApiError):
            get_user_repos("testuser", session=session)


if __name__ == "__main__":
    unittest.main()
    