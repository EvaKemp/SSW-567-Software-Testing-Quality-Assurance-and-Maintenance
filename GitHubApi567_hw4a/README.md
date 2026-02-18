[![CircleCI](https://dl.circleci.com/status-badge/img/gh/EvaKemp/SSW-567-Software-Testing-Quality-Assurance-and-Maintenance/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/EvaKemp/SSW-567-Software-Testing-Quality-Assurance-and-Maintenance/tree/main)

# HW4a – GitHub API

This program takes a GitHub user ID and outputs each repository name and the number of commits in that repository.

## How to run (example)

```bash
python -c "from github_api import list_repos_and_commits, format_output; print(format_output(list_repos_and_commits('richkempinski')))"
