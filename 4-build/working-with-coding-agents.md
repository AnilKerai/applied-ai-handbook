---
title: Working with coding agents
type: guide
created: 2026-11-14
audience: Software engineers using coding agents day to day (Claude Code, GitHub Copilot, Codex, Cursor and similar); tool-agnostic
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Working with coding agents

> **In one minute**
> - You own what ships, even when a coding agent (an AI that writes code) wrote it; speed up only checkable work.
> - Before starting, decide how success will be checked, such as a test to pass or a screen to show.
> - Keep the overall design, security, how data is structured, and whether to build at all, for people to decide.
> - Keep tasks small, give each agent its own separate workspace, review its plan first, and ask for proof it works.
> - Judge the code and evidence over the agent's summary; turn each correction into a reusable instruction and, better still, an automatic check.

*Reading time: about 15 minutes · Best for: software engineers*

The day-to-day companion to the [agent PR policy](../5-run/agent-pr-policy.md): the policy says what must hold before agent work merges; this says how to work so that it does. It applies to any coding agent. Advice is mine and uncited; cited lines are the evidence. Company figures are their own claims.

## 1. The mindset: you own the outcome

The agent writes the code; you own what ships.
Sam Basu (Uno Platform) reminded developers that the pull request carries their name, not the AI's.[5]
Juergen Gutsch: "Errors agents do are my errors".[6]

Writing code is no longer the slow part. Checking it is.
Duolingo: "writing code isn't the hard part anymore, verifying it is."[2]
A Harvard study of 655 firms (revised November 2026; observational data to August 2026) found coding agents raised pull requests by 35.7% but resolved issues by only 13.7% (borderline significant), while time from review submission to approval rose 56.1%.[4]
Chris Shinkle of SEP, a firm that builds software for clients, treats "the joy's all gone. All I do all day is review code." as a sign a team is working in the wrong mode; SEP's principles include "verification before velocity" and chasing review bottlenecks.[1]
Dexter Horthy (Factory): "AI cannot replace human judgment. It can only amplify our judgment".[7]

So speed up only the work you can check, and put your effort into defining *right* and proving it, not into typing.

## 2. Before you start: decide how it will be checked

Jarred Sumner (Anthropic) chose his project by how it could be verified, checking an agent-built compiler against test suites that predated it, and passed on a rewrite whose tests would have needed porting: once you rewrite the tests, "you can't really trust the tests anymore."[8]
AWS's Swami Sivasubramanian supervised an agent rebuilding a replication engine for four nights before seeing it had no way to check its results; with a spec and a test environment the rebuild took about two hours (AWS's account).[9]

Write the spec, then check it.
Rajath Kotyal (AWS) showed specs hiding conflicts, gaps and ambiguities such as *remove the record* (delete it, or hide it?): "Check the spec always before you pass it down to the agent."[10]
McKenna Barlow (Microsoft) warns that if an agent "misunderstands a requirement, that same misunderstanding can actually show up in both places", code and tests.[11]
She anchors new tests to the written requirements and breaks something on purpose to see whether the suite notices.[11]

Plan in proportion to risk.
Horthy scales planning to *expected pain*, the likelihood of a change times how hard it is to change later: plan schemas, not button colours.[7]

Pick tasks by checkability.
Duolingo points its test-writing agent first at the code most likely to succeed and ranks legacy and large files lower.[2]

Recommendations:
- Write acceptance criteria a test, command or screenshot can confirm; for anything bigger than a ticket, use the [AI feature spec template](../2-decide/ai-feature-spec.md).
- Name the check in the prompt: the test to pass, the command to run, the screen to show.
- Where tests are missing, write or approve them first and keep them out of the agent's reach.
- Whether a task suits AI at all: [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md).

## 3. What not to hand to an agent

Michael Washington lets AI write all the code but none of the architecture: "So the AI is the builder, the constructor. However, it is not the architect."[12]
He decides authentication and the data layer himself and reviews every plan, because "if you don't decide, the AI will."[12]
Anthropic's Claude Code team keeps these for people: whether to build at all, risky code and pattern-setting architecture (Anthropic's account).[13]

Foundations matter more with agents, not less.
Lauren Tan calls the codebase a garden: agents copy the established pattern, so one workaround spreads like weeds.[14]
She bans easily misused APIs, because "anything that requires nuance to use well often leads to slop."[14]

Discovery and brownfield work differ.
Justin McCarthy (Diffusion) says "please stop building software factories" for uncertain new products; point factories at brownfield work, where customers have shown what matters and the job is the same but faster, cheaper or safer.[15]
*Better*, he adds, may need judgement and taste, so it may belong in discovery.[15]
Armin Ronacher (Earendil): "It's very easy to basically create the Simpson car of all the features in a software."[16]

Keep these for people; agents can research and draft, you decide:
- architecture, module boundaries and pattern-setting code;
- authentication, authorisation and the security model;
- the data model, schemas and migrations;
- public APIs and contracts with other teams;
- whether to build it, and what to leave out;
- anything nobody can check.

In discovery, treat agent prototypes as throwaway and rebuild deliberately.

## 4. Context: AGENTS.md and skills

Context files (AGENTS.md, CLAUDE.md, Copilot instructions, Cursor rules) load on every run, and a skill's body loads whenever the agent decides it needs it, so every line costs.[19] The policy's section 3 sets the rules; this section covers how to write them.

Write only what the model can't infer.
Lydia Hallie (Anthropic) keeps CLAUDE.md to what Claude cannot see from the code, without IMPORTANT-style rules.[17]
An ETH Zurich study found context files did not generally improve task success but raised inference cost by over 20%.[18]
A study of 3,159 skill files refines that: added rules helped mainly when they named a command or path the skill had not mentioned, restating an existing rule added little, and deleting a rule cut compliance with it.[19]
Nikolay Petrov found large models already knew about 70% of skills' general ideas but only 22% of the specific details.[20]

Agents follow what you write, literally.
Ayush Bhardwaj made a flag do nothing, yet agents passed it in 95 of 95 searches because a skill said to: "So your skill.md, your help text, your error messages are the interface."[21]

Watch rules pile up.
Steve Yegge: "everything you say gets written into this append-only record and nobody ever cleans it up."[23]
His over-fenced agents did nothing overnight: "they put all these rules in place to make sure nothing bad ever happened and so nothing ever happened."[23]
Anthropic's guidance for Claude Fable 5.2 agrees: cautious instructions that build up in memory, notes and instruction files make it ask for needless approvals; the fixes include deleting stale notes, naming the steps that need no approval and writing exceptions into *never* rules (vendor guidance).[22]

Recommendations:
- Put in commands, non-obvious conventions, gotchas, where to look and what *done* means.
- Leave out overviews the code already shows, task state, emphasis in capitals, and anything a check enforces.
- Name the exact command or path, not a virtue such as *write good tests*.
- Test changes on a few real tasks with and without them (see [Evals playbook: how to build and run evals for an AI feature or agent](evals-playbook.md)); prune after model upgrades; treat stale files as bugs.

## 5. During the work

Keep tasks small.
Dmitry Buykin (Maersk) stays below the point where there is more change than anyone can check, using small regular sweeps rather than big rewrites: "Verification speed is the limit."[3]

Plan, then execute.
In Gutsch's *wise coding*, the agent writes the plan; he then reviews every step and challenges the plan, sometimes with a second agent.[6]

Isolate each agent.
Justin Yoo (Microsoft) separates the permission to run from the permission to reach: "we should start from a cloned workspace rather than a real codebase."[25]
Hallie: "this machine is disposable, but the things that leave it aren't."[17]
Cognition gives every agent its own VM, with third-party services mocked.[26]
The required controls are in the policy's section 4.

Ask for proof.
Gerald Versluis (Microsoft): "for every session, start from a running app, ask for proof".[27]
Washington goes further, "All the test cases pass green. Personally, that's worthless to me.", and has his agent drive the running app.[12]
Bhardwaj found a quarter of agent CLI calls piping output through filters such as `head` or `tail`; in one user-reported case, `tail` cut off the error and the agent reported success.[21]
Hallie's hooks exit with code 2 on a failed check, which sends the agent back to fix it.[17]

Recommendations:
- One task, one branch, one worktree or sandbox per agent, fresh session each time.
- Beyond small fixes, ask for a plan and read it. Correct the plan, not the code.
- Ask for evidence up front: commands with full output and exit codes, screenshots for UI, logs for behaviour.
- If the agent loops, stop and re-plan.
- How far an agent may act alone: [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md).

## 6. Reviewing agent output

Code and evidence come before the story.
Robinhood: "If the description says it is safe and the code says otherwise, the code wins."[28]
Duolingo found that "agents sometimes take the shortest path to green CI", so it closes any PR touching a file that isn't a test, mock, fake or stub.[2]
Spotify saw the same in its migration agent, Honk, which got builds to pass by commenting out a test or downgrading Java.[38]
Barlow's assertion check asks what incorrect behaviour could still pass.[11]

Depth follows risk.
On Hallie's team, Claude reviews every PR first; docs then need no person, ordinary changes maybe one reviewer, and risky ones might need two, much as the policy's section 6 sets out.[17]
The busiest teams lean on evidence over line-reading: Tan reviews about 300 PRs a day, against 3 in 2024, with checks carrying the load.[14]
Doug Clauson (AWS): "quality really becomes a testing problem."[31]
The policy still asks reviewers to read the diff and tool output first; I recommend relaxing that only area by area, on measured results.

Know the pushback signals.
Ronacher: "an agent is really rewarded in just completing a goal."[16]
Brian Douglas treats an expert colleague's pushback as a good signal: "he has knowledge that the agent does not."[29]
His agent-written Rust passed AI review, then drew human pushback on API structure, fit with the codebase and duplicated services; he also sees agents reinventing existing libraries.[29]
Tan found agents justifying a timer workaround in comments: "the worst part about comments though is that they're not enforceable."[14]

Push back on:
- tests deleted, skipped, loosened or rewritten alongside the code;
- changes outside the task's scope;
- comments explaining a workaround (timers, sleeps, retries, catch-all handlers);
- new helpers or dependencies duplicating what exists;
- claims it works with no run evidence;
- a diff that grows with every fix round.

Anthropic's Claude Code team caps agent author-reviewer loops at three rounds, then reconsiders the approach (Anthropic's account).[13]

## 7. Turning corrections into checks

Tan: "whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules".[14]
In her inverse pyramid of where to spend time on an agent's environment, the first two layers are deterministic: the code itself (API design, architecture), then lint, types and tests; runtime and formal verification come next, with a little prose last.[14]
Cam Soper (Pulumi) had a rule that one of his home-lab MCP servers be reached only through its own auth, with no CloudFront in front of it, and Claude put CloudFront in front of it anyway.[24]
His conclusion: "a rule in an agent's instructions is just a suggestion. It might follow it, it might not."[24]
Geoffrey Huntley says editing AGENTS.md still leaves a gap that drifts, whereas a pre-commit hook that checks the diff and feeds back a correction took his agent to ten out of ten (one practitioner's experience).[30]

Not everything can be a check.
Gutsch's rule is *tell it twice, make it a skill*.[6]
Douglas: "My recommendation is probably write a skill first.", and "once you have skills you can create eval."[29]
The Claude Code team fixes repeated review findings at the source: a skill, a lint rule, CLAUDE.md or a per-area review file (Anthropic's account).[13]

A ladder for each correction (my recommendation):
1. First time: fix it.
2. Second time: a skill, or a context line naming the command or path.
3. Keeps happening, or matters: a lint rule, analyser, type, test or API change that makes it impossible.
4. Log corrections and bring them to the team's regular review.

SEP calls that review *deliberate iteration*, time set aside each week to discuss the tools; the policy's monthly session is the minimum.[1]

## 8. Parallel agents and cost

More agents help only if you can keep up.
Ronacher: "human attention is for me at least the limiting factor."[16]
Clauson found parallel sessions top out at two or three while you are the feedback loop: "if you make yourself the feedback loop, you are now the bottleneck."[31]
Yegge runs about 50 agents and found "the more agents I deploy, the more humans I need."[23]

Newer evidence tempers these many-agent setups.
Across enterprise deployments, Anthropic found one agent loop with skills often beat subagents on quality, cost and latency, keeping subagents for context bloat or parallel throwaway work (vendor guidance).[33]
A Cohere study found agent teams beat solo agents but cost three to seven times as much.[32]
Warp says tuning models and removing redundant subagents cut its cost from about $80 to $15-20 per PR (Warp's claim).[34]

Watch tokens and cost per task.
Philipp Schmid (Google DeepMind) found a single Bash tool roughly matched richer harnesses on accuracy with fewer tokens: "if your harness is more complex to use, the model will work around it, will find solutions around it, but needs more turns and more tokens".[35]
He and Ronacher see *code mode*, where the model writes code that calls its tools, gaining ground, and Claude Code now offers it as an experimental opt-in.[35][16][36]
The policy advises leaving such modes off until deny rules and logs cover each call.
SEP asks how comfortable an organisation is "spending $10 a day for tokens?"; one client's budget covered only a couple of days' work.[1]
Simon Willison argues pay-per-use services should ship with hard spending caps on.[37]

Recommendations:
- Start with one agent. Add another only for work needing little context from the first (research, an independent module, a fresh-context review), in its own worktree.
- Run no more agents than you can review that day, usually two or three.
- Track tokens and cost per task, failed runs included, and set a cap; the policy's cost per merged PR adds these up.

## 9. Anti-patterns

- **Prompting harder instead of checking:** capitals and *never* where a test belongs.[17][24]
- **One run writing both the code and the tests that judge it.**[8]
- **Trusting green.** Barlow: "When a test suite is green, it's really easy to kind of just treat that as confirmation that a change is correct".[11]
- **Automating a sloppy loop.** Tan: "if your inner coding loop produces slop, then automating that loop just produces more slop".[14]
- **Fixing forever.** Duolingo caps CI fix attempts at five, then closes the PR.[2]
- **Handing over secrets.** Gutsch: "the LLM should not know any credentials".[6]
- **Never pruning** rules and memory.[23][22]

## 10. Cheat sheet

- You own what ships. Speed up only what you can check.
- Before starting: acceptance criteria, the named check, a plan sized to risk.
- Keep architecture, auth, the data model, public APIs and *should we build it* for people.
- AGENTS.md: commands, paths, gotchas, what done means. Test it; prune it.
- One task, one branch, one sandbox per agent. Plan first, then execute.
- Ask for proof: full test output, screenshots, logs.
- Review evidence and code before the description; depth by risk.
- Push back on weakened tests, scope creep and workaround comments.
- Corrected twice? Make it a skill. Still happening? Make it a check.
- Two or three agents at most; track cost per task and set a cap.
- What must hold before merge: [Agent-written pull requests and agent autonomy](../5-run/agent-pr-policy.md).

As a talk: [Talk: working with coding agents](talk-working-with-coding-agents.md), slides and speaker notes for presenting this guide's main ideas to engineers.

**Read next:** [Building AI features in .NET](dotnet-ai-engineering-guide.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026
[2] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AIE CODE 2026
[3] https://ai.engineer/code/2026/talks/online-dmitry-maintenance — Dmitry Buykin (Maersk), Agents Made Code Free. Maintaining It Didn't Get Cheaper., AIE CODE 2026
[4] https://fion.ac/jellyfish.pdf — Chen & Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[5] https://www.youtube.com/watch?v=TF6qzdKwl84&t=20440 — Sam Basu (Uno Platform), Developer Workflows in AI Age - Local or Cloud, .NET Conf 2026
[6] https://www.youtube.com/watch?v=TF6qzdKwl84&t=9595 — Juergen Gutsch, Building a multi agent solution using Aspire, .NET Conf 2026
[7] https://ai.engineer/code/2026/talks/dexter-horthy — Dexter Horthy (Factory), A software factory needs pressure in both directions, AIE CODE 2026
[8] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AIE CODE 2026
[9] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS), AWS Emulator and the engineer's job when agents write the code
[10] https://ai.engineer/code/2026/talks/online-aws-specification-analyzer — Rajath Kotyal (AWS), Specs have bugs too, AIE CODE 2026
[11] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[12] https://www.youtube.com/watch?v=TF6qzdKwl84&t=29691 — Michael Washington (Microsoft MVP), What NOT to AI: Hand-Crafting Your App's Core Foundation, .NET Conf 2026
[13] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[14] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AIE CODE 2026
[15] https://ai.engineer/code/2026/talks/justin-mccarthy — Justin McCarthy (Diffusion), Brownfield factories keep the promises you already made, AIE CODE 2026
[16] https://ai.engineer/code/2026/talks/armin-ronacher — Armin Ronacher (Earendil), The Software Atelier, AIE CODE 2026
[17] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AIE CODE 2026
[18] https://arxiv.org/abs/2602.11988 — ETH Zurich, Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (arXiv 2602.11988)
[19] https://arxiv.org/abs/2610.04832 — Wang et al. (arXiv 2610.04832), Agent Skill Evolution: How Revisions Affect Coding Agents
[20] https://ai.engineer/code/2026/talks/online-skills-knowledge — Nikolay Petrov, Your SKILL.md is 70% of Things the Model Already Knows, AIE CODE 2026
[21] https://ai.engineer/code/2026/talks/online-ayush-cli — Ayush Bhardwaj, Your agent hates your CLI, AIE CODE 2026
[22] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 — Anthropic, Prompting Claude Fable 5.2: Keep caution from piling up
[23] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (Independent), Software Factories: Escape from Trash Mountain, AIE CODE 2026
[24] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[25] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[26] https://ai.engineer/code/2026/talks/walden-yan — Walden Yan (Cognition), A New Age of Software Engineering, AIE CODE 2026
[27] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=20349 — Gerald Versluis (Microsoft), Beyond Code Generation: Give AI Eyes and Hands for .NET MAUI, .NET Conf 2026
[28] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AIE CODE 2026
[29] https://ai.engineer/code/2026/talks/online-brian-douglas — Brian Douglas, If You Are Going to Verbally Abuse Your Agents, at Least Label the Outcome, AIE CODE 2026
[30] https://simonwillison.net/2026/Oct/13 — Simon Willison, weblog 13 Oct 2026: Geoffrey Huntley on enforcing conventions with hooks rather than AGENTS.md
[31] https://ai.engineer/code/2026/talks/doug-clauson — Doug Clauson (AWS), Ship More as a Team of One with Kiro Crew, AIE CODE 2026
[32] https://arxiv.org/abs/2610.17471 — Cohere authors (arXiv 2610.17471), Scaling Inference-Time Compute with Teams of Coding Agents
[33] https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop — Anthropic, When to fold subagents into your main agent loop
[34] https://x.com/latentspacepod/status/2117721636195663898 — Latent Space, Zach Lloyd (Warp) on software factories, 3 Nov 2026
[35] https://ai.engineer/code/2026/talks/philipp-schmid — Philipp Schmid (Google DeepMind), I deleted 90% of my harness (And It Got Better), AIE CODE 2026
[36] https://github.com/anthropics/claude-code/releases/tag/v2.1.323 — Anthropic, Claude Code release v2.1.323 (Code Mode)
[37] https://simonwillison.net/2026/Oct/3/default-hard-budget-caps — Simon Willison, Default hard budget caps
[38] https://www.infoq.com/presentations/spotify-ai-codebase-migration-agent — Aleksandar Mitic & Jo Kelly-Fenton (Spotify), Rewriting All of Spotify's Code Base, All the Time, QCon London 2026
