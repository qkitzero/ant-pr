import subprocess
import sys

from .inputs import get_base_sha, get_head_sha


def get_changed_files() -> list[str]:
    base = get_base_sha()
    head = get_head_sha()
    subprocess.run(
        [
            "git",
            "config",
            "--global",
            "--add",
            "safe.directory",
            "/github/workspace",
        ],
    )
    subprocess.run(["git", "fetch", "origin", base])
    subprocess.run(["git", "fetch", "origin", head])
    try:
        cmd = ["git", "diff", "--numstat", f"{base}...{head}"]
        output = subprocess.check_output(cmd).decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"::error ::Git command failed: {e}")
        sys.exit(1)
    return output
