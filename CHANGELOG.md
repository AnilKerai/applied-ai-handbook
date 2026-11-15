# Changelog

Newest first. Every correction lists what changed and the evidence.

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
    replication engine for four nights; with a spec and a test environment it took about two hours.
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
