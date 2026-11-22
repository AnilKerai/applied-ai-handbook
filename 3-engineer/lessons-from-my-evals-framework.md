---
title: "Lessons from my evals framework"
type: lessons
created: 2026-11-15
audience: "Engineers building evals"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Lessons from my evals framework

> **In one minute**
> - I built a private framework for testing AI agents before they ship. These are the principles it taught me, without examples from the skills it tests.
> - Test fixed, written-down cases with faked tools, so that every run can be compared with the last.
> - Measure what a change adds by running the same cases with it and without it.
> - Prefer exact checks, run each case several times, and test any AI grader against people before trusting it.
> - Keep the cases that guard what already works apart from the hard cases that show room to improve.

*Reading time: about 5 minutes · Best for: engineers building evals*

In May 2026 I started building an evals framework to answer one question: before an agent reaches its users, can I show with repeatable evidence that it works? I started it two weeks before [my harness](https://github.com/AnilKerai/model-harness), and the order says what I believe: model + harness = an agent, but model + harness + evals = an agent I'd trust in front of users. The framework is private, so this page has no link to it and no examples from the skills it tests, only the principles. For the concept, see [Eval engineering](eval-engineering.md); for the practice, see the [Evals playbook](../4-build/evals-playbook.md).

## The case is the unit, not the running system

**What happened.** The problem: watching a live agent run shows whether its parts connect, but live tools answer differently each time, so no two runs measure the same thing.

**What I changed.** I made the unit a case: a scenario fixed in advance and stored as data, holding the user's message, the skills on offer, a canned reply for each tool call, and what to check for. With the tools stubbed, the same case gets the same inputs every time, so what I'm measuring is how well the agent reasons from the replies it's handed. I'm explicit about what that doesn't test: real tool failures, recovery when a real service misbehaves, latency, and anything the case's author didn't imagine.

**The principle.** A stubbed case covers only the situations its author thought to write down, so widen coverage with cases taken from real use rather than with more machinery. The concept page recommends turning each new production failure into a case ([Core principles](eval-engineering.md#core-principles)).

## Three layers give a failure an address

**What happened.** The problem: a single verdict on the final answer shows that a case failed, but not which part of the agent went wrong.

**What I changed.** Every case is now scored on three separate layers. Did the agent notice that the task called for the skill? Were its steps right, calling the tools it needed and leaving alone the ones it shouldn't touch? Was the end result correct? The steps are checked as a partial order, such as looking something up before acting on it, not as one exact sequence, because a right answer can often be reached by more than one route.

**The principle.** A case where the steps were right but the outcome was wrong locates the fault in the reasoning, not in the choice of tools. One overall score can't do that. Testing an agent means testing the model and the code around it together ([Core principles](eval-engineering.md#core-principles)).

## The delta matters, not the score

**What happened.** The problem: a high score says little on its own. If the agent scores almost as well without a skill, the skill is mostly overhead. A lower score against a much lower baseline can mean the skill is doing real work.

**What I changed.** Every case runs twice: once with the skill, and once with the skill withheld and everything else the same, tools included. The headline number is the difference between the two runs. It's an ablation: remove one part, and measure the change.

**The principle.** A score with no baseline can't separate what the skill adds from what the model could already do. The playbook's advice to run both configurations on the same cases and compare the paired difference rests on the same idea ([Evals playbook](../4-build/evals-playbook.md), section 5).

## Exact checks first, and a judge only as a last resort

**What happened.** The problem: many questions that seem to need an AI judge are really about the shape of the trace, such as whether a tool was called or the output has the expected fields. A judge is also slower, costs money and can vary between runs.

**What I changed.** Those questions get exact checks, which are fast, free and give the same answer every time. An AI judge is the exception, kept for questions an exact check can't reach, such as whether a passage is supported by the evidence. I keep two separate judges on purpose. One never sees the expected answer and asks only whether the output is backed by what the tools returned, so an output can't win points by parroting the answer key. The other compares the output with the expected answer. Keeping them apart means a fluent answer can't hide a wrong one inside a single score.

**The principle.** Use a code-based check wherever the right answer can be checked mechanically, and keep model graders for the rest ([Core principles](eval-engineering.md#core-principles)).

## A single run proves little

**What happened.** The model doesn't give the same answer every time, so one passing run could mean that it always passes, or that it passed once.

**What I changed.** Cases run several times, and each check reports two things: whether it passed at least once, which shows the agent can do it, and whether it passed every time, which shows it reliably does. The second is pass^k, which τ-bench's authors proposed "to evaluate the reliability of agent behavior over multiple trials".[1] Every pass rate also carries a 95% confidence interval, and three passes from three runs gives an interval of 44% to 100%, which is honest about how little three runs show. The difference between the runs with and without a skill gets the same treatment, marked either significant or within noise.

**The principle.** Run each case more than once, and report reliability with error bars instead of a single draw ([Core principles](eval-engineering.md#core-principles)).

## Calibrate the judge

**What happened.** Raw agreement between an AI judge and people can mislead. A judge that always says "pass" agrees with people 80% of the time on a set where 80% of the labels are passes, while reading nothing.

**What I changed.** I measure each judge's agreement with labels that people gave, using Cohen's kappa, which discounts the agreement a judge would get by chance, so the always-pass judge scores about zero. A judge has to clear a kappa of 0.6 before I trust it, and the framework warns me when there are too few labels for the score to mean much. For high-stakes questions, running the judge several times and taking the majority damps a single run's variance. Zheng et al. examine LLM judges' "position, verbosity, and self-enhancement biases", which is why I don't take a judge on trust.[2]

**The principle.** Test a model grader against cases a person has marked before trusting its scores ([Core principles](eval-engineering.md#core-principles); the playbook's section 5 covers kappa).

## Guardrails and headroom are different questions

**What happened.** The problem: when every case passes, the set has usually stopped telling good work from bad, and it shows nothing about how far the agent could still improve.

**What I changed.** Each case is one of two kinds. Regression cases protect behaviour that already works: they ought to pass almost every time, any drop in their pass rate is a warning, and they decide whether to ship. Capability cases are probes made hard on purpose, so failing many of them is normal. They're reported on their own and left out of the ship decision, so a difficult probe can't hold back a release or pull the headline number down.

**The principle.** You need both: a guard for what works, and somewhere to climb. The playbook keeps regression and capability evals apart for the same reason ([Evals playbook](../4-build/evals-playbook.md), section 5).

## A verdict you can defend

**What happened.** All those numbers still had to become one decision that someone could act on.

**What I changed.** A run now folds everything into a verdict of ship, review or don't ship. Missing a gate means don't ship, missing a bar that isn't a gate means review, and meeting every bar means ship. A check that was skipped is treated as failed, not passed, and a result that no check scored can reach review at best, because a ship verdict must stand on checks that actually ran. Capability probes inform the verdict but never gate it.

**The principle.** Make the verdict fail closed, and make every line of it traceable to a check that ran. The playbook explains why a passing eval run is the ticket into production ([Evals playbook](../4-build/evals-playbook.md), section 1).

**Read next:** [Lessons from running agent squads](lessons-from-running-agent-squads.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://arxiv.org/abs/2406.12045 — Yao, Shinn, Razavi & Narasimhan (Sierra), τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (arXiv 2406.12045)
[2] https://arxiv.org/abs/2306.05685v4 — Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (arXiv 2306.05685v4)
