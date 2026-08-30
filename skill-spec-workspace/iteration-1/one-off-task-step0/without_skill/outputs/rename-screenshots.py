#!/usr/bin/env python3
"""
rename-screenshots.py

Renames macOS-style screenshot files like:
    Screenshot 2024-03-01 at 11.42.03 AM.png
to a consistent, zero-padded, chronologically-ordered sequence:
    screenshot-001.png
    screenshot-002.png
    ...

Usage:
    python3 rename-screenshots.py [FOLDER]              # dry run (default) - just prints the plan
    python3 rename-screenshots.py [FOLDER] --apply       # actually renames the files

If FOLDER is omitted, defaults to ~/Downloads.

Notes:
- Files are sorted by the timestamp encoded in the filename (not alphabetical
  order and not filesystem mtime), so the numbering reflects when each
  screenshot was actually taken.
- Any file that doesn't match the expected "Screenshot ... .ext" pattern is
  left untouched and reported separately - it will NOT be silently renamed
  or silently skipped without telling you.
- Renaming is done via a two-phase (stage-then-commit) process so that if
  any target filename would collide with an existing file, nothing is
  half-renamed.
- Width of the zero-padding is derived from the count of matched files
  (e.g. 40 files -> 3 digits: 001-040). If you run this again later with
  more files than fit the existing width, it will widen automatically.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# Matches: "Screenshot 2024-03-01 at 11.42.03 AM.png" (and PM variants,
# and screen recordings named "Screen Recording ... .mov" are ignored -
# only "Screenshot" is matched by design, see SKIP note below).
PATTERN = re.compile(
    r"^Screenshot (\d{4})-(\d{2})-(\d{2}) at (\d{1,2})\.(\d{2})\.(\d{2})\s*([AP]M)(?:\s*\(\d+\))?$",
    re.IGNORECASE,
)


def parse_timestamp(stem: str):
    m = PATTERN.match(stem)
    if not m:
        return None
    year, month, day, hour, minute, second, ampm = m.groups()
    hour = int(hour)
    if ampm.upper() == "PM" and hour != 12:
        hour += 12
    if ampm.upper() == "AM" and hour == 12:
        hour = 0
    try:
        return datetime(int(year), int(month), int(day), hour, int(minute), int(second))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", default=str(Path.home() / "Downloads"))
    ap.add_argument("--apply", action="store_true", help="actually rename files (default is dry-run/preview only)")
    ap.add_argument("--prefix", default="screenshot", help="output filename prefix (default: screenshot)")
    args = ap.parse_args()

    folder = Path(args.folder).expanduser()
    if not folder.is_dir():
        print(f"ERROR: folder not found: {folder}", file=sys.stderr)
        sys.exit(1)

    candidates = []
    skipped = []
    for path in folder.iterdir():
        if not path.is_file():
            continue
        ts = parse_timestamp(path.stem)
        if ts is None:
            if path.stem.lower().startswith("screenshot"):
                skipped.append(path)  # looks like a screenshot but didn't match the pattern
            continue
        candidates.append((ts, path))

    if not candidates:
        print("No files matching the expected 'Screenshot YYYY-MM-DD at HH.MM.SS AM/PM.ext' pattern were found.")
        if skipped:
            print("These files start with 'Screenshot' but didn't parse - check them manually:")
            for p in skipped:
                print(f"  - {p.name}")
        sys.exit(0)

    candidates.sort(key=lambda pair: pair[0])
    width = max(3, len(str(len(candidates))))

    plan = []
    for i, (ts, path) in enumerate(candidates, start=1):
        new_name = f"{args.prefix}-{i:0{width}d}{path.suffix.lower()}"
        plan.append((path, folder / new_name, ts))

    # Check for collisions with files not in the rename set
    existing = {p.name for p in folder.iterdir() if p.is_file()}
    being_renamed = {p.name for p, _, _ in plan}
    for _, new_path, _ in plan:
        if new_path.name in existing and new_path.name not in being_renamed:
            print(f"ERROR: target name already exists and isn't part of this rename: {new_path.name}", file=sys.stderr)
            sys.exit(1)

    print(f"Found {len(plan)} matching screenshot(s) in {folder}\n")
    for old_path, new_path, ts in plan:
        print(f"  {old_path.name}")
        print(f"    -> {new_path.name}   ({ts.isoformat(sep=' ')})")
    if skipped:
        print(f"\n{len(skipped)} file(s) look like screenshots but didn't match the naming pattern - left untouched:")
        for p in skipped:
            print(f"  - {p.name}")

    if not args.apply:
        print("\nDRY RUN - no files were changed. Re-run with --apply to perform the rename.")
        return

    # Two-phase rename to avoid any collision between old and new names
    # (e.g. if a file is already named "screenshot-003.png" for some reason).
    staged = []
    for old_path, new_path, _ in plan:
        tmp_path = old_path.with_name(old_path.name + ".renaming.tmp")
        old_path.rename(tmp_path)
        staged.append((tmp_path, new_path))

    for tmp_path, new_path in staged:
        tmp_path.rename(new_path)

    print(f"\nDone. Renamed {len(plan)} file(s).")


if __name__ == "__main__":
    main()
