#!/usr/bin/env bash
# AI-DLC gate check: production code changes must be backed by an approved spec trail.
#
# Usage: scripts/check-gates.sh <base-ref> [branch-name]
#   base-ref     git ref to diff against (e.g. origin/main)
#   branch-name  feature branch name (defaults to the current branch)
#
# Rules (see docs/ai-dlc/AI-DLC.md):
#   - If no files under src/ changed → pass (docs, specs, tests-only and tooling changes are fine).
#   - Branches named bugfix/* or hotfix/* → pass (bug-fix path: issue + regression test).
#   - Otherwise the branch must be NNN-<slug> and specs/NNN-<slug>/ must contain
#     spec.md, plan.md and tasks.md, with no unresolved [NEEDS CLARIFICATION] markers.
set -euo pipefail

base="${1:?usage: check-gates.sh <base-ref> [branch-name]}"
raw_branch="${2:-$(git rev-parse --abbrev-ref HEAD)}"
branch="${raw_branch##*/}"   # keep the last path segment (supports prefixes like feature/001-x)

changed_src=$(git diff --name-only "$base"...HEAD -- src/ || true)
if [[ -z "$changed_src" ]]; then
  echo "✅ No production code (src/) changed: gate check not required."
  exit 0
fi

if [[ "$raw_branch" =~ ^(bugfix|hotfix)/ ]]; then
  echo "✅ Bug-fix path: spec trail not required (link the issue in the PR)."
  exit 0
fi

if [[ ! "$branch" =~ ^[0-9]{3,}-.+ ]]; then
  echo "❌ src/ changed but branch '$branch' is not a Spec Kit feature branch (NNN-name)."
  echo "   Start with /speckit-specify, or use a bugfix/* branch for bug fixes."
  exit 1
fi

dir="specs/$branch"
fail=0
for f in spec.md plan.md tasks.md; do
  if [[ -f "$dir/$f" ]]; then
    echo "✅ $dir/$f"
  else
    echo "❌ Missing $dir/$f"
    fail=1
  fi
done

if [[ -f "$dir/spec.md" ]] && grep -n "\[NEEDS CLARIFICATION" "$dir/spec.md"; then
  echo "❌ Unresolved [NEEDS CLARIFICATION] markers in $dir/spec.md (gate G2 not met)."
  fail=1
fi

if [[ -f "$dir/tasks.md" ]]; then
  open=$(grep -cE '^\s*- \[ \]' "$dir/tasks.md" || true)
  done_=$(grep -cE '^\s*- \[[xX]\]' "$dir/tasks.md" || true)
  echo "ℹ️  tasks.md: $done_ done, $open open"
fi

if [[ $fail -ne 0 ]]; then
  echo "AI-DLC gate check FAILED. See docs/ai-dlc/AI-DLC.md."
  exit 1
fi
echo "✅ AI-DLC gate check passed."
