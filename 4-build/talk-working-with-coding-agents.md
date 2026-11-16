---
title: "Talk: working with coding agents"
type: deck
created: 2026-11-16
audience: engineers
status: checked
last_checked: 2026-11-16
as_of: "November 2026"
---

# Talk: working with coding agents

> **In one minute**
> - A coding agent works in a loop and stops when the work looks done, so give it a way to check.
> - Writing code has become cheap; checking it is now the hard part of the job.
> - Decide how the work will be checked before the agent starts, and keep context files short and current.
> - When you keep making the same correction, turn it into a check that runs, not another instruction.
> - Give an agent more freedom one kind of action at a time, as it earns a track record.

*Reading time: about 10 minutes · Best for: presenting to engineers*

A talk for engineers who already use coding agents, and the first of two sessions: 11 slides, 16:9, for about 25 minutes plus questions. The aim is that everyone leaves with one thing to try before session 2, which opens with what people found. This outline holds the slide text, the speaker notes and the sources; the deck itself is `talk-working-with-coding-agents.pptx` in this folder. Numbers in square brackets point to the Sources list at the end. Anthropic's documentation is quoted as it stood in November 2026, and Meta's ladder is Meta's own account. Slide 9 is the maintainer's own experience, in the first person. The key lines, the action on slide 10 and the other uncited suggestions are our advice, not findings from our sources. Slides 2 and 3 are basics, tagged in the corner; to build the deck without them, run `python3 scripts/build_deck.py 4-build/talk-working-with-coding-agents.md --no-basics --out <file>.pptx`, which leaves 9 slides.

---

## Slide 1 · Working with coding agents

*Layout: title*

**On the slide**

- Subtitle: Session 1 of 2: checking is the job

**Speaker notes**

This is the first of two sessions for engineers who already use coding agents.
The thread through both is that the job is moving from writing code to checking it.
Today is about using coding agents well in your own work; session 2 is about building AI features into the product.
The aim is that you leave with one thing to try this week, and session 2 starts with what people found.

---

## Slide 2 · Basics · What a coding agent is

**On the slide**

- Simon Willison: "An LLM agent runs tools in a loop…" [1]
- A model reasons; its tools search files, edit code and run tests [2]
- It calls tools, gets the results and repeats [3]
- Claude Code's docs: it stops when the work "looks done" [4]

**Key line:** Give it something to run that tells it whether the work is done.

**Speaker notes**

Simon Willison's working definition is short: "An LLM agent runs tools in a loop to achieve a goal."[1]
Anthropic's Claude Code docs, as of November 2026, say the loop is powered by two components: models that reason and tools that act.[2]
Throughout a task, Claude uses those tools: searching files to understand the code, editing to make changes and running tests to check its work.[2]
Anthropic's Agent SDK docs describe the same loop: Claude calls tools, receives the results and repeats.[3]
Anthropic's best-practices page adds that it stops when the work looks done: if it has nothing to run that tells it whether the work actually is done, "looks done" is all it has to go on.[4]

---

## Slide 3 · Basics · What it knows

**On the slide**

- Claude Code's context includes conversation, files and command output [2]
- Each new session starts with a fresh context window [2]
- What carries over is written to files: CLAUDE.md and auto memory [5]

**Key line:** If the agent will need it next session, write it down.

**Speaker notes**

As of November 2026, Anthropic's Claude Code docs say its context window holds the conversation history, file contents, command outputs, CLAUDE.md, auto memory, loaded skills and system instructions.[2]
Each new session starts with a fresh context window, without the conversation from earlier sessions.[2]
Two things carry knowledge across sessions, and both are written to files: CLAUDE.md files that you write, and auto memory, notes Claude writes for itself.[5]
Anthropic also describes agents that keep lightweight references, such as file paths, and load data into context with tools at runtime, instead of loading everything up front.[6]
Those are one tool's documented details, so check how yours works; either way, we recommend writing down anything the agent will need next time.

---

## Slide 4 · Writing is cheap; checking is the job

**On the slide**

- Kush Agrawal: "writing code isn't the hard part anymore. Verifying it is." [7]
- Harvard study: after firms adopted coding agents, PRs opened rose 35.7% [8]
- But resolved issues rose only 13.7% [8]
- And time from PR submission to approval rose 56.1% [8]

**Key line:** A change only counts once it ships, so checking has to keep up.

**Speaker notes**

Kush Agrawal of Duolingo put it in one line: "writing code isn't the hard part anymore. Verifying it is."[7]
A Harvard study of 655 firms, with data from January 2021 to August 2026, looked at what changed after firms adopted coding agents.[8]
Pull requests opened rose 35.7%, but resolved issues rose by only 13.7%, and in their conclusion the authors say "we can rule out increases larger than 30.7%".[8]
After adoption, the time from a pull request's submission to its approval rose 56.1%.[8]
Their conclusion is that AI substantially raises code output but has small effects on final software output, and that "Code review becomes the bottleneck."[8]

---

## Slide 5 · Decide how it'll be checked before you start

**On the slide**

- Prefer tests that predate the change; rewritten ones can't really be trusted [9]
- Anchor tests to written requirements, not the agent's own reading [10]
- Break something on purpose: do the tests notice? [10]
- Ask for proof from the running app, not just green tests

**Key line:** Decide what proof you'll accept before the agent starts.

**Speaker notes**

Jarred Sumner of Anthropic says the approach to a project built at agent scale is driven by how you will verify that it works.[9]
His team decided against rewriting Claude Code in Rust because its test suite would have had to be ported too, and once you rewrite the tests, "you can't really trust the tests anymore."[9]
McKenna Barlow of Microsoft warns that when an agent writes both the code and the tests, a misunderstood requirement "can actually show up in both places".[10]
So she pointed the testing agent at the README's written requirements, and before trusting a green suite, she breaks something on purpose to see whether the tests notice.[10]
The last bullet, proof from the running app, is our advice: passing tests are one piece of evidence, not all of it.

---

## Slide 6 · Context files: short, specific, current

**On the slide**

- ETH Zurich and LogicStar.ai study: no general gain in task success [11]
- But context files raised inference cost by over 20% on average [11]
- Leave out what the agent would find by reading the code [4]
- Make rules concrete enough to verify, and prune stale ones [5]

**Key line:** Treat a context file like code: keep it short, specific and current.

**Speaker notes**

A study by researchers at ETH Zurich and LogicStar.ai found that context files such as AGENTS.md did not generally improve coding agents' task success, while raising inference cost by over 20% on average.[11]
It also found that agents follow the files' instructions well, but that repository overviews, though popular and recommended by model providers, do not help.[11]
The authors conclude that context files are useful for specifying non-standard coding practices, but that any attempt to improve performance should be rigorously evaluated before deployment.[11]
Anthropic's Claude Code docs, as of November 2026, offer a test before writing anything down: if Claude could find it by reading the code and would actually go and look, leave it out.[4]
They also suggest targeting under 200 lines per CLAUDE.md file, since longer files consume more context and reduce adherence, writing instructions concrete enough to verify, and periodically removing outdated or conflicting instructions.[5]

---

## Slide 7 · Turn corrections into checks

**On the slide**

- Cam Soper: "a rule in an agent's instructions is just a suggestion" [12]
- Rule: no CloudFront in front of one server. Claude added it anyway [12]
- In code, the compiler enforces the rule [12]
- Lauren Tan: make each correction a deterministic check if you can [13]

**Key line:** If it must hold every time, make it a lint rule, a test or a type.

**Speaker notes**

Cam Soper of Pulumi had a rule that one of his home-lab MCP servers be reached only through its own auth, with no CloudFront access in front of it, and Claude put CloudFront access in front of it anyway.[12]
Had the policy been in code, he says, Claude couldn't have gone behind his back, because a rule in code is enforced by the compiler.[12]
His summary: "a rule in an agent's instructions is just a suggestion. It might follow it, it might not."[12]
Lauren Tan's advice is that whenever you correct your agent, think about how to make that a deterministic check instead of adding another line to your rules.[13]
In her inverse pyramid of where to spend time on an agent's environment, the first two layers are deterministic: the code itself, through API design, architecture and refactoring, then lint rules, type systems, compilers and tests.[13]

---

## Slide 8 · Earn autonomy one action at a time

**On the slide**

- Meta's on-call agent, level 1: investigates and reports; changes nothing [14]
- Level 2: drafts the fix; a human approves before production [14]
- Level 3: clears lower-criticality work on its own [14]
- To climb: how costly is a mistake, and how easy to catch? [14]

**Key line:** Promote one kind of action at a time, on its track record.

**Speaker notes**

Meta gives its on-call agent the same ladder a new on-call engineer climbs, by Meta's own account.[14]
At level one it investigates and changes nothing, at level two it drafts the fix but nothing reaches production until a human approves, and at level three it clears lower-criticality work on its own while high-criticality work stays with humans.[14]
Promotion turns on one question, "How costly is a mistake and how easy is it to catch?": an action climbs only when mistakes are cheap, they are caught by tests, CI or review, and the agent has a track record on that exact action.[14]
That's why the agent can close a noisy alert on its own while a production mitigation still waits for a human.[14]
We'd ask the same question of a coding agent, action by action: let it run the tests freely, say, long before it may push to the main branch.

---

## Slide 9 · From my own builds: agent squads

**On the slide**

- The card is the prompt: write the whole task into it
- A separate reviewer re-runs the checks; the writer never grades itself
- First snapshot: 19 of 20 reviewed implementation cards approved first time [15]
- Rules in the system: one publish script, the only way out

**Key line:** Put the task, the checks and the rules in the system, not in the agent's head.

**Speaker notes**

My dev squad has a lead, an engineer, an ops role and a reviewer, and each task is a card that a worker picks up from a kanban board.
A worker can't see the cards beside its own, or the chat that produced its card, so the card body is its whole prompt.
In my first five-day snapshot, 19 of the 20 implementation cards reviewed were approved first time, one was sent back for a real defect, and every approval cited checks the reviewer had run.[15]
When I let the lead publish its own pull requests, I found that blocking command patterns wasn't enough: a push to the main branch could be typed in ways the patterns didn't match.
So publishing now goes through one script, the only way out, which refuses the default branch and force-pushes, opens one pull request and never merges; the rest is in [Lessons from running agent squads](../3-engineer/lessons-from-running-agent-squads.md).

---

## Slide 10 · Try this week

**On the slide**

- Pick one correction you keep making
- Make it a check: a lint rule, test, type or hook
- Bring it to session 2: did the mistake stop?

**Key line:** Pick one correction you keep making and turn it into a check this week.

**Speaker notes**

This is the one thing to try before session 2.
Pick a correction you keep making, ideally one you've already written into a context file that the agent still misses, and turn it into something that runs: a lint rule, a test, a type or a hook.
Anthropic's Claude Code docs say that if you keep adding emphasis to a CLAUDE.md line and Claude still misses it, that's a sign the line belongs in a hook.[4]
Mitchell Hashimoto describes harness engineering as engineering a fix whenever an agent makes a mistake, so that the agent never makes that mistake again.[16]
Bring it to session 2: what you turned into a check, and whether the mistake stopped.

**Links:** the ladder for each correction, in [Working with coding agents](working-with-coding-agents.md#7-turning-corrections-into-checks).

---

## Slide 11 · Sources and further reading

*Layout: reading*

**On the slide**

- This outline: every sourced claim cited, with links to all its sources
- The longer guide: Working with coding agents, in this handbook
- The squad lessons: Lessons from running agent squads
- Next time, session 2: Building AI features

**Speaker notes**

Every claim on these slides that comes from a source is cited in the outline that goes with the deck, which lists all 16 sources with links.
The handbook's guide, Working with coding agents, covers the same ground in more depth, including what not to hand to an agent and how to review its output.
The squad lessons page has the full story behind each lesson on the squads slide, with its evidence.
Session 2 picks up from here with building AI features, and it opens with what you turned into a check.

**Links:** [Working with coding agents](working-with-coding-agents.md) · [Lessons from running agent squads](../3-engineer/lessons-from-running-agent-squads.md) · [Talk: building AI features](talk-building-ai-features.md).

---

## Related

- The full guide: [Working with coding agents](working-with-coding-agents.md)
- Session 2: [Talk: building AI features](talk-building-ai-features.md)
- First-hand lessons: [Lessons from running agent squads](../3-engineer/lessons-from-running-agent-squads.md)
- Policy and autonomy: [Agent-written pull requests and agent autonomy](../5-run/agent-pr-policy.md), [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md)
- The disciplines behind it: [Context engineering](../3-engineer/context-engineering.md), [Harness engineering](../3-engineer/harness-engineering.md)

**Read next:** [Talk: building AI features](talk-building-ai-features.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://simonwillison.net/2025/Sep/18/agents — Simon Willison, I think “agent” may finally have a widely enough agreed upon definition to be useful jargon now (18 September 2025)
[2] https://code.claude.com/docs/en/how-claude-code-works — Anthropic, How Claude Code works (Claude Code docs)
[3] https://platform.claude.com/docs/en/agent-sdk/agent-loop — Anthropic, How the agent loop works (Claude Agent SDK docs)
[4] https://code.claude.com/docs/en/best-practices — Anthropic, Best practices for Claude Code (Claude Code docs)
[5] https://code.claude.com/docs/en/memory — Anthropic, How Claude remembers your project (Claude Code docs)
[6] https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — Anthropic, Effective context engineering for AI agents
[7] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AI Engineer Code Summit 2026
[8] https://fion.ac/jellyfish.pdf — Fiona Chen & James Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production (version of 14 November 2026)
[9] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AI Engineer Code Summit 2026
[10] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[11] https://arxiv.org/abs/2602.11988 — Thibaud Gloaguen, Niels Mündler-Sasahara, Mark Niklas Müller, Veselin Raychev & Martin Vechev (ETH Zurich and LogicStar.ai), Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (arXiv 2602.11988, v3 of 29 September 2026)
[12] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[13] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[14] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[15] https://github.com/AnilKerai/hermes-squad/blob/374995b71e7670bd974c27ae838641c2fe7b22b3/docs/05-metrics.md — Anil Kerai, hermes-squad, docs/05-metrics.md, commit of 12 November 2026 (GitHub)
[16] https://mitchellh.com/writing/my-ai-adoption-journey — Mitchell Hashimoto, My AI Adoption Journey
