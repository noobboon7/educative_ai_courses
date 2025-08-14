#!/usr/bin/env python3
"""
Append timestamped entries to the repository CHANGELOG.md.

Usage examples:
  python scripts/log_changelog.py --category Added --message "Initialized rasa_demo scaffold"
  python scripts/log_changelog.py -c Operations -m "Installed uv and created .venv_rasa (Py 3.10)"
  python scripts/log_changelog.py -c Notes -m "Rasa 3.x needs Python < 3.12"

Categories supported: Added, Changed, Removed, Operations, Notes
The script will create today's date header (YYYY-MM-DD) and the category section
if they don't exist, then append the message as a bullet.

By default, it targets the repo root CHANGELOG.md relative to this script.
You can override with --changelog /path/to/CHANGELOG.md
"""
from __future__ import annotations
import argparse
import datetime as dt
import os
import sys
from typing import List

DEFAULT_CATEGORIES = ["Added", "Changed", "Removed", "Operations", "Notes"]

HEADER_TOP = (
    "# Changelog\n\n"
    "All notable changes to this gradio_chatbot workspace will be documented in this file.\n"
    "This log intentionally avoids sensitive information (no secrets, tokens, or personal data).\n\n"
)


def read_file(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def ensure_top_header(content: str) -> str:
    if content.strip().startswith("# Changelog"):
        return content
    if content.strip() == "":
        return HEADER_TOP
    # If a different header exists, keep it and do not inject ours.
    return content


def ensure_date_section(lines: List[str], date_str: str) -> List[str]:
    # Find a line that exactly matches the date header
    header = f"## {date_str}"
    if any(line.strip() == header for line in lines):
        return lines
    # Append date section at end with a separating newline if needed
    if lines and lines[-1].strip() != "":
        lines.append("")
    lines.append(header)
    lines.append("")
    return lines


def ensure_category_section(lines: List[str], date_str: str, category: str) -> List[str]:
    header = f"## {date_str}"
    cat_header = f"### {category}"

    # Locate date section start and the next top-level date header
    date_idx = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            date_idx = i
            break
    if date_idx is None:
        lines = ensure_date_section(lines, date_str)
        # Recompute date_idx
        for i, line in enumerate(lines):
            if line.strip() == header:
                date_idx = i
                break

    # Find the end of this date section (next line starting with '## ' or EOF)
    end_idx = len(lines)
    for i in range(date_idx + 1, len(lines)):
        if lines[i].startswith("## "):
            end_idx = i
            break

    # Check if category header exists within [date_idx, end_idx)
    for i in range(date_idx + 1, end_idx):
        if lines[i].strip() == cat_header:
            return lines

    # Insert category header just before end_idx, ensuring spacing
    insert_at = end_idx
    # Ensure there's a blank line before the category header
    if insert_at > 0 and lines[insert_at - 1].strip() != "":
        lines.insert(insert_at, "")
        insert_at += 1
    lines.insert(insert_at, cat_header)
    lines.insert(insert_at + 1, "")
    return lines


def append_bullet(lines: List[str], date_str: str, category: str, message: str) -> List[str]:
    header = f"## {date_str}"
    cat_header = f"### {category}"

    # Locate bounds of the category within the date section
    date_idx = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            date_idx = i
            break
    if date_idx is None:
        lines = ensure_date_section(lines, date_str)
        lines = ensure_category_section(lines, date_str, category)
        return append_bullet(lines, date_str, category, message)

    # Find end of date section
    end_idx = len(lines)
    for i in range(date_idx + 1, len(lines)):
        if lines[i].startswith("## "):
            end_idx = i
            break

    # Find category header within the date section
    cat_idx = None
    for i in range(date_idx + 1, end_idx):
        if lines[i].strip() == cat_header:
            cat_idx = i
            break
    if cat_idx is None:
        lines = ensure_category_section(lines, date_str, category)
        return append_bullet(lines, date_str, category, message)

    # Find insertion point: after the category header and any existing bullets under it,
    # but before the next category header or end of date section.
    insert_at = cat_idx + 1
    # Skip optional blank line right after header
    if insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    # Move past existing bullets
    while insert_at < end_idx and (lines[insert_at].lstrip().startswith("- ") or lines[insert_at].strip() == ""):
        insert_at += 1
    # Ensure a blank line before inserting if previous isn't blank and isn't a bullet group start
    if insert_at > 0 and lines[insert_at - 1].strip() != "":
        lines.insert(insert_at, "")
        insert_at += 1
    lines.insert(insert_at, f"- {message}")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Append an entry to CHANGELOG.md")
    parser.add_argument("--category", "-c", required=True, choices=DEFAULT_CATEGORIES,
                        help="Category under today's date section")
    parser.add_argument("--message", "-m", required=True, help="Message to append as a bullet")
    parser.add_argument("--date", "-d", default=dt.date.today().isoformat(),
                        help="Date for the section in YYYY-MM-DD (default: today)")
    parser.add_argument("--changelog", default=os.path.join(os.path.dirname(__file__), "..", "CHANGELOG.md"),
                        help="Path to CHANGELOG.md (default: repo root)")
    args = parser.parse_args()

    changelog_path = os.path.abspath(args.changelog)
    content = read_file(changelog_path)
    content = ensure_top_header(content)

    # Work with a list of lines ending with newline on writeback
    lines = content.splitlines()

    # Ensure date and category sections
    lines = ensure_date_section(lines, args.date)
    lines = ensure_category_section(lines, args.date, args.category)

    # Append the new bullet
    lines = append_bullet(lines, args.date, args.category, args.message)

    # Ensure trailing newline
    final = "\n".join(lines).rstrip() + "\n"
    write_file(changelog_path, final)

    print(f"Logged to {changelog_path}: [{args.date}] {args.category} - {args.message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

