# Changelog

Newest first. Every correction lists what changed and the evidence.

## 2026-11-16: decks open in Keynote

- **All three decks now open in Apple Keynote** (and Quick Look). The build script used python-pptx,
  which adds a notes master when the first speaker note is written but never lists it in
  `presentation.xml`; PowerPoint and Google Slides tolerate that, Keynote refuses the file
  (python-pptx issue #1051). `scripts/build_deck.py` now registers the notes master before saving,
  with a test, and the lunch-and-learn and both talk decks are rebuilt. Slides and notes are unchanged.
- **Talk: working with coding agents, slide 2 notes:** "the definition Simon Willison adopted in
  September 2025", not "his working definition". He adopts a definition already in use; the outline
  had implied he originated it.

## 2026-11-16: corrections from the final review

- **Cam Soper's CloudFront story** no longer says he told Claude the rule, or that the rule lived only
  in agent instructions. His talk's captions say neither: "I didn't write that. Actually my claude
  wrote that … I didn't read it". Each page now says he had a rule against putting CloudFront in front
  of one of his servers, and Claude put it there anyway. Changed in Working with coding agents (§7),
  the .NET guide, the pre-mortem (failure mode 8) and the lunch-and-learn speaker notes (slide 5).
- **Lauren Tan's layers** (Working with coding agents, §7) are her inverse pyramid of where to spend
  time on an agent's environment, not an order of strength. Her transcript says "this inverse pyramid
  is how I think about where to spend time"; "strongest constraints" is a heading in the editorial
  write-up of her talk, not her words.
- **Lunch-and-learn slide 13:** the +44% tile now reads "lines of code (not significant)", and the
  outline's first bullet keeps the paper's caveat. Of the 44.0% lines estimate, the Harvard study
  says "this estimate is also marginally insignificant"; the speaker notes already said so. The other
  figures are unchanged. *Should we build a software factory?* (Newer evidence) now carries the same
  caveat on the 44.0% lines figure.
- **Talk: building AI features.** The reading slide says the outline cites every *sourced* claim,
  matching session 1: the first-person lines and the advice are uncited by design. Slide 10 names
  Heidi Porter on the slide for her "rubber stamping fatigue" line, rather than attributing it only
  through its citation.
- **Talk: working with coding agents, slide 2.** The "looks done" line is attributed, on the slide and
  in the notes, to Claude Code's best-practices page, which says it of Claude ("Claude stops when the
  work looks done"), not of every coding agent. The notes' tool-use sentence names Claude as its
  subject again.

## 2026-11-16: two talks for engineers

- **Two new talks in `4-build/`,** a two-session series for engineers. Each has an outline (slide
  text, speaker notes and sources), a citation ledger and a committed pptx:
  - `talk-working-with-coding-agents` (session 1, 11 slides): checking an agent's work, context
    files, turning corrections into checks, and earning autonomy one action at a time.
  - `talk-building-ai-features` (session 2, 12 slides): the model as a replaceable part, narrow jobs
    with the control flow in code, guardrails in code rather than in prompts, evals before launch,
    checking the grader, and review in production. It opens with a recap of session 1 and can also
    be given on its own.
  - Each talk has one slide labelled *From my own builds*, in the first person, linking the matching
    first-person lessons in `3-engineer/`.
  - The committed pptx for each talk is the full version, with its basics slides and, in session 2,
    the recap slide.
- **Reading path and routes:** both talks follow Working with coding agents in the reading path, in
  series order, and join the engineer route on the home page. Working with coding agents and the
  evals playbook each link the matching talk.
- **`scripts/build_deck.py` takes an outline and options:**
  `build_deck.py <outline> [--out <pptx>] [--no-basics] [--standalone] [--overlay <file>]`.
  - With no arguments it still builds the lunch-and-learn deck, with the same slide text as before.
  - A `*Layout: …*` line under a slide heading now picks a special layout, instead of the slide
    number. The lunch-and-learn outline gained these lines for its six special slides. A new
    `discussion` layout serves session 2's recap slide.
  - `--no-basics` drops slides titled `Basics · …`, and `--standalone` drops slides titled
    `Series · …` and the `Session N of M: ` prefix from the title slide's subtitle; the footers are
    renumbered.
  - `--overlay` adds private local notes or slides on top of a public outline. Overlays and the decks
    built from them stay outside this repo: an overlay build refuses to write inside it, comparing
    paths by file identity, so a differently cased spelling of the repo path is refused too.
  - The `ladder`, `data` and `tree` layouts hard-code the lunch-and-learn deck's captions and tiles, so
    only that deck uses them; the other layouts are generic.
  - Tests are in `scripts/test_build_deck.py`.
- **AGENTS.md:** the `4-build/` layout line lists both talks. The first-person rule now covers every
  `3-engineer/lessons-from-*` page (the old pattern missed one of them) and the
  *From my own builds* slides with their speaker notes. A new Decks section describes the outline
  format, the layout hints, the build options and the rule that overlays are never committed here.

## 2026-11-15: Engineer section

- **New section, `3-engineer/`,** between Decide and Build: the engineering disciplines under every AI
  system (prompt, context, harness, loop and eval engineering), how they fit together and when they
  arrived. It comes before Build because Build applies these disciplines, so a reader meets them first.
  Its 11 pages are:
  - the big-picture map of the disciplines;
  - a timeline of how the ideas arrived, with the author's own path alongside;
  - six discipline pages: prompt, context, harness, loop and eval engineering, and multi-agent
    orchestration;
  - three pages of first-person lessons: from building an agent harness and an evals framework, and
    from running agent squads.
- **Later sections renumbered** to keep the folders in learning order: `3-build/` is now `4-build/`,
  `4-run/` is now `5-run/` and `5-lead/` is now `6-lead/`. Every link between documents was updated;
  the renumbering changed documents only in their links and section numbers. The folder READMEs carry
  the new numbers, and the root README lists the new section. Links from outside the repo need the new
  folder number.
- **Glossary:** new entries for prompt engineering, loop engineering, eval engineering and
  orchestration, each cited. The context engineering and harness entries now link to their
  pages in the new section.
- **Reading routes:** the map is now second in the "New to AI" route, and the engineer route starts
  with the map and harness engineering. The root README now says that the Engineer section includes the
  author's own path and first-person lessons.
- `scripts/check.py` now checks all six sections.

## 2026-11-15: reframed as a compendium

- Removed conference and event framing from the documents. The handbook now presents practitioners'
  reports, published studies and our recommendations directly. Speaker attributions, every citation and
  every quote are unchanged; the Sources lists still say where each talk was given.
- The lunch-and-learn deck is renamed `1-understand/ai-lunch-and-learn` (outline and .pptx).
- `scripts/check.py` gained a fifth check that flags event names above the Sources block.

## 2026-11-15: first public version

- Published 19 documents in five sections (Understand, Decide, Build, Run, Lead), each with an
  "In one minute" summary, a reading time and a "Read next" link.
- **Accuracy audit before publishing.** Every cited sentence was re-checked against the original talk
  transcripts, papers and articles, not against earlier summaries. Corrections made, with their
  evidence:
  - **Harvard study of firms using coding agents** (Chen & Stratton) updated to its November 2026
    revision: 655 firms, data to August 2026. Coding agents raised pull requests by 35.7% but resolved
    issues by only 13.7%, which is borderline significant, while time from review submission to
    approval rose 56.1%. Earlier figures (718 firms, +23% PRs, +49% review time) came from the
    October version.
  - **AWS Emulator anecdote** re-attributed: Swami Sivasubramanian supervised an agent rebuilding a
    replication engine for four nights before seeing it had no way to check its results; with a spec
    and a test environment the rebuild took about two hours.
  - **CypherGuard:** a strong model goes from 71.76% unaided to 94.68% with repair (Table 7). The
    88.50% figure is a small model with repair.
  - **SO-Arena** tested 21 models, not 21 decision models. Its best-performing System One model ranked
    seventh for reliability.
  - **Factory's bar for auto-merge** is AI-written changes breaking things *less often* than human ones,
    not merely matching them.
  - **Mark Lay's test** is "something better or something more efficient", not "better or cheaper".
  - **ZoomInfo** trialled a decision model in shadow mode beside its LLM judge; we no longer say it
    replaced the judge.
  - Many smaller fixes to attributions, hedges ("perhaps", "maybe") and release statuses.
