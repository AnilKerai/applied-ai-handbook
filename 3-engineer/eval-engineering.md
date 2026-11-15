---
title: "Eval engineering"
type: concept
created: 2026-11-15
audience: "Engineers and product owners"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Eval engineering

> **In one minute**
> - An eval is a repeatable test of an AI system: give it an input and grade what comes back.
> - Eval engineering is a recent label for an established practice: building those tests, and refining them as you learn.
> - Testing an agent means testing the model and the code around it together.
> - Prefer fixed automatic checks, use AI markers with care, and run each case more than once.
> - The evals playbook in the Build section covers how to do it in practice.

*Reading time: about 4 minutes · Best for: engineers and product owners*

*This page covers the concept. For the practice, see the [Evals playbook](../4-build/evals-playbook.md).*

## What it is

Anthropic defines an eval as "a test for an AI system: give an AI an input, then apply grading logic to its output to measure success".[1]
Eval engineering is the work of building and maintaining those tests, and the name is a label for an established practice rather than a coined discipline: its earliest use found is in the documentation of the ell library, which in December 2024 said "Updating and refining the eval in response to these insights is what we call eval engineering".[2]
No source found coins the term.
Two related terms come from Anthropic. An evaluation harness is "the infrastructure that runs evals end-to-end".[1]
An agent harness is the system that lets a model act as an agent, so when evaluating "an agent", Anthropic says, "we’re evaluating the harness and the model working together".[1]
The grading itself is done by graders, and "Agent evaluations typically combine three types of graders: code-based, model-based, and human."[1]

## When it arrived

The practice is older than the label.
Zheng et al. (June 2023) studied using strong models as judges, known as LLM-as-a-judge, and named their biases.[3]
SWE-bench (Jimenez et al., October 2023) introduced an evaluation framework of "2,294 software engineering problems drawn from real GitHub issues and corresponding pull requests across 12 popular Python repositories".[4]
The best model in that paper, Claude 2, solved 1.96% of the issues (the authors' measurement).[4]
τ-bench (Yao et al., June 2024) tested agents in simulated conversations with users and proposed "a new metric (pass^k) to evaluate the reliability of agent behavior over multiple trials".[5]
The ell docs used the term "eval engineering" in December 2024.[2]
Anthropic's guide *Demystifying evals for AI agents* followed on 9 January 2026.[1]

## Core principles

**Test the system, not just the model.**
An agent's results come from the harness and the model together.[1]
We recommend re-running the evals whenever either changes: the model, the instructions, the tools or the code around them.

**Use deterministic checks first.**
Birgitta Böckeler, writing about the controls around coding agents, contrasts computational checks, "deterministic and fast", such as tests, linters and type checkers, with inferential ones such as an LLM as judge, which are "Slower and more expensive; results are more non-deterministic".[6]
We recommend code-based graders wherever the right answer can be checked mechanically, keeping model and human graders for the rest.

**Check the judge.**
Zheng et al. examine LLM-as-a-judge's "position, verbosity, and self-enhancement biases", and its "limited reasoning ability".[3]
We recommend testing any model grader against cases a person has marked before trusting its scores.

**One run is not evidence.**
τ-bench's authors found that even state-of-the-art function-calling agents "succeed on <50% of the tasks, and are quite inconsistent" (the authors' claim).[5]
Their pass^k metric asks for consistent success across k trials of the same task.[5]
As Anthropic puts it, "As k increases, pass^k falls since demanding consistency across more trials is a harder bar to clear."[1]

**Keep refining the eval.**
The ell docs define eval engineering as updating and refining the eval in response to what it reveals.[2]
We recommend adding each new failure from production to the set as a case, so the same mistake is caught next time.

**Let evals steer the loops.**
LangChain's hill-climbing loop runs an analysis agent over traces and uses the findings to rewrite the harness configuration.[7]
We recommend putting an eval gate in front of any such automatic change; [Loop engineering](loop-engineering.md) describes the loops.

## Where it shows up in this handbook

- [Evals playbook](../4-build/evals-playbook.md): the practice end to end, including graders (section 4), repeated runs (section 5) and when to re-run (section 8).
- [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md): why work must be checkable automatically before an agent gets more freedom.
- [Running AI in production](../5-run/ai-in-production-runbook.md), section 3: scoring live traffic and re-running evals after go-live.
- [What to measure: AI metrics scorecard](../5-run/ai-metrics-scorecard.md): measuring whether AI is working once it is live.
- [AI glossary for leadership](../1-understand/ai-glossary.md): eval, judge and deterministic check in plain words.

## See it built

The [model-harness primer](https://github.com/AnilKerai/model-harness/blob/7caff82/docs/PRIMER.md#how-it-relates-to-harness-and-eval-engineering) shows where one example implementation, the handbook author's open-source .NET agent harness, draws the line: an eval scores runs without changing them, while a check inside a run feeds a failure back so the model can correct itself.

**Read next:** [Multi-agent orchestration](multi-agent-orchestration.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — Anthropic, Demystifying evals for AI agents
[2] https://github.com/MadcowD/ell/blob/0e2759ca95ddb07ae0d0f360e739a5e8500a68c0/docs/src/core_concepts/evaluations.rst — ell, Evaluations documentation, commit of 16 December 2024 (GitHub)
[3] https://arxiv.org/abs/2306.05685v4 — Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (arXiv 2306.05685v4)
[4] https://arxiv.org/abs/2310.06770v3 — Jimenez et al., SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (arXiv 2310.06770v3)
[5] https://arxiv.org/abs/2406.12045 — Yao, Shinn, Razavi & Narasimhan (Sierra), τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (arXiv 2406.12045)
[6] https://martinfowler.com/articles/harness-engineering.html — Birgitta Böckeler, Harness engineering for coding agent users (martinfowler.com)
[7] https://www.langchain.com/blog/the-art-of-loop-engineering — Sydney Runkle (LangChain), The Art of Loop Engineering
