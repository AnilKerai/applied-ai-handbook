---
title: "Where should AI go in our product or operations first?"
type: memo
created: 2026-11-14
audience: senior leadership and engineering leads
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Where should AI go in our product or operations first?

> **In one minute**
> - Start with narrow, repeated steps in existing work, where AI clearly helps and mistakes are cheap to catch or undo.
> - Agree a short AI charter, listing what AI may and may *never* do, before picking any uses.
> - For each step, use rules or code where they suffice, and keep AI to the open-ended language part.
> - Put it inside tools people already use, acting through existing features and asking before anything destructive.
> - Build it with the people who do the job, test it on real cases before launch and name an owner.

*Reading time: about 5 minutes · Best for: leaders and product owners*

## Question

We have more candidate uses for AI than capacity to build them. Where should we start, in products and operations, to get real value without unmanageable risk?

## Short answer

Start with narrow, repeated steps inside work people already do, where AI makes the result better or more efficient and a mistake is cheap to catch or undo. For each step, use the simplest mechanism that works, keep the LLM to the fuzzy part, and build it with the people who do the job, as the strongest case studies did.[1][2] Before choosing anything, we should write down what we will never use AI for, as one organisation did before writing any code.[2]

## Recommendation

1. **Write a short AI charter first.** Agree a *yes* list and a *never* list before picking use cases, so later refusals are quick and consistent.
2. **Screen candidates per task, on reward and risk.** Keep steps where AI is clearly better or more efficient, then rate the cost of an error, whether it can be undone and whether we can check it. Strong first candidates: routine data questions answered from our own systems, compare-and-flag checks on records, routing requests, and drafts for human review.
3. **Pick the mechanism per step.** Use rules or code where they suffice, a decision model where the answer is one of a known list, and an LLM only for open-ended language, inside fixed orchestration.
4. **Put it where people already work, acting through features we already have.** Prefer an existing chat tool or the app's own actions to a new portal; tools should stage changes and ask before anything destructive.
5. **Build with the users and measure before launch.** Build evals from real cases with the people who do the job, keep sampling live results, and name an owner for each use.

## Options considered

- **A general chatbot or assistant first.** Visible and quick to demo, but broad, hard to evaluate and risky for trust; a poorly bounded tool can do more harm than none.[2]
- **End-to-end autonomous agents for whole processes.** The largest prize on paper, but pilots stall when the LLM is asked to hold the data, act as the system of record, make the decision and check its own work.[1]
- **Narrow, checkable steps inside existing workflows (my recommendation).** Less headline value at first, but measurable, low-risk and quick to adopt, and it builds the data, evals and trust larger uses need.

## What the evidence says

- **Pick a mechanism per task, and keep the LLM's job narrow.** Heidi Porter picks rules, classical ML, a decision model or an LLM per task, not per project, and warns that "a rule written in a prompt is not deterministically enforced".[1] In Syngenta's seed tool the LLM is "the interface, the router, and the explainer, not the agronomist". Stanford's surgical co-management screening tool applies an institution-owned rubric and answers yes, maybe or no; before launch, human triage missed half of eligible patients.[1]
- **Delegate on reward and risk.** Mark Lay weighs reward (a better or more efficient result) against the risk and consequence of error: "if you don't get either of those, you really shouldn't put it in AI".[2] Porter would automate outright "only what is cheap to undo", with a person approving consequential, uncertain actions.[1]
- **Decide the boundaries before you build.** Don Barger's organisation wrote an AI charter "before we ever write one line of code". Its yes list includes drafting, summarising, research, translation and code with humans in the loop; its never list includes AI posing as human, final decisions about people, covert monitoring and autonomous high-stakes action. Declining to build an AI counsellor, he said: "Something can be worse than nothing if you're doing the wrong things."[2]
- **Build with the people who do the job.** Kevin Solorio found tools fail when built *for* users through a proxy; he shows them a deliberately rough version, because people correct a wrong answer faster than they describe a right one. In his words, "an agent without evals is a proof of concept", and a data flywheel keeps evals growing after release.[1]
- **Two practical agents from a two-person team.** AeroCore put a text-to-SQL agent into Microsoft Teams, where adoption took off ("No one likes an extra login"). It shows the query it ran, and requests that took the analysts from thirty minutes to a week get an answer in a couple of minutes. A daily vision check compares work-order photos with what technicians typed and flags mismatches, with the prompt "Compare and flag". AeroCore reports cancelling that month's reconciliation meeting, five to six person-hours, because there were no incorrect work orders.[2]
- **Most steps are decisions, not writing.** Chinmay Goyal: "most AI product steps are bounded decisions and not generation problems." His test: "can the output be listed in advance?" If so, Glean uses a decision model returning probabilities, not text, and reports zero invalid outputs on one ranking task.[3] Cloudflare's live demo moved tool pruning and log extraction to such models and cut six LLM calls to one (its claim).[4] UiPath keeps control flow deterministic, in its fraud demo hands off to an agent only when evidence is missing, and reports that its replacements for LLM calls run about 50x faster and 7.1x cheaper.[5]
- **Use the model only for the fuzzy step, and act through existing features.** Luis Quintanilla's media demo generates the parts with AI but stitches the film "using standard code".[6] Gerald Versluis: "Your users don't just want to know the chatbot, they want the app to act, right?" He exposes existing app functions as tools in which "every tool stages an action", and confirms destructive ones.[7]

### Newer evidence

- **Decision models are entering production, checked on live traffic.** For labelling internal tickets, Amazon engineers replaced Sonnet 4.6 with Strands Decider, Amazon's own decision model, which they say performed as well at 98% less cost. They ran both on real traffic, judged every disagreement, and could switch back with a 45-second configuration change.[8] In my reading, this supports Goyal and UiPath and shows how to cut over safely.
- **Accuracy is not reliability.** The SO-Arena benchmark tested 21 models across 11 domains and found the best-performing decision model ranked only seventh for reliability, meaning answers that hold when the options change and that say when none fits.[9] I read this as qualifying the vendor results above, including Glean's: a valid answer can still be wrong, so we should test with reshuffled options and a *none of these* case.
- **Learn on the expensive model, then hand off.** AgentRun had Opus classify merchants, telling it the right answer each time, until it wrote its path down as a workflow. A cheap model now runs that workflow, and a judge sends an answer back to Opus when its quoted evidence isn't on a page the agent read. AgentRun reports cost per merchant falling from $0.89 to about $0.12, with 96% correct against 93% for Opus alone (its own claims).[10] I think this updates Porter's per-task choice: for repeated jobs the mechanism can start expensive and get cheaper, as long as a check controls the hand-back.

## Risks and what would change this advice

- **Starting too small to matter.** Narrow uses can look trivial, so we should count time saved and errors caught from month one.
- **Vendor numbers.** Most figures above are the companies' own, and AeroCore's lack a controlled baseline, so we should measure before and after ourselves.
- **What would change it.** If evals on real cases show a broader agent is reliable across a whole process, with recovery and ownership in place, we can widen scope. A narrow use that fails its evals should stop or fall back to rules, not gain more prompt text.

**Read next:** [AI feature spec template](ai-feature-spec.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; Midwest AI Summit 2026 (Practical AI E378 transcript)
[2] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows; Midwest AI Summit 2026 (Practical AI E379 transcript)
[3] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[4] https://ai.engineer/code/2026/talks/michelle-chen — Michelle Chen (Cloudflare), cloudflare is a neolab, AI Engineer Code Summit 2026
[5] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram & Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[6] https://www.youtube.com/watch?v=SIBdHRrk8os&t=11450 — Luis Quintanilla (Microsoft), The .NET AI Stack: What's New, What's Next, and How It Fits Together, .NET Conf 2026
[7] https://www.youtube.com/watch?v=FYGBT08-N48&t=5 — Gerald Versluis (Microsoft), Less Chat, More Action: AI-Powered .NET MAUI Apps, .NET Conf 2026
[8] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents blog, Amazon saves millions by replacing Sonnet 4.6 with Strands Decider
[9] https://huggingface.co/papers/2611.15777 — SO-Arena: Benchmarking the Capability Spectrum and Reliability of System One Models (arXiv 2611.15777)
[10] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun (Parcha), Opus learns the job, a cheap model runs it (merchant-classification case study)

