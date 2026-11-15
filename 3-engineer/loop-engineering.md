---
title: "Loop engineering"
type: concept
created: 2026-11-15
audience: "Engineers running agents at scale"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Loop engineering

> **In one minute**
> - An agent is a model using tools in a loop until a task is done. Loop engineering designs the system that starts, checks and improves those runs, in place of a person prompting each one.
> - The usual layers are the agent's own loop, a checking loop around it, runs started by events, and a loop that learns from past runs.
> - Every loop needs a stopping rule a machine can check, and a hard limit on turns or spend.
> - The name is new and the claimed benefits are not yet backed by systematic evidence, so measure before scaling up.

*Reading time: about 4 minutes · Best for: engineers running agents at scale*

## What it is

An agent loop is the cycle inside one run: Anthropic's Agent SDK docs describe it as Claude calling tools (functions it can use, such as a search), receiving the results and repeating "until the task is complete".[1]
Loop engineering works one level up: Addy Osmani defines it as "replacing yourself as the person who prompts the agent. You design the system that does it instead."[2]
Lulla et al.'s working definition is more precise: "designing automated control structures that repeatedly invoke coding agents, triggered on a schedule or by events, with each agent loop bounded by a machine-checkable stop condition".[3]
LangChain's Sydney Runkle (16 June 2026) frames it as a stack of four loops, used below.[4]

## When it arrived

Loops across runs are older than the name: Lulla et al. trace them to Geoffrey Huntley's "Ralph Wiggum" technique, published in July 2025.[3]
By their account, which cites Gergely Orosz, agent tools then added loop features between March and May 2026, such as a recurring /loop command in Claude Code.[3]
On 7 June 2026 (UTC) Peter Steinberger posted that "You should be designing loops that prompt your agents", without using the phrase itself.[5]
Osmani's *Loop Engineering* post, the same day, is the earliest dated use of the term found, and he hedged that it was still early.[2]
Lulla et al. say the term "was coined in early June 2026", when Steinberger's post, a remark by Boris Cherny and Osmani's post appeared within days of each other.[3]
On 30 June Andrew Ng wrote that the term "is a hot buzzphrase" after mentions of it by Cherny and Steinberger went viral.[6]
IBM's explainer of 17 July 2026 describes loops that guide agents to goals "with minimal human intervention", and Lulla et al.'s study followed in August.[7][3]

## Core principles

**Start with one bounded agent loop.**
LangChain's first loop is the agent itself: "a model calling tools in a loop until a task is complete".[4]
Anthropic notes that it is "common to include stopping conditions (such as a maximum number of iterations) to maintain control".[8]
Its Agent SDK docs add that "Setting a budget is a good default for production agents".[1]

**Wrap it in a verification loop.**
LangChain's second loop "checks the output and sends feedback back to the model when it falls short".[4]
We recommend making that check deterministic, such as tests, wherever the task allows; see [Eval engineering](eval-engineering.md).

**Start runs from events, not by hand.**
In the third loop, "An event fires — a new document lands, a schedule triggers, a webhook arrives — and the agent runs."[4]

**Keep progress outside the context window.**
In Lulla et al.'s description, the Ralph technique "works around the finite context window by restarting the agent with a fresh context in every iteration while persisting progress to the file system", the context window being the text a model can see at once.[3]

**Close the loop on the harness.**
LangChain's fourth, hill-climbing loop takes traces (step-by-step records of past runs) and "uses the findings to rewrite the harness with improved configuration", the harness being the code and settings around the model.[4]
Done by people, this is what Mitchell Hashimoto called harness engineering: whenever an agent makes a mistake, "engineer a solution such that the agent never makes that mistake again".[9]
A preprint of October 2026 (Wei et al.) formalises the automated version as harness self-evolution, which revises an agent's scaffolding "while keeping model weights fixed".[10]

**Treat the benefits as unproven.**
Lulla et al. found that the practitioner sources on loop engineering "provide no systematic evidence of the claimed benefits".[3]
We recommend measuring each new loop against a baseline before scaling it up, and gating any change a loop makes to its own harness on an eval.

## Where it shows up in this handbook

- [Running AI in production](../5-run/ai-in-production-runbook.md), section 8: four verification loops around a live system.
- [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md): how much a loop may do without a person.
- [Working with coding agents](../4-build/working-with-coding-agents.md), section 7: turning corrections into checks.
- [Multi-agent orchestration](multi-agent-orchestration.md): connecting several agents, and the debate over loops and graphs.

## See it built

The [model-harness primer](https://github.com/AnilKerai/model-harness/blob/7caff82/docs/PRIMER.md#loop-engineering) maps the four loops onto one example implementation, the handbook author's open-source .NET agent harness: the harness owns the agent loop and in-run checks, and leaves the outer loops to the system around it.

**Read next:** [Eval engineering](eval-engineering.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://platform.claude.com/docs/en/agent-sdk/agent-loop — Anthropic, How the agent loop works (Claude Agent SDK docs)
[2] https://addyosmani.com/blog/loop-engineering — Addy Osmani, Loop Engineering
[3] https://arxiv.org/html/2608.21884v3 — Lulla et al., Loop Engineering: Building Blocks, Adoption, and Impact (arXiv 2608.21884v3)
[4] https://www.langchain.com/blog/the-art-of-loop-engineering — Sydney Runkle (LangChain), The Art of Loop Engineering
[5] https://x.com/steipete/status/2063697162748260627 — Peter Steinberger, post on X on designing loops (7 June 2026)
[6] https://x.com/AndrewYNg/status/2071988145667928442 — Andrew Ng, post on X on loop engineering (30 June 2026)
[7] https://www.ibm.com/think/topics/loop-engineering — IBM, What Is Loop Engineering?
[8] https://www.anthropic.com/engineering/building-effective-agents — Anthropic, Building effective agents
[9] https://mitchellh.com/writing/my-ai-adoption-journey — Mitchell Hashimoto, My AI Adoption Journey
[10] https://arxiv.org/abs/2610.18813 — Wei et al., Self-Evolving Agent Harness (arXiv 2610.18813)
