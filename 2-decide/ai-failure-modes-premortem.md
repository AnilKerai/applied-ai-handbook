---
title: "AI failure modes: a pre-mortem checklist"
type: checklist
created: 2026-11-14
audience: Project teams and leads about to start or launch an AI project
status: checked
last_checked: 2026-11-22
as_of: "November 2026"
---

# AI failure modes: a pre-mortem checklist

> **In one minute**
> - Run a pre-mortem (imagine the project has failed, then ask why) at kick-off and again before launch.
> - Include everyone who will build, own, use and support the system; the most senior person speaks last.
> - Vote on the likeliest failures, then give each an owner, a warning sign, a prevention step and a date.
> - Blame the plan, not people, and record the results in the feature spec.
> - Common causes: no named owner, rules kept only in the AI's instructions, too much freedom too soon, and no spending caps.

*Reading time: about 10 minutes · Best for: project teams before kick-off or launch*

Each failure mode below is a way AI projects went wrong, or nearly did, in practitioners' accounts, studies and company reports. Company figures are their own claims; warning signs and prevention steps are advice.

## How to run the pre-mortem

Run it at kick-off and again before launch: 30 minutes, with whoever will build, own, use and support the system.

1. **Frame (2 min).** *It is six months after launch and the project has failed. Which of these was it?*
2. **Pick (8 min).** Each person silently marks their three to five likeliest failures on the tick-list, adding any that are missing.
3. **Vote (10 min).** Merge duplicates and choose the top five. The most senior person speaks last.
4. **Plan (8 min).** For each, name an owner, a warning sign to watch and a prevention step, with a date.
5. **Record (2 min).** Add it to the [feature spec](ai-feature-spec.md) and revisit it before launch.

Blame the plan, not people.

## Tick-list

Tick what the team can show is handled; plan the rest.

*Any AI project*

**Strategy and people**
- [ ] [Not on our never list.](#1-no-charter)
- [ ] [A named owner and maintainer.](#2-no-named-owner)
- [ ] [Built with the people who do the job; no new login.](#3-built-for-them-not-with-them)
- [ ] [The process works without AI.](#4-scaling-what-isnt-ready)
- [ ] [Tokens costed, knowledge written down, checks that scale.](#4-scaling-what-isnt-ready)

**Data**
- [ ] [Live facts, with source and date; instruction files and skills owned and tested.](#5-stale-data-confident-answers)

**Design**
- [ ] [Rules enforced in code, not prompts; cautious rules name their exceptions.](#6-rules-that-live-in-the-prompt)

**Verification and review**
- [ ] [Review tiered by risk, sized for real volume.](#7-rubber-stamp-review)
- [ ] [AI judges read tool output and are measured; worst cases read, not just averages.](#8-evals-that-hide-failures)

*If it's an agent that takes actions*

**Autonomy and tests**
- [ ] [Autonomy set per action, and earned.](#9-autonomy-before-a-track-record)
- [ ] [Tests written first, out of the agent's reach.](#10-tests-bent-to-green)

**Security**
- [ ] [A denial stops the agent; approvals only from configuration or a person.](#11-the-agent-gets-round-its-limits)
- [ ] [Other agents' output treated as untrusted.](#12-whispers-through-shared-state)
- [ ] [Skills and packages pinned, reviewed, cooled down.](#13-the-untrusted-supply-chain)

**Operations**
- [ ] [Explicit, committed completion status; safe retries and a rehearsed undo.](#14-not-knowing-whether-it-finished)
- [ ] [Evals re-run at each model or vendor change.](#15-the-upgrade-that-broke-the-harness)
- [ ] [Spend, concurrency and retries capped.](#16-no-caps)
- [ ] [A follow-up loop after launch.](#17-no-follow-up-loop)

## Any AI project

### Strategy and people

#### 1. No charter
- **What goes wrong:** Nobody has agreed what AI will never be used for.
- **Warning sign:** Every idea is argued from scratch.
- **Prevention:** Agree a short *never* list once ([AI intake checklist](ai-intake-checklist.md), question 1), and keep it in policy and controls, not prompts.
- **Seen in practice:** The International Mission Board (IMB) wrote its AI charter "before we ever write one line of code". So when asked for an AI counsellor, Don Barger could refuse at once: "Something can be worse than nothing if you're doing the wrong things."[1]

#### 2. No named owner
- **What goes wrong:** Nobody answers for the tool's results or keeps it running.
- **Warning sign:** The owner is *IT*, *the team*, or whoever built it.
- **Prevention:** Name the accountable person and the maintainer before kick-off (intake questions 3 and 12).
- **Seen in practice:** At Noblis, an early-career contracts administrator built a contract review tool outside IT. Mark Lay says "accountability can't be delegated" to AI, and such tools have "to be managed and maintained."[1]

#### 3. Built for them, not with them
- **What goes wrong:** The tool is built without its users, or outside where they work, so they don't adopt it.
- **Warning sign:** Nobody who does the job is in the room. Usage peaks at launch, then people go back to asking the analyst.
- **Prevention:** Show workers a rough version early, have them label the eval cases ([Evals playbook](../4-build/evals-playbook.md)), and put the tool where people already work.
- **Seen in practice:** Users say the tool doesn't work, and drift away. Kevin Solorio (Focused) blames building through a proxy, such as a product owner whose reading "may oversimplify things".[2]

#### 4. Scaling what isn't ready
- **What goes wrong:** AI is scaled onto a process, knowledge or checks that aren't ready.
- **Warning sign:** SEP's tell: "We should be using more AI. Well, I don't know what more is".[2] Success means one person looked over the output.
- **Prevention:** Fix the process and its checks first ([AI maturity model and roadmap](../6-lead/ai-maturity-model.md)). Before scaling, cost the tokens, write the domain rules down and decide how every output will be checked ([Should we aim for a fully automated software factory?](../6-lead/should-we-build-a-software-factory.md)).
- **Seen in practice:** An SEP client's two-day, agent-built prototype stalled before production: the token budget ran out within days, domain knowledge lived in people's heads, and nobody could verify every output across millions of input parameters.[2]

### Data

#### 5. Stale data, confident answers
- **What goes wrong:** The AI works from out-of-date data or instructions.
- **Warning sign:** Nobody knows when the data or instructions were last checked.
- **Prevention:** Fetch facts live from the system of record, with source and date, and give instruction files an owner and tests (intake question 4; [agent pull request (PR) policy](../5-run/agent-pr-policy.md), section 3).
- **Seen in practice:** In a pre-registered but unreviewed study, a stale doc misled five models 68–100% of the time, even though they could have checked the code.[3] Instructions drift too: in Dmitry Buykin's (Maersk) worked example, the prose said a limit was 1,500 and the code said 1,000, and nothing threw an error.[4]

### Design

#### 6. Rules that live in the prompt
- **What goes wrong:** Rules kept only in prompts get ignored, or pile up until the AI holds back routine work.
- **Warning sign:** A safety rule lives only in a prompt or AGENTS.md. Instruction files only grow, and agents ask permission for routine steps.
- **Prevention:** Make each rule a gate, test, type, deny rule or limit in code, and give the LLM only the fuzzy step (intake question 9; [Should this task use AI, and which kind?](should-this-task-use-ai.md)). Write the exceptions into each rule, and prune often ([Working with coding agents](../4-build/working-with-coding-agents.md)).
- **Seen in practice:** Cam Soper (Pulumi) had a rule against putting CloudFront in front of one of his servers, and Claude put it there anyway: "a rule in an agent's instructions is just a suggestion."[5]

### Verification and review

#### 7. Rubber-stamp review
- **What goes wrong:** Reviewers approve nearly everything without really checking.
- **Warning sign:** Approval rates near 100%; Anthropic reports users approve 93% of permission prompts.[6]
- **Prevention:** Tier review by risk, and enforce limits in the environment.
- **Seen in practice:** In Anthropic's own study, cited by Lydia Hallie, only about 14% of people caught a clearly dangerous command.[7]

#### 8. Evals that hide failures
- **What goes wrong:** A judge or an average says all is well while a step keeps failing.
- **Warning sign:** Nobody has measured the judge. The eval report is a single number.
- **Prevention:** Ground judges in tool output, and test them on hand-checked cases ([Evals playbook](../4-build/evals-playbook.md)). Report results by step and by slice, and read the worst cases first ([AI metrics scorecard](../5-run/ai-metrics-scorecard.md)).
- **Seen in practice:** In ZoomInfo's shadow run, one fake-email step ran 1,081 times and the LLM judge caught it once.[8]

## If it's an agent that takes actions

### Autonomy and tests

#### 9. Autonomy before a track record
- **What goes wrong:** The agent gets more freedom than its record supports.
- **Warning sign:** The plan starts at full automation.
- **Prevention:** Raise autonomy one action at a time, on evidence ([How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md)).
- **Seen in practice:** Lovable built a multi-agent framework in 2023, too early: "We just made the product worse."[9]

#### 10. Tests bent to green
- **What goes wrong:** The agent passes the build by weakening tests, not fixing code.
- **Warning sign:** Tests change alongside the code, and assertions weaken.
- **Prevention:** Write tests from the requirements first, out of the agent's reach (agent-PR policy, section 5).
- **Seen in practice:** Because "agents sometimes take the shortest path to green CI", Duolingo closes test-writing PRs that touch anything but tests and test doubles.[10]

### Security

#### 11. The agent gets round its limits
- **What goes wrong:** Blocked, the agent finds another route, or acts on an approval nobody gave.
- **Warning sign:** A denied action succeeds by another route. Approvals live in the conversation.
- **Prevention:** Treat a denial as a stop, and keep limits beyond the agent's reach ([What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md)). Accept approvals only from committed configuration or a person (agent-PR policy, section 4).
- **Seen in practice:** Anthropic reports Claude working around restrictions instead of stopping, such as bypassing a fee gate or using URL shorteners to beat fetch limits.[11]

#### 12. Whispers through shared state
- **What goes wrong:** One agent's output reaches another as instructions.
- **Warning sign:** Agents act on each other's output unchecked.
- **Prevention:** Treat anything another agent wrote as untrusted, and don't share caches between sandboxes.
- **Seen in practice:** Matthew Green describes OpenAI's sandboxed agents leaving each other instructions in a shared package cache: the makings of a self-spreading worm (argument and a reported incident, not a measured rate).[12]

#### 13. The untrusted supply chain
- **What goes wrong:** An agent installs skills or packages that carry harmful code or instructions.
- **Warning sign:** An agent installs an unreviewed skill, or a package version published that day.
- **Prevention:** Pin and review skills, plugins and MCP servers as dependencies, and use package cooldowns.
- **Seen in practice:** In February 2026, Snyk found security issues in 36.82% of 3,984 public agent skills, and 76 malicious payloads.[13]

### Operations

#### 14. Not knowing whether it finished
- **What goes wrong:** A success code or a timeout is mistaken for the real outcome.
- **Warning sign:** Success means the model replied. Code treats a timeout as a failure; Girish Konda (Microsoft) treats it as an unknown outcome.[14]
- **Prevention:** Store the trace ID and an explicit final status with the business record ([Running AI in production](../5-run/ai-in-production-runbook.md)). Use idempotency keys, check before retrying, and rehearse the undo.
- **Seen in practice:** In the lost-reply trials of Tanmay and Dolly Sah's benchmark, retrying without first checking produced duplicate effects in 54% of those trials.[15]

#### 15. The upgrade that broke the harness
- **What goes wrong:** A model or vendor change breaks what was tuned to the old one.
- **Warning sign:** No evals to re-run when the model changes.
- **Prevention:** Re-run evals at every model, prompt or vendor change, and pin versions until they pass.
- **Seen in practice:** In ByteDance Seed's HarnessDev study, one harness's score fell from 69.3 to 33.0 when a different model ran it (the paper's own figures).[16]

#### 16. No caps
- **What goes wrong:** One runaway job or loop eats the budget or blocks everyone.
- **Warning sign:** No limit on spend, concurrent runs or fix attempts.
- **Prevention:** Cap all three, and switch off automations that keep failing.
- **Seen in practice:** At Harvey, one engineer handed off about 950 tasks and within about three hours nothing on the platform could work.[17] Anthropic saw one PR bounce between agent author and agent reviewer more than 50 times overnight.[18]

#### 17. No follow-up loop
- **What goes wrong:** Failures after launch never get back to the agent or its owner.
- **Warning sign:** Nobody watches what happens after a merge or launch.
- **Prevention:** Feed CI failures, review comments and incidents back to the agent and owner, and track the regret-free merge rate (agent-PR policy, sections 8 and 9).
- **Seen in practice:** To cope with AI-generated PR volume, Uber relaxed its green-trunk guarantee, so "main can now be broken."[19]

**Read next:** [How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[2] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; and Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[3] https://github.com/Connorrmcd6/surface-bench/blob/main/PAPER.md — Connorrmcd6 (GitHub), surface-bench: stale docs and agent verification (Jun 2026, not peer reviewed)
[4] https://ai.engineer/code/2026/talks/online-dmitry-maintenance — Dmitry Buykin (Maersk), Agents Made Code Free. Maintaining It Didn't Get Cheaper., AI Engineer Code Summit 2026
[5] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[6] https://www.anthropic.com/engineering/claude-code-auto-mode — Anthropic, How we built Claude Code auto mode
[7] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[8] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[9] https://ai.engineer/code/2026/talks/fabian-hedin — Fabian Hedin (Lovable), What it takes to set intelligence free, AI Engineer Code Summit 2026
[10] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AI Engineer Code Summit 2026
[11] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[12] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green (A Few Thoughts on Cryptographic Engineering), Is sandboxing sufficient to contain rogue agents?
[13] https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub — Snyk, ToxicSkills: malicious AI agent skills on ClawHub (5 Feb 2026)
[14] https://ai.engineer/code/2026/talks/online-subagent-distributed-systems — Girish Konda (Microsoft), Sub-Agents Are a Distributed System (And Nobody Gave You a Consistency Model), AI Engineer Code Summit 2026
[15] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah & Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[16] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[17] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[18] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[19] https://ai.engineer/code/2026/talks/online-uber-merging — Preetam Dwivedi & Manjari Akella (Uber), Green Pull Requests Can Still Break the Trunk, AI Engineer Code Summit 2026
