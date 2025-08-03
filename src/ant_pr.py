import os
import subprocess
import sys

import requests
import yaml

CONFIG_PATH = os.environ.get("INPUT_CONFIG-PATH", ".ant-pr.yml")


def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"::error ::Config file not found at: {CONFIG_PATH}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"::error ::Error parsing YAML config: {e}")
        sys.exit(1)


RULES = load_config().get("rules", {})


def get_changed_files():
    base = os.environ["BASE_SHA"]
    head = os.environ["HEAD_SHA"]
    subprocess.run(
        ["git", "config", "--global", "--add", "safe.directory", "/github/workspace"]
    )
    subprocess.run(["git", "fetch", "origin", base])
    subprocess.run(["git", "fetch", "origin", head])
    cmd = ["git", "diff", "--numstat", f"{base}...{head}"]
    output = subprocess.check_output(cmd).decode().splitlines()
    return output


def match_rule(path):
    for key in RULES:
        if path.startswith(key):
            return RULES[key]
    return RULES[""]


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


def main():
    total_violations = 0
    output_lines = []

    changed = get_changed_files()
    for line in changed:
        added, deleted, file_path = line.strip().split("\t")
        added = int(added) if added != "-" else 0
        deleted = int(deleted) if deleted != "-" else 0
        total = added + deleted
        limit = match_rule(file_path)

        if total > limit:
            total_violations += 1
            output_lines.append(
                f"❌ `{file_path}` changed {total} lines (limit: {limit})"
            )
        else:
            output_lines.append(
                f"✅ `{file_path}` changed {total} lines (within {limit})"
            )

    output_lines.append(COMMENT_MARKER)
    title = "# 🐜 Ant PR\n\n"
    output_lines.append(title)
    comment = "\n".join(output_lines)
    post_or_update_comment(comment)

    if total_violations > 0:
        print("::error ::PR has files exceeding allowed change limits.")
        sys.exit(1)


if __name__ == "__main__":
    main()
