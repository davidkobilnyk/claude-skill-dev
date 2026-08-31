#!/usr/bin/env python3
"""Count occurrences of the letter r/R in a text file's exact contents.

Usage: count_r.py <path-to-text-file>

Treats stylized/decorative Unicode forms of R (fullwidth, mathematical
bold/italic, superscript, etc.) as matches, since NFKD normalization
decomposes them to a bare base letter with nothing else attached.
Does NOT treat a letter carrying a diacritical mark (e.g. r-with-caron,
"ř") as a match, since NFKD normalization decomposes those into the
base letter followed by a combining mark, which this script detects
and excludes.
"""
import sys
import unicodedata


def count_r(text: str) -> int:
    normalized = unicodedata.normalize("NFKD", text)
    count = 0
    n = len(normalized)
    i = 0
    while i < n:
        ch = normalized[i]
        if ch in ("r", "R"):
            if i + 1 < n and unicodedata.combining(normalized[i + 1]) != 0:
                # Base letter followed by a combining mark -- this was a
                # distinct accented letter (e.g. ř), not a plain r/R.
                # Skip it and any combining marks that follow it.
                i += 1
                while i < n and unicodedata.combining(normalized[i]) != 0:
                    i += 1
                continue
            count += 1
        i += 1
    return count


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: count_r.py <path-to-text-file>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8", newline="") as f:
        text = f.read()
    print(count_r(text))


if __name__ == "__main__":
    main()
