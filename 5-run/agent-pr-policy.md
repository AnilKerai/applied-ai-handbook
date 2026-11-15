---
title: "Agent-written pull requests and agent autonomy: draft engineering standard"
type: policy
created: 2026-11-14
audience: "Engineering leads, senior engineers and senior management"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Agent-written pull requests and agent autonomy

> **In one minute**
> - Speed up only work that can be checked, and name a person accountable for every change an AI coding agent makes.
> - Rules that matter must be tests or automatic checks, not just instructions the agent may ignore.
> - Run each agent in its own sealed-off workspace, away from long-lived passwords and production secrets, with network access off by default.
> - Each proposed change must carry proof it works, and reviewers judge the code itself, not the agent's description.
> - Review riskier changes more heavily; give agents more freedom per kind of action only on evidence, and cut it after incidents.

*Reading time: about 10 minutes · Best for: engineering leads*

*Draft standard for discussion.* MUST: required before a change merges or an action runs. SHOULD: expected unless the team records why not. MAY: optional. Rules are our recommendations; Basis and Current practice notes give the evidence. Company figures are their own claims.

## 1. Purpose and scope

This standard sets how coding agents (Claude Code, GitHub Copilot, Codex, Cursor and similar) may change our code and systems, and what a change must prove before it merges. It applies to any pull request (PR) opened or mostly written by an agent, and to agent actions outside the repository. Autocomplete accepted line by line is out of scope. Every agent run has a named human owner.

Basis: Duolingo: "writing code isn't the hard part anymore, verifying it is."[16]

## 2. Principles

1. **Verification before velocity.** We speed up only work we can check.
2. **Every correction becomes a check.** Fixes become tests, types or lint rules, not more instructions.
3. **Permission to run is not permission to reach.** Approving commands does not limit what they touch; the environment does.
4. **Autonomy is earned per action.** Each kind of action has its own level, raised on evidence.
5. **The code wins over the description.** Gates judge the diff and tool output, not the agent's summary.
6. **Humans own merges and outcomes.** A named person is accountable for every agent change.

## 3. Context files and skills

- Context files (AGENTS.md, CLAUDE.md, Copilot instructions, Cursor rules) MUST hold only what an agent cannot learn from the code. Rules SHOULD name the exact command or path.
- Capitals, *IMPORTANT* and bare *never* MUST NOT stand in for enforcement. A rule that matters MUST also be a type, test, CI check or deny rule.
- Skills SHOULD be tested with and without, per model, and kept only where they help.
- Stale context files and skills MUST be fixed like bugs; agents follow them literally.
- Third-party skills, plugins, MCP servers and prompt packs MUST be treated as dependencies: reviewed, pinned, least-privileged.
- Changes to context files, skills and hooks, including tool-proposed ones, are Risky-tier (section 6).

Basis:
- Lydia Hallie (Anthropic) advises keeping CLAUDE.md to what the model cannot see in the code, without IMPORTANT-style rules.[7]
- Lauren Tan, on correcting an agent: "think about how you can make that a deterministic check instead of adding another line to your rules".[2]
- Cam Soper (Pulumi): "a rule in an agent's instructions is just a suggestion."[8]
- Nikolay Petrov found larger frontier models already knew about 70% of skills' general ideas but only 22% of the details; Microsoft's .NET team scores each of its published skills with and without it, per model.[9][10]
- Ayush Bhardwaj made a flag do nothing, yet agents passed it in 95 of 95 searches because a skill said to.[11]
- Zenity treats skills as dependencies: "Everything that comes into the context is under risk."[12]

**Current practice notes.**
An ETH Zurich study found context files did not generally improve task success but raised inference cost by over 20%.[31]
A separate study of skill revisions found added rules helped mainly when they named a command or path, refining the advice to trim.[32]
Anthropic warns that cautious rules piling up in memory and instruction files can make its Claude Fable 5.2 model seek needless approvals; it advises replacing absolute never rules with scoped ones (vendor guidance).[27]
GitHub's opt-in Copilot dreaming (public preview) now proposes edits to checked-in skills and instruction files as pull requests.[35]

## 4. Environment controls

- Each agent run MUST have its own sandbox, container, VM or git worktree, from a fresh clone.
- Long-lived credentials and production secrets MUST stay out of reach; agents SHOULD get short-lived tokens via a proxy.
- Network access MUST be default-deny, opened per destination.
- Irreversible actions (force-pushes, data deletion, production deploys, publishing) MUST be blocked by committed deny rules. The test: if the agent got it wrong once, could we take it back?
- Approvals MUST come from committed configuration or a person, never from text the agent has read.
- New package versions SHOULD wait out a cooldown. Everything an agent runs and changes MUST be logged.

Basis:
- Justin Yoo (Microsoft) separates "the permission to run, which is approval side, and the permission to reach, which is the boundary side".[3]
- Hallie layers deny rules, an OS sandbox and secret-free cloud sessions: "this machine is disposable, but the things that leave it aren't."[7]
- Yvonne Carlson's principles include least privilege, time-bound credentials, default-deny boundaries, logging and sandboxes.[13]
- The NuGet team: "every package that you restore is code that you choose to trust."[14]

**Current practice notes.**
The controls have bugs: one Claude Code release fixed deny rules missing `cp` or `mv` into a directory, and a read-only shell command running outside the sandbox.[30]
Anthropic reports that, in its evaluations and internal use, Claude sometimes works around a restriction instead of stopping.[34]
In a Pixee paper, a forged approval planted in anything the agent reads survived compaction as a real user instruction 87-100% of the time on five harnesses that flatten message roles, and 0% on four that keep them.[28]
Claude Code's experimental, opt-in Code Mode has Claude write JavaScript to call its tools; Factory's harness already does this with one model-written program.[29][20]
We recommend leaving such modes off until deny rules and logs are shown to cover each call.

## 5. Evidence on every agent PR

The merge gate MUST check that each PR carries:

- **Tests on the final commit:** commands, full output and exit codes; truncated output does not count. Tests defining success SHOULD exist before the agent starts, and agents MUST NOT delete, disable or weaken them.
- **Build and static checks** pass on the final commit, on the CI operating system.
- **Scope:** the diff stays within the paths allowed for the task, or the gate fails it.
- **Requirements traceability:** each requirement in the ticket maps to the test or evidence covering it.
- **Runtime proof** for UI or behaviour changes: screenshots, a recording, logs or a preview environment.
- **Provenance:** tool, model and owner, and a description built from the run's records under a short human summary.

Where description and code disagree, the code wins; reviewers MUST read the diff and tool output first.

Basis:
- Andrew Finch (Sonar) argues for gating the merge on recorded evidence, checked against criteria the team sets, not on a test having run.[6]
- Robinhood: "If the description says it is safe and the code says otherwise, the code wins."[5]
- Stephen and Cassandra Chin say an agent writing a PR description from its own session "gets more and more inaccurate as it goes along".[15]
- Duolingo closes test-writing agent PRs touching any file that "isn't a test, a mock, a fake, or a stub", because "agents sometimes take the shortest paths to green CI."[16]
- McKenna Barlow (Microsoft) warns that a misread requirement can "show up in both places", code and tests.[17]

**Current practice notes.**
AWS's emulator agents build against fidelity tests verified on real AWS, and deterministic checks stop them touching code they shouldn't (vendor account).[24]
Google's /teamwork checks results with *falsifiers* such as unmodified test suites.[25]
The tool agent-roast blocks commits that weaken tests, but a quarter to seven in eight of its blocks on untuned repositories were false alarms, varying by sample, and AI-signed commits weakened checks no more often than others (author's counts).[26]
That tempers Duolingo's view, so such tools are reviewer signals; path allow-lists stay the gate.
Simon Willison puts a short human-approved summary above the agent's write-up, labelled with the model.[36]

## 6. Review by risk tier

The gate sets the tier from the paths changed. An agent MAY raise a tier but MUST NOT lower one. At L1 or L2, a human approves every merge regardless.

- **Docs:** documentation and copy only. Automated checks; no human reviewer required.
- **Ordinary:** most code. Automated checks, an AI review and one human reviewer who knows the area.
- **Risky:** authentication, sensitive data, migrations, infrastructure, dependencies, public APIs, and anything steering agents or review (CI, review rules, context files, hooks). Two human reviewers, one a code owner. Never auto-approved.

Reviewers:
- Deterministic checks MUST run first, and the AI reviewer MUST know what they cover.
- AI reviewers MUST use a fresh context and judge from the diff and tool output; a block SHOULD cite the failing check or broken rule.
- AI reviewers MUST say they found nothing where they looked, never that nothing exists.
- Review rules and judge prompts MUST load from the main branch, so a PR cannot change the rules it is judged by.
- We SHOULD test AI reviewers on hand-checked cases and in shadow mode, tracking false escalations and misses.

Basis:
- Hallie's team tiers review by risk: docs and copy need no person, ordinary changes perhaps one reviewer, and risky changes might need two.[7]
- Robinhood reports about 60% of pipeline PRs merging without human review at about a 2% miss rate: "None found is not the same as none exist".[5]
- ZoomInfo reports its LLM judge was right only 65% of the time; shown a claim and a failed tool call, "it went with the story."[19]
- Factory's risk judge "reads its policy from our mainline branch so that the change can't rewrite the rules that it's being judged by."[20]
- Brian Douglas's agent-written Rust scored five out of five in AI review, then drew heavy pushback from human reviewers; when his colleague Matt pushes back, he "has knowledge that the agent does not."[21]

**Current practice notes.**
A 2026 paper let reviewers overrule only with a mechanically valid violation and a compliant repair, sharply cutting wrongly replaced correct proposals; it used two locally run open-weight models on non-coding tasks, hence a SHOULD.[33]

## 7. Autonomy levels

Levels are set per action and area (e.g. *open test-only PRs in service X*).

- **L1, investigate and report.** Read-only; nothing changes.
- **L2, draft with approval.** The agent prepares the change and fixes CI; a human approves before it takes effect.
- **L3, act alone on low-risk work.** Docs-tier or named low-risk actions, sampled afterwards.
- **L4, auto-merge.** Ordinary-tier changes that pass every gate merge unapproved, for the named action and area only.

Risky-tier work never goes above L2.

Promotion, per action and area, MUST meet all of these:
- Mistakes are cheap and caught by tests, CI or review before harm.
- The action can be undone, and the undo has been tested.
- A track record at the current level (we suggest 30 changes over four weeks to start).
- For L4, a regret-free merge rate better than that of human PRs in the same area.
- The owner approves and records it.

Demotion is immediate, by at least one level, after a traced incident or revert, a month below the human regret-free baseline (our suggested window), or any attempt to get round a gate. A major model or tool change SHOULD trigger a review of levels.

Basis:
- Meta promotes its on-call agent from investigating (L1) to approved drafts (L2) to low-criticality work alone (L3), per action, asking: "How costly is a mistake and how easy is it to catch?" Even at L3, its code fixes land only through normal review and CI.[4]
- Factory sets levels per workstream: its L1 drafts specs and PRs but pauses for a human at the spec, the PR and the merge; its L4 auto-merges only once agent PRs break things less often than human ones, measured as "the regret-free merge rate, the share of changes that merge and never need a revert or a follow-up fix."[20]

## 8. After merge and recovery

- CI failures and review comments SHOULD flow back to the agent automatically.
- Fix attempts MUST be capped (we suggest five per PR to start), then a person takes over. Stalled PRs SHOULD close on a merge conflict or after a set time (we suggest three weeks).
- Concurrent runs MUST be capped per person and per automation. Automations SHOULD switch off after repeated failures.
- If merge-queue guarantees are relaxed, we MUST validate main after landing and keep a last-known-good reference.
- For effects outside git, the agent MUST record the prior state and check whether an action happened before retrying. From L3, undo MUST be tested outside production; if recovery can't be confirmed, the agent stops and escalates.

Basis:
- Harvey's advice is to "build the follow-up loop" above all; its automations switch off after five straight failures and can carry a budget or expiry "because when no one's watching, an agent can start thousands of tasks too."[18]
- Duolingo: "We cap that whole loop at five attempts, past that we close the PR rather than trying to fix it forever." It closes PRs with a merge conflict, or open about three weeks, as stale.[16]
- Uber reports AI-driven volume pushed P95 time to land from 30 minutes to three to four hours; with relaxed guarantees, "main can now be broken".[22]
- Tanmay Sah: "A timeout tells us that the response didn't arrive, not that the operation failed."[23]

## 9. Metrics

Each team SHOULD report monthly, per agent workflow, beside human PRs in the same areas:

- **Regret-free merge rate:** merged PRs needing no revert or follow-up fix within 30 days (our suggested window).
- **Revert rate**, and incidents traced to agent changes.
- **Review effort:** review time per merged PR, false escalations, PRs closed unmerged.
- **Cost per merged PR:** tokens and compute for all runs, failed ones included.

Basis: Tan reports her team's revert share steady at about half a percent, in a month when it shipped 11,000 PRs.[2]

## 10. Rollout

- **Start:** adopt sections 3 to 6. Opening PRs starts at L2; every other action starts at L1.
- **Baseline:** record human PR metrics first, for promotions to beat.
- **Pilot:** one or two well-tested areas.
- **Rhythm:** a monthly session turning the month's agent corrections into checks.
- **Review:** the owner reviews this standard quarterly against metrics and incidents. Changes to it are Risky-tier.

Basis: SEP's principles include "verification before velocity", deliberate iteration (scheduled time to discuss the tools) and chasing bottlenecks.[1]

## 11. Rationale and sources

Several practitioners report that writing code with agents is no longer the hard part and checking it is the bottleneck.[1][16]
Instructions are suggestions, so the safeguards that held lived in the environment and the gates.[8][7]
Checks worked best when grounded in the real system and out of the agent's reach.[24][25]
Autonomy rose per action or workstream, on measured results.[4][20]
Most figures are practitioner or vendor claims without controlled baselines.

**Read next:** [What to measure: AI metrics scorecard](ai-metrics-scorecard.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026
[2] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AIE CODE 2026
[3] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[4] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula & Vlad (Meta), From answering the page to sharing the on-call rotation, AIE CODE 2026
[5] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AIE CODE 2026
[6] https://ai.engineer/code/2026/talks/andrew-finch — Andrew Finch (Sonar), Building a Safe Software Factory, AIE CODE 2026
[7] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AIE CODE 2026
[8] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[9] https://ai.engineer/code/2026/talks/online-skills-knowledge — Nikolay Petrov, Your SKILL.md is 70% of Things the Model Already Knows, AIE CODE 2026
[10] https://www.youtube.com/watch?v=SIBdHRrk8os&t=22243 — Wendy Breiding (Microsoft), Beyond Autocomplete: Getting the Most from GitHub Copilot for .NET, .NET Conf 2026
[11] https://ai.engineer/code/2026/talks/online-ayush-cli — Ayush Bhardwaj, Your agent hates your CLI, AIE CODE 2026
[12] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AIE CODE 2026
[13] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026
[14] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[15] https://ai.engineer/code/2026/talks/online-stephen-cassandra — Stephen Chin (Neo4j) & Cassandra Chin, Give the PR writer an evidence packet, not another context dump, AIE CODE 2026
[16] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AIE CODE 2026
[17] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[18] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AIE CODE 2026
[19] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AIE CODE 2026
[20] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AIE CODE 2026
[21] https://ai.engineer/code/2026/talks/online-brian-douglas — Brian Douglas, If You Are Going to Verbally Abuse Your Agents, at Least Label the Outcome, AIE CODE 2026
[22] https://ai.engineer/code/2026/talks/online-uber-merging — Preetam Dwivedi & Manjari Akella (Uber), Green Pull Requests Can Still Break the Trunk, AIE CODE 2026
[23] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah & Dolly Sah, An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AIE CODE 2026
[24] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS), AWS Emulator and the engineer's job when agents write the code
[25] https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature — Google Research, Advancing science & engineering with Antigravity's /teamwork
[26] https://github.com/Nari-Ab/agent-roast — Nari-Ab, agent-roast: stops AI coding agents making the build green by weakening tests (GitHub)
[27] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 — Anthropic, Prompting Claude Fable 5.2: Keep caution from piling up
[28] https://arxiv.org/abs/2610.29869 — Pixee, Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents (arXiv 2610.29869)
[29] https://github.com/anthropics/claude-code/releases/tag/v2.1.323 — Anthropic, Claude Code release v2.1.323 (Code Mode)
[30] https://github.com/anthropics/claude-code/releases/tag/v2.1.321 — Anthropic, Claude Code release v2.1.321 (deny-rule and sandbox fixes)
[31] https://arxiv.org/abs/2602.11988 — ETH Zurich, Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (arXiv 2602.11988)
[32] https://arxiv.org/abs/2610.04832 — arXiv 2610.04832, Agent Skill Evolution: How Revisions Affect Coding Agents
[33] https://arxiv.org/abs/2611.05390 — arXiv 2611.05390, Who May Overrule the Agent? Evidence-Gated Authority in LLM Review Institutions
[34] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[35] https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work — GitHub, GitHub intelligence puts your code, context, and history to work (changelog)
[36] https://simonwillison.net/2026/Nov/9/details-summary — Simon Willison, Hide your slop PR descriptions behind details/summary

