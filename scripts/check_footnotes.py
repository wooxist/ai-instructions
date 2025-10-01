#!/usr/bin/env python3
import re
from pathlib import Path
import sys

BOOK_DIR = Path(__file__).resolve().parent.parent / "book"

FN_DEF_RE = re.compile(r"^\[\^(\d+)\]:\s")
FN_REF_RE = re.compile(r"\[\^(\d+)\]")

def check_file(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Collect footnote definitions and references
    defs = []
    refs = []
    def_lines = []
    for i, line in enumerate(lines):
        mdef = FN_DEF_RE.match(line)
        if mdef:
            n = int(mdef.group(1))
            defs.append(n)
            def_lines.append(i)
        # collect refs but ignore lines that are definitions
        for m in FN_REF_RE.finditer(line):
            # skip if this is the definition line start
            if mdef and m.start() == 0:
                continue
            refs.append(int(m.group(1)))

    errs = []

    # Enforce numeric-only scheme: any non-numeric refs like [^word] are flagged
    if re.search(r"\[\^[^\d\]]+\]", text):
        errs.append("Found non-numeric footnote reference (use [^1], [^2], ...)")

    if defs:
        # Find sections
        try:
            ref_idx = next(i for i, l in enumerate(lines) if l.strip() == "## 참고 자료")
        except StopIteration:
            errs.append("Footnotes defined but '## 참고 자료' section not found")
            ref_idx = None

        # last '---' after 참고 자료
        sep2_idx = None
        if ref_idx is not None:
            for i in range(ref_idx + 1, len(lines)):
                if lines[i].strip() == "---":
                    sep2_idx = i
            if sep2_idx is None:
                errs.append("Expected '---' after '## 참고 자료' before footnotes")

        # status (should come after footnotes)
        status_idx = None
        for i, l in enumerate(lines):
            if l.strip().startswith("**상태:**"):
                status_idx = i
                break

        first_def = def_lines[0]
        if sep2_idx is not None and first_def <= sep2_idx:
            errs.append("Footnotes must appear after the second '---' following '## 참고 자료'")
        if status_idx is not None and any(dl > status_idx for dl in def_lines):
            errs.append("Footnote definitions must appear before 상태 block")

        # Reference/definition consistency (warnings)
        undefined = sorted(set(refs) - set(defs))
        unused = sorted(set(defs) - set(refs))
        if undefined:
            errs.append(f"Undefined footnote references: {undefined}")
        if unused:
            # not fatal, but report
            errs.append(f"Unused footnote definitions: {unused}")

        # Optional: ensure numbering starts at 1 and increases without gaps
        if defs:
            seq = sorted(set(defs))
            expected = list(range(1, max(seq) + 1))
            if seq != expected:
                errs.append(f"Footnote numbering should be contiguous from 1 (found {seq})")

    return errs


def main():
    if not BOOK_DIR.exists():
        print("ERROR: book/ directory not found", file=sys.stderr)
        sys.exit(2)
    files = sorted(p for p in BOOK_DIR.glob("*.md") if p.is_file())
    had_error = False
    for path in files:
        errs = check_file(path)
        if errs:
            had_error = True
            print(f"ERROR: {path}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK: {path}")
    sys.exit(1 if had_error else 0)

if __name__ == "__main__":
    main()

