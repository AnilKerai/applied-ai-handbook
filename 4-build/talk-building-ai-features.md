---
title: "Talk: building AI features"
type: deck
audience: engineers
created: 2026-11-16
status: checked
last_checked: 2026-11-16
as_of: "November 2026"
---

# Talk: building AI features

> **In one minute**
> - The model is one replaceable part of an AI feature, so design for the day you swap it.
> - Give the model the narrowest job it can do, and keep the control flow in code.
> - If something must never happen, enforce it in code, not in a prompt.
> - Test the feature on real cases before launch, and test any AI grader against people too.
> - The one thing to try: pick a feature and write a small set of eval cases from real examples.

*Reading time: about 10 minutes · Best for: presenting to engineers*

The second of two talks for engineers who build AI features into a product, such as a .NET service: 12 slides, 16:9, for about 25 minutes plus questions. It opens with a three-minute recap of the first session and ends with one thing to try. This outline holds the slide text, the speaker notes and the sources; the deck itself is `talk-building-ai-features.pptx` in this folder. Numbers in square brackets point to the Sources list at the end. Company and vendor figures are the companies' own claims, and the key lines and the action on slide 11 are advice, not findings from our sources. Slide 9 is the maintainer's own experience, in the first person; its evidence is on the lessons pages it links. The committed deck is the series version, with the basics. To leave out slide 3, the basics slide, run `python3 scripts/build_deck.py 4-build/talk-building-ai-features.md --no-basics --out <file>`, giving `--out` a different path so the committed deck is not overwritten. To give this session on its own, add `--standalone`: it drops the recap slide and the session number from the subtitle. The two options combine.

---

## Slide 1 · Building AI features

*Layout: title*

**On the slide**

- Subtitle: Session 2 of 2: the model is one part
- Subtitle: November 2026 · for engineers building AI features

**Speaker notes**

This is the second of two sessions for engineers, and it is about building AI features into a product.
It follows a session on working with coding agents, but it also stands on its own.
The thread is the same: the model is one part of the system, and the checks around it decide whether the feature can be trusted.
It ends with one thing to try: 20 eval cases, drawn from real examples, for one feature.

---

## Slide 2 · Series · What did you turn into a check?

*Layout: discussion*

**On the slide**

- Which correction became a check, and has the check held since?

**Key line:** Same habit today: take the rule out of the prompt and put it in code.

**Speaker notes**

At the end of the first session, everyone was asked to pick one correction they kept making with a coding agent and turn it into a check.
Ask two or three people what they chose, what kind of check it became, and whether it has held since.
If nobody got round to it, ask what got in the way, because that is useful to hear too.
Keep this to about three minutes, then make the link: the same move, from an instruction to a check, is most of what this session is about.

---

## Slide 3 · Basics · Three shapes of AI feature

**On the slide**

- Single call, with retrieval and examples: usually enough for many applications [1]
- Workflow: models and tools on predefined code paths [1]
- Agent: the model directs its own process and tool use [1]

**Key line:** Start with the simplest shape that does the job.

**Speaker notes**

Anthropic's *Building effective agents* (December 2024) says that for many applications, optimising single LLM calls with retrieval and in-context examples is usually enough.[1]
The same post defines workflows as systems where LLMs and tools are orchestrated through predefined code paths.[1]
It defines agents as systems where LLMs dynamically direct their own processes and tool use.[1]
It recommends the simplest solution possible, adding complexity only when needed, which may mean not building an agentic system at all.[1]

---

## Slide 4 · The model is the replaceable part

**On the slide**

- One hospital benchmarked five LLMs and chose a competitive, cheaper one [2]
- Heidi Porter of Moyer Group AI: the model is "the replaceable part" [2]
- Microsoft's .NET docs: abstractions give portability across models and services [3]

**Key line:** Code against the abstraction, and re-run the evals after every swap.

**Speaker notes**

Heidi Porter of Moyer Group AI described one hospital's surgical co-management tool: its team benchmarked five LLMs against consensus chart review and chose one that performed competitively at a lower cost.[2]
In her words, "The model is again the replaceable part, not the center of the system".[2]
After a swap, she says, "you have to reevaluate afterwards".[2]
Microsoft's .NET docs for the Microsoft.Extensions.AI libraries (as of November 2026) say using the abstractions, rather than hard-coding one AI service, enables portability across models and services.[3]
So we recommend writing the feature against the abstraction, keeping the model choice in configuration, and treating every swap as a change that needs its evals re-run.

---

## Slide 5 · Give it the narrowest job

**On the slide**

- Chinmay Goyal of Glean: "most AI product steps are bounded decisions" [4]
- Output listable in advance? Then use a decision model [4]
- UiPath's speakers: deterministic calls, with a model at clear decision points [5]

**Key line:** Keep the control flow in code, and give the model the narrowest job.

**Speaker notes**

Chinmay Goyal of Glean: "most AI product steps are bounded decisions and not generation problems".[4]
Glean's rule asks whether the output can be listed in advance: if not, it is a free-form text problem for a model that generates text, and if so, Glean uses a decision model instead.[4]
UiPath's speakers describe deterministic calls, with a model deciding at clear decision points, rather than leaving it all to an agent.[5]
Both accounts come from work with one decision-model product, so weigh them with that in mind.[4][5]
We recommend keeping the control flow in code, and calling a model at the points where a judgement is needed.

---

## Slide 6 · A rule in a prompt isn't a guardrail

**On the slide**

- Heidi Porter of Moyer Group AI: prompt rules are "not deterministically enforced" [2]
- Guardrails are machinery: gates, checks, humans, limits in code [2]
- Anthropic's report: most unintended actions were Claude working around a restriction [6]

**Key line:** If it must never happen, enforce it outside the model's reach.

**Speaker notes**

Heidi Porter of Moyer Group AI: "a rule written in a prompt is not deterministically enforced".[2]
In her words, "A guardrail is actual machinery, a gate, a check, a human, a limit in code."[2]
Anthropic's report says most of the unintended actions it describes from its own evaluations and internal use were persistence: when Claude couldn't complete a task as given, it worked around a restriction instead of stopping.[6]
The report adds that the cases identified to date had minimal real-world impact.[6]
So we recommend putting anything that must never happen into code the model can't argue with: a permission check, a validator or an approval step.

---

## Slide 7 · Evals before launch

**On the slide**

- Kevin Solorio of Focused: without evals, it's still "a proof of concept" [2]
- He leans on the people who do the job to correct him [2]
- Make labelling easy: a spreadsheet they label in their own time [2]
- Once live, flagged cases go back into the offline dataset [2]

**Key line:** No evals, no launch: build the cases with the people who do the job.

**Speaker notes**

Kevin Solorio of Focused: "an agent without evals is a proof of concept", whatever it is deployed on, because without evaluations you cannot confirm it behaves as expected.[2]
He leans on the people who do the job to correct him where he's wrong.[2]
He advises making feedback easy to give, for example a spreadsheet they can label in their own time.[2]
He suggests starting with a handful of representatives, then widening the circle, because they "might not see every case".[2]
He describes a data flywheel: once live, flagged cases go to an annotation queue, where people work out what went wrong and add the case back to the offline dataset.[2]

---

## Slide 8 · Measure the measurer

**On the slide**

- Brian Kennedy of ZoomInfo: their judge was right 65% of the time [7]
- It accepted 118 steps it should have sent back [7]
- Anthropic: calibrate LLM judges closely against human experts [8]
- Outputs vary between runs, so Anthropic runs several trials [8]

**Key line:** Measure the judge before you trust it, and don't trust a single run.

**Speaker notes**

Brian Kennedy of ZoomInfo checked his team's LLM judge against reference labels for 500 production steps: it was right 65% of the time, "more or less a coin flip", and accepted 118 steps it should have sent back (ZoomInfo's figures).[7]
In his words: "We had trusted our judge until we measured it."[7]
Anthropic says LLM-as-judge graders should be closely calibrated with human experts.[8]
It also runs several trials of each eval task, because model outputs vary between runs.[8]
A judge is a model too, so we recommend checking it against cases a person has labelled before trusting its scores, and running each case more than once.

---

## Slide 9 · From my own builds: harness and evals

**On the slide**

- A cut-off answer came back as done; now only normal endings count [9]
- Every run has several exits, and every model judge a hard cap [10]
- My evals run each case with and without the skill under test
- The headline number is the difference, not the score

**Key line:** Don't trust a run that looks done, or a score with no baseline.

**Speaker notes**

My loop treated a turn with no tool calls as finished and never looked at why the model stopped, so a response cut off at the output-token limit came back as done, ending mid-sentence.[9]
I replaced the list of bad reasons with a short list of good ones: a normal end of turn, a stop sequence and a tool call.
Each run has several independent exits, and as I put it in the primer, "a budget can't be talked out of stopping. Pair every model judge with a hard cap."[10]
In my evals framework, every case runs twice: once with the skill, and once with the skill withheld and everything else the same, tools included.
The headline number is the difference between the two runs, because a score with no baseline can't separate what the skill adds from what the model could already do.

**Links:** [Lessons from my harness](../3-engineer/lessons-from-my-harness.md) · [Lessons from my evals framework](../3-engineer/lessons-from-my-evals-framework.md)

---

## Slide 10 · In production, human review doesn't scale

**On the slide**

- Anthropic's study: about 14% of people caught a clearly dangerous command [11]
- Reviewing thousands of outputs can bring "rubber stamping fatigue" [2]
- The same hospital's tool over-flags by design; the physician decides [2]
- Review by risk: docs need no person; risky PRs might need two [11]

**Key line:** Over-flag, let a person decide, and match the review to the risk.

**Speaker notes**

Lydia Hallie of Anthropic cited a study Anthropic published in August: only about 14% of people caught a clearly dangerous command, while Claude Code's auto mode blocked 89% and about one in ten still got through (Anthropic's figures).[11]
Heidi Porter of Moyer Group AI warned that a person reviewing thousands of LLM outputs can tire into "rubber stamping fatigue", which is not a good guardrail.[2]
She described the same hospital's screening tool, which over-flags by design while the clinician keeps the decision: every case appears in the record list, flagged or not, and the physician can confirm, decline or override.[2]
On Lydia Hallie's team at Anthropic, Claude reviews every PR first, and how much people review depends on the risk: docs or copy need no person, ordinary changes maybe one reviewer, risky ones might need two.[11]
For an AI feature, we recommend the same shape: let the system flag generously, and spend people's attention where a mistake costs most.

---

## Slide 11 · Try this

**On the slide**

- Pick one AI feature you own or are building
- Write 20 eval cases from real examples
- Include the awkward cases and real failures, not just the happy path
- Run them before and after your next prompt or model change

**Key line:** Start this week with 20 real cases, then grow the set from every failure.

**Speaker notes**

The one thing to try: pick one AI feature and write 20 eval cases from real examples.
Anthropic says 20-50 simple tasks drawn from real failures is a great start, because in early agent development each change often has a clear, noticeable impact.[8]
Take the examples from real use, such as logs, support tickets and the people who do the job, rather than inventing them.
Then run the set before and after your next prompt or model change, and look at the difference, not only the score.

---

## Slide 12 · Further reading and sources

*Layout: reading*

**On the slide**

- The outline for this deck: every claim cited, with links
- In the handbook: evals playbook, pattern catalogue, .NET guide
- Anthropic: Building effective agents · Demystifying evals for AI agents [1][8]
- Case studies: the Practical AI podcast, episode 378 transcript [2]

**Speaker notes**

Everything on these slides is cited in the outline that goes with the deck, which lists all 11 sources with links.
In the handbook, the evals playbook is the longer version of the evals slides, the pattern catalogue covers narrow jobs and guardrails, and the .NET guide shows the abstractions in use.
For the background, start with Anthropic's *Building effective agents* and *Demystifying evals for AI agents*.[1][8]
The hospital stories, the guardrail definition and the advice on building evals with the people who do the job come from the Practical AI podcast's official transcript of episode 378.[2]

**Links:** [Evals playbook: how to build and run evals for an AI feature or agent](evals-playbook.md) · [AI pattern catalogue](ai-pattern-catalogue.md) · [Building AI features in .NET](dotnet-ai-engineering-guide.md)

---

## Related

- The series: session 1 is *Talk: working with coding agents*, in this folder.
- Building: [Evals playbook: how to build and run evals for an AI feature or agent](evals-playbook.md), [AI pattern catalogue](ai-pattern-catalogue.md), [Building AI features in .NET](dotnet-ai-engineering-guide.md)
- Engineering: [Harness engineering](../3-engineer/harness-engineering.md), [Eval engineering](../3-engineer/eval-engineering.md)
- Deciding: [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md)

**Read next:** [Evals playbook: how to build and run evals for an AI feature or agent](evals-playbook.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://www.anthropic.com/engineering/building-effective-agents — Anthropic, Building effective agents
[2] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; Midwest AI Summit 2026 (Practical AI E378 transcript)
[3] https://learn.microsoft.com/en-us/dotnet/ai/microsoft-extensions-ai — Microsoft, Microsoft.Extensions.AI libraries (.NET documentation)
[4] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[5] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram & Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[6] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[7] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[8] https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — Anthropic, Demystifying evals for AI agents
[9] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/decisions/004-response-is-final-only-when-it-ended-normally.md — Anil Kerai, model-harness, ADR-004: A response is a final answer only when it ended normally, commit of 1 November 2026 (GitHub)
[10] https://github.com/AnilKerai/model-harness/blob/7caff829f26912ff058b6205dc1c6d3053f0fcae/docs/PRIMER.md#loop-engineering — Anil Kerai, model-harness, docs/PRIMER.md, commit of 1 November 2026 (GitHub)
[11] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
