# AGENTS.md: Applied AI Handbook

A public, CC BY 4.0 compendium of practical, evidence-cited knowledge about AI engineering and about
bringing AI into a business or an engineering team. Readers are colleagues, engineering leads and senior
leadership, many of them new to AI. Write for them.

## Layout

- `1-understand/`: the basics. Glossary, common questions answered, a talk for colleagues new to
  using AI (`talk-using-ai-at-work`), and a lunch-and-learn deck.
- `2-decide/`: is this a job for AI, and which kind? Decision trees, intake checklist, feature spec,
  pre-mortem, where AI goes first.
- `3-engineer/`: the engineering disciplines (prompt, context, harness, loop and eval engineering,
  orchestration), the big-picture map, the timeline, and first-person lessons from the maintainer's own
  builds.
- `4-build/`: how to build it. Pattern catalogue, evals playbook, working with coding agents, .NET guide,
  and two talks for engineers (`talk-*`: outline, speaker notes and pptx).
- `5-run/`: how to run it. Production runbook, agent PR policy, metrics scorecard.
- `6-lead/`: how to steer it. Leadership memos, maturity model.
- `README.md` in the root and in each folder: reading routes and the folder's contents.
- `.citations/<doc-slug>.json`: the citation ledger behind each document's Sources block.
- `scripts/check.py`: the pre-publish check (citations, links, leaks, structure, framing).
- `scripts/build_deck.py`: builds a deck's pptx from its outline (see "Decks" below).
- `scripts/build_site.py`, `website/` and `.github/workflows/site.yml`: the website (see "Website"
  below).
- `CHANGELOG.md`: every correction and update, newest first.

## Rules for every document

1. **No employer or client details, ever.** Never name an employer or client, use their domain
   vocabulary, or describe their internal systems, people or projects. The maintainer's own public
   projects may be named, but only in the first-person material (rule 4). `scripts/check.py` enforces
   the built-in patterns, plus a private, git-ignored `.leakcheck.local`. If that file is missing, ask
   the maintainer before publishing.
2. **Cite every factual sentence** with `[n]`, pointing at a public URL in the document's Sources block:
   - a talk's page or timestamped video;
   - a paper;
   - an article or vendor documentation.

   Label a company's or vendor's numbers as its own claim ("Glean reports…"). Phrase recommendations as
   advice ("We recommend…") and leave them uncited. Link the maintainer's own repos only as files pinned
   to a full commit SHA that pass the leak check: never a repo root, a commit page or a private repo.
   Check what a linked file links on to as well. When the rest of a page is wrong, cite one section with
   `sources.py anchor <id> <fragment>`.
3. **Quotes are verbatim** from the transcript or article, attributed by name in the sentence.
   Otherwise paraphrase without quote marks.
4. **Plain British English, and two voices kept apart.**
   - Concepts, principles and guidance are factual and impersonal (or "we" for recommendations).
   - The maintainer's own experience is first person. It appears only in:
     - the `3-engineer/lessons-from-*` pages;
     - the *My path* entries on the timeline;
     - the slides labelled *From my own builds* in the `talk-*` decks, with their speaker notes.
   - Every first-person claim must be backed by the maintainer's files or git history.
   - Keep sections short. No tables: they read badly on phones.
5. **Every document has, in this order:**
   - frontmatter, including `last_checked: YYYY-MM-DD` and `as_of`;
   - the title;
   - an `> **In one minute**` box of 3–5 plain-English bullets with no new facts or figures;
   - a `*Reading time … · Best for …*` line;
   - the body;
   - a `**Read next:**` line;
   - Sources.
6. **A compendium, not an event write-up.** Attribute claims to people, organisations and studies,
   never to the event where they were said. Event names belong only in Sources entries.
7. **Links between documents** are relative Markdown links (`../4-build/evals-playbook.md`).
   No `[[wikilinks]]`.
8. **Timeline and origin verbs match the evidence.** Say "coined" only when the source shows a term's
   first use. Otherwise say "first seen", "popularised", "published" or "released". Keep the source's
   hedges, including when trimming to fit a word cap.

## Changing a document

- **Edit citations with the grounded-citations `sources.py` workflow.** Pass
  `--ledger .citations/<slug>.json` before the subcommand. Render the Sources block with
  `render --replace-in`, then run `verify --strict`.
- **Re-fetch a study before reusing its figures.** Papers at the same URL get revised: the Harvard
  firm study changed its firm count and effect sizes between October and November 2026.
- **Update `last_checked`** on any document you verify, and add a `CHANGELOG.md` entry for every
  correction (what changed, and the evidence).
- **Run `python3 scripts/check.py`** before every commit. It must exit 0.

## Decks

- **The outline is the source of truth.**
  - Each slide is a `## Slide N · Title` section with **On the slide** bullets, an optional
    **Key line** and **Speaker notes**.
  - An optional `*Layout: …*` line under the heading picks a special layout. Without one, a slide
    uses the standard layout. The general layouts are `title`, `three`, `standard`, `discussion`
    and `reading`. `ladder`, `data` and `tree` hard-code the lunch-and-learn deck's own captions,
    so use them only there.
  - Slides titled `Basics · …` are optional basics. Slides titled `Series · …` only make sense after
    the previous session.
- **Edit the outline,** then run `python3 scripts/build_deck.py <outline.md>`.
  - With no arguments, it builds `1-understand/ai-lunch-and-learn`.
  - It needs `python-pptx` and `pillow`.
- **Options:**
  - `--out <pptx>` sets the output file.
  - `--no-basics` drops the `Basics ·` slides.
  - `--standalone` drops the `Series ·` slides and the `Session N of M: ` prefix from the title
    slide's subtitle.
  - `--overlay <file>` builds a private local version. It adds local notes or slides on top of the
    public outline.
- **The committed pptx for each talk is the full version,** with its basics and series slides.
- **Overlays and the local decks built from them live outside this repo and are never committed
  here,** nor named in any file.

## Website

The handbook is also published as a website, https://anilkerai.github.io/applied-ai-handbook/, built
with Zensical. The markdown in this repo stays the source of truth.

- **Write for GitHub first.** Every page must read correctly on GitHub. Don't add site-only syntax
  (admonitions, tabs, attribute lists, HTML).
- **How it's built.** `scripts/build_site.py` copies the tracked pages into `.site-build/`, which is
  git-ignored.
  - It adapts the copies only where Python-Markdown differs from GitHub: nested lists indented by two
    spaces, and a list straight after a line of text.
  - It renames the frontmatter `status` key, which the theme would show as a badge.
  - It writes the navigation from the root README's sections and each folder README's numbered
    reading order. So a page appears on the site where the READMEs list it.
- **Publishing.** The `Website` workflow runs `scripts/check.py`, builds the site and deploys it to
  GitHub Pages on every push to `main`. A push that fails the check publishes nothing.
- **Preview locally** with `python3 scripts/build_site.py --serve`. It needs `zensical==0.1.2`, or
  `uv`, which the script uses to run that version.
- **Settings.** The theme, features and markdown extensions are in `website/zensical.toml`; styles
  are in `website/extra.css`. Keep off any extension that gives plain text a new meaning (math for
  `$`, subscript for `~`, smart fractions and arrows), because the pages are written for GitHub.
- **Keep it an ordinary website.** Links are plain page loads: keep `navigation.instant` off, as it
  kept the old page on screen with no sign of loading. Keep `navigation.tracking` off, so the
  address bar doesn't change on scroll. Fonts are the device's own (`font = false`), with no Google
  Fonts.
- **Only tracked files are published:** the root README, CHANGELOG and LICENSE, and the `.md` and
  `.pptx` files in the numbered folders. Nothing git-ignored can reach the site.

## Where updates come from

The maintainer's private research (notes on talks, papers and research briefs) feeds this
handbook one way: when the evidence changes, a PR updates the affected documents here. Transcripts,
notes and briefs themselves are never copied into this repo.

## Keep this file current

When the layout, rules or checks change, update this file in the same commit.
