import sys

from .config import match_rule
from .git import get_changed_files
from .github import COMMENT_MARKER, post_or_update_comment


def main():
    total_violations = 0
    output_lines = ["# 🐜 Ant PR\n\n"]

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
    comment = "\n".join(output_lines)
    post_or_update_comment(comment)

    if total_violations > 0:
        print("::error ::PR has files exceeding allowed change limits.")
        sys.exit(1)


if __name__ == "__main__":
    main()
