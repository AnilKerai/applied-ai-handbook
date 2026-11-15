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
> - I built a private framework for testing AI agents before they ship. These are the principles it taught me, without its examples.
> - Test fixed, written-down cases with faked tools, so that every run can be compared with the last.
> - Measure what a change adds by running the same cases with it and without it.
> - Prefer exact checks, run each case several times, and test any AI grader against people before trusting it.
> - Keep the cases that guard what already works apart from the hard cases that show room to improve.

*Reading time: about 5 minutes · Best for: engineers building evals*

In May 2026 I started building an evals framework to answer one question: how do I know an agent I'm about to ship actually works, with evidence I can defend, before a user ever sees it? The framework is private, so this page has no link to it and no examples from it, only the principles. For the concept, see [Eval engineering](eval-engineering.md); for the practice, see the [Evals playbook](../4-build/evals-playbook.md).

## The case is the unit, not the running system

**What happened.** Running the agent live and watching its trace tested the plumbing, but it didn't give me a measurement I could repeat, because live tools return something different on every run.

**What I changed.** I made the unit a case: a fixed scenario written down as data, with the user's message, the skills available, a canned reply for every tool call, and the expectations to check. With the tools stubbed, the same case gets the same inputs every time, so I'm testing whether the agent reasons well given what the tools return. I'm explicit about what that doesn't test: real tool failures, recovery when a real service misbehaves, latency, and anything the case's author didn't imagine.

**The principle.** A case is only as good as the scenario behind it, so the answer to that limit is more cases drawn from real use, not a cleverer framework. The concept page recommends turning each new production failure into a case ([Core principles](eval-engineering.md#core-principles)).

## Three layers give a failure an address

**What happened.** One pass or fail on the final answer told me that something broke, but not where.

**What I changed.** Every case is now scored on three separate layers. Did the agent recognise that it should use the skill at all? Did it take the right steps, calling the tools it needed and avoiding the ones it shouldn't? Did it produce the right result? The steps are checked as a partial order, such as looking something up before acting on it, not as one exact sequence, because there is usually more than one valid route to a right answer.

**The principle.** A case where the steps were right but the outcome was wrong points at the reasoning, not the routing, which one overall score never could. Testing an agent means testing the model and the code around it together ([Core principles](eval-engineering.md#core-principles)).

## The delta matters, not the score

**What happened.** A high score told me little on its own. If the agent scores almost as well without a skill, the skill is mostly overhead. A lower score against a much lower baseline can mean the skill is doing real work.

**What I changed.** Every case runs twice: once with the skill, and once with the skill withheld and everything else the same, tools included. The headline number is the difference between the two runs. It's an ablation: remove one part, and measure the change.

**The principle.** Without a baseline you're measuring noise and calling it value. The playbook's advice to compare each re-run against the last baseline rests on the same idea ([Evals playbook](../4-build/evals-playbook.md), section 8).

## Deterministic checks first, a judge only when you must

**What happened.** Most of what looked like a quality judgement turned out to be a structural check on the trace: was a tool called, and does the output contain the expected fields?

**What I changed.** Those questions get exact checks, which are fast, free and give the same answer every time. An AI judge is the exception, kept for questions an exact check can't reach, such as whether prose is grounded in the evidence. I split two judges on purpose. One checks that the output is faithful to the tool evidence without seeing the expected answer, so an output can't score well by echoing the answer key. The other checks the output against the expected answer. That stops sounding right and being right from blurring into one score.

**The principle.** Use a code-based check wherever the right answer can be checked mechanically, and keep model graders for the rest ([Core principles](eval-engineering.md#core-principles)).

## One run is not evidence

**What happened.** The model doesn't give the same answer every time, so one passing run could mean that it always passes, or that it passed once.

**What I changed.** Cases run several times, and each check reports two things: whether it passed at least once, which shows the agent can do it, and whether it passed every time, which shows it reliably does. The second is pass^k, which τ-bench's authors proposed "to evaluate the reliability of agent behavior over multiple trials".[1] Every pass rate also carries a 95% confidence interval, and three passes from three runs gives an interval of 44% to 100%. That is honest about how little three runs show. The difference between the runs with and without a skill gets the same treatment, marked either significant or within noise.

**The principle.** Run each case more than once, and report reliability with error bars instead of a single draw ([Core principles](eval-engineering.md#core-principles)).

## Calibrate the judge

**What happened.** Raw agreement between an AI judge and people can mislead. A judge that always says "pass" agrees with people 80% of the time on a set where 80% of the labels are passes, while reading nothing.

**What I changed.** I score each judge against human labels with Cohen's kappa, which discounts the agreement a judge would get by chance, so the always-pass judge scores about zero. A judge has to clear a kappa of 0.6 before I trust it, and the framework warns me when there are too few labels for the score to mean much. For high-stakes questions, running the judge several times and taking the majority damps a single run's variance. Zheng et al. examine LLM judges' "position, verbosity, and self-enhancement biases", which is why I don't take a judge on trust.[2]

**The principle.** Test a model grader against cases a person has marked before trusting its scores ([Core principles](eval-engineering.md#core-principles); the playbook's section 5 covers kappa).

## Guardrails and headroom are different questions

**What happened.** A 100% pass rate across every case looked good, but it usually means the cases aren't hard enough to tell good work from bad.

**What I changed.** Each case is one of two kinds. Regression cases guard behaviour that already works: they should sit near 100%, a drop is an alarm, and they decide whether to ship. Capability cases are deliberately hard probes, where a low pass rate is expected. They're reported separately and kept out of the ship decision, so a hard probe can never block a release or drag down the headline number.

**The principle.** You need both: a guard for what works, and somewhere to climb. The playbook keeps regression and capability evals apart for the same reason ([Evals playbook](../4-build/evals-playbook.md), section 5).

## A verdict you can defend

**What happened.** All those numbers still had to become one decision that someone could act on.

**What I changed.** A run now folds everything into a verdict of ship, review or don't ship. Missing a gate means don't ship, missing a bar that isn't a gate means review, and meeting every bar means ship. A check that never ran counts as a miss, not a pass, and a result that nothing scored caps the verdict at review, because a ship verdict should never rest on a check that didn't happen. Capability probes inform the verdict but never gate it.

**The principle.** Make the verdict fail closed, and make every line of it traceable to a check that ran. The playbook explains why a passing eval run is the ticket into production ([Evals playbook](../4-build/evals-playbook.md), section 1).

**Read next:** [Lessons from running agent squads](lessons-from-running-agent-squads.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://arxiv.org/abs/2406.12045 — Yao, Shinn, Razavi & Narasimhan (Sierra), τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (arXiv 2406.12045)
[2] https://arxiv.org/abs/2306.05685v4 — Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (arXiv 2306.05685v4)
