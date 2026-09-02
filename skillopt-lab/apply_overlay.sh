#!/usr/bin/env bash
# Recreate the SkillOpt working tree used in this lab.
# Usage: ./apply_overlay.sh [target-dir]   (default: ./SkillOpt)
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
TARGET=${1:-./SkillOpt}
COMMIT=$(cat "$HERE/SKILLOPT_COMMIT")
if [ ! -d "$TARGET/.git" ]; then
  git clone https://github.com/microsoft/SkillOpt "$TARGET"
fi
cd "$TARGET"
git checkout --quiet "$COMMIT"
git apply "$HERE/overlay/skillopt-core.patch"
cp -r "$HERE/overlay/skillopt/envs/csvqa" skillopt/envs/
cp -r "$HERE/overlay/configs/csvqa" configs/
python3 -m pip install -e ".[claude]"
echo "Overlay applied at $COMMIT. Example:"
echo "  CLAUDE_CHAT_TOOLS='' python3 scripts/train.py --config configs/csvqa/proplogic_rep.yaml --out_root outputs/proplogic_rep"
