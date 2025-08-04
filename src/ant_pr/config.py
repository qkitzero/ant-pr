import os
import sys

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


def match_rule(path):
    for key in RULES:
        if path.startswith(key):
            return RULES[key]
    return RULES.get("default", 0)
