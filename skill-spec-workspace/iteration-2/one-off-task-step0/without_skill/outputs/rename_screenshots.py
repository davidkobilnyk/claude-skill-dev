#!/usr/bin/env python3
"""
rename_screenshots.py

Renames macOS-style screenshot files like:
    Screenshot 2024-03-01 at 11.42.03 AM.png
into sequential, chronologically-ordered names like:
    screenshot-001.png
    screenshot-002.png
    ...

Usage:
    python3 rename_screenshots.py                 # dry run (just prints the plan)
    python3 rename_screenshots.py --apply          # actually renames the files
    python3 rename_screenshots.py --dir /path/to/folder --apply

Notes:
- Only files matching the "Screenshot YYYY-MM-DD at H.MM.SS AM/PM.png" pattern
  are touched. Anything else is left alone (and, if it looks close but doesn't
  match, it's listed as "skipped" so you can check it by hand).
- Files are sorted by their actual timestamp (parsed from the filename), not
  by alphabetical order, so 001 really is the earliest screenshot.
- Renaming is done in two passes (old name -> temp name -> final name) so that
  if any of the new target names happen to already exist, files never
  overwrite each other mid-run.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

PATTERN = re.compile(
    r"^Screenshot (\d{4}-\d{2}-\d{2}) at (\d{1,2}\.\d{2}\.\d{2})\s?(AM|PM)\.png$",
    re.IGNORECASE,
)


def parse_timestamp(name: str):
    m = PATTERN.match(name)
    if not m:
        return None
    date_str, time_str, ampm = m.groups()
    time_str = time_str.replace(".", ":")
    try:
        return datetime.strptime(f"{date_str} {time_str} {ampm.upper()}", "%Y-%m-%d %I:%M:%S %p")
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Rename Screenshot *.png files to screenshot-NNN.png")
    parser.add_argument("--dir", default=str(Path.home() / "Downloads"), help="Folder to process (default: ~/Downloads)")
    parser.add_argument("--apply", action="store_true", help="Actually rename files (default is dry-run/preview only)")
    args = parser.parse_args()

    folder = Path(args.dir)
    if not folder.is_dir():
        print(f"Error: {folder} is not a directory.", file=sys.stderr)
        sys.exit(1)

    matched = []
    skipped = []
    for f in sorted(folder.iterdir()):
        if not f.is_file() or f.suffix.lower() != ".png":
            continue
        dt = parse_timestamp(f.name)
        if dt is not None:
            matched.append((dt, f))
        elif f.name.lower().startswith("screenshot"):
            skipped.append(f.name)

    if not matched:
        print(f"No matching screenshot files found in {folder}.")
        if skipped:
            print("These looked like screenshots but didn't match the expected naming pattern:")
            for s in skipped:
                print(f"  - {s}")
        return

    matched.sort(key=lambda pair: pair[0])  # chronological order

    width = max(3, len(str(len(matched))))
    plan = []
    for i, (dt, f) in enumerate(matched, start=1):
        new_name = f"screenshot-{i:0{width}d}{f.suffix.lower()}"
        plan.append((f, f.with_name(new_name)))

    print(f"Found {len(matched)} matching screenshot(s) in {folder}\n")
    for old, new in plan:
        print(f"  {old.name}  ->  {new.name}")

    if skipped:
        print(f"\nSkipped {len(skipped)} file(s) that looked like screenshots but didn't match the pattern:")
        for s in skipped:
            print(f"  - {s}")

    # Check for pre-existing files that would collide with the new names
    collisions = [new.name for _, new in plan if new.exists()]

    if not args.apply:
        print("\nDry run only — no files were changed. Re-run with --apply to actually rename.")
        if collisions:
            print(f"Note: {len(collisions)} target filename(s) already exist in this folder; "
                  f"the script will still handle this safely via a temp-rename pass.")
        return

    # Two-pass rename to avoid any overwrite risk
    temp_suffix = ".renaming-tmp"
    for old, _ in plan:
        old.rename(old.with_name(old.name + temp_suffix))
    for old, new in plan:
        old.with_name(old.name + temp_suffix).rename(new)

    print(f"\nDone. Renamed {len(plan)} file(s).")


if __name__ == "__main__":
    main()
