import os
import subprocess


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
