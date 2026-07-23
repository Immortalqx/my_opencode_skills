#!/usr/bin/env bash
# Export a .drawio file to PNG with a hard 60s timeout.
# macOS / Linux only. On Windows, use export_drawio.ps1.
#
# Usage:
#   export_drawio.sh -i sketch.drawio [-o image_draft] [-s 1.5] [-t 60]

set -u

usage() {
  cat >&2 <<'USAGE'
Usage: export_drawio.sh -i <drawio> [-o <out-dir>] [-s <scale>] [-t <timeout-seconds>]
  -i  input .drawio file (required)
  -o  output directory (default: same as input)
  -s  export scale (default: 1.5)
  -t  hard timeout in seconds (default: 60)
USAGE
  exit 64
}

input=""
outdir=""
scale="1.5"
timeout="60"

while getopts ":i:o:s:t:h" opt; do
  case "$opt" in
    i) input="$OPTARG" ;;
    o) outdir="$OPTARG" ;;
    s) scale="$OPTARG" ;;
    t) timeout="$OPTARG" ;;
    h) usage ;;
    \?) echo "Unknown flag: -$OPTARG" >&2; usage ;;
    :) echo "Missing value for -$OPTARG" >&2; usage ;;
  esac
done
shift $((OPTIND - 1))

[ -n "$input" ] || { echo "Error: -i <drawio> is required" >&2; usage; }
[ -f "$input" ] || { echo "Error: drawio file not found: $input" >&2; exit 66; }

# Resolve to absolute path.
input="$(cd "$(dirname "$input")" && pwd)/$(basename "$input")"

if [ -z "$outdir" ]; then
  outdir="$(dirname "$input")"
else
  mkdir -p "$outdir" || { echo "Error: cannot create $outdir" >&2; exit 73; }
fi

base="$(basename "$input")"
base_noext="${base%.*}"
png="$outdir/$base_noext.png"

# Locate drawio CLI.
drawio=""
if [ -n "${DRAWIO_EXE:-}" ] && [ -x "${DRAWIO_EXE}" ] && [ -f "${DRAWIO_EXE}" ]; then
  drawio="${DRAWIO_EXE}"
elif cmd=$(command -v drawio 2>/dev/null) && [ -n "$cmd" ]; then
  drawio="$cmd"
elif [ -x "/Applications/draw.io.app/Contents/MacOS/draw.io" ]; then
  drawio="/Applications/draw.io.app/Contents/MacOS/draw.io"
elif [ -x "/Applications/draw.app/Contents/MacOS/draw.app" ]; then
  drawio="/Applications/draw.app/Contents/MacOS/draw.app"
fi

if [ -z "$drawio" ]; then
  echo "Error: drawio CLI not found." >&2
  echo "Set DRAWIO_EXE or install drawio:" >&2
  case "$(uname -s 2>/dev/null)" in
    Darwin) echo "  brew install --cask drawio" >&2 ;;
    Linux)
      echo "  Download AppImage from https://www.drawio.com/ and chmod +x" >&2
      echo "  Or: snap install drawio  /  yay -S drawio (Arch)" >&2
      ;;
  esac
  exit 69
fi

echo "drawio : $drawio"
echo "input  : $input"
echo "output : $png"
echo "scale  : $scale"
echo "timeout: ${timeout}s"

# Run export with hard timeout. Prefer GNU `timeout`; otherwise use an internal watchdog.
rc=0
if command -v timeout >/dev/null 2>&1; then
  timeout "${timeout}s" "$drawio" --export --format png --output "$png" --scale "$scale" "$input"
  rc=$?
elif command -v gtimeout >/dev/null 2>&1; then
  gtimeout "${timeout}s" "$drawio" --export --format png --output "$png" --scale "$scale" "$input"
  rc=$?
else
  # Pure-POSIX fallback: 1-second granularity via background watchdog.
  "$drawio" --export --format png --output "$png" --scale "$scale" "$input" &
  pid=$!
  (
    sleep "${timeout}" 2>/dev/null || true
    if kill -0 "$pid" 2>/dev/null; then
      kill -TERM "$pid" 2>/dev/null || true
      sleep 1
      kill -KILL "$pid" 2>/dev/null || true
    fi
  ) &
  killer=$!
  wait "$pid"
  rc=$?
  kill "$killer" 2>/dev/null || true
  wait "$killer" 2>/dev/null || true
fi

if [ "$rc" = 124 ]; then
  echo "Error: drawio PNG export timed out after ${timeout}s. Aborted." >&2
  rm -f "$png" 2>/dev/null || true
  exit 5
fi

if [ "$rc" != 0 ]; then
  echo "Error: drawio exited with code $rc" >&2
  rm -f "$png" 2>/dev/null || true
  exit 1
fi

if [ ! -s "$png" ]; then
  echo "Error: PNG was not produced at $png" >&2
  exit 1
fi

ls -la "$png" 2>/dev/null || true
echo "OK: $png"
