import re
from dataclasses import dataclass
from typing import List, Optional

import requests


class GitHubApiError(Exception):
    """Raised when the GitHub API call fails or returns unexpected data."""


@dataclass(frozen=True)
class RepoCommits:
    name: str
    commits: int


def _get_json(session: requests.Session, url: str, timeout: float = 10.0):
    try:
        resp = session.get(url, timeout=timeout, headers={"Accept": "application/vnd.github+json"})
    except requests.RequestException as e:
        raise GitHubApiError(f"Network error calling GitHub: {e}") from e

    if resp.status_code == 403 and "rate limit" in resp.text.lower():
        raise GitHubApiError("GitHub rate limit exceeded (HTTP 403). Try again later.")

    if resp.status_code == 404:
        raise GitHubApiError("User or resource not found (HTTP 404).")

    if resp.status_code != 200:
        raise GitHubApiError(f"GitHub API error: HTTP {resp.status_code}: {resp.text[:200]}")

    try:
        return resp.json(), resp.headers
    except ValueError as e:
        raise GitHubApiError("GitHub returned invalid JSON.") from e


def _parse_last_page(link_header: str) -> Optional[int]:
    if not link_header:
        return None

    parts = link_header.split(",")
    for p in parts:
        if 'rel="last"' in p:
            match = re.search(r"[?&]page=(\d+)", p)
            if match:
                return int(match.group(1))
    return None


def get_user_repos(user_id: str, session: Optional[requests.Session] = None) -> List[str]:
    if not user_id or not user_id.strip():
        raise ValueError("user_id must be a non-empty string")

    session = session or requests.Session()
    url = f"https://api.github.com/users/{user_id}/repos"
    data, _headers = _get_json(session, url)

    if not isinstance(data, list):
        raise GitHubApiError("Unexpected response: repos endpoint did not return a list.")

    repo_names = []
    for obj in data:
        if isinstance(obj, dict) and "name" in obj:
            repo_names.append(obj["name"])
    return repo_names


def get_commit_count(user_id: str, repo: str, session: Optional[requests.Session] = None) -> int:
    if not user_id or not repo:
        raise ValueError("user_id and repo must be provided")

    session = session or requests.Session()

    # per_page=1 => last page number equals commit count
    url = f"https://api.github.com/repos/{user_id}/{repo}/commits?per_page=1"
    data, headers = _get_json(session, url)

    if not isinstance(data, list):
        raise GitHubApiError("Unexpected response: commits endpoint did not return a list.")

    link = headers.get("Link", "")
    last_page = _parse_last_page(link)

    if last_page is not None:
        return last_page

    # For 0 or 1 commit, Link header often not present
    return len(data)


def list_repos_and_commits(user_id: str, session: Optional[requests.Session] = None) -> List[RepoCommits]:
    session = session or requests.Session()

    repos = get_user_repos(user_id, session=session)

    results: List[RepoCommits] = []
    for repo in repos:
        count = get_commit_count(user_id, repo, session=session)
        results.append(RepoCommits(name=repo, commits=count))

    return results


def format_output(items: List[RepoCommits]) -> str:
    return "\n".join([f"Repo: {i.name} Number of commits: {i.commits}" for i in items])