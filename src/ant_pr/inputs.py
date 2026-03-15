import json
import os
from functools import lru_cache

EVENT_PATH = os.environ.get("GITHUB_EVENT_PATH")


@lru_cache(maxsize=1)
def get_event() -> dict:
    if not EVENT_PATH:
        return {}
    with open(EVENT_PATH) as f:
        return json.load(f)


def get_base_sha() -> str | None:
    return get_event().get("pull_request", {}).get("base", {}).get("sha")


def get_head_sha() -> str | None:
    return get_event().get("pull_request", {}).get("head", {}).get("sha")


def get_pr_number() -> int | None:
    return get_event().get("pull_request", {}).get("number")


def get_repo() -> str | None:
    return os.environ.get("GITHUB_REPOSITORY")


def get_token() -> str | None:
    return os.environ.get("GITHUB_TOKEN")
