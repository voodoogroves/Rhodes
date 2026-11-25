#!/usr/bin/env python3
"""Context prep: list the memory docs that apply to a project. Read only.

  memindex.py <project-dir>      types come from the project's CLAUDE.md ("types: [fo4-mod]")
  memindex.py --type fo4-mod     without a project
  memindex.py --check            validate every doc

Prints paths and descriptions, never bodies. Spec: Rhodes docs/memory-system.md.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

TYPES = {"fo4-mod"}
KINDS = ("gotcha", "lookup")
FIELDS = ("name", "description", "applies-to", "kind", "verified")
GOTCHA_LINES, GOTCHA_CHARS, LOOKUP_CHARS = 60, 5000, 20000
STALE_DAYS = 90
DEFAULT_MEMORY = Path(__file__).resolve().parents[3] / "Alexandria" / "memory"


def parse_list(value):
    return [v.strip() for v in value.strip().strip("[]").split(",") if v.strip()]


def load_doc(path):
    """Return (doc, problems). doc is None when it cannot be listed."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as e:
        return None, [f"unreadable: {e}"]
    if not lines or lines[0].strip() != "---":
        return None, ["no frontmatter"]
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return None, ["frontmatter is not closed"]
    meta = {}
    for line in lines[1:end]:
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    missing = [f for f in FIELDS if not meta.get(f)]
    if missing:
        return None, ["missing " + ", ".join(missing)]

    problems = []
    if meta["name"] != path.stem:
        problems.append(f"name '{meta['name']}' does not match the file name")
    types = parse_list(meta["applies-to"])
    unknown = sorted(set(types) - TYPES)
    if unknown or not types:
        problems.append("unknown or empty applies-to: " + ", ".join(unknown))
    if meta["kind"] not in KINDS:
        problems.append(f"kind must be one of {', '.join(KINDS)}")
    try:
        verified = datetime.date.fromisoformat(meta["verified"])
    except ValueError:
        verified = None
        problems.append("verified is not YYYY-MM-DD")

    body = "\n".join(lines[end + 1:]).strip()
    if meta["kind"] == "gotcha":
        count = len(body.splitlines())
        if count > GOTCHA_LINES or len(body) > GOTCHA_CHARS:
            problems.append(f"gotcha too long ({count} lines, {len(body)} chars; "
                            f"limit {GOTCHA_LINES}, {GOTCHA_CHARS})")
    elif len(body) > LOOKUP_CHARS:
        problems.append(f"lookup too long ({len(body)} chars; limit {LOOKUP_CHARS})")

    doc = dict(meta, path=path, types=types, date=verified, chars=len(body))
    return (doc if meta["kind"] in KINDS else None), problems


def load_all(memory):
    docs, problems, seen = [], [], {}
    if not memory.is_dir():
        return docs, [f"{memory}: memory directory not found"]
    for path in sorted(memory.rglob("*.md")):
        doc, found = load_doc(path)
        problems += [f"{path}: {p}" for p in found]
        if doc:
            if doc["name"] in seen:
                problems.append(f"{path}: duplicate name, also {seen[doc['name']]}")
            seen[doc["name"]] = path
            docs.append(doc)
    return docs, problems


def project_types(project):
    """Return (types, problem)."""
    header = project / "CLAUDE.md"
    if not header.is_file():
        return [], f"{header}: not found (needs a 'types: [...]' line)"
    match = re.search(r"^types:\s*(\[[^\]]*\])\s*$", header.read_text(encoding="utf-8"), re.M)
    if not match or not parse_list(match.group(1)):
        return [], f"{header}: no 'types: [...]' line"
    return parse_list(match.group(1)), None


def line_for(doc, today):
    stale = doc["date"] and (today - doc["date"]).days > STALE_DAYS
    mark = " STALE" if stale else ""
    return f"- {doc['path']}\n    {doc['description']} (verified {doc['verified']}{mark})"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("project", nargs="?", type=Path)
    parser.add_argument("--type", action="append", default=[], dest="types")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--memory", type=Path, default=DEFAULT_MEMORY)
    args = parser.parse_args(argv)
    if not (args.project or args.types or args.check):
        parser.error("give a project directory, --type or --check")

    docs, problems = load_all(args.memory)

    if args.check:
        print(f"{len(docs)} docs listed, {len(problems)} problems")
    else:
        types = list(args.types)
        project = args.project.expanduser().resolve() if args.project else None
        if project:
            found, problem = project_types(project)
            types += found
            if problem:
                problems.append(problem)
        problems += [f"unknown type: {t}" for t in sorted(set(types) - TYPES)]
        matched = [d for d in docs if set(d["types"]) & set(types)]
        today = datetime.date.today()
        print(f"project: {project.name if project else '-'}   types: {', '.join(types) or '-'}")
        for kind, title in (("gotcha", "Read now, each in full"),
                            ("lookup", "Lookups: read in full only when the task matches")):
            group = [d for d in matched if d["kind"] == kind]
            print(f"\n## {title} ({len(group)})")
            for doc in group:
                print(line_for(doc, today))
        if project and project.is_dir():
            print("\n## Project files")
            read = [project / n for n in ("README.md", "docs/decisions.md", "docs/notes.md")]
            for path in read:
                if path.is_file():
                    print(f"- read: {path}")
            for path in sorted((project / "docs").rglob("*.md")):
                if path not in read:
                    print(f"- listed: {path}")

    if problems:
        print("\n## Problems")
        for problem in problems:
            print(f"- {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
