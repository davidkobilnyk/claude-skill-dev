#!/usr/bin/env bash
# Count occurrences of the letter r/R in a text file's exact contents.
#
# Usage: count_r.sh <path-to-text-file>
#
# Treats stylized/decorative Unicode forms of R (fullwidth, mathematical
# bold/italic, superscript, etc.) as matches. Does NOT treat a letter
# carrying a diacritical mark (e.g. r-with-caron, "ř") as a match, since
# it is not in the character class below.
#
# LC_ALL=C.UTF-8 is required here, not optional: without an explicit
# UTF-8 locale, grep can silently return wrong (not erroring) results
# on non-ASCII input.
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: count_r.sh <path-to-text-file>" >&2
  exit 1
fi

LC_ALL=C.UTF-8 grep -oP '[rRＲｒ𝐑𝐫𝑅ʳ]' "$1" | wc -l
