#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_URL="https://github.com/dexterqiu-collab/life-coach.git"
TARGET_KIND="${1:-auto}"
FORCE_INSTALL="false"

if [[ "${2:-}" == "--force" || "${1:-}" == "--force" ]]; then
  FORCE_INSTALL="true"
  if [[ "${1:-}" == "--force" ]]; then
    TARGET_KIND="auto"
  fi
fi

case "$TARGET_KIND" in
  auto|codex|workbuddy|codebuddy|all) ;;
  *)
    echo "Usage: bash scripts/install.sh [auto|codex|workbuddy|codebuddy|all] [--force]" >&2
    exit 2
    ;;
esac

SCRIPT_DIRECTORY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd "$SCRIPT_DIRECTORY/.." && pwd)"
TEMP_DIRECTORY=""

cleanup() {
  if [[ -n "$TEMP_DIRECTORY" && -d "$TEMP_DIRECTORY" ]]; then
    rm -rf "$TEMP_DIRECTORY"
  fi
}
trap cleanup EXIT

if [[ ! -f "$REPOSITORY_ROOT/skills/career-coach/SKILL.md" ]]; then
  TEMP_DIRECTORY="$(mktemp -d)"
  if command -v git >/dev/null 2>&1; then
    git clone --depth 1 "$REPOSITORY_URL" "$TEMP_DIRECTORY/life-coach" >/dev/null
  elif command -v curl >/dev/null 2>&1 && command -v tar >/dev/null 2>&1; then
    curl -fsSL "https://github.com/dexterqiu-collab/life-coach/archive/refs/heads/main.tar.gz" \
      | tar -xz -C "$TEMP_DIRECTORY"
    mv "$TEMP_DIRECTORY/life-coach-main" "$TEMP_DIRECTORY/life-coach"
  else
    echo "Installation needs git, or curl plus tar." >&2
    exit 1
  fi
  REPOSITORY_ROOT="$TEMP_DIRECTORY/life-coach"
fi

SOURCE_SKILL="$REPOSITORY_ROOT/skills/career-coach"

install_skill() {
  local destination_root="$1"
  local destination="$destination_root/career-coach"

  mkdir -p "$destination_root"
  if [[ -e "$destination" ]]; then
    if [[ "$FORCE_INSTALL" != "true" ]]; then
      echo "Skipped existing installation: $destination (use --force to update safely)" >&2
      return 0
    fi
    local backup="${destination}.backup-$(date +%Y%m%d%H%M%S)"
    mv "$destination" "$backup"
    echo "Backed up existing installation to $backup"
  fi

  mkdir -p "$destination"
  cp -R "$SOURCE_SKILL"/. "$destination"/

  if [[ ! -f "$destination/SKILL.md" ]] || ! grep -q '^name: career-coach$' "$destination/SKILL.md"; then
    echo "Verification failed for $destination" >&2
    exit 1
  fi

  for reference in decision-frameworks.md coaching-playbook.md templates.md; do
    if [[ ! -f "$destination/references/$reference" ]]; then
      echo "Missing reference after install: $reference" >&2
      exit 1
    fi
  done

  echo "Installed and verified: $destination"
}

detected_targets=()

if [[ "$TARGET_KIND" == "auto" ]]; then
  if [[ -n "${CODEX_HOME:-}" || -d "$HOME/.codex" ]]; then
    detected_targets+=("codex")
  fi
  if [[ -d "$HOME/.workbuddy" ]]; then
    detected_targets+=("workbuddy")
  fi
  if [[ -d "$HOME/.codebuddy" ]]; then
    detected_targets+=("codebuddy")
  fi
  if [[ ${#detected_targets[@]} -eq 0 ]]; then
    echo "Could not detect Codex, WorkBuddy, or CodeBuddy. Choose a target explicitly." >&2
    exit 2
  fi
else
  detected_targets+=("$TARGET_KIND")
fi

if [[ "${detected_targets[*]}" == "all" ]]; then
  detected_targets=("codex" "workbuddy" "codebuddy")
fi

for target in "${detected_targets[@]}"; do
  case "$target" in
    codex)
      install_skill "${CAREER_COACH_CODEX_SKILLS_DIR:-${CODEX_HOME:-$HOME/.codex}/skills}"
      ;;
    workbuddy)
      install_skill "${CAREER_COACH_WORKBUDDY_SKILLS_DIR:-$HOME/.workbuddy/skills}"
      ;;
    codebuddy)
      install_skill "${CAREER_COACH_CODEBUDDY_SKILLS_DIR:-$HOME/.codebuddy/skills}"
      ;;
  esac
done

echo "Start a new conversation or reload Skills, then invoke career-coach."
