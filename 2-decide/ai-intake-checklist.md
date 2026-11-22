---
title: AI intake checklist
type: checklist
created: 2026-11-14
audience: The in-house AI adviser, and the engineering leads, product owners and senior managers who bring AI ideas to them
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# AI intake checklist

> **In one minute**
> - Run these questions for each task or workflow step, not for a whole project; it is quick to do.
> - Stop if the task is on your *never* list, AI won't improve it, or nobody is named as accountable.
> - Fix the data first if it isn't good enough, and use plain rules or code wherever they can do the step.
> - Let the cost of a mistake, and how easily it is undone, decide who acts; enforce safety rules in code.
> - Without tests on real cases, a way to trace what the AI did, and a maintainer, it is only a trial.

*Reading time: about 10 minutes · Best for: anyone reviewing an AI idea*

Run it per task or workflow step, not per project, as Heidi Porter (Moyer Group AI) advises for choosing a mechanism.[1] It takes about 15 minutes.

## The questions (one page)

**Should we?**

1. Is this task on our *never* list?
2. Will AI make the result better, or the work more efficient, than it is today?
3. Which named person is accountable for every output?

**Which kind of AI?**

4. Is the data accurate, complete, consistent and current enough for this task?
5. Could rules or ordinary code do this step?
6. Can every possible output be listed in advance?
7. Do we know the steps in advance?

**How safe?**

8. What does a mistake cost, and how would we undo it?
9. Where do the guardrails live: in code and infrastructure, or only in a prompt?

**Ready to ship?**

10. Do we have evals on real cases, built with the people who do the job?
11. Can we trace a business outcome back to what the AI did?
12. Who will maintain it, and what would it cost to reverse?

## What the answers mean

*Red-flag answers in italics are illustrations, not quotes.*

### 1. Is this task on our *never* list?

- **Why it matters:** The International Mission Board (Don Barger) wrote its AI charter "before we ever write one line of code". Its never list includes AI posing as a human, AI-only final decisions about people, covert monitoring and counselling.[2]
- **Red flags:** No list exists. *Something is better than nothing*; Barger's reply: "something can be worse than nothing if you're doing the wrong things".[2]
- **What a good answer looks like (industry practice):** A short charter, agreed once; Barger finds "these clear limits are actually freeing me up".[2] Newer guidance: Anthropic's Claude Fable 5.2 guide says cautious rules piling up in memory and notes make the model ask for approvals it doesn't need or hold back routine work, and that it treats any *never* as absolute.[12] So keep the list in policy and hard controls, not prompts.

### 2. Will AI make the result better or the work more efficient?

- **Why it matters:** Mark Lay (Noblis) starts with the reward: a better or more efficient result, "and if you don't get either of those, you really shouldn't put it in AI". Barger adds: judge ideas "against trust, not just feasibility".[2]
- **Red flags:** No baseline for today's cost or quality, or the benefit is simply that it uses AI.
- **What a good answer looks like (industry practice):** Measure the outcome, not activity. In a Harvard study of 655 firms, coding agents raised pull requests far more than resolved issues, while reviews took longer to approve (observational data to August 2026; figures in [Working with coding agents](../4-build/working-with-coding-agents.md#1-the-mindset-you-own-the-outcome)).[13]

### 3. Which named person is accountable for every output?

- **Why it matters:** Lay's premise is that "accountability can't be delegated" to AI, so a person always holds the A in the RACI chart. Someone must validate and own the output, even of tools a department builds outside IT.[2]
- **Red flags:** *The model decides.* The owner is a committee, or just IT, or nobody.
- **What a good answer looks like (industry practice):** Anthropic's Claude Code team holds whoever prompted an agent-written change on the hook for it: that person counts as one of the required human reviewers wherever the change's risk tier calls for any, and an agent's approval never fills a human slot (its own account).[14]

### 4. Is the data good enough for this task?

- **Why it matters:** Porter's test is whether the data is "good enough for the task you're doing": accurate, complete and consistent. Stale data will "quietly give you the wrong answers", so ground any LLM in the systems of record at runtime.[1]
- **Red flags:** The design asks the model to "hold the data, be the system of record".[1] Nobody knows who owns the data or when it was last refreshed.
- **What a good answer looks like (industry practice):** Fetch facts live from the system of record, labelled with source and date. In one pre-registered working paper (not peer reviewed), a stale doc misled five models 68–100% of the time, because agents stop checking once any doc looks authoritative.[15]

### 5. Could rules or ordinary code do this step?

- **Why it matters:** UiPath keeps the control flow deterministic and calls a model only at marked decision points.[3] In Porter's Syngenta case, application code handles access, existing agronomy models make the predictions, and the LLM is "the interface, the router, and the explainer, not the agronomist".[1]
- **Red flags:** The rules already exist in a policy, or the step is a lookup, calculation or format change. *We'll prompt it to follow our rules.*
- **What a good answer looks like (industry practice):** Use a model to design the rules, then run without it. UiPath's email-mining flow has an LLM propose categories offline, and at runtime "we basically removed the LLM completely from the picture on this one."[3]

### 6. Can every possible output be listed in advance?

- **Why it matters:** This is Glean's test: "can the output be listed in advance?" If so, use a decision model that returns choices with probabilities and no text, or a fine-tuned classifier when labels are stable and volume is high.[4]
- **Red flags:** A chat model's yes, no or category is parsed from its text. The categories change often, yet the plan is to fine-tune.
- **What a good answer looks like (industry practice):** Decision models have become mainstream products: OpenAI's Decisions API is now generally available, and Google has launched Gemini Decision 1.[16][17] Test reliability too: in SO-Arena's test of 21 models, the best-performing decision model ranked only seventh for reliability, on measures that include spotting when no option fits ([Evals playbook](../4-build/evals-playbook.md#3-what-to-score)).[18]

### 7. Do we know the steps in advance?

- **Why it matters:** If we do, a fixed workflow with the LLM in one narrow job is enough; Darren Taillie's photo check at AeroCore ended with the prompt "Compare and flag".[2] In UiPath's fraud demo, the decision model escalates to a slower agent only when the evidence is missing.[3]
- **Red flags:** *An agent will work out the process.* Nobody can describe how the job is done today.
- **What a good answer looks like (industry practice):** For unknown steps, use one agent loop that loads tools on demand, not a team of agents; Anthropic reports it often won on quality, cost and latency.[19] Newer practice goes further: once a repeated job settles, a cheaper model runs its path as a workflow and sends hard cases back; AgentRun reports $0.89 falling to $0.124 per record.[20]

### 8. What does a mistake cost, and how would we undo it?

- **Why it matters:** Porter sets autonomy like a dial, by consequence, confidence and reversibility, and reserves full automation for actions that are cheap to undo.[1] Meta's test for more autonomy is how costly a mistake would be and how easy it would be to catch.[5]
- **Red flags:** *A person will check everything*, at volumes where reviewers can fall into "rubber stamping fatigue".[1] Nobody has tested the undo, although "A timeout tells us that the response didn't arrive, not that the operation failed."[6]
- **What a good answer looks like (industry practice):** The Claude Code team's PR template asks how to undo each change, and low, medium and high risk need none, one or two human approvals.[14] Porter's fatigue warning now has a number: Anthropic reports users approve 93% of permission prompts.[21]

### 9. Where do the guardrails live?

- **Why it matters:** "A rule written in a prompt is not deterministically enforced"; a real guardrail is a gate, a check, a human or a limit in code.[1] Cam Soper (Pulumi) found that a rule in an agent's instructions is no more than a suggestion, and Azure's AI Gateway runs guardrails in hooks outside the agent's reach.[7][8]
- **Red flags:** Safety rules exist only in the prompt. The agent holds standing credentials, against Yvonne Carlson's call for least privilege and time-bound credentials.[9] Destructive actions run unconfirmed; in Gerald Versluis's (Microsoft) design, "every tool stages an action".[10]
- **What a good answer looks like (industry practice):** Guardrails fail closed: Claude Code hooks can now be set to block an action when the check itself fails.[22] No agent session gets private data, untrusted input and an outbound channel together (Simon Willison's *lethal trifecta*), and a blocked agent should be expected to seek another route, as Anthropic found Claude doing.[23][24]

### 10. Do we have evals on real cases, built with the users?

- **Why it matters:** Kevin Solorio (Focused) counts any agent without evals as a proof of concept. He has workers label outputs themselves, not via a proxy, then after launch scores sampled live traces and feeds failures back into the test set.[1]
- **Red flags:** *The demo looked good.* Developers or a product owner wrote the test cases. Only averages are reported, though Porter warns that averages can mask a bad result.[1]
- **What a good answer looks like (industry practice):** Evals grow from real failures: the Claude Code team runs its reviewer daily against past PRs that caused incidents, and NVIDIA's NeMo tools mine stored traces for failures and help a coding agent write evals for them, a tool-assisted version of Solorio's flywheel.[14][25] AWS's Swami Sivasubramanian reports an agent rebuilding a replication engine far faster once it had a spec and a test environment to check its results against (AWS's account).[26]

### 11. Can we trace a business outcome back to what the AI did?

- **Why it matters:** Shweta Iyer (Microsoft) showed an agent call succeeding while the business write failed and rolled back, so she stores the trace ID with the business record and records an explicit final status.[11]
- **Red flags:** Success means the model replied. Logs live only inside the AI tool. Nobody can replay a run.
- **What a good answer looks like (industry practice):** AI traces should use the OpenTelemetry standard, like the rest of our telemetry; Claude Code now emits OpenTelemetry GenAI attributes and records whether a classifier or a permission rule decided each tool call.[27]

### 12. Who will maintain it, and what would it cost to reverse?

- **Why it matters:** Lay asks what reversing a deployment would actually cost, and "do they have the capacity to keep running what they deployed?"[2]
- **Red flags:** One enthusiast built it and nobody has agreed to run it. There is no rollback plan.
- **What a good answer looks like (industry practice):** Re-run evals at every model change: in ByteDance Seed's HarnessDev study, one harness's score fell sharply under a different model ([Evals playbook](../4-build/evals-playbook.md#8-when-to-re-run)).[28] Track vendor retirement dates too; Anthropic's Opus 4.8 fast mode was due to end on 30 November 2026, with no fallback.[29]

## Outcomes

These are recommendations, following [Should this task use AI, and which kind?](should-this-task-use-ai.md), not findings from the sources.

**Recommendation**

- **Stop:** yes to Q1, no to Q2, or nobody named at Q3.
- **Fix the data first:** no to Q4.
- **Rules or code:** yes to Q5.
- **Classic ML or a fine-tuned classifier:** yes to Q6, with stable labels and high volume.
- **Decision model:** yes to Q6, but the labels change or the volume is modest.
- **Fixed workflow, with an LLM for the fuzzy step only:** no to Q6, yes to Q7.
- **Bounded agent:** no to Q6 and Q7. Keep it inside deterministic orchestration with cost and time limits.

**Execution dial (from Q8)**

Porter's dial decides who acts:[1]

- **Human approves first:** consequential, uncertain actions.
- **Threshold and escalate:** high volume with mixed confidence.
- **Act with an undo window:** time-sensitive work; a person can veto or undo.
- **Automate outright:** only what is cheap to undo.

Meta grants autonomy per kind of action, on a track record for that exact action.[5]
Do the same: treat the dial's answer as a ceiling that each kind of action climbs to step by step ([How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md)).
Treat any idea failing Q9 to Q12 as a proof of concept, whatever the dial says.

## Related

- [Should this task use AI, and which kind?](should-this-task-use-ai.md): the decision tree behind questions 1 to 9.
- [How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md): autonomy per kind of action.

**Read next:** [Where should AI go in our product or operations first?](where-ai-goes-first.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; and Kevin Solorio (Focused), Building AI With Workers, Not For Them, Midwest AI Summit 2026 (Practical AI E378 transcript)
[2] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[3] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram and Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[4] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[5] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[6] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah and Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[7] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[8] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=25809 — Matt Soucoup and Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 2), .NET Conf 2026
[9] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[10] https://www.youtube.com/watch?v=FYGBT08-N48&t=5 — Gerald Versluis (Microsoft), Less Chat, More Action: AI-Powered .NET MAUI Apps, .NET Conf 2026
[11] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[12] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 — Anthropic, Prompting Claude Fable 5.2: keep caution from piling up
[13] https://fion.ac/jellyfish.pdf — Chen & Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[14] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[15] https://github.com/Connorrmcd6/surface-bench/blob/main/PAPER.md — Connorrmcd6 (GitHub), surface-bench: stale docs and agent verification
[16] https://developers.openai.com/api/docs/guides/decisions — OpenAI, Decisions API guide
[17] https://simonwillison.net/2026/Nov/11 — Simon Willison, weblog for 11 Nov 2026 (Gemini Decision 1)
[18] https://huggingface.co/papers/2611.15777 — Hugging Face Papers, SO-Arena (paper 2611.15777)
[19] https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop — Anthropic, When to fold subagents into your main agent loop
[20] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun (Parcha), merchant-classification case study
[21] https://www.anthropic.com/engineering/claude-code-auto-mode — Anthropic, Claude Code auto mode
[22] https://github.com/anthropics/claude-code/releases/tag/v2.1.295 — Anthropic, Claude Code v2.1.295 release notes
[23] https://simonwillison.net/2025/Jun/16/the-lethal-trifecta — Simon Willison, The lethal trifecta for AI agents
[24] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions
[25] https://developer.nvidia.com/blog/use-nvidia-nemo-to-turn-agent-failures-into-tests-and-harness-fixes — NVIDIA, Turn agent failures into tests and harness fixes
[26] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS), AWS Emulator and the engineer's job when agents write the code
[27] https://code.claude.com/docs/en/changelog — Anthropic, Claude Code changelog (v2.1.300-302)
[28] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[29] https://github.com/anthropics/claude-code/releases/tag/v2.1.316 — Anthropic, Claude Code v2.1.316 release notes

