import os
import subprocess
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


def get_changed_files():
    base = os.environ["BASE_SHA"]
    head = os.environ["HEAD_SHA"]
    subprocess.run(["git", "config", "--global", "--add", "safe.directory", "/github/workspace"])
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

    print("\n".join(output_lines))

    if total_violations > 0:
        print("::error ::PR has files exceeding allowed change limits.")
        sys.exit(1)


if __name__ == "__main__":
    main()
