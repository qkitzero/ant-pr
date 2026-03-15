import sys

import requests

from .inputs import get_pr_number, get_repo, get_token

COMMENT_MARKER = "<!-- ant-pr-comment -->"
GITHUB_API_BASE = "https://api.github.com"
HTTP_OK = 200
HTTP_CREATED = 201


def _api_url(repo: str, *parts: str) -> str:
    return f"{GITHUB_API_BASE}/repos/{repo}/{'/'.join(parts)}"


def find_existing_comment(repo: str, pr_number: int, token: str) -> int | None:
    url = _api_url(repo, "issues", str(pr_number), "comments")
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != HTTP_OK:
        print(f"::error ::Failed to list comments: {response.text}")
        sys.exit(1)

    comments = response.json()
    for comment in comments:
        if COMMENT_MARKER in comment["body"]:
            return comment["id"]
    return None


def post_or_update_comment(comment: str) -> None:
    token = get_token()
    repo = get_repo()
    pr_number = get_pr_number()

    existing_comment_id = find_existing_comment(repo, pr_number, token)

    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }
    data = {"body": comment}

    if existing_comment_id:
        url = _api_url(repo, "issues", "comments", str(existing_comment_id))
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code != HTTP_OK:
            print(f"::error ::Failed to update comment: {response.text}")
            sys.exit(1)
    else:
        url = _api_url(repo, "issues", str(pr_number), "comments")
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != HTTP_CREATED:
            print(f"::error ::Failed to post comment: {response.text}")
            sys.exit(1)
