---
title: "What to measure: AI metrics scorecard"
type: scorecard
created: 2026-11-14
audience: "Engineering leads and senior leadership"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# What to measure: AI metrics scorecard

> **In one minute**
> - Compare against a baseline, such as human work or the pre-AI process, and pair every speed measure with a quality one.
> - For coding agents (AI that writes code), measure whether changes hold up without being undone, and whether real work finishes sooner.
> - For business AI, measure task success on real cases, how bad the worst errors are, cost, and the business outcome.
> - Treat tokens (units of AI billing), lines of code and usage counts as cost or context, never as targets.
> - Steer week to week on early signals, but give AI more freedom only on longer-term results, such as bugs and incidents.

*Reading time: about 10 minutes · Best for: engineering leads and leadership*

*A starting scorecard: adapt it to your team.* How to tell whether AI is working: (A) coding agents in engineering, (B) AI features and agents in the business. The formulas and the template are recommendations; Evidence lines report sources, and company figures are their own, mostly unbaselined, claims.

This scorecard expands section 9 of [Agent-written pull requests and agent autonomy](agent-pr-policy.md) and the measurement answer in [AI questions answered](../1-understand/ai-questions-answered.md); evals are in [Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md).

## Ground rules

- Compare with a baseline: human PRs in the same areas, or the process before AI. Heidi Porter (Moyer Group AI): "measure quality against your own baselines".[10]
- Report monthly per workflow or feature; pair every speed metric with a quality one.

## A. AI in engineering (coding agents)

**1. Regret-free merge rate vs human PRs**
- *Tells you:* whether agent changes hold up as well as human ones; the policy's auto-merge bar.
- *Formula:* merged agent PRs with no revert or follow-up fix within 30 days ÷ merged agent PRs, beside the human figure.
- *Watch out for:* untraced follow-up fixes; an easy work mix flatters it.
- *Evidence:* Factory auto-merges only once agent PRs beat human ones on this measure, tracing reverts and errors to their PRs.[1] Duolingo warns "agents sometimes take the shortest path to green CI."[3]

**2. Revert and rework rate**
- *Tells you:* how much work had to be undone or redone.
- *Formula:* reverted PRs ÷ merged PRs; rework is change-request rounds and commits after first review, per merged PR.
- *Watch out for:* fixes landed as new PRs rather than reverts; count both.
- *Evidence:* Lauren Tan reports reverts of about half a percent in a month of 11,000 PRs.[2] Anthropic's Claude Code team reports merged PRs more than doubling from June to September while the reverted share fell over 40% (its claim).[4]

**3. Review time and review load**
- *Tells you:* whether review, usually the bottleneck, copes.
- *Formula:* median and 95th-percentile (p95) time from PR opened to merged; human approvals, comments and waiting time per merged PR.
- *Watch out for:* faster can mean rubber-stamping; Jeffrey Palermo (Clear Measure) called a hundred PRs at 45 seconds each no review.[8]
- *Evidence:* Across 655 firms, time from review submission to approval rose 56.1% with coding agents (observational, to August 2026).[5] Uber reports AI-driven volume pushed p95 time to land from 30 minutes to three to four hours; relaxing its merge guarantees brought it back to 30 minutes.[7]

**4. Cost per accepted change**
- *Tells you:* what a kept change really costs.
- *Formula:* spend on all runs, failed ones included, plus review time ÷ merged changes not reverted within 30 days (extends the policy's cost per merged PR).
- *Watch out for:* dropping failed runs or review time.
- *Evidence:* DORA recommends pairing outcome metrics with "cost per accepted change and code rework rates".[6] Steve Yegge's factory burns about 5 billion tokens a day, yet "the more agents I deploy, the more humans I need."[9]

**5. Lead time for real outcomes**
- *Tells you:* whether requested work finishes sooner, not whether more code moves.
- *Formula:* median time from issue or alert to fix live in production; resolved issues per month.
- *Watch out for:* issue-splitting; the bottleneck moving elsewhere, as SEP warns.[10]
- *Evidence:* In the Harvard study, agents raised PRs by 35.7% but resolved issues by only 13.7%, a borderline-significant rise.[5] Meta says about three quarters of its new code is now written with AI, yet on-call did not speed up.[20]

**6. Escaped defects**
- *Tells you:* what got past every gate.
- *Formula:* incidents and bugs traced to agent PRs ÷ merged agent PRs, by severity, beside the human figure.
- *Watch out for:* without provenance on each PR, the agent column reads zero.
- *Evidence:* Andrew Finch (Sonar) describes post-deploy checks (still early) and scheduled scans that catch slow drift, quoting Sonar's CEO: "code is abundant, confidence is not."[11] Robinhood reports about a 2% miss rate for its review agent, mostly rule gaps (its claim).[12]

**7. Human override and pushback rate**
- *Tells you:* where people know more than the agent, and whether they still check.
- *Formula:* agent PRs with changes requested or closed unmerged ÷ agent PRs; AI review comments marked wrong ÷ all; false escalations ÷ escalations.
- *Watch out for:* near-zero pushback may be fatigue: Anthropic reports users accept 93% of permission prompts,[14] and in an Anthropic study Lydia Hallie cited, only about 14% caught a clearly dangerous command.[15]
- *Evidence:* Brian Douglas reads an expert colleague's pushback as a sign "he has knowledge that the agent does not."[13] Anthropic sorts each AI review comment by response: fixed, wrong, intentional or not mattering.[4]

**8. Agent PR share by risk tier**
- *Tells you:* where agents work, and whether light review stays on low-risk work.
- *Formula:* agent PRs ÷ all PRs, and the share merged without human review, per tier (docs, ordinary, risky).
- *Watch out for:* share is context, not a target; tiers come from paths changed, not the agent.
- *Evidence:* Anthropic's classifier sets the tier from the change, not the author.[4] Robinhood reports about 60% of pipeline PRs merging without human review (its claim).[12]

## B. AI features and agents in the business

**1. Task success, offline and online**
- *Tells you:* whether it does the job on real cases, before and after launch.
- *Formula:* on an eval set of real cases, the share passing all of at least three runs (pass^k), with a confidence interval, as in the evals playbook; successes ÷ sampled live tasks, checked against the business record.
- *Watch out for:* unchecked LLM judges; an agent reporting success is not success.
- *Evidence:* Kevin Solorio (Focused): "an agent without evals is a proof of concept"; he scores live traces too.[10] ZoomInfo's LLM judge proved right only 65% of the time against hand-checked labels.[16] Shweta Iyer (Microsoft) showed an agent call succeed while the business request failed.[17]

**2. Worst-case error severity**
- *Tells you:* how bad the bad results are.
- *Formula:* errors per 1,000 tasks by severity, the worst class (such as a missed case) reported alone; the worst ten reviewed monthly.
- *Watch out for:* severity classes not agreed with the business owner up front.
- *Evidence:* Porter: "averages can hide a bad result".[10] In her Stanford case, a small sample of missed patients showed more process errors than LLM errors.[10]

**3. Escalation and hand-back rate**
- *Tells you:* how often AI hands work to people, and whether they can absorb it.
- *Formula:* tasks escalated or handed back ÷ tasks; escalations per reviewer per day against capacity.
- *Watch out for:* too low may be overconfidence; too high saves no time.
- *Evidence:* Robinhood: "A gate that escalates everything is not actually saving anyone any time."[12] Don Barger (International Mission Board) could take over critical chatbot conversations at 5,000 users: "It is not possible when you have 2,500,000 users."[18]

**4. Human override rate and time to dismiss a flag**
- *Tells you:* whether suggestions are useful, and quick to dismiss when wrong.
- *Formula:* recommendations overridden or declined ÷ recommendations reviewed; median time from flag raised to resolved.
- *Watch out for:* near-zero overrides can mean what Porter calls "rubber stamping fatigue".[10]
- *Evidence:* Stanford's navigator over-flags by design: physicians agreed with 97% of its negative answers and declined about four in ten flagged patients.[10] AeroCore's flags were set and tracked while it built a resolution system.[18]

**5. Adoption and active use**
- *Tells you:* whether intended users choose it.
- *Formula:* weekly active ÷ intended users; share of the task done in the tool, not workarounds.
- *Watch out for:* mandates inflate it; DORA notes adoption does not guarantee impact.[6]
- *Evidence:* AeroCore's data agent took off once it moved into Microsoft Teams: "No one likes an extra login."[18]

**6. Cost per task and latency**
- *Tells you:* whether it is affordable and fast enough.
- *Formula:* spend plus human review time ÷ completed tasks; median and p95 time per task.
- *Watch out for:* cost reported apart from success rate.
- *Evidence:* Philipp Schmid (Google DeepMind) measures efficiency, not just scores: harnesses scoring about the same differed almost twofold in cost.[19]

**7. Outcome metrics**
- *Tells you:* whether the business is better off, on a measure agreed before building.
- *Formula:* that measure (hours, errors, meetings, cycle time) before and after, over equal periods.
- *Watch out for:* no controlled baseline, which an outside review notes AeroCore's results lack;[21] saved hours count only if reused.
- *Evidence:* Mark Lay (Noblis): if AI gives neither a better nor a more efficient result, don't use it.[18] AeroCore cancelled that month's reconciliation meeting, usually five to six person-hours: "There were no incorrect work orders."[18]

**8. Incident count**
- *Tells you:* harm AI caused in production.
- *Formula:* incidents traced to AI per month, by severity, with time to detect and near misses.
- *Watch out for:* untraced incidents go uncounted.
- *Evidence:* Lay counts it a human duty to "monitor the behavior of the agents".[18] Iyer stores the trace ID with business records, so failures can be followed end to end.[17]

## Vanity metrics to avoid

- **Tokens.** DORA calls token counts an easily gamed input metric; the biggest spenders often gain little throughput at ten times the cost.[6]
- **Lines of code and PR counts.** In the Harvard study both rose far faster than resolved issues did.[5] DORA lists lines of code and commit counts among past vanity metrics.[6]
- **Usage for its own sake.** Among the complaints SEP says teams may hear: "We should be using more AI. Well, I don't know what more is".[10]
- Show these as cost or context, never as targets.

## Leading and lagging indicators

- **Leading** (weekly): eval pass^k, judge agreement with hand labels (kappa), review load, pushback, override and escalation rates, cost per task, active use.
- **Lagging** (monthly or quarterly): regret-free merge rate, escaped defects, incidents, lead time, outcome metrics.
- Steer on leading indicators and promote autonomy only on lagging ones, as the policy does.

## Monthly scorecard template

```text
AI scorecard: <team or feature>, <month>. Owner: <name>

A. Engineering (agent vs human)
- Regret-free merge rate (30 days): __% vs __%
- Revert rate __% vs __% | escaped defects __ vs __
- Review time p50/p95: __ / __ hours
- Cost per accepted change: £__
- Issue to production p50: __ days
- Pushback on agent PRs: __%
- Agent PR share: docs __% | ordinary __% | risky __%

B. Business
- Task success: eval set pass^3 __% (±__) | live __%
- Worst-severity errors per 1,000 tasks: __
- Escalation __% | override __% | time to dismiss a flag __
- Weekly active users: __ of __
- Cost per task £__ | latency p50/p95 __ / __ s
- Outcome vs baseline: <measure> __ -> __
- Incidents: __ (worst severity __)

Autonomy changes, evals added, decisions needed: <lines>
```

Related: [Running AI in production](ai-in-production-runbook.md) · [AI maturity model and roadmap](../6-lead/ai-maturity-model.md) · [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md)

**Read next:** [What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AIE CODE 2026
[2] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AIE CODE 2026
[3] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AIE CODE 2026
[4] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[5] https://fion.ac/jellyfish.pdf — Chen & Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[6] https://dora.dev/insights/finding-balance-in-the-era-of-tokenmaxxing — DORA (Evan Conaway), Finding balance in the era of tokenmaxxing
[7] https://ai.engineer/code/2026/talks/online-uber-merging — Preetam Dwivedi & Manjari Akella (Uber), Green Pull Requests Can Still Break the Trunk, AIE CODE 2026
[8] https://www.youtube.com/watch?v=TF6qzdKwl84&t=26062 — Jeffrey Palermo (Clear Measure), .NET AI Architecture and DevOps, .NET Conf 2026
[9] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (Independent), Software Factories: Escape from Trash Mountain, AIE CODE 2026
[10] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; and Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[11] https://ai.engineer/code/2026/talks/andrew-finch — Andrew Finch (Sonar), Building a Safe Software Factory, AIE CODE 2026
[12] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AIE CODE 2026
[13] https://ai.engineer/code/2026/talks/online-brian-douglas — Brian Douglas (organisation unconfirmed), If You Are Going to Verbally Abuse Your Agents, at Least Label the Outcome, AIE CODE 2026
[14] https://www.anthropic.com/engineering/claude-code-auto-mode — Anthropic, How we built Claude Code auto mode
[15] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AIE CODE 2026
[16] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AIE CODE 2026
[17] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[18] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[19] https://ai.engineer/code/2026/talks/philipp-schmid — Philipp Schmid (Google DeepMind), I deleted 90% of my harness (And It Got Better), AIE CODE 2026
[20] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula & Vlad (Meta), From answering the page to sharing the on-call rotation, AIE CODE 2026
[21] https://intelligentartifact.com/posts/practical-ai-midwest-summit-boundaries-and-accountability — Intelligent Artifact, review of Practical AI's Midwest AI Summit Part 2

