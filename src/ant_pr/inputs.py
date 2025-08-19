import json
import os

EVENT_PATH = os.environ.get("GITHUB_EVENT_PATH")


def get_event():
    if not EVENT_PATH:
        return {}
    with open(EVENT_PATH) as f:
        return json.load(f)


event = get_event()


def get_base_sha():
    return event.get("pull_request", {}).get("base", {}).get("sha")


def get_head_sha():
    return event.get("pull_request", {}).get("head", {}).get("sha")


def get_pr_number():
    return event.get("pull_request", {}).get("number")


def get_repo():
    return os.environ.get("GITHUB_REPOSITORY")


def get_token():
    return os.environ.get("GITHUB_TOKEN")
