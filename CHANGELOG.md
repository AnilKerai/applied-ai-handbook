# Changelog

Newest first. Every correction lists what changed and the evidence.

## 2026-11-22: two Decide pages rewritten, and model + harness + evals

- **[AI failure modes: a pre-mortem checklist](2-decide/ai-failure-modes-premortem.md)** is
  restructured.
  - The tick-list now comes straight after "How to run the pre-mortem".
  - Failure modes are grouped into *Any AI project* and *If it's an agent that takes actions*,
    and overlapping ones are merged (23 became 17).
  - Each mode has one shape: what goes wrong, a warning sign, a prevention and what was seen in
    practice.
  - Examples that were dropped still appear on other pages of the handbook.
  - Two quotes are corrected against the cited talks. Duolingo's now reads "shortest path to green
    CI", and the UndoBench retry figure is paraphrased, because the talk's captions don't carry the
    quoted words.
- **[How much should an agent be trusted to do on its own?](2-decide/how-much-autonomy-for-an-agent.md)**
  is rewritten for anyone about to let an AI agent act, not only software teams.
  - It has four gates: checkable work, decisions about people, limits enforced outside the
    agent, and the cost of a mistake.
  - Then a four-step ladder, from reporting only to acting alone, with people at the helm.
  - Coding specifics such as auto-merge and review tiers are in one *For software teams* point.
  - SEP's six constraints, which are about how automated a whole team should be, are in
    [Should we aim for a fully automated software factory?](6-lead/should-we-build-a-software-factory.md).
  - Sources are now numbered.
- **Two quotes corrected across the handbook.**
  - Duolingo's line is "agents sometimes take the shortest path to green CI", not "paths".
  - Tanmay and Dolly Sah's 54% duplicate-effects figure is now a paraphrase. The words quoted
    before were a corrected reading of the talk's captions, not its exact words.
- **Model + harness + evals:** my shorthand, model + harness = an agent and model + harness + evals
  = an agent you can trust in production, is now on [The big picture](3-engineer/the-big-picture.md),
  in the glossary's *Agent* entry and in my evals-framework lessons, with Kevin Solorio's "an agent
  without evals is a proof of concept".
- **[What modern AI is](1-understand/what-modern-ai-is.md):**
  - Claude is now among the chat assistants, cited to Anthropic, because the judges' guidance
    names only the other three.
  - Decision models are added to the kinds of AI.
  - Web search is named in the one-minute box.

## 2026-11-22: a plain-English start

- **New: [What modern AI is, in plain English](1-understand/what-modern-ai-is.md),** now the first
  page of Understand and of the *New to AI* route.
  - It covers the kinds of AI you'll meet and how a chat assistant works: it predicts likely
    next words and doesn't look things up unless it's connected to search or your documents.
  - It explains why it sounds sure when it's wrong, and what it is and isn't: not a person, not
    shown to be conscious and not accountable for its work. The reasoning it shows isn't always how
    it got there.
  - It ends with three habits: brief it, check it, own it.
- **[Should this task use AI, and which kind?](2-decide/should-this-task-use-ai.md):** the box
  "Output listable in advance?" now asks "Is the answer a pick from a fixed list?", and the bullet
  below it explains the test with examples.
- **The glossary is now "AI glossary",** not "AI glossary for leadership", because Understand is
  for everyone.

## 2026-11-21: talks are in the repository only

- **The four talks are no longer on the website.** They are the outlines, speaker notes and slide
  decks for *Using AI well at work*, *What works with AI*, and the two engineer sessions. They stay
  here in the repository, listed under "Talks you can give" in the Understand and Build sections.
- **The reading order, the routes and the reading-time total now skip them.** The *Presenting to
  your team* route is gone.

## 2026-11-21: questions for everyone, and model choice

- **[AI questions answered](1-understand/ai-questions-answered.md) now works for everyone at
  work.**
  - Each answer starts with *My recommendation* in plain English, then the evidence. Where
    engineering detail matters, it ends with a *For software teams* line.
  - *How sure I am* replaces the old confidence ratings, on a three-step scale: very sure,
    fairly sure or not very sure, each with a plain reason.
  - Questions only engineers ask (reviewing AI-written code, AGENTS.md, stopping agents breaking
    things, decision models and MCP) are grouped in *For teams building with AI*.
  - No existing claim, quote or citation was removed.
- **New: METR's randomised trial in the measurement answer.** In METR's early-2025 trial, 16
  experienced open-source developers took 19% longer with AI tools, yet believed AI had sped them
  up by 20%. The answer adds METR's own limits (one trial, software development only, results
  since marked out of date) and its February 2026 update. That update says developers are likely
  sped up more by AI tools now, but calls its newer data "only very weak evidence for the size of
  this increase".
- **Model choice:**
  - I now recommend defaulting to open-weight models we can run ourselves, behind a good harness
    and evals. Step up to a frontier model only where evals show the open model failing and the
    step is worth the cost.
  - The evidence on both sides is in the answer: how far open models lag on a broad index and on
    harder tests, how small tuned models did on one narrow task, and the costs of running a model
    yourself.
  - The same line is in the [.NET guide](4-build/dotnet-ai-engineering-guide.md).
- **Glossary:** new entries for *domain agent*, *frontier model* and *open-weight model*. The model
  recommendation now links to them instead of explaining each term in place.
- **"Buy the models" now reads "use existing models rather than making our own",** because
  open-weight models are free to download. This covers the FAQ and the glossary.
- **The four talk outlines** lose their boilerplate introductions. The slides are unchanged.

## 2026-11-21: links to my harness

- **[model-harness](https://github.com/AnilKerai/model-harness), my open-source .NET agent
  harness, is now linked** from the README, the *See it built* pointers on the Engineer pages and
  the first-person lessons. Citations still point at files pinned to one commit, so they don't
  change when the code does.

## 2026-11-21: written from my point of view

- **The handbook now says whose view it is.** It is written from my point of view and backed by
  evidence. The evidence stays impersonal and cited, and my judgement is first person: "I
  recommend", "My reasoning", "in my view". The recommendations are my own view, not my
  employer's.
  - Where a page stated a judgement as if it were a finding, it is now marked as mine.
  - Templates, checklists, decision trees, the runbook, the PR policy, the scorecard and the talks
    stay neutral, so anyone can adopt or present them.
  - "We" now means the reader's own team. The runbook, PR policy, scorecard and intake checklist
    now use plain imperatives instead of "we should".
  - No cited claim, figure, quote or citation changed.
  - Four lines that overstated were corrected in review:
    - The maturity model cited AgentRun's own case study for "no independent replication" of
      its figures; that is now my own statement.
    - "A calibration set labelled entirely pass cannot measure a judge at all" now says what such a
      set cannot show: whether a judge catches failures. It can still show false alarms.
    - "The furthest-ahead teams rebuilt around it" now reads "One team", since only Cognition is
      cited.
    - The pattern catalogue's "proven" patterns are now patterns "seen in practice".

## 2026-11-21: humans at the helm

- **New: [Can AI replace our people?](6-lead/can-ai-replace-our-people.md)**, a leadership memo.
  - It sets out the evidence on both sides:
    - studies and working papers on jobs, from payroll, administrative and résumé data;
    - two rulings, on an airline's responsibility for its chatbot's answers and on lawyers' duty to
      check AI legal research;
    - studies of people working with AI;
    - a meta-analysis in which people and AI together did worse on average than the better of the
      two alone, though better than people alone;
    - chief executives' own words: one of the opinion that AI can already do people's jobs, another
      expecting it to shrink his company's corporate workforce.
  - It recommends a human at the helm: people set the limits, the system hands them the judgement
    calls, and a named person owns every outcome.
- **New question for everyone at work:**
  [Will AI replace my job?](1-understand/ai-questions-answered.md#q-will-ai-replace-my-job),
  in a new first section of *AI questions answered*.
- **Heidi Porter's warning, on four more pages:** the feature spec, the pre-mortem, the intake
  checklist and the lunch-and-learn deck now say reviewers facing thousands of items *can* fall
  into rubber-stamping fatigue. They had said they do. Her talk's transcript says "They can just
  have rubber stamping fatigue". The deck is rebuilt.
- **[Will AI replace our developers?](1-understand/ai-questions-answered.md#q-will-ai-replace-our-developers)**
  now adds that, in a Stanford payroll study revised in August 2026, employment fell for
  early-career workers in the jobs most exposed to AI, software development among them. The
  authors call this descriptive, not causal. The answer had said only "not on the evidence so far".
- **Glossary:** a new entry, *Human at the helm*, which also says where checking each result still
  applies. *Human in the loop* now warns that approving each output can turn into a rubber stamp.
- **[Talk: using AI well at work](1-understand/talk-using-ai-at-work.md):** slide 10 is now "Three
  habits that keep you at the helm", and the reading slide adds the new question. The slides are
  rebuilt.
- **[How much should an agent be trusted to do on its own?](2-decide/how-much-autonomy-for-an-agent.md)
  and [What must be true before AI agents can act in production?](6-lead/before-agents-act-in-production.md):**
  - Each gains a helm point for agent actions that aren't decisions about people: limits set in
    advance, escalation, and review of the exceptions. The decision tree allows this once results
    can be checked automatically, and the production memo once its safeguards are in place.
  - Each adds that decisions about people are different. Under the UK GDPR's rules on automated
    decision-making, as rewritten by section 80 of the Data (Use and Access) Act 2025, a decision
    with legal or similarly significant effects on a person, taken without meaningful human
    involvement, needs safeguards, including a way for the person to obtain human intervention and
    to contest it; if it uses special category data, it is allowed only in limited cases. The ICO's
    draft guidance (March 2026) says that, for involvement to count as meaningful, a person should
    review each decision, the review must come before the decision takes effect, and spot-checks
    aren't enough.
- **Correction, glossary (*Human in the loop*):** Heidi Porter's warning now says that reviewers
  facing thousands of items can fall into rubber-stamping fatigue; it had said they do. Her talk's
  transcript says "They can just have rubber stamping fatigue".

## 2026-11-19: website links load as normal pages

- **The website now behaves like an ordinary website.** Pages use the device's own fonts rather
  than downloading them from Google Fonts, so nothing waits on a third-party server, and the address
  bar no longer changes as you scroll down a page.
- **Links on the website now load as ordinary pages,** so the phone's own loading indicator shows.
  Before, the site fetched the next page in the background and kept the old page on screen until it
  arrived: on a slow phone connection a tap seemed to do nothing for a few seconds. Its built-in
  loading bar was tried first, but on GitHub Pages it disappeared long before the page arrived.

## 2026-11-18: the handbook as a website

- **New: the handbook is also a website,** at https://anilkerai.github.io/applied-ai-handbook/,
  with search, a sidebar in reading order, next and previous links, and a layout that works on
  phones. It is built from the same markdown by `scripts/build_site.py` (Zensical) and published by
  the `Website` workflow on every push to main; the markdown here stays the source.
- **Evals playbook, the ten-day plan:** Week 2's days showed as one run-on paragraph on GitHub,
  because a numbered list that starts at 5 can't follow a line of text directly. A blank line now
  separates them.
- **What works with AI (lunch-and-learn):** its title metadata is now quoted, so it parses.

## 2026-11-16: a talk for anyone new to using AI

- **New: [Talk: using AI well at work](1-understand/talk-using-ai-at-work.md)**, with its slides
  (`1-understand/talk-using-ai-at-work.pptx`). Twelve slides for colleagues in any role who are new
  to AI tools: what the tools do, where they help, where they fail, what not to paste in, and three
  habits, ending with one thing to try that week. Two basics slides can be dropped with
  `--no-basics`. It is wired into the Understand section and the "Presenting to your team" route.

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
