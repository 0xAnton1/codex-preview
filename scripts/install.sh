#!/usr/bin/env bash
set -euo pipefail

TARGET="codex"
PROJECT_DIR=""
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
RAW_BASE="${ANSI_PREVIEW_RAW_BASE:-https://raw.githubusercontent.com/0xAnton1/ansi-preview/main}"

usage() {
  cat <<'EOF'
Install ansi-preview for Codex, Claude, or both.

Examples:
  ./scripts/install.sh --target codex
  ./scripts/install.sh --target codex --codex-dir "$PWD/.codex"
  ./scripts/install.sh --target claude --project-dir /path/to/project
  ./scripts/install.sh --target both --project-dir "$PWD"

Remote one-liner:
  curl -fsSL https://raw.githubusercontent.com/0xAnton1/ansi-preview/main/scripts/install.sh | bash -s -- --target codex

Flags:
  --target codex|claude|both
  --project-dir PATH   Claude project root. Defaults to current directory for Claude installs.
  --codex-dir PATH     Codex home dir. Defaults to \$CODEX_HOME or ~/.codex
  -h, --help           Show this help
EOF
}

fetch() {
  local rel="$1"
  local out="$2"

  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "${RAW_BASE}/${rel}" -o "${out}"
    return
  fi

  if command -v wget >/dev/null 2>&1; then
    wget -qO "${out}" "${RAW_BASE}/${rel}"
    return
  fi

  echo "Need curl or wget to download ansi-preview files." >&2
  exit 1
}

install_codex() {
  local dest="${CODEX_DIR%/}/skills/ansi-preview"
  mkdir -p "${dest}/agents" "${dest}/references"

  fetch "SKILL.md" "${dest}/SKILL.md"
  fetch "agents/openai.yaml" "${dest}/agents/openai.yaml"
  fetch "references/patterns.md" "${dest}/references/patterns.md"

  echo "Installed Codex skill to ${dest}"
}

install_claude() {
  local root="${PROJECT_DIR:-$PWD}"
  mkdir -p "${root}/.claude/commands"

  fetch ".claude/commands/ansi-preview.md" "${root}/.claude/commands/ansi-preview.md"

  if [ -e "${root}/CLAUDE.md" ]; then
    fetch "CLAUDE.md" "${root}/.claude/ansi-preview-reference.md"
    echo "Installed Claude command to ${root}/.claude/commands/ansi-preview.md"
    echo "Existing ${root}/CLAUDE.md preserved."
    echo "Reference guidance saved to ${root}/.claude/ansi-preview-reference.md"
  else
    fetch "CLAUDE.md" "${root}/CLAUDE.md"
    echo "Installed Claude command to ${root}/.claude/commands/ansi-preview.md"
    echo "Installed ${root}/CLAUDE.md"
  fi
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --project-dir)
      PROJECT_DIR="${2:-}"
      shift 2
      ;;
    --codex-dir)
      CODEX_DIR="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

case "${TARGET}" in
  codex)
    install_codex
    ;;
  claude)
    install_claude
    ;;
  both)
    install_codex
    install_claude
    ;;
  *)
    echo "Invalid --target: ${TARGET}" >&2
    usage >&2
    exit 1
    ;;
esac
