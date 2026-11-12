#!/usr/bin/env python3
"""Review, Attack & Fix: state helper.

Subcommands
  start-round --scope S [--base REF]   Open the next review round for a scope (exit 3 = round limit hit: escalate).
  paths --scope S --role review|attack Print JSON paths for the latest round; create the findings file if missing.
  pack-path --scope S                  Print JSON with the context pack path (and create the folder).
  summary --scope S                    Print finding counts for the latest round.
  check [--feature-dir D] [--require-review]
                                       Exit 1 if any BLOCKER/MAJOR finding is unresolved (for CI).

Layout (inside the feature folder):
  review/context/<scope>.md
  review/<scope>/round-<n>/{meta.json, findings.md, attack.md, fix-report.md}
  review/audit.md, review/manual-checklist.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

EXT_DIR = Path(__file__).resolve().parents[2]
FINDING_RE = re.compile(r"^###\s+([FA]-\d{3})\s+·\s+(BLOCKER|MAJOR|MINOR)\s+·\s+(.+?)\s*$")
STATUS_RE = re.compile(r"^\s*-\s+\*\*Status\*\*:\s*([A-Z][A-Z-]*)")
UNRESOLVED = {"OPEN", "NOT-FIXED", "DISPUTED"}
BLOCKING = {"BLOCKER", "MAJOR"}


def sh(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def repo_root() -> Path:
    return Path(sh("git", "rev-parse", "--show-toplevel"))


def load_config() -> dict:
    """Read review-config.yml. Uses PyYAML if present, else a small reader for this file's simple shape."""
    path = EXT_DIR / "review-config.yml"
    if not path.is_file():
        path = EXT_DIR / "config-template.yml"
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        cfg: dict = {}
        section = None
        for raw in text.splitlines():
            line = raw.split(" #")[0].rstrip() if not raw.lstrip().startswith("#") else ""
            if not line.strip() or line.strip().startswith("- "):
                continue
            key, _, val = line.strip().partition(":")
            val = val.strip().strip('"')
            if not raw.startswith(" "):
                section = key
                cfg[section] = {} if not val else val
            elif isinstance(cfg.get(section), dict):
                cfg[section][key] = {"true": True, "false": False}.get(val, int(val) if val.isdigit() else val)
        return cfg


def feature_dir(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    root = repo_root()
    out = sh(sys.executable, str(root / ".specify/scripts/python/check_prerequisites.py"), "--json", "--paths-only")
    return Path(json.loads(out)["FEATURE_DIR"]).resolve()


def slug(scope: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", scope).strip("-")
    if not s:
        sys.exit("scope must contain letters or digits")
    return s


def rounds(scope_dir: Path) -> list[Path]:
    found = [p for p in scope_dir.glob("round-*") if p.name[6:].isdigit()]
    return sorted(found, key=lambda p: int(p.name[6:]))


def resolve_base(cfg: dict) -> str:
    ref = str(cfg.get("loop", {}).get("base_ref", "auto"))
    if ref != "auto":
        return sh("git", "rev-parse", ref)
    for cand in ("origin/main", "main", "origin/master", "master"):
        try:
            return sh("git", "merge-base", "HEAD", cand)
        except subprocess.CalledProcessError:
            continue
    return sh("git", "rev-list", "--max-parents=0", "HEAD").splitlines()[0]


def parse_findings(path: Path) -> list[dict]:
    items, cur = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = FINDING_RE.match(line)
        if m:
            cur = {"id": m[1], "severity": m[2], "where": m[3], "status": "OPEN", "file": str(path)}
            items.append(cur)
            continue
        s = STATUS_RE.match(line)
        if s and cur:
            cur["status"] = s[1]
    return items


def fill(template: str, **kw: str) -> str:
    for k, v in kw.items():
        template = template.replace("{" + k + "}", v)
    return template


def cmd_start_round(a, cfg):
    fdir = feature_dir(a.feature_dir)
    scope_dir = fdir / "review" / slug(a.scope)
    existing = rounds(scope_dir)
    max_rounds = int(cfg.get("loop", {}).get("max_rounds", 2))
    if len(existing) >= max_rounds:
        print(json.dumps({"error": "round_limit", "max_rounds": max_rounds,
                          "message": f"{a.scope} already had {max_rounds} review rounds. Escalate to a person instead of starting another."}))
        sys.exit(3)
    if existing:
        prev = json.loads((existing[-1] / "meta.json").read_text(encoding="utf-8"))
        base = a.base or prev["head"]
    else:
        base = sh("git", "rev-parse", a.base) if a.base else resolve_base(cfg)
    n = len(existing) + 1
    rdir = scope_dir / f"round-{n}"
    rdir.mkdir(parents=True, exist_ok=False)
    meta = {"scope": a.scope, "round": n, "base": base, "head": sh("git", "rev-parse", "HEAD"),
            "created": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
    (rdir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"round_dir": str(rdir), **meta}))


def cmd_paths(a, cfg):
    fdir = feature_dir(a.feature_dir)
    scope_dir = fdir / "review" / slug(a.scope)
    existing = rounds(scope_dir)
    if not existing:
        sys.exit(f"No review round for scope '{a.scope}'. Run start-round first.")
    rdir = existing[-1]
    meta = json.loads((rdir / "meta.json").read_text(encoding="utf-8"))
    tests = cfg.get("tests", {})
    test_file = str(Path(tests.get("directory", "tests")) /
                    fill(tests.get("file_pattern", "{scope}_{role}_r{round}_Tests"),
                         scope=slug(a.scope).replace("-", "_"), role=a.role, round=str(meta["round"])))
    findings = rdir / ("findings.md" if a.role == "review" else "attack.md")
    pack = fdir / "review" / "context" / f"{slug(a.scope)}.md"
    if not findings.exists():
        tpl = (EXT_DIR / "templates" / "findings-template.md").read_text(encoding="utf-8")
        root = repo_root()
        rel = lambda p: str(Path(p).resolve().relative_to(root)) if Path(p).resolve().is_relative_to(root) else str(p)
        tpl = fill(tpl, scope=a.scope, round=str(meta["round"]), role=a.role, feature_dir=rel(fdir),
                   base=meta["base"][:12], head=meta["head"][:12], context_pack=rel(pack), test_file=test_file)
        if a.role == "attack":
            tpl = tpl.replace("### F-001", "### A-001")
        findings.write_text(tpl, encoding="utf-8")
    print(json.dumps({"round_dir": str(rdir), "findings": str(findings), "test_file": test_file,
                      "context_pack": str(pack), "context_pack_exists": pack.exists(),
                      "fix_report": str(rdir / "fix-report.md"), **meta}))


def cmd_pack_path(a, cfg):
    fdir = feature_dir(a.feature_dir)
    pack = fdir / "review" / "context" / f"{slug(a.scope)}.md"
    pack.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps({"feature_dir": str(fdir), "context_pack": str(pack), "exists": pack.exists(),
                      "template": str(EXT_DIR / "templates" / "context-pack-template.md"),
                      "max_lines": cfg.get("limits", {}).get("context_pack_lines", 150)}))


def all_findings(fdir: Path, scope: str | None) -> list[dict]:
    review = fdir / "review"
    scopes = [review / slug(scope)] if scope else [p for p in review.iterdir() if p.is_dir() and p.name != "context"] if review.is_dir() else []
    items = []
    for sdir in scopes:
        for rdir in rounds(sdir):
            for name in ("findings.md", "attack.md"):
                if (rdir / name).is_file():
                    items += parse_findings(rdir / name)
    return items


def cmd_summary(a, cfg):
    items = all_findings(feature_dir(a.feature_dir), a.scope)
    counts: dict = {}
    for f in items:
        counts.setdefault(f["severity"], {}).setdefault(f["status"], 0)
        counts[f["severity"]][f["status"]] += 1
    print(json.dumps({"total": len(items), "counts": counts,
                      "unresolved_blocking": [f["id"] for f in items if f["severity"] in BLOCKING and f["status"] in UNRESOLVED]}))


def cmd_check(a, cfg):
    fdir = feature_dir(a.feature_dir)
    ci = cfg.get("ci", {})
    has_rounds = (fdir / "review").is_dir() and any((fdir / "review").glob("*/round-*"))
    if (a.require_review or ci.get("require_review") is True) and not has_rounds:
        print(f"❌ No review round found under {fdir}/review (require_review is on). Run /speckit-review-code.")
        sys.exit(1)
    if ci.get("block_on_open_findings", True) is False:
        print("ℹ️  block_on_open_findings is off: findings not checked.")
        return
    bad = [f for f in all_findings(fdir, None) if f["severity"] in BLOCKING and f["status"] in UNRESOLVED]
    for f in bad:
        print(f"❌ {f['id']} {f['severity']} {f['status']}: {f['where']}  ({Path(f['file']).relative_to(repo_root()) if Path(f['file']).is_absolute() else f['file']})")
    if bad:
        print(f"Review gate FAILED: {len(bad)} unresolved BLOCKER/MAJOR finding(s). Fix them, or record a ruling and mark WONTFIX.")
        sys.exit(1)
    print("✅ Review gate: no unresolved BLOCKER/MAJOR findings." if has_rounds else "ℹ️  No review rounds yet.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--feature-dir", help="Feature folder (default: current Spec Kit feature)")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start-round"); s.add_argument("--scope", required=True); s.add_argument("--base")
    s = sub.add_parser("paths"); s.add_argument("--scope", required=True); s.add_argument("--role", choices=["review", "attack"], required=True)
    s = sub.add_parser("pack-path"); s.add_argument("--scope", required=True)
    s = sub.add_parser("summary"); s.add_argument("--scope")
    s = sub.add_parser("check"); s.add_argument("--require-review", action="store_true")
    a = p.parse_args()
    cfg = load_config()
    {"start-round": cmd_start_round, "paths": cmd_paths, "pack-path": cmd_pack_path,
     "summary": cmd_summary, "check": cmd_check}[a.cmd](a, cfg)


if __name__ == "__main__":
    main()
