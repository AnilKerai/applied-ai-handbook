---
title: "Prompt engineering"
type: concept
created: 2026-11-15
audience: "Engineers new to AI, and anyone writing instructions for a model"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Prompt engineering

> **In one minute**
> - Prompt engineering is writing the text a model is given so that it does the task well.
> - Worked examples, and asking for the steps of reasoning, often help more than instructions alone.
> - A prompt is only as good as its results on real cases, so test each change.
> - Outside text that reaches a prompt can carry hostile instructions, so the defences belong in the code around the model.
> - For agents that run over many steps, the bigger job is choosing everything the model sees: context engineering.

*Reading time: about 4 minutes · Best for: engineers new to AI*

## What it is

A prompt is the text a language model (an AI model trained to predict text) is given: the task, any worked examples and the input to work on.
Brown et al.'s GPT-3 paper (2020) applied its model to tasks "specified purely via text interaction with the model", with a few worked examples and "without any gradient updates or fine-tuning", meaning no further training.[1]
Prompt engineering is the craft of writing that text well, and a 2021 survey of prompting methods by Pengfei Liu and colleagues gave an early academic definition: creating a prompting function "that results in the most effective performance on the downstream task".[2]
Anthropic describes prompt engineering's primary focus as "how to write effective prompts, particularly system prompts", the standing instructions that frame every request.[3]

## When it arrived

No source found for this page shows who first used the term, so it gives no coining date.
The earliest milestone on this page is the GPT-3 paper, which Brown et al. posted on 28 May 2020.[1]
Liu et al.'s survey shows the term in academic use by July 2021.[2]
Two prompting methods followed in 2022: chain-of-thought prompting from Wei et al. in January, and ReAct from Yao et al. in October.[4][5]
In February 2023 Simon Willison wrote that "Prompt engineering as a discipline doesn’t get nearly the respect it deserves", answering people who expected better models to make it obsolete.[6]
By mid-2025 the name was under strain: on 25 June 2025 Andrej Karpathy argued that "People associate prompts with short task descriptions you'd give an LLM in your day-to-day use", which undersells industrial-strength applications.[7]
Two days later Willison observed that, unfortunately, most people's inferred definition of the term is "a laughably pretentious term for typing things into a chatbot".[8]
In September 2025 Anthropic called context engineering "the natural progression of prompt engineering".[3]

## Core principles

**Show the task as well as describing it.**
GPT-3's tasks came with a few worked examples, known as few-shot demonstrations, inside the prompt itself.[1]
I recommend a few real examples of input and wanted output, covering the awkward cases.

**Ask for the reasoning, not only the answer.**
Wei et al. reported that giving a few worked examples of intermediate reasoning steps, which they call chain-of-thought prompting, improves reasoning in "sufficiently large language models".[4]

**Let the model act, and show it what happened.**
ReAct had models generate "reasoning traces and task-specific actions in an interleaved manner", such as calls to a Wikipedia API between steps of thought.[5]
Today's agents work in a cycle that resembles ReAct's: Anthropic defines them as "LLMs autonomously using tools in a loop".[3]

**Judge a prompt by its results.**
Liu et al.'s definition measures a prompt by its performance on the downstream task.[2]
I recommend changing a prompt only against a fixed set of test cases; [Eval engineering](eval-engineering.md) covers how such tests are built.

**Keep instructions and outside text apart.**
Simon Willison named prompt injection, an attack in which text fed to the model overrides its instructions, in September 2022, after Riley Goodside's examples against GPT-3, and called it "a form of security exploit".[9]
Research defences such as CaMeL (Debenedetti et al., 2025) work outside the prompt: it extracts the control and data flow from the trusted request, so that "the untrusted data retrieved by the LLM can never impact the program flow".[10]
I recommend treating any outside text in a prompt as data that may be hostile, never as instructions.

**Know where prompts stop.**
Anthropic notes that agents "operate over multiple turns of inference and longer time horizons", so they need strategies for the whole context, not only well-written prompts.[3]
That wider job is [context engineering](context-engineering.md).

## Where it shows up in this handbook

- [Context engineering](context-engineering.md): choosing everything the model sees at each step.
- [Working with coding agents](../4-build/working-with-coding-agents.md), section 4: the standing instructions (AGENTS.md files and skills) coding agents load.
- [Evals playbook](../4-build/evals-playbook.md): the test cases a prompt change should be checked against.
- [AI questions answered](../1-understand/ai-questions-answered.md): the question on prompt injection.
- [AI glossary for leadership](../1-understand/ai-glossary.md): prompt injection and tokens in plain words.

## See it built

The [primer for model-harness](https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/PRIMER.md#context-engineering), [my open-source .NET agent harness](https://github.com/AnilKerai/model-harness), shows one example implementation: its *guide* pattern decides what goes into the model's context window at each step.

**Read next:** [Context engineering](context-engineering.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://arxiv.org/abs/2005.14165 — Brown et al., Language Models are Few-Shot Learners (arXiv 2005.14165)
[2] https://arxiv.org/pdf/2107.13586v1 — Pengfei Liu et al., Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing (arXiv 2107.13586v1)
[3] https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — Anthropic, Effective context engineering for AI agents
[4] https://arxiv.org/abs/2201.11903v6 — Wei et al., Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (arXiv 2201.11903v6)
[5] https://arxiv.org/abs/2210.03629 — Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models (arXiv 2210.03629)
[6] https://simonwillison.net/2023/Feb/21/in-defense-of-prompt-engineering — Simon Willison, In defense of prompt engineering
[7] https://x.com/karpathy/status/1937902205765607626 — Andrej Karpathy, post on X on context engineering (25 June 2025)
[8] https://simonwillison.net/2025/Jun/27/context-engineering — Simon Willison, Context engineering
[9] https://simonwillison.net/2022/Sep/12/prompt-injection — Simon Willison, Prompt injection attacks against GPT-3
[10] https://arxiv.org/abs/2503.18813 — Debenedetti et al., Defeating Prompt Injections by Design (arXiv 2503.18813)
