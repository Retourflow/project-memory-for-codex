#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET="${1:-.}"
FORCE="${2:-}"

mkdir -p "${TARGET}/docs" "${TARGET}/scripts"

copy_file() {
  local source="$1"
  local destination="$2"

  if [[ -e "${destination}" && "${FORCE}" != "--force" ]]; then
    printf 'Skipped existing file: %s\n' "${destination}"
    return
  fi

  cp "${source}" "${destination}"
  printf 'Created: %s\n' "${destination}"
}

copy_file "${SOURCE_DIR}/templates/AGENTS.md" "${TARGET}/AGENTS.md"
copy_file "${SOURCE_DIR}/templates/docs/PROJECT_CONTEXT.md" "${TARGET}/docs/PROJECT_CONTEXT.md"
copy_file "${SOURCE_DIR}/templates/docs/CURRENT_STATE.md" "${TARGET}/docs/CURRENT_STATE.md"
copy_file "${SOURCE_DIR}/templates/docs/ARCHITECTURE.md" "${TARGET}/docs/ARCHITECTURE.md"
copy_file "${SOURCE_DIR}/templates/docs/DECISIONS.md" "${TARGET}/docs/DECISIONS.md"
copy_file "${SOURCE_DIR}/templates/docs/CHANGELOG.md" "${TARGET}/docs/CHANGELOG.md"
copy_file "${SOURCE_DIR}/scripts/validate.py" "${TARGET}/scripts/validate.py"

printf '\nProject memory initialized. Replace template statements with verified facts.\n'
