#!/usr/bin/env python3
"""Build the handbook website with Zensical, from the same markdown GitHub shows.

The markdown in the numbered folders stays the source of truth and must keep reading well on
GitHub. This script:

1. copies the published files (the root README, CHANGELOG and LICENSE, and every tracked .md
   in the numbered folders) into `.site-build/docs/`, taking the file list from `git ls-files`,
   so nothing untracked or git-ignored can reach the site. Talk outlines (frontmatter
   `type: deck`) and the .pptx decks are source-only: they stay in the repo but are left out of
   the site. A folder README's "Talks you can give" block and any "As a talk:" line are dropped,
   and any other link to a talk points at its page on GitHub instead;
2. adapts the copies where Python-Markdown reads a file differently from GitHub: nested lists
   indented by two spaces, and lists that start straight after a line of text;
3. writes the site navigation from the root README's section list and each folder README's
   numbered reading order, into a copy of `website/zensical.toml`;
4. runs `zensical build`, writing the site to `.site-build/site/`.

Usage:
    python3 scripts/build_site.py            # build
    python3 scripts/build_site.py --serve    # build, then preview at http://localhost:8000

It needs `zensical` on the PATH (`pip install zensical==0.1.2`, the version the website workflow
pins), or `uv`, which it then uses to run that version.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / ".site-build"
DOCS = BUILD / "docs"
ROOT_FILES = ["README.md", "CHANGELOG.md", "LICENSE"]
FOLDER_RE = re.compile(r"^\d-[a-z0-9-]+/")
LIST_RE = re.compile(r"^( *)([-*+]|\d+[.)])( +|$)")
FENCE_RE = re.compile(r"^ *(```|~~~)")
REPO_BLOB = "https://github.com/AnilKerai/applied-ai-handbook/blob/main/"
TALKS_HEADING = "Talks you can give"
LINK_RE = re.compile(r"\]\(([^)\s#]+\.md)(#[^)\s]*)?\)")


def is_deck(rel):
    """Talk outlines are marked `type: deck` in their frontmatter."""
    head = (ROOT / rel).read_text(encoding="utf-8").split("\n---\n", 1)[0]
    return bool(re.search(r"^type:\s*deck\s*$", head, re.M))


def source_only(rel):
    """Files kept in the repo but left off the website: talk outlines and their slide decks."""
    return rel.endswith(".pptx") or (FOLDER_RE.match(rel) is not None and rel.endswith(".md") and is_deck(rel))


def drop_talks(rel, text, excluded):
    """Remove talk material from a page's site copy (the source file is untouched)."""
    lines, out, skipping = text.split("\n"), [], False
    for line in lines:
        if line.startswith(TALKS_HEADING):  # folder README block: heading, blank, bullets
            skipping = True
            continue
        if skipping:
            if line.startswith("- ") or not line.strip():
                continue
            skipping = False
        if line.startswith("As a talk:"):
            continue
        out.append(line)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))

    def relink(m):
        target = (Path(rel).parent / m.group(1)).as_posix()
        target = str(Path(os.path.normpath(target)))
        if target in excluded:
            return f"]({REPO_BLOB}{target}{m.group(2) or ''})"
        return m.group(0)
    return LINK_RE.sub(relink, text)


def published_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    files = []
    for rel in out.stdout.splitlines():
        if rel in ROOT_FILES or (FOLDER_RE.match(rel) and rel.endswith((".md", ".pptx"))):
            files.append(rel)
    return sorted(f for f in files if not source_only(f))


def excluded_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return {r for r in out.stdout.splitlines() if FOLDER_RE.match(r) and r.endswith((".md", ".pptx")) and source_only(r)}


def adapt_markdown(text):
    """Make GitHub-style lists read the same in Python-Markdown.

    Python-Markdown needs four spaces per nesting level and a blank line before a list; GitHub
    accepts two spaces and no blank line. Fenced code is left untouched, and lines inside a
    blockquote are handled the same way after their `>` prefix.
    """
    out, in_fence = [], False
    stack = []          # marker indents of the open list levels
    prev_kind = "blank"  # blank | list | text
    prev_quote = False
    for raw in text.split("\n"):
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            out.append(raw)
            prev_kind, stack = "text", []
            continue
        if in_fence:
            out.append(raw)
            continue
        quote = raw.startswith(">")
        prefix, line = "", raw
        if quote:
            prefix = "> " if raw.startswith("> ") else ">"
            line = raw[len(prefix):]
        if quote != prev_quote:
            stack, prev_kind = [], "blank"
        prev_quote = quote

        if not line.strip():
            out.append(raw)
            prev_kind = "blank"
            continue
        m = LIST_RE.match(line)
        if m:
            indent = len(m.group(1))
            if indent == 0 or not stack:
                stack = [indent]
            else:
                while stack and indent < stack[-1]:
                    stack.pop()
                if not stack or indent > stack[-1]:
                    stack.append(indent)
            level = len(stack) - 1
            if prev_kind == "text" and level == 0:
                out.append(prefix.rstrip() if quote else "")
            out.append(prefix + " " * (4 * level) + line.lstrip(" "))
            prev_kind = "list"
            continue
        indent = len(line) - len(line.lstrip(" "))
        if stack and indent > 0:
            # A continuation line inside a list item: indent it under its item.
            out.append(prefix + " " * (4 * (len(stack) - 1) + 4) + line.lstrip(" "))
            prev_kind = "list"
            continue
        # Unindented text: straight after a list item it is GitHub's lazy continuation of that
        # item; after a blank line or other text it ends the list.
        if prev_kind != "list":
            stack = []
        out.append(raw)
        prev_kind = "list" if stack else "text"
    return "\n".join(out)


def adapt_frontmatter(text):
    """Rename keys the site theme would misread. `status` means review status here, but the
    theme reads it as a page badge and shows an info icon beside every page in the sidebar."""
    if not text.startswith("---\n"):
        return text
    head, sep, body = text[4:].partition("\n---\n")
    head = re.sub(r"^status:", "review_status:", head, flags=re.M)
    return "---\n" + head + sep + body


def readme_links(path, pattern):
    return re.findall(pattern, (ROOT / path).read_text(encoding="utf-8"), flags=re.M)


def build_nav(files):
    nav: list[dict[str, str | list[str]]] = [{"Home": "README.md"}]
    sections = readme_links("README.md", r"\]\((\d-[a-z0-9-]+)/README\.md\)")
    seen = set()
    for folder in dict.fromkeys(sections):
        heading = readme_links(f"{folder}/README.md", r"^# (.+)$")
        title = re.sub(r"^\d+\.\s*", "", heading[0]) if heading else folder
        pages = [f"{folder}/README.md"]
        for page in readme_links(f"{folder}/README.md", r"^\d+\. \*\*\[[^\]]+\]\(([^)]+\.md)\)\*\*"):
            if f"{folder}/{page}" in files:
                pages.append(f"{folder}/{page}")
        for rel in files:  # any page the README doesn't list goes at the end, never dropped
            if rel.startswith(folder + "/") and rel.endswith(".md") and rel not in pages:
                print(f"note: {rel} is not in {folder}/README.md; adding it at the end of the section")
                pages.append(rel)
        seen.update(pages)
        nav.append({title: pages})
    nav.append({"Changelog": "CHANGELOG.md"})
    missing = [f for f in files if f.endswith(".md") and f not in seen | {"README.md", "CHANGELOG.md"}]
    if missing:
        sys.exit(f"build_site: pages not in any section: {missing}")
    return nav


def toml_nav(nav):
    def entry(item):
        (k, v), = item.items()
        if isinstance(v, str):
            return "  { " + json.dumps(k) + " = " + json.dumps(v) + " },"
        inner = ", ".join(json.dumps(p) for p in v)
        return "  { " + json.dumps(k) + " = [" + inner + "] },"
    return "nav = [\n" + "\n".join(entry(i) for i in nav) + "\n]"


def main():
    files = published_files()
    excluded = excluded_files()
    if BUILD.exists():
        shutil.rmtree(BUILD)
    DOCS.mkdir(parents=True)
    for rel in files:
        src, dst = ROOT / rel, DOCS / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if rel.endswith(".md"):
            text = adapt_frontmatter(src.read_text(encoding="utf-8"))
            front = ""
            if text.startswith("---\n") and "\n---\n" in text[4:]:
                end = text.index("\n---\n", 4) + 5
                front, text = text[:end], text[end:]
            dst.write_text(front + adapt_markdown(drop_talks(rel, text, excluded)), encoding="utf-8")
        else:
            shutil.copy2(src, dst)
    (DOCS / "assets").mkdir()
    shutil.copy2(ROOT / "website" / "extra.css", DOCS / "assets" / "extra.css")

    config = (ROOT / "website" / "zensical.toml").read_text(encoding="utf-8")
    marker = "# @nav: written by scripts/build_site.py"
    if marker not in config:
        sys.exit("build_site: website/zensical.toml has lost its nav marker line")
    config = config.replace(marker, toml_nav(build_nav(files)))
    (BUILD / "zensical.toml").write_text(config, encoding="utf-8")
    print(f"staged {len(files)} files into {DOCS.relative_to(ROOT)} ({len(excluded)} source-only files left out)")

    zensical = shutil.which("zensical")
    cmd = [zensical] if zensical else ["uv", "tool", "run", "--from", "zensical==0.1.2", "zensical"]
    subprocess.run(cmd + ["build", "--clean", "-f", str(BUILD / "zensical.toml")], cwd=BUILD, check=True)
    print(f"site built in {(BUILD / 'site').relative_to(ROOT)}")
    if "--serve" in sys.argv:
        subprocess.run(cmd + ["serve", "-f", str(BUILD / "zensical.toml")], cwd=BUILD)


if __name__ == "__main__":
    main()
