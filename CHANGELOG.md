# Changelog

Newest first. Every correction lists what changed and the evidence.

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
  orchestration, each with its source. The context engineering and harness entries now link to their
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
