import os
import sys
from functools import lru_cache

import yaml

CONFIG_PATH = os.environ.get("INPUT_CONFIG-PATH", ".ant-pr.yml")


def load_config() -> dict:
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
            if not isinstance(config, dict):
                return {}
            return config
    except FileNotFoundError:
        return {}
    except yaml.YAMLError as e:
        print(f"::error ::Error parsing YAML config: {e}")
        sys.exit(1)


@lru_cache(maxsize=1)
def _get_config() -> dict:
    return load_config()


def get_line_limits() -> dict:
    return _get_config().get("limits", {}).get("lines", {})


def get_file_limit() -> int:
    return _get_config().get("limits", {}).get("files", 0)


def get_ignore() -> list[str]:
    return _get_config().get("ignore", [])


def find_matching_path_prefix(path: str) -> str:
    match = ""
    for key in get_line_limits():
        if path.startswith(key) and len(key) > len(match):
            match = key
    return match
