#!/usr/bin/env python3
import re
from pathlib import Path
import sys

BOOK_DIR = Path(__file__).resolve().parent.parent / "book"

STATUS_RE = re.compile(r"^\*\*상태:\*\*\s+v(\d+)-(draft|released)\s*$")
START_RE = re.compile(r"^\*\*작성 시작일:\*\*\s+\d{4}-\d{2}-\d{2}\s*$")

def check_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    errs = []

    # Disallow per-chapter change log headings
    for i, l in enumerate(lines):
        if l.strip() == "## 변경 이력":
            errs.append(f"Line {i+1}: '## 변경 이력' section is not allowed (track in VCS)")
            break

    status_idx = None
    start_idx = None
    for i in range(len(lines)-1, -1, -1):
        if status_idx is None and STATUS_RE.match(lines[i]):
            status_idx = i
        if start_idx is None and START_RE.match(lines[i]):
            start_idx = i
        if status_idx is not None and start_idx is not None:
            break

    if status_idx is None:
        errs.append("Missing or invalid status line (expected '**상태:** v{n}-{draft|released}')")
    if start_idx is None:
        errs.append("Missing or invalid start date line (expected '**작성 시작일:** YYYY-MM-DD')")
    if status_idx is not None and start_idx is not None and not (status_idx > start_idx or start_idx > status_idx):
        # order not enforced strictly; both must exist near end
        pass

    return errs

def main():
    files = sorted(p for p in BOOK_DIR.glob("*.md") if p.is_file() and p.name != "index.md")
    had_err = False
    for p in files:
        errs = check_file(p)
        if errs:
            had_err = True
            print(f"ERROR: {p}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK: {p}")
    sys.exit(1 if had_err else 0)

if __name__ == "__main__":
    main()
