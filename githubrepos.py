#!/usr/bin/env python3

"""A simple script retrieve & show all GitHub repos of a username

Usage:
	$ python3 githubrepos.py username
	
For example, with username "duyhdb":
	$ python3 githubrepos.py duyhdb
"""

import argparse

import requests
from typing import Generator, List

Resp = requests.models.Response


def get_pages(username: str) -> Generator[List[dict], None, None]:
    """Yield all pages containing repos from GitHub API

    :param username: GitHub username
    :yield: GitHub repos page
    """
    client = requests.Session()
    page: Resp = client.get(f"https://api.github.com/users/{username}/repos")
    yield page.json()

    # Paging when GitHub user has more than 30 repos
    # https://docs.github.com/en/rest/reference/repos
    if page.links.get('next'):
        while 'next' in page.headers.get('link'):
            page = client.get(page.links['next']['url'])
            yield page.json()

    client.close()


def extract_repos_name(username: str) -> List[str]:
    """Return the name of each repository from each page

    :param username: GitHub username
    :rtype list:
    """
    repos_name = []
    for page in get_pages(username):
        for repo in page:
            repos_name.append(repo['name'])

    return repos_name


def solve(input_data: str) -> List[str]:
    """Function `solve` for `test` purpose

    Return the same value in both `solve` and `extract_repos_name`

    :param input_data: GitHub username
    :rtype list:
    """
    result = extract_repos_name(input_data)

    return result


def main() -> None:
    # Parse positional args
    parser = argparse.ArgumentParser(
        description="Find GitHub repos by username"
    )
    parser.add_argument(
        'username',
        type=str,
        help="username of GitHub account you want to find.",
    )
    args = parser.parse_args()
    user = args.username

    # Show repos name
    for index, name in enumerate(solve(user), start=1):
        print(index, name)


if __name__ == "__main__":
    main()
