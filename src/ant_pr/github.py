import os
import sys

import requests

COMMENT_MARKER = "<!-- ant-pr-comment -->"


def find_existing_comment(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"::error ::Failed to list comments: {response.text}")
        return None

    comments = response.json()
    for comment in comments:
        if COMMENT_MARKER in comment["body"]:
            return comment["id"]
    return None


def post_or_update_comment(comment):
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PULL_REQUEST_NUMBER"]

    existing_comment_id = find_existing_comment(repo, pr_number, token)

    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }
    data = {"body": comment}

    if existing_comment_id:
        url = (
            f"https://api.github.com/repos/{repo}/issues/comments/{existing_comment_id}"
        )
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"::error ::Failed to update comment: {response.text}")
            sys.exit(1)
    else:
        url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 201:
            print(f"::error ::Failed to post comment: {response.text}")
            sys.exit(1)
