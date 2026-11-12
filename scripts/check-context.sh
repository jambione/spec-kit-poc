#!/usr/bin/env bash
# Readiness check for gate G1: docs/poc/PROJECT-CONTEXT.md must have no unanswered TODO items.
# OPEN: items are allowed; they become clarification questions during /speckit-clarify.
#
# Usage: scripts/check-context.sh [path-to-context-file]
set -euo pipefail

file="${1:-docs/poc/PROJECT-CONTEXT.md}"
[[ -f "$file" ]] || { echo "❌ $file not found"; exit 1; }

# Ignore the instructions block at the top (lines starting with '>').
todos=$(grep -n 'TODO:' "$file" | grep -v '^[0-9]*:>' || true)
opens=$(grep -c 'OPEN:' "$file" || true)

if [[ -n "$todos" ]]; then
  count=$(printf '%s\n' "$todos" | wc -l | tr -d ' ')
  echo "❌ $count unanswered item(s) in $file:"
  printf '%s\n' "$todos" | sed -E 's/^([0-9]+):\| *([^|]*)\|.*/  line \1: \2/; s/^([0-9]+):([^|].*)/  line \1: \2/'
  echo
  echo "Answer each one, or mark it 'OPEN: <question>' to resolve it during /speckit-clarify."
  exit 1
fi

echo "✅ $file is complete ($opens item(s) marked OPEN, to be resolved in /speckit-clarify)."
