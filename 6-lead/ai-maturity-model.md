---
title: AI maturity model and roadmap
type: model
created: 2026-11-14
audience: senior leadership and engineering leads planning AI adoption
status: checked
last_checked: 2026-11-22
as_of: "November 2026"
---

# AI maturity model and roadmap

> **In one minute**
> - The model gives two ladders of stages, for AI in engineering and AI in the business, plus a roadmap template.
> - Assess each team or workflow separately, never the whole company at once.
> - Aim for the right fit, not the top stage: a team that stops early on purpose is mature, not behind.
> - Set how much an AI agent may do on its own separately for each kind of action.
> - Move up a stage only once its exit criteria (agreed tests for moving on) are met; move back when they lapse.

*Reading time: about 10 minutes · Best for: leaders planning adoption*

This page gives two ladders, for AI in engineering (coding agents) and AI in the business (features and operations), plus a roadmap template. It builds on [Should we aim for a fully automated software factory?](should-we-build-a-software-factory.md) and [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md) without repeating their arguments. Stages and risks are cited; exit criteria, questions and the roadmap are my advice.

## 1. How to use it

- **Assess per team or per workflow, never company-wide.** SEP, a firm that builds software for clients, finds its teams working in four modes, ways of working with AI agents that differ in how much autonomy the agents have (section 2).[1]
  Its Andrew Dunlap says a team's constraints decide its mode: "The mode is your fit."[1]
- **Aim for fit, not the top stage.** SEP's Chris Shinkle, summing up recent studies, says AI "amplifies what's already there", and "More AI won't fix the AI fit."[1] In my view, a team that stops at E2 on purpose is mature, not behind.
- **Set autonomy per kind of action.** The levels adapt Meta's and Factory's ladders.[3][4] Definitions follow [Agent-written pull requests and agent autonomy](../5-run/agent-pr-policy.md): L1 investigate, L2 draft with approval, L3 act alone on low-risk work, L4 auto-merge.
- **Promote on exit criteria, demote when they lapse,** and re-assess quarterly.

## 2. Engineering track: coding agents

The stages follow SEP's four modes, which run along a scale of agent autonomy from individual, human-in-the-loop work to a *dark factory*; SEP names the individual and shared modes and the dark factory, and stresses that the goal is fit, not the last mode.[1] The E2 and E3 names, the prerequisites and exit criteria, the autonomy levels, and the last stage's name are my additions. That stage is named after Andrew Finch's line that the factory "runs dim, not dark".[2]

### E1: Individual

- **Looks like:** each developer uses an agent their own way, and a human reads every line. L1–L2.
- **Prerequisites:** none. SEP puts the most constrained work here, such as prototypes or code where every line must be right.[1]
- **Exit criteria:** conventions are in the repo, and the team regularly reviews how the tooling works (SEP's *deliberate iteration*, one of five principles SEP applies in every mode).[1] Corrections to agents become lint rules or tests rather than more instructions, as Lauren Tan advises for every correction.[6]
- **Risks:** small gains (Doug Clauson saw 10–20% at Amazon while teams bolted AI onto an unchanged process).[8] Review overload ("All I do all day is review code", one of the signs Chris Shinkle gives of a team in the wrong mode), and prototypes that stall at scale.[1]

### E2: Shared knowledge base

- **Looks like:** one body of domain rules, architecture and workflows that every developer and agent uses.[1] Mostly L2.
- **Prerequisites:** the domain-knowledge constraint eased: rules pulled into one shared body of knowledge (SEP's *shared infrastructure* principle), with subject-matter experts brought in where knowledge sits in people's heads.[1] Finch adds a loop that feeds review and outage lessons back to agents.[2]
- **Exit criteria:** verification runs against tests that predate the work; Jarred Sumner trusts such suites because the agent couldn't have changed them, and warns that rewritten tests can't be trusted.[10] Review is tiered by risk (Lydia Hallie: after an AI review, no person for docs, maybe one reviewer normally, and perhaps two for risky changes).[5] Budget and sponsor are agreed.
- **Risks:** knowledge left as prose nobody enforces.[6] Stopping here can be right: Andrew Dunlap's building-components team at SEP stayed because verifiability mattered more ("Buildings don't fall down.").[1]

### E3: Orchestrated agent team

- **Looks like:** agents take roles under an orchestrator, and the team supplies intent and context.[1] Autonomy rises per action from L2 to L3.
- **Prerequisites:** SEP's six constraints (token budget, organisational readiness, goal definition, domain knowledge, verifiability and code oversight) are loose enough; SEP ties more autonomy to looser constraints but sets no threshold.[1] SEP's team rebuilding a credit union's mobile banking app had no real token limit and strong backing, and reported a "six x reduction of effort" (SEP's figure).[1]
- **Exit criteria, per action:**
  - Meta's test: what a mistake would cost, and how easily it would be caught ([How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md)).[3]
  - Factory's L4 bar: agent changes break things less often than human ones, measured by "the regret-free merge rate, the share of changes that merge and never need a revert or a follow-up fix."[4]
  - The merge gate judges recorded evidence against written criteria.[2]
- **Risks:** review becomes the bottleneck, and fixing it moves the bottleneck elsewhere.[1] Slop at scale: Lauren Tan warns that "if your inner coding loop produces slop, then automating that loop just produces more slop".[6] Steve Yegge found that the more agents he deployed, the more people he needed.[7]

### E4: Dim factory

- **Looks like:** standing workstreams auto-merge (L4) ordinary-tier changes for named actions and areas only; risky-tier work stays at L2 or below, as in the policy. Factory's Luke Alvoeiro: "The owner gets to set the level, but the confidence to raise it comes from watching the work."[4] Humans audit risky code, handle incidents, review architecture and engineer the factory.[2]
- **Prerequisites:** all six constraints relaxed, plus post-deploy checks and rollback (my reading). None of SEP's three example teams worked in this mode.[1] Finch says post-deploy verification is still early.[2] Justin McCarthy points factories at brownfield products, not uncertain greenfield ideas.[9]
- **Exit criteria:** none upward; [the memo](should-we-build-a-software-factory.md) explains why. A traced incident or revert, or a month below the human regret-free baseline, moves an action down at least one rung, as in the policy.
- **Risks:** no automatic brake. The Claude Code team does not yet have circuit breakers that tighten approval when reverts rise.[18]

## 3. Business track: features and operations

### B1: Ad-hoc assistants

- **Looks like:** chat tools, and department-built tools that central IT can't police, like Excel macros in Mark Lay's analogy; someone must own each one.[11]
- **Prerequisites:** none, which is the problem.
- **Exit criteria:** a charter with a yes list and a never list, a named owner for each use, and candidates screened on reward and risk.
- **Risks:** Jason Beutler argues the hardest part is getting people to buy into how AI changes their daily work.[12] Heidi Porter sees pilots stall when the LLM must hold the data, be the system of record, decide and check itself.[1]

### B2: Governed pilots

- **Looks like:** a few pilots, each with a charter, an owner and evals. Don Barger's charter came "before we ever write one line of code", and he asks "what will we never do?"[11] For Lay, accountability can't be handed over to AI, and data has named stewards.[11]
- **Prerequisites:** build *with* the people who do the job, from a deliberately rough version they can correct (Kevin Solorio).[1] Beutler's three phases cover buy-in, the right solution and production costs.[12]
- **Exit criteria:** evals on real cases built with users, because, in Kevin Solorio's view, without evals an agent is still only a proof of concept.[1] A known cost to reverse, and an owner with what Mark Lay calls "the capacity to keep running what they deployed".[11]
- **Risks:** a tool that crosses the never list; Barger turned down an AI counsellor because "Something can be worse than nothing if you're doing the wrong things."[11]

### B3: AI inside workflows

- **Looks like:** fixed orchestration, with an LLM only for the fuzzy step.
  - Porter picks rules, ML, a decision model or an LLM per task. In Syngenta's seed tool the LLM is "the interface, the router, and the explainer, not the agronomist".[1]
  - Chinmay Goyal asks whether the output can be listed in advance. If yes, Glean uses a decision model.[13] In UiPath's fraud demo, a decision model calls in an agent only when it lacks the evidence to decide.[14]
  - AeroCore's agent took off once it was in Microsoft Teams ("No one likes an extra login.").[11]
- **Prerequisites:** good enough data, plus guardrails, evals and observability. Guardrails go in code, since Porter warns that a rule written in a prompt is not guaranteed to be enforced.[1]
- **Exit criteria:** live results are sampled and failures fed back into evals (Solorio's flywheel); worst cases are reviewed, because Porter warns that averages can mask a bad result.[1] Gains are measured against a baseline.
- **Risks:** vendor churn. At Noblis an upgrade broke every app built on the old version.[11]

### B4: Bounded agents under the execution dial

- **Looks like:** each action is set on Porter's dial. A person approves consequential, uncertain actions; high-volume work acts above a confidence threshold; time-sensitive work gets an undo window. Porter's advice is to reserve full automation for actions that are cheap to undo.[1] Meta's on-call ladder is the operations version.[3]
- **Prerequisites:** see [What must be true before AI agents can act in production?](before-agents-act-in-production.md). For Porter, failing evals block promotion.[1]
- **Exit criteria:** a track record per action, a tested undo, and a review load people can sustain.
- **Risks:** reviewers facing thousands of items can fall into what Porter calls "rubber stamping fatigue".[1] Barger's personal takeover of critical conversations stopped being practical as usage grew.[11]

### B5: Learn, then hand off, at scale

- **Looks like:** on repeated per-record jobs, an expensive model learns and a cheap one runs.
  - At AgentRun, Opus wrote its path down as a workflow for a cheap model; a judge hands back answers whose quote isn't on a page that was read.[15] It reports cost per merchant falling from $0.89 to $0.124, at 96% correct against 93% for Opus alone (its own claims).[15]
  - UiPath designs categories with an LLM offline: "we basically removed the LLM completely from the picture on this one."[14]
- **Prerequisites:** a stable, high-volume, checkable job, run side by side on live traffic before cut-over.
- **Exit criteria:** top stage for fitting jobs; keep measuring hand-backs (answers passed back to the expensive model) and reliability.
- **Risks:** a weak check, and technical debt while the stack keeps changing.[11]

## 4. Self-assessment

Answer per team or workflow; any no means stay.

- **E1 → E2:** Are our conventions in the repo? Do we review the tooling regularly? Have our corrections to agents become checks?
- **E2 → E3:** Would existing tests catch a planted bug? Is review tiered by risk? Are budget and sponsor agreed?
- **E3 → E4:** Do we compare regret-free merges per action with humans'? Does the gate read evidence? Is review time flat as output rises?
- **At E4:** Is every L4 action named, owned and demotable? Was rollback rehearsed this quarter? Who reviews architecture?
- **B1 → B2:** Do we have a never list? Is every use owned? Do we know what departments built?
- **B2 → B3:** Were evals built with users? Is the reversal cost known? Can the owner run it next year?
- **B3 → B4:** Is the LLM confined to the fuzzy step? Do failures feed back? Do we report worst cases?
- **B4 → B5:** Is each dial setting written down? Is undo tested? Are reviewers keeping up?
- **At B5:** Is the job repeated and checkable? Do we measure hand-backs? Can we switch back in minutes?

## 5. Roadmap template

A recommendation; swap in each team's own examples.

- **90 days, baseline:** place every team and two or three workflows, noting what blocks each. Agree the charter and owners ([AI intake checklist](../2-decide/ai-intake-checklist.md)). Engineering: shared repo context, [Agent-written pull requests and agent autonomy](../5-run/agent-pr-policy.md) at L1–L2, and baselines for review time, reverts and regret-free merges. Business: one narrow, checkable step ([Where should AI go in our product or operations first?](../2-decide/where-ai-goes-first.md)) with user-built evals ([Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md)).
- **6 months, first promotions:** one or two teams at E2; one brownfield workstream (flaky-test fixes, test-only PRs) at L3. The first pilot live as a B3 workflow, and one operations agent at L1–L2. Monthly reviews of token spend and the [What to measure: AI metrics scorecard](../5-run/ai-metrics-scorecard.md).
- **12 months, scale where it fits:** E3 where constraints allow; L4 only for named actions whose regret-free merge rate beats our engineers'. B4 agents with tested undo, and one learn-then-hand-off trial alongside the current path. Re-assess every team, noting who stayed put by choice.

## 6. Newer evidence

- **Independent data tempers throughput expectations.**
  - Ars Technica reported that Fiona Chen and James Stratton's Harvard study of Jellyfish engineering data first covered over 700 firms to March 2026.[17] In that version agents raised lines of code 30% and pull requests 23%, with no significant change in resolved issues, while review time rose 49%.[17]
  - The November revision (the current copy is dated 14 November 2026) covers 655 firms to August 2026: 35.7% more pull requests, a borderline-significant 13.7% rise in resolved issues, and 56.1% longer from review submission to approval ([the software factory memo](should-we-build-a-software-factory.md) has every figure).[16]
  - The study is observational, based on adoption timing.[16] In my reading, the revision softens October's no-change finding, but code still far outruns delivered work, and both versions back SEP and Finch on review as the limit. So we should treat SEP's six-fold and vendor figures as best cases, not plans.
- **Risk-tiered review is documented practice.** The Claude Code team sets human approvals with a risk classifier, and reports merged PRs more than doubling over June–September as the revert share fell over 40% (vendor figures).[18]
- **More agents cost more.** One preprint found agent teams beat solo agents at three to seven times the cost.[19]
- **Decision models are checked on live traffic.** Amazon engineers ran Sonnet 4.6 and Strands Decider side by side, judging every disagreement, with a 45-second switch back. They report equal results at 98% less cost (their claim).[20]
- **Accuracy is not reliability.** In SO-Arena, the best-performing decision model ranked only seventh for reliability ([Evals playbook](../4-build/evals-playbook.md#3-what-to-score)).[21] In my reading, that qualifies the vendor results above; at B5 we should test hand-backs and cases where none of the fixed answers fits.
- **Learn-then-hand-off updates Porter's per-task choice.** I think that, for repeated jobs, the mechanism chosen for a task can start expensive and get cheaper if a check controls the hand-back. AgentRun's figures are its own.[15] I know of no independent replication.

**Read next:** you've reached the end of the path. Go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory; Midwest AI Summit 2026 (Practical AI E378 transcript)
[2] https://ai.engineer/code/2026/talks/andrew-finch — Andrew Finch (Sonar), Building a Safe Software Factory, AI Engineer Code Summit 2026
[3] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[4] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AI Engineer Code Summit 2026
[5] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[6] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[7] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
[8] https://ai.engineer/code/2026/talks/doug-clauson — Doug Clauson (AWS, Kiro), Ship More as a Team of One with Kiro Crew, AI Engineer Code Summit 2026
[9] https://ai.engineer/code/2026/talks/justin-mccarthy — Justin McCarthy (Diffusion), Brownfield factories keep the promises you already made, AI Engineer Code Summit 2026
[10] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AI Engineer Code Summit 2026
[11] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows; Midwest AI Summit 2026 (Practical AI E379 transcript)
[12] https://midwestaisummit.com/jason-beutler — Jason Beutler (Robosource), The Order Matters: Structuring AI Projects Around People, Midwest AI Summit 2026 (abstract)
[13] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[14] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram & Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[15] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun (Parcha), Opus learns the job, a cheap model runs it (merchant-classification case study)
[16] https://fion.ac/jellyfish.pdf — Fiona Chen & James Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production (revised Nov 2026; copy dated 14 Nov 2026, accessed 15 Nov)
[17] https://arstechnica.com/ai/2026/10/ai-coding-agents-generate-more-code-but-not-more-software — Ars Technica, AI coding agents generate more code, but not more software
[18] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[19] https://arxiv.org/abs/2610.17471 — arXiv 2610.17471, Scaling Inference-Time Compute with Teams of Coding Agents
[20] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents blog, Amazon saves millions by replacing Sonnet 4.6 with Strands Decider
[21] https://huggingface.co/papers/2611.15777 — SO-Arena: Benchmarking the Capability Spectrum and Reliability of System One Models (arXiv 2611.15777)

