import os
import sys

import yaml

CONFIG_PATH = os.environ.get("INPUT_CONFIG-PATH", ".ant-pr.yml")


def load_config():
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


config = load_config()
LIMITS = config.get("limits", {})
LINE_LIMITS = LIMITS.get("lines", {})


def get_file_limit():
    return LIMITS.get("files", 0)


def get_line_limits(path):
    match = ""
    for key in LINE_LIMITS:
        if path.startswith(key) and len(key) > len(match):
            match = key

    if match:
        return LINE_LIMITS[match]

    return None
