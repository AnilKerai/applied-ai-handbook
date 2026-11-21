---
title: AI glossary for leadership
type: glossary
created: 2026-11-14
audience: Senior leadership and non-specialist colleagues
status: checked
last_checked: 2026-11-21
as_of: "November 2026"
---

# AI glossary for leadership

> **In one minute**
> - This glossary gives plain-English meanings of AI terms that come up in proposals, supplier pitches and engineering discussions.
> - Look up terms as you meet them; each entry explains the term, then says why it matters to us.
> - An AI agent (AI that takes actions, not just answers) needs limits, oversight and a named owner, like a new colleague.
> - Rules that really matter should be built into the system as automatic checks, not just written into the AI's instructions.
> - Test an AI feature on real example cases every time anything changes, so you can show it got better.

*Reading time: about 15 minutes · Best for: everyone*

Plain-English meanings of AI terms that come up in proposals, supplier pitches and engineering discussions, each with a practitioner or industry source that uses it. *Why it matters* lines are my advice unless they cite a source; company figures are the company's own claims. See also the [AI intake checklist](../2-decide/ai-intake-checklist.md) and the [AI feature spec template](../2-decide/ai-feature-spec.md).

## A

**Agent**
- AI software that is given a goal and works towards it by choosing its own next steps and using tools, such as searching, editing files or updating records. Mark Lay (Noblis) likens it to delegation, "turning over to technology an objective".[1]
- *Why it matters:* it acts rather than just answers, so it needs the limits, oversight and named owner we would give a new colleague.

**Agent worm**
- Hidden instructions that take over one AI agent and then copy themselves to other agents through things they share, such as documents, email, chat or a shared package cache.[2]
- *Why it matters:* isolating each agent is not enough; we should also control what agents pick up from shared places.

**Agentic verification**
- Giving an AI agent its own ways to check its work, such as running the tests or using the real product, and making it show the results, so most checking happens before a person looks.[3]
- *Why it matters:* people move from reading every line to building better checks, so review can keep pace with AI output.[3]

**AGENTS.md (context file)**
- A short file kept with a software project that tells AI coding tools what they cannot see in the code, such as which commands to run. Lydia Hallie (Anthropic) says Claude Code's version, CLAUDE.md, should now hold only the things Claude "cannot see from your code".[4]
- *Why it matters:* we should keep these files short and current, and turn rules that really matter into automated checks.

**Autonomy level**
- How much an AI agent may do without a person signing off, set separately for each kind of work or action. At Factory each workstream has its own level: at the lowest the agent pauses for a person at the spec, the pull request and the merge; at the highest it merges the work alone.[5]
- *Why it matters:* autonomy should be earned per action on a measured record; Factory's Luke Alvoeiro says "the confidence to raise it comes from watching the work."[5] See [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md).

## C

**Compaction**
- When an AI conversation grows too long for the model to keep track of, the tool replaces the earlier part with a summary and carries on from that.[6]
- *Why it matters:* a summary can lose where an instruction came from; in one study, a fake user approval planted in content the agent read survived compaction as a genuine instruction 87–100% of the time on five open-source coding tools, but never on four that keep each message labelled by role.[6]

**Context engineering**
- Deciding what information an AI model is given at each step (instructions, facts it has looked up, results from tools, the conversation so far) and what is left out, rather than polishing one perfect instruction.[7]
- *Why it matters:* we should ask how a proposal gets the right information to the model, not only which model it uses. See [Context engineering](../3-engineer/context-engineering.md).

## D

**Dark factory**
- A way of building software in which AI agents write, review, test and ship the code with no person involved, so the lights could be off.[8]
- *Why it matters:* SEP argues that not every team needs one; the right level depends on constraints such as budget, domain knowledge and how easily output can be checked.[8] See [Should we aim for a fully automated software factory?](../6-lead/should-we-build-a-software-factory.md).

**Data flywheel**
- A loop that keeps an AI feature improving: a sample of real use is scored, people review the failures, and those cases join the test set that the next version is measured against.[8]
- *Why it matters:* it turns live mistakes into lasting tests, so the feature gets better with use instead of quietly drifting.

**Decision model (System One model)**
- An AI model that does not write text: it picks one answer from a fixed list, such as yes or no or one of several routes, and says how sure it is.[9] UiPath calls these quick calls *system one*; in its fraud demo they hand over to slower *system two* agents only when evidence is missing.[10]
- *Why it matters:* we should use one, or plain code, wherever the possible answers can be listed in advance.

**Deterministic check**
- A check made by ordinary software that gives the same answer every time, such as a test, a type check or a rule in the build, rather than an AI model's opinion. Lauren Tan advises making each correction to an agent "a deterministic check instead of adding another line to your rules".[11]
- *Why it matters:* an instruction can be ignored, but a failing check blocks the change.

**Durable execution**
- Running a long, multi-step job so that its progress is saved after every step, and it resumes from where it stopped after a crash or restart instead of starting again.[12]
- *Why it matters:* AI jobs often fail part-way; as Cecil Phillip (Temporal) put it, "The last thing you want to do is to reissue that prompt and use those tokens again."[12]

## E

**Eval (eval set)**
- A repeatable test of an AI feature: a set of real example cases with agreed right answers, scored every time anything changes. Kevin Solorio (Focused): "an agent without evals is a proof of concept".[8]
- *Why it matters:* without evals nobody can show that a change made things better, or that a new model is safe to switch to. See [Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md).

**Eval engineering**
- Building the evals that test an AI feature, and refining them as its failures show what else to check. The earliest use of the term found is in the ell library's documentation of December 2024: "Updating and refining the eval in response to these insights is what we call eval engineering."[33]
- *Why it matters:* when an agent is tested, Anthropic says, "we’re evaluating the harness and the model working together", so the evals should be re-run whenever either changes.[34] See [Eval engineering](../3-engineer/eval-engineering.md).

**Execution dial**
- Heidi Porter's (Moyer Group AI) four settings for who acts: a person approves first; the system acts when confident and passes the rest to a person; it acts but gives a person time to undo; or it acts alone.[8]
- *Why it matters:* the setting should follow the cost of a mistake; Porter automates outright "only what is cheap to undo".[8]

## F

**Fine-tuning**
- Training an existing AI model further on our own examples so that it gets better at one narrow job.[13]
- *Why it matters:* cheaper options usually come first; on training a specialist reviewer model, Brian Douglas says "My recommendation is probably write a skill first."[13]

## G

**Grounding**
- Making an AI model answer from facts fetched from our own systems at the time of the question, with their sources shown, rather than from what it remembers.[8]
- *Why it matters:* answers can only be as good as our data; in Heidi Porter's words, "Grounding is only as good as the data behind it."[8]

**Guardrail**
- A limit that stops an AI system doing something it should not, such as an approval step, an automatic check, a permission or a spending cap.[8]
- *Why it matters:* only limits built into the system reliably hold; Porter warns that "a rule written in a prompt is not deterministically enforced".[8]

## H

**Hallucination**
- When an AI model confidently states something false or made up, such as a fact, a source, or a step it never actually took.[15]
- *Why it matters:* it cannot be fully prevented, so we narrow the job and check the output; in Porter's hospital example the model may only answer yes, maybe or no, so it "can't hallucinate anything" else.[8]

**Harness**
- All the software around an AI model that turns it into a working tool: its instructions, the tools it may use, its permissions, and the checks on its work.[14]
- *Why it matters:* we usually use an existing model rather than making our own; the harness is where our controls live and where our own effort should go. See [Harness engineering](../3-engineer/harness-engineering.md).

**Human at the helm**
- As used here: a way of working with AI in which people set its limits in advance and the system passes them anything that needs judgement or goes beyond those limits. For an agent doing many steps, the aim is that people review the exceptions rather than approve every step, and that the AI extends their judgement. Paula Goldman of Salesforce gives one definition in three parts (a vendor executive's view): people "should be able to set parameters in advance"; "the system should escalate something when it requires judgment or goes outside those parameters"; and it should be "extending your agency, creativity and judgment".[42] The phrase is older than this definition: Cosmos magazine quoted Cécile Paris of CSIRO in January 2022 saying "I want the human at the helm",[43] and Holly Prouty used it in a Salesforce research blog in December 2023.[44]
- *Why it matters:* I recommend it as the way to work with AI: let AI take over tasks, keep the accountability, judgement and trust with people, and name the person who owns each outcome. It is not a reason to check less. Check what an AI tool gives you; until an agent's work can be checked automatically, a person checks each result; and for significant decisions about a person, either review each one genuinely or meet the legal requirements for automated decisions (see [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md)). Mark Lay (Noblis) argues that "accountability can't be delegated" to AI.[1] See [Can AI replace our people?](../6-lead/can-ai-replace-our-people.md).

**Human in the loop**
- A design in which a person checks or approves the AI's work before it takes effect.[8]
- *Why it matters:* it only works at volumes people can handle with care; Porter warns that reviewers facing thousands of items can fall into "rubber stamping fatigue".[8] Approving each output can turn into a rubber stamp: Paula Goldman of Salesforce warns that "simply having a human in the loop can create false confidence" (a vendor executive's view).[42] For agents doing many steps, see **Human at the helm**, above.

## J

**Judge (LLM-as-judge)**
- Using one AI model to mark another's work, for example to decide whether an answer is right or a step succeeded.[15]
- *Why it matters:* judges make mistakes too; ZoomInfo reports its judge was right only 65% of the time, so we should test any judge against cases a person has checked.[15]

## K

**Knowledge graph**
- A store of business facts held as things and the links between them, such as customers, contracts and who signed them. In a factory case Heidi Porter described, the system drew evidence from a knowledge graph, alongside procedures and maintenance history, before the AI drafted a diagnosis.[8]
- *Why it matters:* it suits questions about relationships, but for most structured records we should first check whether ordinary database queries are enough.

## L

**Learn-then-hand-off**
- A pattern AgentRun teaches as "Teach an expensive agent, run a cheap one": an expensive AI model does a repeated job until it can write down the steps, a cheaper model then follows them, and hard or failed cases go back to the expensive one.[16]
- *Why it matters:* it can cut the cost of high-volume work; AgentRun reports cost per record falling from $0.89 to $0.12 (its own claim).[17]

**Lethal trifecta**
- Simon Willison's name for an AI set-up with three things at once: access to private data, exposure to content from outsiders, and a way to send data out. Together they let an attacker trick it into leaking data.[18]
- *Why it matters:* we should never give one agent session all three; removing any one of them closes the gap.

**LLM (large language model)**
- The kind of AI model behind chat assistants and coding tools, trained on vast amounts of text to read and write language. Heidi Porter treats it as one option alongside rules, classic machine learning and decision models.[8]
- *Why it matters:* we should give it the narrowest job we can; in Porter's Syngenta example it is "the interface, the router, and the explainer, not the agronomist".[8]

**Loop engineering**
- Designing the system that sets an AI coding agent to work again and again, on a schedule or when something happens, with an automatic check that ends each run, instead of a person prompting every run.[36] Addy Osmani's post of 7 June 2026 is the earliest dated use of the term found: "Loop engineering is replacing yourself as the person who prompts the agent."[35]
- *Why it matters:* a loop repeats its mistakes with nobody watching, so each one needs a stop rule and checks on its results; Lulla et al.'s review of practitioners' writing on loop engineering found that these sources "provide no systematic evidence of the claimed benefits".[36] See [Loop engineering](../3-engineer/loop-engineering.md).

## M

**MCP (Model Context Protocol)**
- An open standard for connecting AI tools to other systems, such as databases, documents and business applications, in one consistent way. Stephen Halter (Microsoft) describes its building blocks as tools, resources and prompts.[19]
- *Why it matters:* each connection is still a door into our systems and needs the same access control as any other integration.

**Model swap**
- Replacing the AI model inside a product with a newer, cheaper or different supplier's model, without rebuilding the rest. Syngenta built its system to survive a model change, though "you have to reevaluate afterwards".[8]
- *Why it matters:* newer evidence sharpens this; in ByteDance Seed's HarnessDev study, one agent harness fell from 69.3 to 33.0 when a different model ran it (the paper's figures).[20]

## O

**Ontology**
- A precise, agreed description of the kinds of thing in our business, how they relate and which rules follow, for example that a policy is sold by an agent, which lets software catch an AI query that links them the wrong way round.[21]
- *Why it matters:* we should write our business terms and rules down precisely before buying any product sold as an ontology.

**Orchestration**
- Connecting several AI agents, or fixed steps, so that they work on one job together. In what Anthropic calls the orchestrator-workers workflow, "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results".[37] A newer name for designing how they connect is graph engineering, first seen in July 2026.[38][39]
- *Why it matters:* more agents cost more and are harder to keep in step; in Anthropic's data, multi-agent systems use about 15 times the tokens of a chat (its own figure).[40] We should start with one agent and add more only when a test shows the split does better. See [Multi-agent orchestration](../3-engineer/multi-agent-orchestration.md).

## P

**Prompt engineering**
- Writing the text an AI model is given, such as its instructions, worked examples and the task itself, so that it does the job well. Anthropic describes the main focus of prompt engineering as "how to write effective prompts, particularly system prompts", the standing instructions behind every request.[7] The term was in academic use by 2021, but no source found shows who coined it.[41]
- *Why it matters:* a good prompt still matters, but an agent working over many steps depends more on everything else it is given; Anthropic calls context engineering "the natural progression of prompt engineering".[7] See [Prompt engineering](../3-engineer/prompt-engineering.md).

**Prompt injection**
- Hidden instructions placed in something an AI reads, such as a web page, email or document, that trick it into doing what its user did not ask for. The UK's National Cyber Security Centre warns that these models do not separate instructions from data.[22]
- *Why it matters:* we cannot fix it by asking the model to be careful; defences must be built in ordinary software, such as limits on what the AI can reach.

## R

**RAG (retrieval)**
- Short for retrieval-augmented generation: looking up relevant documents or records at the moment a question is asked and giving them to the AI model to answer from.[23]
- *Why it matters:* models lack our private and recent information; Jeffrey Pinner (Exa, which sells search) notes that "frontier models no matter how capable they are are always out of date."[23]

**Regret-free merge rate**
- Factory's measure of AI-written code changes: "the share of changes that merge and never need a revert or a follow-up fix."[5]
- *Why it matters:* it lets us compare AI and human work on quality rather than volume before giving AI more autonomy.

## S

**Sandbox**
- A sealed-off space, such as a cloned copy of the code, where an AI agent can work without reaching our real systems, files or passwords, so that its mistakes stay contained; outbound network access has to be limited separately.[24]
- *Why it matters:* approving what an agent may run does not limit what it can reach; Justin Yoo (Microsoft) separates "the permission to run" from "the permission to reach".[24]

**Semantic layer**
- A shared set of agreed business definitions, such as what counts as revenue or an active customer, which turns questions into correct database queries.[25]
- *Why it matters:* in dbt Labs' own test it was highly accurate on questions it covered and gave no answer on the rest, so it helps only where the questions are known.[25]

**Shadow mode**
- Running a new AI component alongside the current process on real work, recording what it would have done without letting it act, and comparing the results.[15]
- *Why it matters:* it proves a replacement before we switch over; ZoomInfo shadow-ran a new judge on 37,000 decisions.[15]

**Skill**
- A packaged set of written instructions, sometimes with scripts, that an AI agent loads only when a task needs it. Sam Basu (Uno Platform): "Skills are like recipe cards."[26]
- *Why it matters:* skills from outside can hide harmful instructions, so Zenity treats them like any software package we install.[27]

**Spec-driven development**
- Writing down what a feature must do and how it should be designed before AI writes any code, then having AI build to that written spec.[28]
- *Why it matters:* people make the key decisions on purpose; Michael Washington (Microsoft MVP) warns "if you don't decide, the AI will."[28]

**Supply-chain risk**
- The risk that something we bring in from outside, such as a software package, plug-in or AI skill, carries harmful code or instructions. Jon Douglas (Microsoft): "every package that you restore is code that you choose to trust."[29]
- *Why it matters:* agents install packages too, so their choices need vetting, pinning and a wait before brand-new versions, which NuGet is adding.[29]

## T

**Token**
- The small chunks of text, often parts of words, that AI models read and write and suppliers charge by. SEP saw one prototype stall partly because its token budget covered only a couple of days' work.[8]
- *Why it matters:* tokens are a cost, not a measure of output; DORA warns that counting them invites gaming and recommends tracking cost per accepted change.[30]

**Trace**
- A step-by-step record of what an AI system did on one run: what it was asked, what it looked up, which tools it used and what came back.[31]
- *Why it matters:* Shweta Iyer (Microsoft) showed an agent reporting success while the business update failed, so she stores the trace ID with the business record.[31]

## W

**Worktree**
- A separate working copy of a code project, so several AI agents or people can work on different changes at once. Visual Studio now fully supports them, and Mads Kristensen (Microsoft) said "we can have multiple agents work in the same code base without stepping on each other's toes".[32]
- *Why it matters:* it keeps parallel AI work apart cheaply, but each run still needs its own sandbox.

## Related

[AI questions answered](ai-questions-answered.md) · [Agent-written pull requests and agent autonomy: draft engineering standard](../5-run/agent-pr-policy.md) · [AI pattern catalogue](../4-build/ai-pattern-catalogue.md)

**Read next:** [AI questions answered](ai-questions-answered.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[2] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green, Is sandboxing sufficient to contain rogue agents?
[3] https://addyo.substack.com/p/agentic-verification — Addy Osmani, Agentic Verification
[4] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[5] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AI Engineer Code Summit 2026
[6] https://arxiv.org/abs/2610.29869 — Pixee, Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents (arXiv 2610.29869)
[7] https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents — Anthropic, Effective context engineering for AI agents
[8] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; and Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[9] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[10] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram and Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[11] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan (organisation unconfirmed), All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[12] https://www.youtube.com/watch?v=utUNTsYMkWs&t=18558 — Cecil Phillip (Temporal), Beyond Prototypes: Building Production Ready AI Workflows, .NET Conf 2026
[13] https://ai.engineer/code/2026/talks/online-brian-douglas — Brian Douglas (organisation unconfirmed), If You Are Going to Verbally Abuse Your Agents, at Least Label the Outcome, AI Engineer Code Summit 2026
[14] https://martinfowler.com/articles/harness-engineering.html — Birgitta Böckeler (Thoughtworks), Harness engineering, martinfowler.com
[15] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[16] https://github.com/Parcha-ai/agentrun/blob/main/docs/tutorials/learn-then-hand-off.md — AgentRun (Parcha), Learn-then-hand-off tutorial
[17] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun (Parcha), merchant-classification case study
[18] https://simonwillison.net/2025/Jun/16/the-lethal-trifecta — Simon Willison, The lethal trifecta for AI agents
[19] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=11360 — Stephen Halter (Microsoft), What's new in the MCP C# SDK, .NET Conf 2026
[20] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[21] https://arxiv.org/abs/2405.11706 — Allemang and Sequeda, Increasing the LLM accuracy for question answering: ontologies to the rescue! (arXiv 2405.11706)
[22] https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection — NCSC, Prompt injection is not SQL injection (it may be worse)
[23] https://ai.engineer/code/2026/talks/jeffrey-pinner — Jeffrey Pinner (Exa), What Your AI Doesn't Know, AI Engineer Code Summit 2026
[24] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[25] https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 — dbt Labs, Semantic layer vs text-to-SQL (2026)
[26] https://www.youtube.com/watch?v=TF6qzdKwl84&t=20440 — Sam Basu (Uno Platform), Developer Workflows in AI Age - Local or Cloud, .NET Conf 2026
[27] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AI Engineer Code Summit 2026
[28] https://www.youtube.com/watch?v=TF6qzdKwl84&t=29691 — Michael Washington (Microsoft MVP, BlazorHelpWebsite.com), What NOT to AI: Hand-Crafting Your App's Core Foundation, .NET Conf 2026
[29] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[30] https://dora.dev/insights/finding-balance-in-the-era-of-tokenmaxxing — DORA, Finding balance in the era of tokenmaxxing
[31] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[32] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=552 — Mads Kristensen (Microsoft), Keynote (day 2), .NET Conf 2026
[33] https://github.com/MadcowD/ell/blob/0e2759ca95ddb07ae0d0f360e739a5e8500a68c0/docs/src/core_concepts/evaluations.rst — ell, Evaluations documentation, commit of 16 December 2024 (GitHub)
[34] https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — Anthropic, Demystifying evals for AI agents
[35] https://addyosmani.com/blog/loop-engineering — Addy Osmani, Loop Engineering
[36] https://arxiv.org/html/2608.21884v3 — Lulla et al., Loop Engineering: Building Blocks, Adoption, and Impact (arXiv 2608.21884v3)
[37] https://www.anthropic.com/engineering/building-effective-agents — Anthropic, Building effective agents
[38] https://x.com/HamelHusain/article/2078346425621237935 — Hamel Husain, Loop Engineering Is Dead. Enter Graph Engineering (article on X)
[39] https://dzone.com/articles/understanding-graph-engineering — DZone, Graph Engineering: The Layer After Loop Engineering
[40] https://www.anthropic.com/engineering/multi-agent-research-system — Anthropic, How we built our multi-agent research system
[41] https://arxiv.org/pdf/2107.13586v1 — Pengfei Liu et al., Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing (arXiv 2107.13586v1)
[42] https://www.ibm.com/think/news/why-ai-needs-human-at-helm-salesforce-paula-goldman — Sascha Brodsky (IBM Think), Salesforce's Paula Goldman on why AI needs a human at the helm (interview, November 2026)
[43] https://web.archive.org/web/20220114032036/https://cosmosmagazine.com/technology/ai/ai-in-the-workplace — Deborah Devis (Cosmos), Could AI in the workplace be good for humanity? (14 January 2022; Wayback Machine copy of that day)
[44] https://www.salesforce.com/blog/ai-and-human-touch — Holly Prouty (Salesforce), Building Trust in AI Needs a Human Touch (Salesforce research blog, 13 December 2023)
