---
title: AI feature spec template
type: template
created: 2026-11-14
audience: Product owners and engineers proposing an AI feature
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# AI feature spec template

> **In one minute**
> - Use this template for any feature where AI drafts, decides or acts.
> - Fill it in after the intake checklist and before any code, with the people who will use the feature.
> - It turns the checklist answers into commitments the team builds and tests against.
> - It covers a named owner, data, tests, human checks, safety rules in code, costs, rollout and reversing it.
> - Keep it short, especially for a small feature, and list unknowns as open questions rather than guessing.

*Reading time: about 5 minutes · Best for: product owners and engineers*

Use this for any feature in which AI drafts, decides or acts. Run the [AI intake checklist](ai-intake-checklist.md) first; this spec turns its answers into commitments the team builds and tests against. Write it before any code, with the people who will use the feature, and keep it short: a line or two per section suits a small feature. Put unknowns under Open questions rather than guessing.

## The template

*Copy everything from here to the end of section 16 into a new document.*

- **Feature:**
- **Proposer and date:**
- **Status:** draft / agreed / in pilot / live / retired
- **Intake checklist answers:** link

### 1. Problem and user

*Who does this job today, what goes wrong, and how do we know? Name the users who helped write this spec. Describe the problem without mentioning AI.*

### 2. Why AI (better or more efficient)

*Today's baseline for quality, cost and time, and the result we expect instead. If AI makes the result neither better nor more efficient, stop here.*

### 3. Charter check ('never' list)

*Confirm the feature touches nothing on our 'never' list. Note anything it comes close to, and how we stay clear of it.*

### 4. Accountable owner and data steward

*One named person accountable for every output, and the named steward of each dataset the feature uses. A committee or a department is not an owner.*

### 5. Data sources and freshness

*Each system of record the feature reads, who owns it, and how current it must be. Say how facts are fetched at the moment of use, rather than taken from the model's memory.*

### 6. Mechanism chosen and why (rules / ML / decision model / workflow + LLM / bounded agent)

*The mechanism for each step, and why each simpler option was not enough. A bounded agent needs its tools, limits and stopping rules listed.*

### 7. Acceptance criteria and eval plan

*Testable criteria, written before the build. The eval set: real cases labelled with users, worst cases included. How cases are graded (code checks, people, or an AI judge we have measured), the pass bar, and the worst single result we accept.*

### 8. Execution dial and human role

*For each action: a person approves first, the system acts above a confidence threshold and escalates the rest, it acts with an undo window, or it acts alone. Who reviews what, at what volume, and how we stop reviews becoming a rubber stamp.*

### 9. Guardrails in code (where enforced)

*Each rule the feature must never break, and the gate, check, limit or permission that enforces it. A rule that lives only in a prompt does not count.*

### 10. Security and data handling

*What the AI can reach, with which credentials and for how long. What data leaves our environment and under which contract terms. Confirm that no session combines private data, untrusted input and a way to send data out.*

### 11. Observability (trace ID on the business record)

*What we record on each run, and how the trace ID is stored with the business record it changed, so we can tell a reply from an outcome that actually succeeded.*

### 12. Failure handling and undo

*What happens on a timeout, a wrong answer or a partial failure. How each action is undone, and when that undo was last tested.*

### 13. Cost budget and caps

*Expected cost per task and per month. Hard caps on spend, runs and retries, and who is alerted when a cap trips.*

### 14. Rollout and adoption (in existing tools, with users)

*Where users will meet the feature (inside a tool they already use), the pilot group, any shadow or limited launch, and how users report problems.*

### 15. Maintenance and reversibility

*Who runs it after launch. When the evals re-run (at least on every model, prompt or data change). What switching it off or reversing it would cost.*

### 16. Open questions

*Decisions not yet made, each with an owner and a date. Record decisions taken, and options rejected, here too, so the spec stays the one record of the design.*

## Why each section is here

A written spec matters more when AI does the building or the deciding. Michael Washington (Microsoft MVP) lets AI write all of an app's code but none of its design, because "if you don't decide, the AI will."[1] Doug Clauson (AWS) finds that with agents "quality really becomes a testing problem."[2] McKenna Barlow (Microsoft) generates tests from the written requirements, rather than "asking the code whether it agrees with itself".[3]

1. **Problem and user:** Kevin Solorio (Focused) builds *with* frontline workers, not *for* them through a proxy such as a product owner who interprets what users said.[4]
2. **Why AI:** Mark Lay (Noblis) wants a better or more efficient result, "and if you don't get either of those, you really shouldn't put it in AI."[5]
3. **Charter check:** Don Barger's organisation, the International Mission Board, wrote its AI charter "Before we ever write one line of code", and still uses it to decide what it will never do.[5]
4. **Owner and steward:** Lay's premise is that "accountability can't be delegated" to AI; Noblis named about 30 data stewards for its critical datasets.[5]
5. **Data:** Heidi Porter (Moyer Group AI) warns that stale data will "quietly give you the wrong answers", and that "Grounding is only as good as the data behind it."[4]
6. **Mechanism:** Porter chooses rules, classic machine learning, a decision model or an LLM per task,[4] and Chinmay Goyal (Glean) asks "can the output be listed in advance?"[6]
7. **Acceptance and evals:** Solorio holds that "an agent without evals is a proof of concept", and Porter that "averages can hide a bad result".[4] Barlow warns that a misread requirement can put "that same misunderstanding" in code and tests alike, so criteria come from the spec.[3] ZoomInfo reports its AI judge was right only 65% of the time; Brian Kennedy: "We had trusted our judge until we measured it."[7]
8. **Execution dial:** Porter sets autonomy like a dial and automates outright "only what is cheap to undo"; people reviewing thousands of items can fall into "rubber stamping fatigue".[4]
9. **Guardrails:** Porter: "a rule written in a prompt is not deterministically enforced".[4] Cam Soper (Pulumi): "a rule in an agent's instructions is just a suggestion."[8]
10. **Security:** Yvonne Carlson (ExploreGod) calls for least privilege, time-bound credentials, default-deny boundaries and sandboxes (abstract only).[9] Simon Willison's *lethal trifecta* is private data, untrusted content and a way to send data out in one agent.[10]
11. **Observability:** Shweta Iyer (Microsoft) showed an agent call succeeding while the business write rolled back; her API returns a trace ID with each business request ID, she persists the trace ID in her database as a durable correlation value, and she says to "make any completions explicit".[11]
12. **Failure and undo:** Tanmay Sah: "A timeout tells us that the response didn't arrive, not that the operation failed."[12]
13. **Cost:** SEP saw a prototype stall partly because the token budget covered only a couple of days' work.[4] Harvey lets automations carry a budget or expiry date "because when no one's watching, an agent can start thousands of tasks too."[13] Willison argues pay-per-use services should ship with hard budget caps switched on.[14]
14. **Rollout:** Darren Taillie's data agent at AeroCore took off once it moved into Microsoft Teams: "No one likes an extra login."[5] Solorio finds that people who helped build a tool become its champions.[4]
15. **Maintenance:** Lay asks "do they have the capacity to keep running what they deployed?"[5] This tempers practitioners' view that the model is the replaceable part: ByteDance Seed's HarnessDev study found one model-built harness fell from 69.3 to 33.0 when a different model ran it, though others improved (the paper's figures).[15]
16. **Open questions:** Washington keeps accepted and rejected decisions in his master plan, and when something breaks he fixes the spec files and regenerates.[1] Rajath Kotyal (AWS): "Check the spec always before you pass it down to the agent."[16]

## Related

- Start with [AI intake checklist](ai-intake-checklist.md); [Should this task use AI, and which kind?](should-this-task-use-ai.md) and [How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md) help with sections 6 and 8.
- [Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md) helps with section 7 and [Running AI in production](../5-run/ai-in-production-runbook.md) with sections 11 to 13; use [AI failure modes: a pre-mortem checklist](ai-failure-modes-premortem.md) to test a finished spec.
- [Agent-written pull requests and agent autonomy: draft engineering standard](../5-run/agent-pr-policy.md) if coding agents will build it; [AI glossary](../1-understand/ai-glossary.md) for terms.

**Read next:** [AI failure modes: a pre-mortem checklist](ai-failure-modes-premortem.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://www.youtube.com/watch?v=TF6qzdKwl84&t=29691 — Michael Washington (Microsoft MVP, BlazorHelpWebsite.com), What NOT to AI: Hand-Crafting Your App's Core Foundation, .NET Conf 2026
[2] https://ai.engineer/code/2026/talks/doug-clauson — Doug Clauson (AWS), Ship More as a Team of One with Kiro Crew, AI Engineer Code Summit 2026
[3] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[4] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; and Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[5] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[6] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[7] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[8] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[9] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[10] https://simonwillison.net/2025/Jun/16/the-lethal-trifecta — Simon Willison, The lethal trifecta for AI agents
[11] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[12] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah and Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[13] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[14] https://simonwillison.net/2026/Oct/3/default-hard-budget-caps — Simon Willison, Default hard budget caps
[15] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[16] https://ai.engineer/code/2026/talks/online-aws-specification-analyzer — Rajath Kotyal (AWS), Specs have bugs too, AI Engineer Code Summit 2026

