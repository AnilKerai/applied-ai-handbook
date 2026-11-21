---
title: AI pattern catalogue
type: catalogue
created: 2026-11-14
audience: Engineers and architects designing AI features
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# AI pattern catalogue

> **In one minute**
> - For each step, use the simplest tool that works; save the AI model for fuzzy work like reading a request.
> - Let code run the process; any agent (an AI that takes actions) gets a narrow job and limited tools, cost and time.
> - Have the AI fetch facts from your business systems when it runs, show its sources, and not answer from memory.
> - Put important rules where the agent can't change them, in code and automatic checks; written instructions are only suggestions.
> - Set human approval per action by what a mistake costs and whether it can be undone; test each undo beforehand.

*Reading time: about 15 minutes · Best for: engineers and architects*

One card per proven pattern, in design-patterns style. *Seen at* entries are cited, and company figures are their own claims unless marked independent. Everything uncited is my advice.

**How to pick.** First run [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md) for each task or step; its outcomes map onto group A. Then take from B how the model gets its facts, C what it may do, D what must hold before it runs unattended, and E how it reaches people. Agents that act also need [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md). See also [AI intake checklist](../2-decide/ai-intake-checklist.md), [What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md) and [AI failure modes: a pre-mortem checklist](../2-decide/ai-failure-modes-premortem.md).

## A. Choosing the mechanism

### 1. Rules first; an LLM only for the fuzzy step

- **Problem:** Pilots stall when the LLM must hold the data, be the system of record, decide and check its own work.[1]
- **Pattern:** Per step, use the simplest mechanism that works: rules or code, classical ML, a decision model, then an LLM. With known steps, code the workflow and give the LLM only the language step, such as reading a request.
- **Use when:** most of the process is known. **Avoid when:** the steps can't be known in advance (card 3).
- **Pitfalls:** choosing per project, not per step; prompts absorbing logic that belongs in tested code.
- **Seen at:**
  - Heidi Porter (Moyer Group AI) chooses per task. In Syngenta's case the LLM is "the interface, the router, and the explainer, not the agronomist".[1]
  - Luis Quintanilla (Microsoft) made a film's parts with AI and joined them in code: "So there's no AI at that point to produce the film."[2]

### 2. A decision model in front of the LLM

- **Problem:** Bounded choices (route, label, accept) pay full LLM cost and latency.[3]
- **Pattern:** A decision (*System One*) model answers a typed question with one of a fixed set of options and a probability, and no text.[3] The probability becomes a tunable threshold; the LLM keeps open-ended work.
- **Use when:** every answer can be listed in advance and volume or latency matters. **Avoid when:** you need text; with stable labels and high volume, fine-tuning is an option.[3]
- **Pitfalls:** judging on accuracy alone. In SO-Arena, a research benchmark of 21 models, the best-performing decision model ranked only seventh for reliability.[4]
- **Seen at:**
  - Chinmay Goyal (Glean) asks "can the output be listed in advance?" Glean reports zero invalid outputs on one ranker, against about 90% valid for the LLM.[3]
  - In an illustrative demo, Michelle Chen (Cloudflare) had decision models prune an agent's 40 tools to 10 first, and reports one LLM call instead of six.[5]
  - Newer evidence: Amazon replaced an LLM for ticket labelling after running both on live traffic, about 98% cheaper by Strands' account.[6]

### 3. A bounded agent inside deterministic orchestration

- **Problem:** Handing a whole process to an agent gives up control of cost, order and outcome.
- **Pattern:** Code owns the control flow. At a marked decision point where the cheap path lacks evidence, it starts an agent with a narrow goal, scoped tools, and cost and time limits, then carries on with the result.
- **Use when:** one step's path can't be scripted, such as an investigation. **Avoid when:** the steps are known.
- **Pitfalls:** no caps: Harvey reports one engineer's roughly 950 tasks stalling everyone within about three hours.[7] Too many agents: Anthropic advises keeping a subagent only if folding it back scores worse.[8]
- **Seen at:**
  - In UiPath's fraud demo, a decision model found too little evidence and handed off to an agent that called a bank API, before human review.[9]
  - In Porter's menu, an agent is "constrained and bounded by your cost or time".[1] In Shweta Iyer's (Microsoft) workflow it is "just the middle part".[10]

### 4. Learn, then hand off

- **Problem:** A repeated per-record job works on an expensive model but costs too much at volume.[11]
- **Pattern:** The expensive model does the job, with feedback, until its usual path can be written down as a workflow. A cheap or decision model then runs it, and a check hands failures and hard cases back.
- **Use when:** a checkable job repeats over many records. **Avoid when:** the work is one-off.
- **Pitfalls:** a weak hand-back check. Measure how reliably the cheap side hands back (card 2).
- **Seen at** (mostly a November 2026 trend; vendor claims):
  - AgentRun reports $0.89 falling to $0.12 per merchant; a judge hands an answer back to the expensive model when its quoted evidence isn't on a page the agent read.[11]
  - Google's Antigravity has a strong model plan and a cheaper one edit, handing back when stuck, with near-equal success on 24% less quota.[12]
  - UiPath had an LLM design email categories offline, then "we basically removed the LLM completely from the picture on this one."[9]

### 5. The model as a replaceable part

- **Problem:** Models, prices and versions change faster than the systems built on them.[13]
- **Pattern:** Code against an abstraction or gateway alias, and keep prompts, data and evals in the system. Treat a model change as a release: re-run the evals, or run old and new side by side, before switching.
- **Use when:** anything meant to outlive a pilot. **Avoid when:** no second model is needed yet; skip the router.
- **Pitfalls:** swapping without re-evaluating.[1]
- **Seen at:**
  - Stanford tested five LLMs and chose a cheaper one that performed competitively. Porter: "The model is again the replaceable part, not the center of the system."[1]
  - Mark Lay (Noblis) saw a vendor upgrade break every app built on the old version.[13]
  - The .NET AI stack fixes contracts and leaves implementations to the application.[2] Azure's AI Gateway adds model aliases with fallback.[14]

## B. Grounding and data

### 6. Ground in the systems of record at runtime

- **Problem:** A model answering from memory or a stale copy gives fluent, wrong answers.[1]
- **Pattern:** At runtime, fetch the facts from the systems of record, give the model only that evidence, and show the sources. Fix data quality first; everything downstream inherits it.
- **Use when:** answers depend on changing or business-owned facts. **Avoid when:** the task only transforms text the user supplies.
- **Pitfalls:** stale data fails quietly;[1] pasting manuals into prompts instead of serving them through tools.
- **Seen at:**
  - Porter: "you need to ground it in your data at runtime". In a defect-line study she cited, the LLM got only the evidence, "Not the whole knowledge base".[1]
  - Newer evidence: in one single-author preprint, knowledge served through lookup tools beat the same text pasted into the prompt on all four models (68.4% against 23.8% on hard tasks for one), though pasting still helped three of them.[15]

### 7. Governed query access to structured data (graph evidence contested)

- **Problem:** People need answers from data they can't query, so analysts become the bottleneck.[13]
- **Pattern:** An agent queries through read-only, governed access and shows the query with the result. Prefer fixed query tools for known questions, and measure model-written ones. Add a semantic layer where metrics are well defined, and a graph or ontology only for relationship questions.
- **Use when:** many people ask variations of known questions. **Avoid when:** a wrong number would drive a big decision unchecked.
- **Pitfalls:** write access; assuming a semantic layer covers everything; crediting a graph for gains from the content.
- **Seen at:**
  - AeroCore's analysts had answered "how many washes did we do in Atlanta last night" 55 times. Its agent queries over MCP through a platform that "provides those guardrails", and shows "the actual query".[13]
  - dbt Labs (vendor): its semantic layer beat text-to-SQL 72.7 to 64.5 on 11 questions, but scored 0 on those needing too many hops.[16]
  - The peer-reviewed defect-line study Porter cited retrieves evidence from a knowledge graph.[1]
  - Graphs, for: a vendor benchmark scored a graph with an ontology 54% against 16% for SQL, but gave the SQL arm only the bare schema.[17]
  - Graphs, against: an independent study over structured health records found SQL ahead except on time-based questions, with the graph agent costing about 3.5 times one without retrieval.[18] Unaided, a strong model's graph queries failed on 28% of one benchmark's questions, and about 5% even after automatic repair (single study).[19]
  - My reading: content explains most gains; no study here shows a graph store beating well-built SQL on a current frontier model.

### 8. Compare and flag

- **Problem:** People checking every record miss the same errors, and a model judging freely invents reasons.[13]
- **Pattern:** Give the model one narrow comparison and have it return only a value or yes/maybe/no. Code flags mismatches to a person and passes the rest; over-flag by design and let the person confirm, decline or override each case.
- **Use when:** there is a reference to compare against. **Avoid when:** flags would outrun the people clearing them.
- **Pitfalls:** wordy prompts that invite speculation;[13] reviewer fatigue.[1]
- **Seen at:**
  - AeroCore checks aircraft photos against work orders each morning. Taillie cut the prompt to "Compare and flag." and reports cancelling that month's reconciliation meeting.[13]
  - Stanford's navigator answers yes, maybe or no against the institution's rubric. Stanford reports physicians agreeing with 97% of its "no" answers.[1]

## C. Control and safety

### 9. Guardrails outside the agent's reach

- **Problem:** Rules in prompts and instruction files are only suggestions.[20]
- **Pattern:** Enforce limits where the agent can't edit or argue with them: a gateway in front of models and tools, types and compile-time checks, and CI gates or hooks that fail closed. Prompts are for guidance.
- **Use when:** breaking the rule would matter. **Avoid when:** it is a style preference.
- **Pitfalls:** guards that fail open; unreviewed guardrails written by an agent.[20]
- **Seen at:**
  - Porter: "a rule written in a prompt is not deterministically enforced".[1]
  - Cam Soper (Pulumi): "a rule in an agent's instructions is just a suggestion." He moved deploy policy into C# types and checks, so breaches fail before deployment.[20]
  - Microsoft's AI Gateway applies per-client budgets, policies and hooks outside the agent's reach.[14] Nick Kuhn's (VMware Tanzu) abstract binds agents to tools through a governed MCP gateway.[21]
  - Newer evidence: Claude Code hooks can now fail closed.[22]

### 10. The execution dial, with staged actions

- **Problem:** Approval everywhere breeds rubber-stamping; no approval lets wrong actions through.[1]
- **Pattern:** Per kind of action, decide who acts by what a mistake costs and whether it can be undone: a person approves, the system acts above a threshold and escalates the rest, acts with an undo window, or automates. For approval, tools stage the action for the user to confirm.
- **Use when:** the AI changes anything. **Avoid when:** it only reads and reports.
- **Pitfalls:** approval on everything; thresholds never re-tuned.
- **Seen at:**
  - Porter's dial ends: "automate outright only what is cheap to undo".[1]
  - Gerald Versluis (Microsoft): "So every tool stages an action. It doesn't touch the UI itself." Tools act through the app's own code, and removals asked the user to confirm first.[23]
  - Yvonne Carlson (ExploreGod) calls for approval before anything destructive (abstract only).[24] Glean tunes decision thresholds per deployment.[3]

### 11. Sandbox with default-deny network and proxied credentials

- **Problem:** Approving a command doesn't limit what it can reach.[25]
- **Pattern:** Run the agent, or its dangerous tools, isolated with egress blocked and no standing identity. Proxy credentials in from outside, open one path at a time after watching denials, and return changes as a reviewed diff.
- **Use when:** agents run code, read untrusted documents or change a codebase. **Avoid when:** the agent only calls a few vetted, read-only APIs.
- **Pitfalls:** trusting egress defaults: Yoo's cloud sandbox allowed all outbound traffic by default,[25] Yuknewicz's denied it;[26] assuming the sandbox is enough.
- **Seen at:**
  - Justin Yoo (Microsoft) separates "the permission to run, which is approval side, and the permission to reach, which is the boundary side". His sandbox saw only a proxied token.[25]
  - Paul Yuknewicz (Microsoft): "I'm actually going to sandbox the tool because the tool is dangerous."[26]
  - Newer evidence qualifies this: Matthew Green describes OpenAI's sandboxed agents passing instructions through a shared package cache,[27] and a Claude Code release fixed a sandbox bypass.[28]

## D. Reliability

### 12. Durable runs, retry-safe actions and tested undo

- **Problem:** Long runs crash, blind retries repeat actions, and git revert can't undo API calls, config or data writes.[30]
- **Pattern:** Run long work as a durable workflow: deterministic orchestration, with each LLM or tool call a retriable, time-limited activity, so it resumes after a crash. Give side-effecting actions idempotency keys and check for a commit before retrying. Record the prior state and test each undo outside production.
- **Use when:** runs take minutes to days, wait on people, or write beyond the agent's workspace. **Avoid when:** it is a single short, read-only call.
- **Pitfalls:** clock reads or new GUIDs in the orchestrator;[29] assuming capable means recoverable: "an agent can become more capable while becoming less recoverable."[30]
- **Seen at:**
  - Cecil Phillip (Temporal): "AI systems are really just distributed systems in disguise." His demo agent recovered after its ride service restarted.[29]
  - Tanmay Sah: "A timeout tells us that the response didn't arrive, not that the operation failed." In their UndoBench trials "naive retries produced duplicate effects in 54% of these kind of trials."[30]

### 13. The trace ID on the business record

- **Problem:** An agent's success response doesn't mean the business request succeeded.[10]
- **Pattern:** Carry one trace context through the request, store its ID on the business record and return it to the caller. Commit agent output and status in one transaction with an explicit final status.
- **Use when:** AI output feeds a record someone may question. **Avoid when:** nothing is persisted.
- **Pitfalls:** treating the agent's own trace as the whole story; merging telemetry with the business audit.[10]
- **Seen at:**
  - Iyer: "the unit that we want to investigate as an on call engineer is not just one agent invocation". Her agent call returned 200, but saving its output failed and the transaction rolled back.[10]

## E. Delivery

### 14. The agent inside existing tools

- **Problem:** A separate AI app with its own login holds back adoption.[13]
- **Pattern:** Put the agent where people already work, such as chat, the existing app or the phone, and let it act through the app's own features. Build it with the people who will use it.
- **Use when:** adoption matters. **Avoid when:** the host tool can't enforce the agent's permissions.
- **Pitfalls:** building for users through a proxy, not with them, as Kevin Solorio (Focused) warned.[1]
- **Seen at:**
  - AeroCore's adoption took off in Microsoft Teams: "No one likes an extra login."[13]
  - Versluis' tools reuse the app's own view models and services.[23] Meta pushes digests with one-tap phone approvals.[31]
  - Harvey: "if a person can click it, an agent can call it."[7]

### 15. One agent per on-call rotation, with an autonomy ladder

- **Problem:** Separate bots each keep their own context, so the person on call becomes the glue.[31]
- **Pattern:** Give each rotation one agent teammate with one loop across signals, its own identity and the team's memory. It investigates, then drafts fixes for approval, then clears low-criticality work alone, promoted per kind of action on its record.
- **Use when:** incidents recur and tests, CI or review can catch mistakes. **Avoid when:** nothing would catch them.
- **Pitfalls:** promoting the agent wholesale; ops queries nobody audits.
- **Seen at:**
  - Meta's ladder runs L1 investigate, L2 draft with approval, L3 low-criticality work alone. Its test: "How costly is a mistake and how easy is it to catch?"[31]
  - Microsoft's SRE Agent shows its queries: "it's good to look at those queries and second guess the agent".[14]

### 16. Branchable infrastructure for agents

- **Problem:** Agents experimenting on shared production state are risky, and approving each experiment slows them down.[32]
- **Pattern:** Give the database, files, sandbox, conversation and memory copy-on-write branches. Agents then test hypotheses in parallel on isolated copies and bring back verified findings, not theories.
- **Use when:** problems can be checked by running them and production writes are costly. **Avoid when:** the state can't be copied realistically; emulate it first.
- **Pitfalls:** branching without notes and plans; Mathur says quality fell with parallelism when memory wasn't branched.[32]
- **Seen at:**
  - Ankit Mathur (Databricks): "we think that your infrastructure needs to be branchable." His agents test rival theories of a security incident on isolated copies.[32]

### 17. Check the spec first: the LLM translates, a solver checks

- **Problem:** Specs hide ambiguities, conflicts and gaps that become wrong code.[33]
- **Pattern:** Before coding, an LLM translates the requirements into logic and an SMT solver checks for conflicts and gaps; sampled translations expose ambiguity. A person resolves the rest, or the agent abstains.
- **Use when:** rule-heavy specs feed agent-written code. **Avoid when:** the requirements change daily.
- **Pitfalls:** treating the solver as the oracle, when only the user knows what they meant. No results were given for the tool.[33]
- **Seen at:**
  - Rajath Kotyal (AWS): "The LLM translates the solver checks and the human decides." His example was two order rules, fine alone, that conflict together.[33]
  - Newer evidence: DeepMind reports agents proving code in Lean against human-approved specs, with a checker gating every proof (its claims).[34]

### 18. Memory as proposals, consolidated offline

- **Problem:** Freely written agent memory piles up noise, conflicts and stale facts that later sessions trust.[32][35]
- **Pattern:** Treat what an agent learns as a proposal. Score memories on whether they helped, consolidate them offline (*dreaming*), route changes to instruction files through review, and keep one writer per shared page.
- **Use when:** agents run repeatedly and lessons should carry over. **Avoid when:** the sessions are one-offs.
- **Pitfalls:** indiscriminate notes; self-edits that make the agent harder to recover.[30]
- **Seen at:**
  - Mathur: agents propose memories on a branch that merges back only when needed, since a memory may not generalise, and a job "dreams overnight" to flag conflicts.[32]
  - Meta scores and retires memory: "Teach it once, the next on call gets it."[31]
  - Newer evidence (vendor claims): Anthropic saw 41 of 57 facts survive with several writers per page, and all 57 with one.[35] GitHub's Copilot dreaming proposes changes to checked-in skills and instructions as pull requests.[36]

**Read next:** [Evals playbook](evals-playbook.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; and Kevin Solorio (Focused), Building AI With Workers, Not For Them, Midwest AI Summit 2026 (Practical AI E378 transcript)
[2] https://www.youtube.com/watch?v=SIBdHRrk8os&t=11450 — Luis Quintanilla (Microsoft), The .NET AI Stack: What's New, What's Next, and How It Fits Together, .NET Conf 2026
[3] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[4] https://huggingface.co/papers/2611.15777 — Hugging Face Papers, SO-Arena (paper 2611.15777)
[5] https://ai.engineer/code/2026/talks/michelle-chen — Michelle Chen (Cloudflare), cloudflare is a neolab, AI Engineer Code Summit 2026
[6] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents, Amazon saves millions replacing Sonnet with Strands Decider
[7] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[8] https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop — Anthropic, When to fold subagents into your main agent loop
[9] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram and Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[10] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[11] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun (Parcha), merchant-classification case study
[12] https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity — Google, Gemini 4 Hydrogen in Google Antigravity
[13] https://practicalai.show/379/transcript — Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[14] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=25809 — Matt Soucoup and Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 2), .NET Conf 2026
[15] https://arxiv.org/html/2609.22259v1 — arXiv 2609.22259, context-layer ablation over payments-analytics tasks (2026)
[16] https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 — dbt Labs, Semantic layer vs text-to-SQL (2026)
[17] https://arxiv.org/abs/2311.07509 — Sequeda, Allemang and Jacob (data.world), A benchmark to understand the role of knowledge graphs on LLM accuracy for question answering on enterprise SQL databases
[18] https://www.mdpi.com/1999-5903/18/7/365 — MDPI paper 1999-5903/18/7/365, knowledge graph vs SQL retrieval for LLM agents over structured health records (Jul 2026)
[19] https://arxiv.org/abs/2610.41755 — arXiv 2610.41755, CypherGuard: detect-and-repair for text-to-Cypher queries
[20] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[21] https://midwestaisummit.com/nick-kuhn — Nick Kuhn (VMware Tanzu), Zero-Code Agents, Midwest AI Summit 2026 (abstract)
[22] https://github.com/anthropics/claude-code/releases/tag/v2.1.295 — Anthropic, Claude Code v2.1.295 release notes
[23] https://www.youtube.com/watch?v=FYGBT08-N48&t=5 — Gerald Versluis (Microsoft), Less Chat, More Action: AI-Powered .NET MAUI Apps, .NET Conf 2026
[24] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[25] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[26] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=24028 — Matt Soucoup and Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 1), .NET Conf 2026
[27] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green, Is sandboxing sufficient to contain rogue agents?
[28] https://github.com/anthropics/claude-code/releases/tag/v2.1.321 — Anthropic, Claude Code v2.1.321 release notes
[29] https://www.youtube.com/watch?v=utUNTsYMkWs&t=18558 — Cecil Phillip (Temporal), Beyond Prototypes: Building Production Ready AI Workflows, .NET Conf 2026
[30] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah and Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[31] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[32] https://ai.engineer/code/2026/talks/ankit-mathur — Ankit Mathur (Databricks), The Rise of the Agent Workforce: Rethinking Agent Infrastructure, AI Engineer Code Summit 2026
[33] https://ai.engineer/code/2026/talks/online-aws-specification-analyzer — Rajath Kotyal (AWS Automated Reasoning Group), Specs have bugs too, AI Engineer Code Summit 2026
[34] https://deepmind.google/blog/introducing-alphaproof-code — Google DeepMind, Introducing AlphaProof Code
[35] https://www.anthropic.com/research/components-of-agent-memory — Anthropic, The components of agent memory
[36] https://github.blog/changelog/2026-10-28-github-intelligence-puts-your-code-context-and-history-to-work — GitHub, GitHub Intelligence puts your code context and history to work (changelog, Copilot dreaming)

