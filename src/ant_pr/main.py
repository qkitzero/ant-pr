import fnmatch
import sys

from .config import (
    find_matching_path_prefix,
    get_file_limit,
    get_ignore,
    get_line_limits,
)
from .git import get_changed_files
from .github import COMMENT_MARKER, post_or_update_comment

BINARY_FILE_MARKER = "-"
HEADER_HAPPY = "## 🐜The Ants are Happy!!🎉\n"
HEADER_ANGRY = "## 🐜The Ants are Angry!!🔥\n"


def parse_numstat_line(line: str) -> tuple[str, int, int]:
    added_str, deleted_str, file_path = line.strip().split("\t")
    added = int(added_str) if added_str != BINARY_FILE_MARKER else 0
    deleted = int(deleted_str) if deleted_str != BINARY_FILE_MARKER else 0
    return file_path, added, deleted


def format_limit_check(
    label: str, value: int, limit: int, unit: str = "lines"
) -> tuple[str, bool]:
    unit_str = f" {unit}" if unit else ""
    if value > limit:
        return f"❌ {label} `{value}`{unit_str} (limit: `{limit}`)", True
    return f"✅ {label} `{value}`{unit_str} (within `{limit}`)", False


def main() -> None:
    total_violations = 0
    output_lines = []

    changed_files = get_changed_files()
    ignore_patterns = get_ignore()
    ignored_files = []

    filtered_changed_files = []
    for line in changed_files:
        file_path, _, _ = parse_numstat_line(line)
        if any(fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns):
            ignored_files.append(file_path)
        else:
            filtered_changed_files.append(line)

    changed_files_count = len(filtered_changed_files)
    changed_files_count_limit = get_file_limit()

    if changed_files_count_limit:
        line, violated = format_limit_check(
            "Total changed files:",
            changed_files_count,
            changed_files_count_limit,
            unit="",
        )
        output_lines.append(line)
        if violated:
            total_violations += 1

    line_limits = get_line_limits()
    line_changes_by_path = {path: 0 for path in line_limits}
    unlimited_files = []

    for line in filtered_changed_files:
        file_path, added, deleted = parse_numstat_line(line)
        total = added + deleted

        matching_prefix = find_matching_path_prefix(file_path)

        is_root_only_match = matching_prefix == "" and "/" in file_path
        if is_root_only_match or matching_prefix not in line_limits:
            unlimited_files.append((file_path, total))
        else:
            line_changes_by_path[matching_prefix] += total

    for path, total in line_changes_by_path.items():
        if total > 0:
            limit = line_limits[path]
            display_path = path if path else "root"
            line, violated = format_limit_check(
                f"`{display_path}` changed", total, limit
            )
            output_lines.append(line)
            if violated:
                total_violations += 1

    for file_path, total in unlimited_files:
        output_lines.append(f"➖ `{file_path}` changed `{total}` lines (no limit set)")

    if ignored_files:
        output_lines.append("\nIgnored files:")
        for file_path in ignored_files:
            output_lines.append(f"➖ `{file_path}`")

    if total_violations == 0:
        output_lines.insert(0, HEADER_HAPPY)
    else:
        output_lines.insert(0, HEADER_ANGRY)

    output_lines.append(f"\n{COMMENT_MARKER}")
    comment = "\n".join(output_lines)
    print(comment)
    post_or_update_comment(comment)

    if total_violations > 0:
        print("::error ::PR has files or lines exceeding allowed limits.")
        sys.exit(1)


if __name__ == "__main__":
    main()
