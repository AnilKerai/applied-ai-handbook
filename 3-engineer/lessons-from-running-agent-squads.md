---
title: "Lessons from running agent squads"
type: lessons
created: 2026-11-15
audience: "Engineers running several agents"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Lessons from running agent squads

> **In one minute**
> - I run two small teams of AI agents, one that builds software and one that researches, each working from a shared task board.
> - Each agent starts every task fresh, so the task card has to carry everything it needs.
> - Keep the agent that does the work apart from the agent that checks it.
> - A rule the system enforces beats a rule written in an agent's instructions.
> - The context each agent rereads on every call cost more than the choice of model.

*Reading time: about 5 minutes · Best for: engineers running several agents*

In October 2026 I set up two teams of AI agents on Hermes Agent, using Anthropic's Claude models. The dev team has a lead, an engineer, an ops role and a reviewer. The research team turns an idea into questions, researches them and writes up a brief. Both work from kanban boards, where each task is a card, and each worker that picks up a card is a new process with an empty context window.[1] The setup and its records are public in my hermes-squad repo; this page is what running it taught me.

## The card is the prompt

**What happened.** A worker can't see the cards beside its own, or the chat that produced its card. As I wrote in my context-engineering notes, "The card body is the prompt."[1] Ambiguity left in a card gets resolved by a guess, which copies into every child card, or by the worker blocking.[1] Early on, the board's automatic task splitter also routed work by each role's one-line description, ignoring the lead's own instructions.

**What I changed.** Any decision two cards share is written into both, numbered so that the reviewer can audit against it, and product decisions are made with me before the card exists.[1] I now assign work to the lead directly, and rough ideas wait for me instead of being split automatically. The lead also runs a ready check before work starts: the problem, the acceptance criteria, what is out of scope, the constraints, and no open product decision.

**The principle.** Each agent sees only what you give it, so write the whole task down where the agent will read it ([Context engineering principles](context-engineering.md#core-principles)).

## Separate the writer from the checker

**What happened.** The reviewer re-runs a card's verify commands itself, so the engineer never marks its own homework.[1] In my first five-day snapshot, 19 of the 20 implementation cards reviewed were approved first time, one was sent back for a real defect, and every approval cited checks the reviewer had run.[2] The gap showed where no reviewer stood. A lead with no terminal ran a bug hunt alone and filed sixteen fix cards from reading the code. An independent audit found fifteen of them real, but seven specified a fix narrower than the bug, and nobody had reviewed the hunt itself.

**What I changed.** A bug hunt now goes through the same lane as code. Engineers prove each finding with a probe that passes on the unmodified code, the reviewer re-runs the probes, and only then does the lead write fix cards. When an engineer once closed its own card and skipped review, the rule against it had lived only in the lead's memory, so I added it to the engineer's instructions.

**The principle.** Don't let the agent that did the work sign it off, and review the plan as well as the code ([Loop engineering principles](loop-engineering.md#core-principles)).

## Enforce rules in the system, not in prose

**What happened.** Every agent shared my real home directory, so my cloud sign-in was reachable by every role, the researcher included. Later, when I let the lead publish its own pull requests, I found that blocking command patterns wasn't enough: a push to the main branch could be typed in ways the patterns didn't match.

**What I changed.** Each role now has its own deny rules. Ops and the reviewer can only read and validate, and the other roles have no cloud command-line tools. Publishing goes through one script, the only way out, which refuses the default branch and force-pushes, opens one pull request and never merges. As I put it in my notes, "Prefer a mechanism to a sentence."[1]

**The principle.** A check the machine runs beats an instruction the model may not follow ([Guides and sensors](harness-engineering.md#guides-and-sensors)).

## Context size cost more than the model

**What happened.** The researchers were the most expensive role. Over five days they cost about $72, and their average call carried about 233,000 tokens of context.[2] Most of that was context being read again. Compression never fired, because its threshold was half of a million-token window, and every role had inherited an extra-high thinking level from the profile it was cloned from.

**What I changed.** Researchers now run at a medium thinking level and compress their context at 120,000 tokens using a cheaper model, and the analyst compresses at 150,000. I haven't yet measured whether that worked. I had also ruled out the cheapest model tier without checking its current release and price, which was wrong, so now I check before ruling a tier out. As I wrote in my notes, "Context size costs more than model tier."[1]

**The principle.** Treat the context window as a budget, because every call sends it again ([Context engineering principles](context-engineering.md#core-principles)).

## Handoffs and clones carry context, good and bad

**What happened.** The next role gets a handoff summary and metadata, not the transcript, so a thin summary starves it. Cloning a role also copied more than I meant: three roles started with a stale copy of another profile's memory, which put wrong facts into every run.[1]

**What I changed.** I cleared the inherited memory, and after cloning I now set each role's memory, thinking level and tools myself instead of trusting the copy.[1]

**The principle.** A handoff is a compression boundary, so decide what crosses it ([Multi-agent orchestration principles](multi-agent-orchestration.md#core-principles)).

## Stopping a card doesn't stop its worker

**What happened.** I blocked a running card to pause it, but its worker process carried on, and kept spending.

**What I changed.** To stop a card, I now reclaim it first, which stops the worker, and then park it. A worker that picks it up again starts fresh from the card, its comments and the files on disk.

**The principle.** It's the same lesson I learnt [building my harness](lessons-from-my-harness.md): marking a task stopped in a queue doesn't stop a worker already running it, so the stop has to reach the run itself ([Budgets and stopping](harness-engineering.md#budgets-and-stopping)).

## Split a role for tools, not for knowledge

**What happened.** I considered a role for each specialism, such as frontend and backend. But every extra role adds a handoff, and handoffs lose context.

**What I changed.** I create a new role only when it needs different tools, credentials, a different model or different risk rules, and use a skill when only the knowledge differs. That is why ops is its own role, while frontend and backend are skills.[1] I also gave the lead a simplicity rule: the simplest design that meets the acceptance criteria. The reviewer now counts unneeded complexity as a defect, but only when it can name the simpler change.

**The principle.** Use as few agents as the work allows. Anthropic's Applied AI team reports that "a single agent with skills frequently outperformed both the one-prompt-for-everything design and the subagent design on quality" (Anthropic's claim).[3] See the [multi-agent orchestration principles](multi-agent-orchestration.md#core-principles).

## The task loop works; the improvement loop is manual

**What happened.** In that first snapshot, 53 of 65 cards were done, and none had crashed.[2] But lessons stayed where they were learnt. Only the lead had real lessons in its memory, and my own review of the squad missed its biggest gap, which the research team had already found: in 14 of 16 repos the agents' instruction file was only a pointer, so workers never got the repo's rules.[1]

**What I changed.** Now I read the existing research before I review anything. Agents propose and I promote: a lesson becomes a change to a role's instructions, a skill or a repo's instruction file only after I've reviewed it.[1] I can't yet tell whether such a change helped, because there's no regression set, and runs don't record which version of the context they used.[2]

**The principle.** Measure an improvement before you automate it ([Loop engineering principles](loop-engineering.md#core-principles), and [Eval engineering](eval-engineering.md#core-principles)).

**Read next:** [AI pattern catalogue](../4-build/ai-pattern-catalogue.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://github.com/AnilKerai/hermes-squad/blob/374995b71e7670bd974c27ae838641c2fe7b22b3/docs/02-context-engineering.md — Anil Kerai, hermes-squad, docs/02-context-engineering.md, commit of 12 November 2026 (GitHub)
[2] https://github.com/AnilKerai/hermes-squad/blob/374995b71e7670bd974c27ae838641c2fe7b22b3/docs/05-metrics.md — Anil Kerai, hermes-squad, docs/05-metrics.md, commit of 12 November 2026 (GitHub)
[3] https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop — Anthropic, When to fold subagents into your main agent loop
