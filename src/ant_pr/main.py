import sys

from .config import get_file_limit, get_line_limits
from .git import get_changed_files
from .github import COMMENT_MARKER, post_or_update_comment


def main():
    total_violations = 0
    output_lines = []

    changed_files = get_changed_files()
    changed_files_count = len(changed_files)
    changed_files_count_limit = get_file_limit()

    if changed_files_count_limit:
        if changed_files_count > changed_files_count_limit:
            total_violations += 1
            output_lines.append(
                f"❌ Total changed files: `{changed_files_count}` (limit: `{changed_files_count_limit}`)"
            )
        else:
            output_lines.append(
                f"✅ Total changed files: `{changed_files_count}` (within `{changed_files_count_limit}`)"
            )

    for line in changed_files:
        added, deleted, file_path = line.strip().split("\t")
        added = int(added) if added != "-" else 0
        deleted = int(deleted) if deleted != "-" else 0
        total = added + deleted
        limit = get_line_limits(file_path)

        if limit:
            if total > limit:
                total_violations += 1
                output_lines.append(
                    f"❌ `{file_path}` changed `{total}` lines (limit: `{limit}`)"
                )
            else:
                output_lines.append(
                    f"✅ `{file_path}` changed `{total}` lines (within `{limit}`)"
                )
        else:
            output_lines.append(
                f"➖ `{file_path}` changed `{total}` lines (no limit set)"
            )

    if total_violations == 0:
        output_lines.insert(0, "## 🐜 All checks passed 🐜\n")
    else:
        output_lines.insert(0, "## 🐜 Checks failed 🐜\n")

    output_lines.append(f"\n{COMMENT_MARKER}")
    comment = "\n".join(output_lines)
    print(comment)
    post_or_update_comment(comment)

    if total_violations > 0:
        print("::error ::PR has files or lines exceeding allowed limits.")
        sys.exit(1)


if __name__ == "__main__":
    main()
