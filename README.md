# Applied AI Handbook

Practical, evidence-backed guidance for bringing AI into a business or an engineering team: when to use it, which kind, how to build and test it, how to run it safely, and how to lead the change.

**A living compendium by Anil Kerai, as of November 2026, written from my point of view and backed by evidence.** It separates three things: what practitioners report works, what published studies show, and my own recommendations. The evidence is cited so you can check it; the recommendations are my own view, not my employer's. Every factual sentence cites a public source you can check: a talk, a paper or an article. Before publishing, every cited claim was re-checked against the original transcripts, papers and articles, and every correction is logged. The Engineer section also includes my own path through these ideas and lessons from my own builds, written as experience rather than as findings. Templates, checklists and talks are written neutrally, so anyone can adopt or present them.

**Read it as a website:** [anilkerai.github.io/applied-ai-handbook](https://anilkerai.github.io/applied-ai-handbook/) has search, a sidebar in reading order and a layout that works on phones. The same pages are markdown in [the GitHub repository](https://github.com/AnilKerai/applied-ai-handbook).

**My own code:** [model-harness](https://github.com/AnilKerai/model-harness), my open-source .NET agent harness, is where the Engineer section's first-person lessons come from.

## Start here: pick a route

**New to AI** (about 50 minutes)

1. [AI questions answered](1-understand/ai-questions-answered.md)
2. [The big picture](3-engineer/the-big-picture.md)
3. [Should this task use AI, and which kind?](2-decide/should-this-task-use-ai.md)
4. [AI intake checklist](2-decide/ai-intake-checklist.md)
5. [AI failure modes: a pre-mortem checklist](2-decide/ai-failure-modes-premortem.md)

Skim the questions you care about and the map of how an AI system fits together, then the tools you'll use most. Keep the glossary open.

**Engineer building AI features or using coding agents** (about 105 minutes)

1. [The big picture](3-engineer/the-big-picture.md)
2. [Harness engineering](3-engineer/harness-engineering.md)
3. [Should this task use AI, and which kind?](2-decide/should-this-task-use-ai.md)
4. [AI pattern catalogue](4-build/ai-pattern-catalogue.md)
5. [Evals playbook](4-build/evals-playbook.md)
6. [Working with coding agents](4-build/working-with-coding-agents.md)
7. [Talk: working with coding agents](4-build/talk-working-with-coding-agents.md)
8. [Talk: building AI features](4-build/talk-building-ai-features.md)
9. [Agent-written pull requests and agent autonomy](5-run/agent-pr-policy.md)
10. [Running AI in production](5-run/ai-in-production-runbook.md)

Add the .NET guide if you work in .NET, and the rest of the Engineer section for each discipline in depth. To give the two talks, the slides are `4-build/talk-working-with-coding-agents.pptx` and `4-build/talk-building-ai-features.pptx`; the outlines have the speaker notes and sources.

**Leader planning AI adoption** (about 50 minutes)

1. [Where should AI go in our product or operations first?](2-decide/where-ai-goes-first.md)
2. [What must be true before AI agents can act in production?](6-lead/before-agents-act-in-production.md)
3. [Should we aim for a fully automated software factory?](6-lead/should-we-build-a-software-factory.md)
4. [Can AI replace our people?](6-lead/can-ai-replace-our-people.md)
5. [AI maturity model and roadmap](6-lead/ai-maturity-model.md)
6. [What to measure: AI metrics scorecard](5-run/ai-metrics-scorecard.md)
7. [How much should an agent be trusted to do on its own?](2-decide/how-much-autonomy-for-an-agent.md)

**Presenting to your team** (about 35 minutes)

1. [Talk: using AI well at work](1-understand/talk-using-ai-at-work.md)
2. [What works with AI: practical lessons](1-understand/ai-lunch-and-learn.md)

For colleagues new to AI, the slides are `1-understand/talk-using-ai-at-work.pptx`; for a general lunch-and-learn, `1-understand/ai-lunch-and-learn.pptx`. Each outline has the speaker notes and sources.

## The six sections

- **[1. Understand](1-understand/README.md)**: Start here if AI is new to you. The words, the common questions, a talk for colleagues new to using AI, and a lunch-and-learn on what works in practice.
- **[2. Decide](2-decide/README.md)**: Before anything gets built: is this a job for AI, which kind, how could it fail, and how much should it be trusted to do alone?
- **[3. Engineer](3-engineer/README.md)**: The disciplines under every AI system: prompt, context, harness, loop and eval engineering, how they fit together, when they arrived, and first-hand lessons from building them.
- **[4. Build](4-build/README.md)**: How to build AI features well: proven patterns, how to test them, how developers should work with coding agents, and two talks you can give to engineers.
- **[5. Run](5-run/README.md)**: Once it's live: operating AI safely, governing agent-written code, and measuring whether it's working.
- **[6. Lead](6-lead/README.md)**: For leaders: the big decisions about agents, automation and people, and a maturity model for planning adoption.

Reading everything takes about 5 hours. Nobody needs to; pick a route.

## How to read it

- Each document opens with an **In one minute** box, so you can stop there.
- **[n]** points to the numbered Sources list at the bottom of that document.
- **"X reports…"** or **"(X's claim)"** means the figure is that company's own, not independently checked.
- **"I recommend…"** and **"My reasoning"** are my own judgement, not a finding from a source.
- Each document has a `last_checked` date. This field moves fast, so check the date before relying on a figure.

## Corrections and updates

Every correction is logged in [CHANGELOG.md](CHANGELOG.md). If you spot something wrong or out of date, open an issue with the source.

## Licence

[CC BY 4.0](LICENSE). Share and adapt it, with credit: *Applied AI Handbook by Anil Kerai, CC BY 4.0*.
