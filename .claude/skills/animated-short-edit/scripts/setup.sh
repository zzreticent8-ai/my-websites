#!/usr/bin/env bash
# Prepare the HyperFrames student kit for an animated-short edit.
# Usage: setup.sh [kit_dir]
set -euo pipefail

KIT="${1:-${SCRATCH:-$PWD}/hyperframes-student-kit}"

if ! command -v ffmpeg >/dev/null || ! command -v ffprobe >/dev/null; then
  echo "Installing ffmpeg..."
  (apt-get install -y ffmpeg >/dev/null 2>&1) || (apt-get update >/dev/null 2>&1 && apt-get install -y ffmpeg >/dev/null 2>&1)
fi

if [ ! -d "$KIT/.git" ]; then
  git clone --depth 1 https://github.com/nateherkai/hyperframes-student-kit.git "$KIT"
fi
if [ ! -d "$KIT/node_modules/hyperframes" ]; then
  (cd "$KIT" && npm ci --no-audit --no-fund >/dev/null)
fi

python3 -c "import numpy" 2>/dev/null || pip install -q numpy

# HyperFrames needs a Chrome headless shell. Prefer a preinstalled Playwright one.
SHELL_BIN="$(find /opt/pw-browsers ~/.cache/ms-playwright -type f -name headless_shell 2>/dev/null | head -n1 || true)"
echo
echo "Kit: $KIT"
if [ -n "$SHELL_BIN" ]; then
  echo "Prefix renders with:"
  echo "  export PRODUCER_HEADLESS_SHELL_PATH=$SHELL_BIN HYPERFRAMES_BROWSER_PATH=$SHELL_BIN"
else
  echo "No headless shell found; run: (cd $KIT && npx hyperframes browser ensure)"
fi
