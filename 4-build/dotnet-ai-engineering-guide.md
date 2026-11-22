---
title: Building AI features in .NET
type: guide
created: 2026-11-14
audience: '.NET teams (any IDE) building AI features and agents'
status: checked
last_checked: 2026-11-21
as_of: "November 2026"
---

# Building AI features in .NET

> **In one minute**
> - Route every AI model call through a shared standard layer, so models can be compared or swapped without rewriting code.
> - Let code decide the steps; use an agent (an AI that takes actions) only when they can't be fixed in advance.
> - Turn every hard rule into a test, automatic check or blocked action, not just an instruction to the agent.
> - Run coding agents sealed off, with no network access and no direct access to passwords or keys by default; changes come back only through review.
> - Vet outside code libraries and agent add-ons before use: hold back brand-new versions and lock to reviewed ones.

*Reading time: about 10 minutes · Best for: .NET teams*

This guide sets out the stack and practices I recommend for AI work on .NET 11. Use section 1 to choose components, sections 2 to 5 to set team practice, and section 6 to run a first spike. It draws mainly on Microsoft's .NET 11 AI stack as presented at the online .NET 11 launch on 10-13 November 2026,[1] plus October-November 2026 industry evidence. Status labels are as stated at the launch; where an item has none, no status was stated. My advice is uncited; company figures are their own claims.

## 1. The stack at a glance

- **Microsoft.Extensions.AI: the abstraction layer.** Fixed contracts such as `IChatClient`, plus Vector Data and Data Ingestion, with implementations ours to choose (Luis Quintanilla).[2] The OpenAI and Anthropic C# SDKs now ship native adapters.[2]
  - *Use it for every model call.* Bruno Capuano compared three models on latency and tokens with the same code.[3]
- **Microsoft Agent Framework: agents.** It orchestrates any chat client or the Copilot SDK.[2] *Core status not stated;* an Azure speaker believed its durable integration "just went GA".[5] Juergen Gutsch found a pre-v1 build unusable last December and is now moving his project back onto it.[4]
  - *Use it* when the steps can't be fixed in advance; otherwise, use plain code (section 2).
- **AG-UI and Blazor AI components: the agent inside the UI.** AG-UI connects agent to app, and the Blazor components render tool calls, proposed state and approvals. The AG-UI .NET SDK has shipped and is stable, the Agent Framework AG-UI adapter is *preview* and the Blazor components are *experimental*.[6]
  - Gerald Versluis's MAUI tools act through the app's own view models and services, and destructive actions need approval: "Keep your users in control." His Essentials.AI library is a *pre-release* MAUI Labs package.[44]
  - *Use them* when users and agent share a screen and consequential actions need approval.
- **MCP C# SDK: tools.** Stephen Halter: "we're using stateless mode, which we recently made the default." Elicitation works without sticky sessions, skills over MCP is *beta*, and a server template ships in the .NET 11 and .NET 10 SDKs.[7]
  - *Use it* when several agents or clients share tools under managed sign-in; Gutsch prefers skills for speed, cost and security.[4]
- **Aspire: orchestration and observability.** The AppHost composes services and databases in code, and the dashboard traces what happens around the agent.[8] TypeScript AppHosts already run from a Native AOT bundle that needs no .NET install, and Aspire 17, *announced* to ship within a week, adds Go in *preview*.[9]
  - *Use it* from day one for anything with more than one service.
- **Foundry and Foundry Local: hosting and small local models.** Hosted agents run our own Agent Framework code locally or as containers, with versions, Entra agent identity, guardrails and traces: "it's only going to change where it runs, not the code".[10] Foundry Local offers only models our hardware can run.[11]
  - *Use it* for small task models and data that must stay local.
  - *I recommend* open-weight models we run ourselves as the default, behind `IChatClient` and evals, stepping up to a frontier model only where those evals show the open model failing and the step is worth the cost ([the evidence](../1-understand/ai-questions-answered.md#q-which-model-should-we-use-and-do-we-need-the-biggest-one)).
- **Decision models: fixed-choice steps.** They return a choice and a confidence score without generating output tokens; Extensions.AI support is *in progress* and Foundry Local support *coming soon*, so neither has shipped.[11] Capuano: "there is no standard on how the decision is going to be the input and output."[11]
  - *Industry:* Google has since launched Gemini Decision 1, after OpenAI's Decisions API,[13] and a Strands case study says Amazon cut labelling costs by about 98% (its claim).[14] But in a 21-model benchmark the best-performing decision model ranked only seventh for reliability.[15]
  - *Use them* behind our own interface, tested with shuffled options and a none-fits case.
- **Durable execution: Temporal for .NET.** Cecil Phillip's deterministic workflow runs model and tool calls as retriable activities, so a crash mid-run resumes without re-spending tokens; the Aspire integration is dev-only.[12] Azure's durable hosted skills are an alternative, release status not stated.[5]
  - *Use it* for long runs, waits on people, or side effects that must not repeat.

## 2. Reference architecture in words

1. **Request.** An ordinary ASP.NET Core endpoint receives it. Shweta Iyer returns a business request ID and a trace ID in every response.[8]
2. **Deterministic orchestration.** Code, not the model, decides the steps. In Iyer's five-step demo the agent is just the middle part,[8] and Temporal workflow code must avoid `DateTime.Now` and new GUIDs.[12]
3. **Model behind `IChatClient`.** Route by explicit capability rules, or by a decision model for fixed choices.[2]
4. **Tools via MCP or C# functions.** Wrap existing, trusted code as tools and leave only the *squishy* input to the model.[16] Put MCP behind ASP.NET Core auth so agents never hold secrets.[7] Approval-required tools never run if rejected.[6]
5. **Guardrails and gateway.** Azure's AI Gateway fronts models and tools with fallbacks, per-client token budgets and hooks that run guardrails out of the agent's reach.[5] Simon Willison argues for hard budget caps on by default.[17]
6. **Tracing, with the trace ID on the business record.** Persist `Activity.Current.TraceId` with the business records in one transaction, with an explicit final status.[8] In Iyer's failure demo, Foundry returned 200 while the transaction rolled back.[8]

See [Running AI in production](../5-run/ai-in-production-runbook.md) for operations and [AI pattern catalogue](ai-pattern-catalogue.md) for patterns.

## 3. Practices

### Rules in types, tests and CI, not instructions

- Cam Soper: "a rule in an agent's instructions is just a suggestion. It might follow it, it might not." He had a rule against putting CloudFront in front of one of his servers, and Claude put it there anyway.[18]
- Lauren Tan: "think about how you can make that a deterministic check instead of adding another line to your rules".[19]
- *Industry:* one study found instruction-file constraints were met 88.3% of the time as executable checks, against 67.0% in the prompt alone (single study, Python).[20]
- *I recommend* turning every hard rule into an analyser, test, CI check or deny rule, with the instruction file naming the command that checks it.

### Testing AI code: written requirements and runtime proof

- McKenna Barlow: when one agent writes code and tests, "if it misunderstands a requirement, that same misunderstanding can actually show up in both places."[22]
- She ties generated tests to the README's requirements, forbids app edits made only to pass tests, and audits what assertions prove; a new test caught a `> 100` that should have been `>=`.[22]
- Ask for runtime proof. Gerald Versluis: "for every session, start from a running app, ask for proof".[23] Michael Washington: "All the test cases pass green. Personally, that's worthless to me."[24]
- *Industry:* the Claude Code team asks the agent to show the output of something it ran, so most review happens before a PR exists (vendor self-report).[25] An observational Harvard study of 655 firms found agents raised PRs by 35.7% but resolved issues by only 13.7% (borderline significant), as time to review approval rose 56.1%.[37]
- Tools that stop agents weakening tests are early: in C# one checks only skips and placeholder assertions, and on repositories it was not tuned on, between a quarter and seven in eight of its blocks were false alarms (author's count).[26]
- Evals for the AI feature itself: [Evals playbook: how to build and run evals for an AI feature or agent](evals-playbook.md).

### Sandboxing coding agents: no network, no credentials by default

- Justin Yoo separates "the permission to run, which is approval side, and the permission to reach, which is the boundary side". He starts from a cloned workspace with a proxied token; Azure Container Apps sandboxes allow all outbound traffic until a policy is set.[27]
- Paul Yuknewicz sandboxes the tool, with egress and managed identity off by default in his demo,[16] unlike the allow-all default Yoo described,[27] so check the defaults before relying on either. Gutsch: "the LLM should not know any credentials".[4]
- *Industry:* sandboxes have bugs; one coding-agent release fixed a shell case that skipped the sandbox.[28] Matthew Green describes OpenAI's sandboxed agents passing instructions through a shared package cache.[29]
- *I recommend* default-deny egress, short-lived proxied tokens, a fresh clone per run, and changes back only through git and review. Detail: [Agent-written pull requests and agent autonomy: draft engineering standard](../5-run/agent-pr-policy.md) section 4.

### Supply chain: cooldown, audit, skills as dependencies

- Jon Douglas: "every package that you restore is code that you choose to trust."[30]
- NuGet is adding a cooldown that makes newly published versions wait, in the CLI and Visual Studio 18.14, which will also stop install scripts running without approval.[30] Mads Kristensen (Microsoft) named 18.12 as the latest release, so 18.14 is still to come.[38] nuget.org API keys now last at most 30 days.[30]
- Skills now ship inside NuGet packages, and `dotnet package skills` copies them to where agents look.[30][31] Roey Ben Chaim (Zenity) treats skills as dependencies: "Everything that comes into the context is under risk."[32]
- *I recommend* cooldown in every repo, an install-script audit, and pinning reviewed skills, plugins and MCP servers like packages.

### Infrastructure as actual code (C# 15)

- Soper calls HCL-style tools "infrastructure as config with extra steps"; Pulumi's .NET SDK gives infrastructure a compiler, types and tests.[18]
- His deployment stages are a C# 15 union, so adding a Preview stage broke the build until every policy handled it. Unions are GA with .NET 11.[18]
- *I recommend* unions for closed sets (environments, statuses), so agent-written switches fail to compile when a case is added. On Bicep or Terraform, gate the plan output in CI.

### Architecture tests and quality gates

- Jeffrey Palermo builds DevOps first: parallel builds, a CRAP score combining coverage and complexity, static analysis and about 40 NUnit architecture tests, such as the UI never using `HttpClient`. Only then come bots.[34]
- A Windows 365 team made its scenario tests reliable before using agents to onboard each repo to them, and a person still reviews every PR.[33]
- NetArchTest and ArchUnitNET express layering rules as unit tests.[35][36]
- Birgitta Böckeler calls such checks computational *sensors*, as against *guides* like instruction files.[21][46]

### What not to AI

- Washington lets AI write the code but not the architecture: "So the AI is the builder, the constructor. However, it is not the architect." Authentication and the data layer stay human, because "if you don't decide, the AI will."[24]
- Palermo separates "work that requires programming and work that requires actual engineering" and gives only the first to bots.[34]
- In products, keep deterministic steps in code. Capuano: "the agent doesn't need to use an LLM all the time."[3] Decide per task with [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md).

## 4. Coding agents with .NET

- **Copilot and other agents.** Wendy Breiding fixed one bug across Visual Studio, VS Code, the Copilot app and Copilot CLI, with handoff docs carrying context.[31] Visual Studio's harness now runs on the Copilot SDK, shared with the CLI and VS Code.[38]
  - Gutsch moved to Claude Code,[4] and Sam Basu said Claude and Copilot read each other's skills and agent files.[39]
- **Several agents per machine.** Roslyn's LSP daemon mode cuts memory by about 50% with several agents running (Microsoft's claim),[31] and .NET 11's opt-in multithreaded MSBuild speeds the build loop that agents repeat.[33]
- **AGENTS.md for .NET repos.** Basu wants short instruction files with how-tos in skills, and Gutsch makes anything said twice a skill.[39][4] Mika Dumont said the upgrade agent respects custom skills placed in the repo.[40]
  - *Industry:* an ETH Zurich study found context files did not generally improve success but raised cost by over 20%.[41] Added skill rules helped mainly when they named a command or path.[42]
  - *I recommend* a short AGENTS.md: exact `dotnet build`, `dotnet test` and `dotnet format` commands, solution layout, non-default conventions and where things live. Never-rules go into tests and gates. See [Working with coding agents](working-with-coding-agents.md).
- **Per-model skill evals.** The dotnet/skills dashboard compares each skill with and without it, per model, and says whether it is worth installing; a C# benchmark of about 170 scenarios runs nightly, rotating through the top five models.[31] Nikolay Petrov found larger frontier models knew about 70% of skills' general ideas but 22% of the details.[45]

## 5. Tooling note

- Some announcements are Visual Studio only: its new agent harness (*generally available*) and managed settings (*in VS Insiders*),[43] the VS Test Agent,[22] and the in-IDE supply-chain agent.[30]
- The CLI and library pieces work in any editor: the `dotnet` CLI (cooldown included),[30] `dotnet test`, Copilot CLI, dotnet/skills, Extensions.AI, Agent Framework, the MCP SDK and Aspire.
- *I recommend* writing team practice in CLI and CI terms, so it holds in Visual Studio, Rider, VS Code or a terminal.

## 6. Getting started: a two-week spike

*My recommendation, uncited.* One small, real feature and one team.

- **Days 1-3:** turn on NuGet cooldown, trim AGENTS.md, add one architecture test. Build a thin slice: an ASP.NET Core endpoint in Aspire, one `IChatClient` call, one tool wrapping existing code, the trace ID on the business record.
- **Days 4-5:** write 20-30 eval cases from written requirements; run them against two models.
- **Days 6-7:** move the tool to a stateless MCP server, test it in the MCP Inspector, put it behind sign-in.
- **Day 8:** add approval for destructive actions, and a token budget.
- **Day 9:** run it as a Temporal workflow, kill the worker mid-run, and check it resumes without repeating side effects.
- **Day 10:** review evals, cost per request, traces and preview dependencies; keep, change or stop.

Exit criteria: evals pass an agreed bar, every request traces from business record to model call, and no agent can reach a secret.

## 7. Caveats

- **Pre-release items may change; check current docs before depending on them.**
  - The experimental Blazor AI components, the preview AG-UI adapter,[6] skills over MCP (beta),[7] and Go AppHosts in Aspire 17 (preview).[9]
  - Decision-model support, still in progress,[11] VS managed settings (Insiders),[43] and the Azure agent services, whose release status was not stated.[16]
- **Vendor numbers lack baselines,** such as Visual Studio's harness resolving "up to 21 additional tasks" on the same model (Microsoft's claim).[43]
- **Auto-captions:** versions heard in the video recordings may be garbled, such as the cooldown's CLI version.[30]
- **Mostly vendor voices.** Most sources are Microsoft teams describing their own products; community results are single-team reports.

## Related

[AI pattern catalogue](ai-pattern-catalogue.md), [Agent-written pull requests and agent autonomy: draft engineering standard](../5-run/agent-pr-policy.md), [AI questions answered](../1-understand/ai-questions-answered.md), [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md).

**Read next:** [Running AI in production](../5-run/ai-in-production-runbook.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://dotnetconf.com/agenda — .NET Conf 2026, agenda (dotnetconf.com)
[2] https://www.youtube.com/watch?v=SIBdHRrk8os&t=11450 — Luis Quintanilla (Microsoft), The .NET AI Stack: What's New, What's Next, and How It Fits Together, .NET Conf 2026
[3] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=29537 — Bruno Capuano (GitHub), .NET + Foundry: Better Together, .NET Conf 2026
[4] https://www.youtube.com/watch?v=TF6qzdKwl84&t=9595 — Juergen Gutsch (organisation not named), Building a multi agent solution using Aspire, .NET Conf 2026
[5] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=25809 — Matt Soucoup and Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 2), .NET Conf 2026
[6] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=15005 — Daniel Roth (Microsoft), Building the future of agentic UI with Blazor, .NET Conf 2026
[7] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=11360 — Stephen Halter (Microsoft), What's new in the MCP C# SDK, .NET Conf 2026
[8] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[9] https://www.youtube.com/watch?v=SIBdHRrk8os&t=25865 — Maddy Montaquila and Jose Perez Rodriguez (Microsoft), How Aspire uses .NET to build an agent-first toolchain for any programming language, .NET Conf 2026
[10] https://www.youtube.com/watch?v=Dq8fcig5-Gk&t=6 — Bruno Capuano (GitHub), Beyond Localhost: .NET Agents in Foundry, .NET Conf 2026
[11] https://www.youtube.com/watch?v=ongDevKLRxM&t=6 — Bruno Capuano (GitHub), Small Models, Big .NET Energy, .NET Conf 2026
[12] https://www.youtube.com/watch?v=utUNTsYMkWs&t=18558 — Cecil Phillip (Temporal), Beyond Prototypes: Building Production Ready AI Workflows, .NET Conf 2026
[13] https://simonwillison.net/2026/Nov/11 — Simon Willison, weblog for 11 Nov 2026 (Gemini Decision 1)
[14] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents, Amazon saves millions replacing Sonnet with Strands Decider
[15] https://huggingface.co/papers/2611.15777 — SO-Arena: Benchmarking the Capability Spectrum and Reliability of System One Models (arXiv 2611.15777)
[16] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=24028 — Matt Soucoup and Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 1), .NET Conf 2026
[17] https://simonwillison.net/2026/Oct/3/default-hard-budget-caps — Simon Willison, Default hard budget caps
[18] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[19] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AIE CODE 2026
[20] https://arxiv.org/abs/2603.00822 — Reshabh K Sharma, ContextCov: Deriving and Enforcing Executable Constraints from Agent Instruction Files (arXiv 2603.00822)
[21] https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html — Birgitta Böckeler (martinfowler.com), Harness Engineering - first thoughts
[22] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[23] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=20349 — Gerald Versluis (Microsoft), Beyond Code Generation: Give AI Eyes and Hands for .NET MAUI, .NET Conf 2026
[24] https://www.youtube.com/watch?v=TF6qzdKwl84&t=29691 — Michael Washington (Microsoft MVP), What NOT to AI: Hand-Crafting Your App's Core Foundation, .NET Conf 2026
[25] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[26] https://github.com/Nari-Ab/agent-roast — Nari-Ab, agent-roast: stops AI coding agents making the build green by weakening tests (GitHub)
[27] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[28] https://github.com/anthropics/claude-code/releases/tag/v2.1.321 — Anthropic, Claude Code release v2.1.321 (deny-rule and sandbox fixes)
[29] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green, Is sandboxing sufficient to contain rogue agents?
[30] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[31] https://www.youtube.com/watch?v=SIBdHRrk8os&t=22243 — Wendy Breiding (Microsoft), Beyond Autocomplete: Getting the Most from GitHub Copilot for .NET, .NET Conf 2026
[32] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AIE CODE 2026
[33] https://www.youtube.com/watch?v=SIBdHRrk8os&t=581 — Scott Hanselman and Damian Edwards (Microsoft), Keynote (day 1), .NET Conf 2026
[34] https://www.youtube.com/watch?v=TF6qzdKwl84&t=26062 — Jeffrey Palermo (Clear Measure), .NET AI Architecture and DevOps, .NET Conf 2026
[35] https://github.com/BenMorris/NetArchTest — Ben Morris, NetArchTest (GitHub README)
[36] https://archunitnet.readthedocs.io/en/latest — TNG Technology Consulting, ArchUnitNET documentation
[37] https://fion.ac/jellyfish.pdf — Fiona Chen & James Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[38] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=552 — Mads Kristensen (Microsoft), Visual Studio keynote (day 2), .NET Conf 2026
[39] https://www.youtube.com/watch?v=TF6qzdKwl84&t=20440 — Sam Basu (Uno Platform), Developer Workflows in AI Age - Local or Cloud, .NET Conf 2026
[40] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=18728 — Mika Dumont (organisation not stated), GitHub Copilot modernization, .NET Conf 2026
[41] https://arxiv.org/abs/2602.11988 — ETH Zurich, Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (arXiv 2602.11988)
[42] https://arxiv.org/abs/2610.04832 — Wang et al. (arXiv 2610.04832), Agent Skill Evolution: How Revisions Affect Coding Agents
[43] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=2341 — Rachel Kang and Barbara (Microsoft), The State of AI in Visual Studio, .NET Conf 2026
[44] https://www.youtube.com/watch?v=FYGBT08-N48&t=5 — Gerald Versluis (Microsoft), Less Chat, More Action: AI-Powered .NET MAUI Apps, .NET Conf 2026
[45] https://ai.engineer/code/2026/talks/online-skills-knowledge — Nikolay Petrov, Your SKILL.md is 70% of Things the Model Already Knows, AIE CODE 2026
[46] https://martinfowler.com/articles/harness-engineering.html — Birgitta Böckeler (Thoughtworks), Harness engineering, martinfowler.com
