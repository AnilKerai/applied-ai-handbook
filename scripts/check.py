#!/usr/bin/env python3
"""Check the handbook before publishing.

Runs five checks over every Markdown document in the numbered folders:

1. Citations. Every [n] in the body has an entry in the document's Sources block, and every
   Sources entry is cited at least once.
2. Links. Every relative Markdown link points at a file that exists.
3. Leaks. No line matches a private pattern: the built-in patterns (local paths, wiki links), plus any
   patterns in a local, git-ignored `.leakcheck.local` file (one regex per line). Keep the
   names of employers and clients in that local file only, so the check never publishes them.
4. Structure. Every document has an "In one minute" box, a "Read next" line and a
   `last_checked` date in its frontmatter.
5. Framing. The handbook is a compendium, not an event write-up: no conference or event names
   above the Sources block (quotes, link URLs and the Sources block itself are exempt).

Usage: python3 scripts/check.py        (exit code 1 if anything fails)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FOLDERS = ["1-understand", "2-decide", "3-engineer", "4-build", "5-run", "6-lead"]

BUILTIN_PATTERNS = [
    r"/Users/", r"~/", r"\[\[", r"\bVault notes\b", r"talk-notes/",
]

FRAMING_PATTERNS = [
    r"\bmidwest\b", r"\bsummits?\b", r"\.net conf\b", r"\bconferences?\b", r"\bkeynotes?\b",
    r"\bon stage\b", r"\bthe talks\b", r"\bno talk\b", r"\bqcon\b",
    r"\bai engineer (?:code|nyc|new york|world'?s fair|paris|europe|london|shanghai|singapore|miami)\b", r"\baie\b",
]


def docs():
    for folder in FOLDERS:
        yield from sorted(p for p in (ROOT / folder).glob("*.md") if p.name != "README.md")


def split_sources(text):
    m = re.search(r"^## Sources\s*$", text, re.M)
    if not m:
        return text, ""
    return text[: m.start()], text[m.end():]


def check_citations(path, text):
    body, sources = split_sources(text)
    body = re.sub(r"^---\n.*?\n---\n", "", body, flags=re.S)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    cited = {int(n) for n in re.findall(r"\[(\d+)\](?!\()", body)}
    listed = {int(n) for n in re.findall(r"^\[(\d+)\] ", sources, re.M)}
    problems = []
    if cited - listed:
        problems.append(f"cited but not in Sources: {sorted(cited - listed)}")
    if listed - cited:
        problems.append(f"in Sources but never cited: {sorted(listed - cited)}")
    return problems


def check_links(path, text):
    problems = []
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        file_part = target.split("#")[0]
        if file_part and not (path.parent / file_part).resolve().exists():
            problems.append(f"broken link: {target}")
    return problems


def leak_patterns():
    pats = list(BUILTIN_PATTERNS)
    local = ROOT / ".leakcheck.local"
    if local.exists():
        pats += [l.strip() for l in local.read_text().splitlines() if l.strip() and not l.startswith("#")]
    return [re.compile(p, re.I) for p in pats]


def check_leaks(path, text, patterns):
    problems = []
    for i, line in enumerate(text.splitlines(), 1):
        for p in patterns:
            if p.search(line):
                problems.append(f"line {i} matches a private pattern ({'local' if p.pattern not in BUILTIN_PATTERNS else p.pattern})")
    return problems


def check_framing(path, text):
    body, _ = split_sources(text)
    body = re.sub(r"^---\n.*?\n---\n", "", body, flags=re.S)
    problems = []
    for i, line in enumerate(body.splitlines(), 1):
        line = re.sub(r"\]\([^)]*\)", "]", line)          # link URLs
        line = re.sub(r'"[^"]*"|“[^”]*”', "", line)       # verbatim quotes
        for p in FRAMING_PATTERNS:
            if re.search(p, line, re.I):
                problems.append(f"line {i} uses event framing ({p})")
    return problems


def check_structure(path, text):
    problems = []
    if "**In one minute**" not in text:
        problems.append("no 'In one minute' box")
    if "**Read next:**" not in text:
        problems.append("no 'Read next' line")
    if not re.search(r"^last_checked: \d{4}-\d{2}-\d{2}$", text, re.M):
        problems.append("no last_checked date in frontmatter")
    return problems


def main():
    patterns = leak_patterns()
    failures = 0
    count = 0
    for path in docs():
        count += 1
        text = path.read_text(encoding="utf-8")
        problems = (check_citations(path, text) + check_links(path, text)
                    + check_leaks(path, text, patterns) + check_structure(path, text)
                    + check_framing(path, text))
        rel = path.relative_to(ROOT)
        if problems:
            failures += 1
            print(f"FAIL {rel}")
            for p in problems:
                print(f"     {p}")
        else:
            print(f"ok   {rel}")
    for extra in ["README.md", *[f"{f}/README.md" for f in FOLDERS]]:
        p = ROOT / extra
        if p.exists():
            txt = p.read_text(encoding="utf-8")
            probs = check_links(p, txt) + check_leaks(p, txt, patterns) + check_framing(p, txt)
            if probs:
                failures += 1
                print(f"FAIL {extra}")
                for q in probs:
                    print(f"     {q}")
    local = "with local patterns" if (ROOT / ".leakcheck.local").exists() else "WITHOUT a local .leakcheck.local"
    print(f"\n{count} documents checked ({local}); {failures} with problems.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
