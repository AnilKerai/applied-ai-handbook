---
title: "Lessons from my harness"
type: lessons
created: 2026-11-15
audience: "Engineers building agents"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Lessons from my harness

> **In one minute**
> - I built my own agent harness to learn how agents work, and to teach my team with it.
> - Several of my bugs came from the harness deciding a run had finished, or had been cancelled, when it had not.
> - Summarising old steps costs more each turn unless each summary builds on the last one.
> - Check the shape of an answer at the end, and send a bad answer back for a few repairs.
> - Give every run several independent exits, and back every judgement a model makes with a hard limit.

*Reading time: about 5 minutes · Best for: engineers building agents*

In May 2026 I started model-harness, an open-source agent harness for .NET. This page is what building it taught me. Each lesson links to the matching principle on the [Harness engineering](harness-engineering.md) page, which carries the field's evidence.

## Build it to learn it

**What happened.** I wanted to learn how agents actually work by implementing the loop, not by reading about it. I also wanted something to teach my team with.

**What I changed.** I implemented the loop myself, made every control point a named, swappable part, and wrote a primer alongside the code as teaching notes. I also built it on a bet I haven't measured yet: that a well-structured harness closes much of the gap between a large model and a smaller, cheaper one.

**The principle.** Naming each part gives every new concern an obvious home ([What it is](harness-engineering.md#what-it-is)).

## A timeout is not a cancellation

**What happened.** In .NET, I found that a request timing out and a run being cancelled raise the same kind of exception. As I wrote in the decision record, "The two are the same exception type and mean opposite things".[2] Treating them alike gave me four bugs. In one, a slow memory store ended a whole run as "cancelled"; in another, the circuit breaker never opened against a hung backend, because it counted the timeout as a success.[2]

**What I changed.** Every catch now asks whether the run's own cancellation was requested, never what type of exception arrived. The tool path is the one deliberate exception: it has no cancellation clause, so every exception there becomes an error result, and a cancelled run still ends as cancelled one step later.[2] A timeout from anything the loop calls is a fault, and takes the fault path. Two parts deliberately fail closed instead: the gate that guards privileged actions blocks the action, and the tool selector offers no tools that turn. A failing check must also report an error, never a pass.[2]

**The principle.** Ask who stopped the work, not what was thrown, and make every safety check fail in the safe direction ([Prompt injection and data-flow tracking](harness-engineering.md#prompt-injection-and-data-flow-tracking)).

## Compaction costs more each turn unless you fold

**What happened.** Near the limit of the context window, my harness drops the oldest steps and puts a summary in their place. My first version re-summarised every dropped step from scratch, every turn. As I wrote in the decision record, "On a long-horizon run the compaction spend outgrew the saving it existed to produce".[3] No budget counted that spend, and the compaction trigger shared a setting with the run's total token cap, so compacted runs stopped at about one window.[3]

**What I changed.** Compaction is now an incremental fold: it summarises only the newly dropped steps on top of the previous summary, so the cost per turn stays flat. The trigger is separate from the run's cap, and compaction spend counts against the budget.[3] After the fold shipped, I found its summary was being sent as an extra system message that the adapters dropped, so I was paying for summaries the model never saw. Now the summary goes into the single system message, and one definition serves both what is counted and what is sent.[3]

**The principle.** Treat a summary as lossy and paid for: budget it, and keep the goal and any output contract out of the part that gets summarised. Anthropic warns that "overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later".[4] I still don't know whether dropping the oldest steps beats dropping the middle ones ([Compaction](harness-engineering.md#compaction)).

## Structured output is a check at the end

**What happened.** My first design for typed answers was a "final answer" tool, which needed a new flag, a loop change, and a guard so that the tool could never be dropped and strand the run.[5] The obvious alternative, constraining every model call to the schema, must be applied before each call, and nothing knows in advance which turn will be the last.

**What I changed.** My loop reaches its final check only on a turn with no tool calls, so that turn is known to be the last. As I wrote in the decision record, "A validator only needs to know after the call."[5] So the schema is stated as text every turn and enforced only on the final one. A non-conforming answer goes back with the parser's own error for at most two repairs, and then the run returns a partial result instead of throwing.[5] Parsing is lenient about markdown fences and strict about shape.

**The principle.** Check the shape where the program reads the answer, and repair a bad answer a small, fixed number of times ([Structured output](harness-engineering.md#structured-output)).

## A response is final only when it ended normally

**What happened.** My loop read "no tool calls" as "finished" and never looked at why the model stopped, so a response cut off at the output-token limit came back as done, ending mid-sentence.[6] My first fix special-cased that one reason. Review found that every unlisted reason still meant "finished", so a refusal came back as a successful answer, and the loop still ran tool calls from a cut-off response.[6]

**What I changed.** I replaced the list of bad reasons with a short list of good ones: a normal end of turn, a stop sequence and a tool call. Anything else, including reasons a provider adds later, returns a partial result that names the cause, and no tool call runs from a cut-short response.[6] The harness's own model calls, such as summaries, follow the same rule. As I wrote in the decision record, "A denylist of N fails open on reason N+1."[6]

**The principle.** Anthropic's docs class a stop reason as part of a successful response, not an error, so a cut-off answer arrives looking like success.[7] Read the stop reason on every response, and accept only known normal endings ([Stop reasons](harness-engineering.md#stop-reasons)).

## Give every run several exits, and back every judge with a hard cap

**What happened.** The signature bug of a hand-rolled loop is that it never stops, and that is where my harness is deliberately strong. As I put it in the primer, "a budget can't be talked out of stopping. Pair every model judge with a hard cap."[1]

**What I changed.** Each run has several independent exits. Turns, tokens, cost and wall-clock time are hard limits checked at the top of every turn, and running out returns a partial result, never an exception. Other checks catch a run that spends turns without progress, and a final-answer check can send the model back a capped number of times.[1] The budget sits outside the pluggable checks and runs before them, so an agent with none configured still has a ceiling, and a caller can tell "ran out" from "finished".[8]

**The principle.** Give every run limits a machine can check, report a hit limit as its own outcome, and back any model-judged stop condition with a hard limit ([Budgets and stopping](harness-engineering.md#budgets-and-stopping)). Anthropic's Agent SDK docs say: "Setting a budget is a good default for production agents."[9] It holds beyond one run, too. Running my [agent squads](lessons-from-running-agent-squads.md) later taught me that marking a task stopped in a queue does not stop a worker already running it, and I wrote that into the primer.[1]

## Taint is my label, not CaMeL's, and the tracking lives outside the model

**What happened.** I wanted text from tool results, web pages and documents to be unable to trigger an action with real-world side effects. In my harness I call data from an untrusted source *tainted*, and anything computed from it is tainted too. The research I drew on, CaMeL, doesn't use that word: it attaches capabilities to each value, which "track the sources and allowed recipients of each value".[10]

**What I changed.** I can't see inside the model's reasoning to track which output came from which input, so my approximation is conservative: the gate blocks a privileged action while tainted content sits in the context, and it fails closed.[2] CaMeL goes further, extracting the control and data flow from the trusted request so that untrusted data can never change the program's path.[11] Doing that in a free-form agent is still an open problem for me.

**The principle.** Let the harness, not the model, decide where untrusted data may flow, and make that gate fail closed ([Prompt injection and data-flow tracking](harness-engineering.md#prompt-injection-and-data-flow-tracking)).

**Read next:** [Lessons from my evals framework](lessons-from-my-evals-framework.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/PRIMER.md#loop-engineering — Anil Kerai, model-harness, docs/PRIMER.md, commit of 1 November 2026 (GitHub)
[2] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/decisions/001-collaborator-timeout-is-not-a-cancelled-run.md — Anil Kerai, model-harness, ADR-001: A collaborator's own timeout is not a cancelled run, commit of 1 November 2026 (GitHub)
[3] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/decisions/002-incremental-fold-compaction.md — Anil Kerai, model-harness, ADR-002: Trajectory compaction is an incremental fold, executed in the guide, commit of 1 November 2026 (GitHub)
[4] https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — Anthropic, Effective context engineering for AI agents
[5] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/decisions/003-structured-output-as-a-prereturn-validator.md — Anil Kerai, model-harness, ADR-003: Structured output is a PreReturn validator, not a generator constraint, commit of 1 November 2026 (GitHub)
[6] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/decisions/004-response-is-final-only-when-it-ended-normally.md — Anil Kerai, model-harness, ADR-004: A response is a final answer only when it ended normally, commit of 1 November 2026 (GitHub)
[7] https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons — Anthropic, Stop reasons and fallback (Claude API docs)
[8] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/FAQ.md — Anil Kerai, model-harness, docs/FAQ.md, commit of 1 November 2026 (GitHub)
[9] https://platform.claude.com/docs/en/agent-sdk/agent-loop — Anthropic, How the agent loop works (Claude Agent SDK docs)
[10] https://arxiv.org/html/2503.18813v2 — Debenedetti et al., Defeating Prompt Injections by Design, HTML of version 2 (arXiv 2503.18813v2)
[11] https://arxiv.org/abs/2503.18813 — Debenedetti et al., Defeating Prompt Injections by Design (arXiv 2503.18813)
