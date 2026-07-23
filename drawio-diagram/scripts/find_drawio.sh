#!/usr/bin/env bash
# Locate the drawio CLI binary on macOS or Linux.
# Prints absolute path on success. Exits 1 (with hints) on failure.

set -u

try_path() {
  if [ -n "$1" ] && [ -x "$1" ] && [ -f "$1" ]; then
    printf '%s\n' "$1"
    exit 0
  fi
}

# 1. Explicit override (env var or already exported).
try_path "${DRAWIO_EXE:-}"

# 2. PATH lookup (Linux binaries usually named `drawio`; macOS bundle uses .app — handled below).
if cmd=$(command -v drawio 2>/dev/null); then
  try_path "$cmd"
fi

# 3. Per-OS common locations.
case "$(uname -s 2>/dev/null)" in
  Darwin)
    try_path "/Applications/draw.io.app/Contents/MacOS/draw.io"
    try_path "/Applications/draw.app/Contents/MacOS/draw.app"
    try_path "$HOME/Applications/draw.io.app/Contents/MacOS/draw.io"
    try_path "$HOME/Applications/draw.app/Contents/MacOS/draw.app"
    ;;
  Linux)
    try_path "/usr/local/bin/drawio"
    try_path "/usr/bin/drawio"
    try_path "$HOME/.local/bin/drawio"
    try_path "/snap/bin/drawio"
    try_path "/opt/drawio/drawio"
    # AppImage glob in $HOME (e.g. ~/drawio-21.x.x/drawio-21.x.x.AppImage)
    if [ -d "$HOME" ]; then
      for f in "$HOME"/drawio-*/drawio-*.AppImage; do
        [ -f "$f" ] && try_path "$f"
      done
    fi
    # Wider AppImage scan in /opt and $HOME (best-effort, capped).
    if command -v find >/dev/null 2>&1; then
      while IFS= read -r f; do
        [ -n "$f" ] && try_path "$f"
      done < <(find "$HOME" "/opt" -maxdepth 5 -type f -name 'drawio*.AppImage' 2>/dev/null | head -n 20)
    fi
    ;;
esac

# 4. Surface actionable hints on failure.
echo "drawio CLI not found." >&2
echo "Set DRAWIO_EXE to the binary, or install drawio:" >&2
case "$(uname -s 2>/dev/null)" in
  Darwin)
    echo "  brew install --cask drawio    # Homebrew" >&2
    echo "  or download .dmg from https://www.drawio.com/" >&2
    ;;
  Linux)
    echo "  Download AppImage from https://www.drawio.com/ and chmod +x" >&2
    echo "  Or: snap install drawio  /  yay -S drawio (Arch)" >&2
    ;;
  *)
    echo "  See https://www.drawio.com/" >&2
    ;;
esac

exit 1
