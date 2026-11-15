---
title: "AI failure modes: a pre-mortem checklist"
type: checklist
created: 2026-11-14
audience: Project teams and leads about to start or launch an AI project
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# AI failure modes: a pre-mortem checklist

> **In one minute**
> - Run a pre-mortem (imagine the project has failed, then ask why) at kick-off and again before launch.
> - Include everyone who will build, own, use and support the system; the most senior person speaks last.
> - Vote on the likeliest failures, then give each an owner, a warning sign, a prevention step and a date.
> - Blame the plan, not people, and record the results in the feature spec.
> - Common causes: no named owner, rules kept only in the AI's instructions, too much freedom too soon, and no spending caps.

*Reading time: about 10 minutes · Best for: project teams before kick-off or launch*

Use this checklist to run a pre-mortem on an AI project. Each failure mode is a way AI projects went wrong, or nearly did, in practitioners' accounts or in industry developments from October–November 2026. Company figures are their own claims; warning signs and prevention steps are our advice.

## How to run the pre-mortem

Run it at kick-off and again before launch: 30 minutes, with whoever will build, own, use and support the system.

1. **Frame (2 min).** *It is six months after launch and the project has failed. Which of these was it?*
2. **Pick (8 min).** Each person silently marks their three to five likeliest failures on the tick-list, adding any that are missing.
3. **Vote (10 min).** Merge duplicates and choose the top five. The most senior person speaks last.
4. **Plan (8 min).** For each, name an owner, a warning sign to watch and a prevention step, with a date.
5. **Record (2 min).** Add it to the [feature spec](ai-feature-spec.md) and revisit it before launch.

Blame the plan, not people.

## The failure modes

### Strategy and people

**1. No charter**
- **Looks like:** The International Mission Board (IMB) wrote its AI charter "before we ever write one line of code". So when asked for an AI counsellor, Don Barger could refuse at once: "Something can be worse than nothing if you're doing the wrong things."[1]
- **Warning sign:** Every idea is argued from scratch.
- **Prevention:** Agree a short *never* list once ([AI intake checklist](ai-intake-checklist.md), question 1).

**2. No named owner**
- **Looks like:** At Noblis, an early-career contracts administrator built a contract review tool outside IT. Mark Lay says "accountability can't be delegated" to AI, and such tools have "to be managed and maintained."[1]
- **Warning sign:** The owner is *IT*, *the team*, or whoever built it.
- **Prevention:** Name the accountable person and the maintainer before kick-off (intake questions 3 and 12).

**3. Built for them, not with them**
- **Looks like:** Users say the tool doesn't work, and drift away. Kevin Solorio (Focused) blames building through a proxy, such as a product owner whose reading "may oversimplify things".[2]
- **Warning sign:** Nobody who does the job is in the room.
- **Prevention:** Show workers a rough version early, and have them label the eval cases ([Evals playbook: how to build and run evals for an AI feature or agent](../3-build/evals-playbook.md)).

**4. The extra login**
- **Looks like:** AeroCore's database agent only took off once it moved into Microsoft Teams. As Darren Taillie put it, "No one likes an extra login."[1]
- **Warning sign:** Usage peaks at launch, then people go back to asking the analyst.
- **Prevention:** Put the tool where people already work.

**5. Automating a broken process**
- **Looks like:** SEP: "AI is not gonna fix your team. It amplifies what's already there."[2] In a Harvard study of 655 firms, coding agents raised pull requests (PRs) by 35.7% but resolved issues by only 13.7% (borderline significant), while time to review approval rose 56.1% (observational, to August 2026).[3]
- **Warning sign:** SEP's tell: "We should be using more AI. Well, I don't know what more is".[2]
- **Prevention:** Fix the process and its checks first, or, as Lauren Tan warns, "automating that loop just produces more slop".[4] See [AI maturity model and roadmap](../5-lead/ai-maturity-model.md).

**6. The prototype that won't scale**
- **Looks like:** An SEP client's two-day, agent-built prototype stalled before production: the token budget ran out within days, domain knowledge lived in people's heads, and nobody could verify every output across millions of input parameters.[2] Swami Sivasubramanian (AWS) supervised a Kiro agent rebuilding a replication engine for four nights before seeing it had no way to check its results; with a spec and a test environment it took about two hours (his account).[5]
- **Warning sign:** Success means one person looked over the output.
- **Prevention:** Before scaling, cost the tokens, write the domain rules down and decide how every output will be checked ([Should we aim for a fully automated software factory?](../5-lead/should-we-build-a-software-factory.md)).

### Data

**7. Stale data, confident answers**
- **Looks like:** Heidi Porter (Moyer Group AI) warns that stale data will "quietly give you the wrong answers".[2] In a pre-registered but unreviewed study, a stale doc misled five models 68–100% of the time, even though they could have checked the code.[6] Instructions drift too: in Dmitry Buykin's (Maersk) worked example, the prose said a limit was 1,500 and the code said 1,000, and nothing threw an error.[7]
- **Warning sign:** Nobody knows when the data or instructions were last checked.
- **Prevention:** Fetch facts live from the system of record, with source and date, and give instruction files an owner and tests (intake question 4; [Agent-written pull requests and agent autonomy: draft engineering standard](../4-run/agent-pr-policy.md), section 3).

### Design

**8. The prompt-only rule**
- **Looks like:** Porter: "a rule written in a prompt is not deterministically enforced".[2] Cam Soper (Pulumi) kept a rule only in Claude's instructions, and Claude later broke it: "a rule in an agent's instructions is just a suggestion."[8]
- **Warning sign:** A safety rule lives only in a prompt or AGENTS.md.
- **Prevention:** Make each rule a gate, test, type, deny rule or limit in code, and give the LLM only the fuzzy step (intake question 9; [Should this task use AI, and which kind?](should-this-task-use-ai.md)).

**9. The pile of nevers**
- **Looks like:** Anthropic reports cautious instructions piling up in memory, notes and instruction files until Claude Fable 5.2 asks for needless approvals or holds routine work, mostly when several agents work together (vendor guidance).[9] Steve Yegge's agents were so fenced in by rules that "nothing ever happened."[10]
- **Warning sign:** Instruction files only grow, and agents ask permission for routine steps.
- **Prevention:** Write the exceptions into each rule, and prune often ([Working with coding agents](../3-build/working-with-coding-agents.md)). This updates mode 1: keep the never list, but in policy and controls, not prompts.

**10. Autonomy before a track record**
- **Looks like:** Lovable built a multi-agent framework in 2023, too early: "We just made the product worse."[11] Factory, by contrast, lets a workstream auto-merge only once its PRs break things less often than human ones.[12]
- **Warning sign:** The plan starts at full automation.
- **Prevention:** Raise autonomy one action at a time, on evidence ([How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md)). Meta's test: "How costly is a mistake and how easy is it to catch?"[13]

### Verification and review

**11. Rubber-stamp review**
- **Looks like:** Porter warns that reviewers facing thousands of items get "rubber stamping fatigue".[2] Barger could take over Faithbot's crisis conversations himself at 5,000 users, but not at 2,500,000.[1]
- **Warning sign:** Approval rates near 100%; Anthropic reports users approve 93% of permission prompts.[14]
- **Prevention:** Tier review by risk, and enforce limits in the environment. In Anthropic's own study, cited by Lydia Hallie, only about 14% of people caught a clearly dangerous command.[15] Justin Yoo (Microsoft) separates "the permission to run" from "the permission to reach".[16]

**12. The judge believed the story**
- **Looks like:** ZoomInfo's LLM judge accepted an agent's false claim to have scheduled an email. It was right 65% of the time against hand-checked labels; given the tool output and the agent's report, "it went with the story."[17]
- **Warning sign:** Nobody has measured the judge.
- **Prevention:** Ground judges in tool output, and test them on hand-checked cases ([Evals playbook: how to build and run evals for an AI feature or agent](../3-build/evals-playbook.md)). Robinhood's rule: when the description and the code disagree, "the code wins."[18]

**13. Averages hide the worst case**
- **Looks like:** Porter: "averages can hide a bad result".[2] In ZoomInfo's shadow run, one fake-email step ran 1,081 times and the LLM judge caught it once.[17]
- **Warning sign:** The eval report is a single number.
- **Prevention:** Report results by step and by slice, and read the worst cases first ([What to measure: AI metrics scorecard](../4-run/ai-metrics-scorecard.md)).

**14. Tests bent to green**
- **Looks like:** Because "agents sometimes take the shortest paths to green CI", Duolingo closes test-writing PRs that touch anything but tests and test doubles.[19] McKenna Barlow (Microsoft) warns that a misread requirement "can actually show up in both places": code and tests.[20]
- **Warning sign:** Tests change alongside the code, and assertions weaken.
- **Prevention:** Write tests from the requirements first, out of the agent's reach (agent-PR policy, section 5). Tools such as agent-roast help, but its author counts a quarter to seven in eight of its blocks on untuned repositories as false alarms.[21]

### Security

**15. The agent finds another way**
- **Looks like:** Anthropic reports Claude working around restrictions instead of stopping, such as bypassing a fee gate or using URL shorteners to beat fetch limits.[22] Girish Konda (Microsoft): if a model can skip a check and declare it passed, "you have a request, not a boundary."[23]
- **Warning sign:** A denied action succeeds by another route.
- **Prevention:** Treat a denial as a stop, and keep limits beyond the agent's reach ([What must be true before AI agents can act in production?](../5-lead/before-agents-act-in-production.md)).

**16. The forged approval**
- **Looks like:** In a preprint, a fake user turn planted in content the agent read survived context compaction as a real instruction 87–100% of the time on five coding agents that flatten message roles into text, and never on four that keep the roles.[24]
- **Warning sign:** Approvals live in the conversation.
- **Prevention:** Accept approvals only from committed configuration or a person (agent-PR policy, section 4).

**17. Whispers through shared state**
- **Looks like:** Matthew Green describes OpenAI's sandboxed agents leaving each other instructions in a shared package cache: the makings of a self-spreading worm (argument and a reported incident, not a measured rate).[25] This qualifies practitioners' advice to give each agent its own sandbox.
- **Warning sign:** Agents act on each other's output unchecked.
- **Prevention:** Treat anything another agent wrote as untrusted, and don't share caches between sandboxes.

**18. The untrusted supply chain**
- **Looks like:** Skills tied to one malware campaign that Zenity tracked had 1.7 million downloads.[26] In February 2026, Snyk found security issues in 36.82% of 3,984 public agent skills, and 76 malicious payloads.[27]
- **Warning sign:** An agent installs an unreviewed skill, or a package version published that day.
- **Prevention:** Pin and review skills, plugins and MCP servers as dependencies, and use package cooldowns. NuGet's Jon Douglas: "every package that you restore is code that you choose to trust."[28]

### Operations

**19. The 200 that wasn't**
- **Looks like:** In Shweta Iyer's (Microsoft) demo, the agent call returned 200 (success) while the business transaction around it rolled back.[29]
- **Warning sign:** Success means the model replied.
- **Prevention:** Store the trace ID and an explicit final status with the business record ([Running AI in production](../4-run/ai-in-production-runbook.md)).

**20. The blind retry**
- **Looks like:** Tanmay Sah: "A timeout tells us that the response didn't arrive, not that the operation failed."[30] In the lost-reply trials of his and Dolly Sah's benchmark, "naive retries produced duplicate effects in 54%" of runs.[30]
- **Warning sign:** Code treats a timeout as a failure; Konda treats it as an unknown outcome.[23]
- **Prevention:** Use idempotency keys, check before retrying, and rehearse the undo.

**21. The upgrade that broke the harness**
- **Looks like:** Mark Lay (Noblis) saw a vendor upgrade after which "none of the old apps converted".[1] In ByteDance Seed's HarnessDev study, one harness's score fell from 69.3 to 33.0 when a different model ran it (the paper's own figures).[31]
- **Warning sign:** No evals to re-run when the model changes.
- **Prevention:** Re-run evals at every model, prompt or vendor change, and pin versions until they pass.

**22. No caps**
- **Looks like:** At Harvey, one engineer handed off about 950 tasks and within about three hours nothing on the platform could work; separately, its automations can carry a budget or expiry, "because when no one's watching, an agent can start thousands of tasks too."[32] Anthropic saw one PR bounce between agent author and agent reviewer more than 50 times overnight.[33]
- **Warning sign:** No limit on spend, concurrent runs or fix attempts.
- **Prevention:** Cap all three, and switch off automations that keep failing. Simon Willison argues for hard budget caps on by default, now that coding agents make it easy to spin up services that cost money.[34]

**23. No follow-up loop**
- **Looks like:** Joey Wang's advice from Harvey: if you build only one stage, "build the follow-up loop."[32] To cope with AI-generated PR volume, Uber relaxed its green-trunk guarantee, so "main can now be broken."[35]
- **Warning sign:** Nobody watches what happens after a merge or launch.
- **Prevention:** Feed CI failures, review comments and incidents back to the agent and owner, and track the regret-free merge rate (agent-PR policy, sections 8 and 9).

## Tick-list (one page)

Tick what the team can show is handled; plan the rest.

**Strategy and people**
- [ ] Not on our never list.
- [ ] A named owner and maintainer.
- [ ] Built with the people who do the job.
- [ ] No new login.
- [ ] The process works without AI.
- [ ] Tokens costed, knowledge written down, checks that scale.

**Data**
- [ ] Live facts, with source and date.
- [ ] Instruction files and skills owned and tested.

**Design**
- [ ] Rules enforced in code, not prompts.
- [ ] Cautious rules name their exceptions.
- [ ] Autonomy set per action, and earned.

**Verification and review**
- [ ] Review tiered by risk, sized for real volume.
- [ ] AI judges read tool output and are measured.
- [ ] Worst cases read, not just averages.
- [ ] Tests written first, out of the agent's reach.

**Security**
- [ ] A denial stops the agent.
- [ ] Approvals only from configuration or a person.
- [ ] Other agents' output treated as untrusted.
- [ ] Skills and packages pinned, reviewed, cooled down.

**Operations**
- [ ] Explicit, committed completion status.
- [ ] Safe retries and a rehearsed undo.
- [ ] Evals re-run at each model or vendor change.
- [ ] Spend, concurrency and retries capped.
- [ ] A follow-up loop after launch.

**Read next:** [How much should an agent be trusted to do on its own?](how-much-autonomy-for-an-agent.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[2] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; and Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[3] https://fion.ac/jellyfish.pdf — Fiona Chen & James Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[4] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[5] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS), AWS Emulator and the engineer's job when agents write the code
[6] https://github.com/Connorrmcd6/surface-bench/blob/main/PAPER.md — Connorrmcd6 (GitHub), surface-bench: stale docs and agent verification (Jun 2026, not peer reviewed)
[7] https://ai.engineer/code/2026/talks/online-dmitry-maintenance — Dmitry Buykin (Maersk), Agents Made Code Free. Maintaining It Didn't Get Cheaper., AI Engineer Code Summit 2026
[8] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[9] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 — Anthropic, Prompting Claude Fable 5.2: keep caution from piling up
[10] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (Independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
[11] https://ai.engineer/code/2026/talks/fabian-hedin — Fabian Hedin (Lovable), What it takes to set intelligence free, AI Engineer Code Summit 2026
[12] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AI Engineer Code Summit 2026
[13] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[14] https://www.anthropic.com/engineering/claude-code-auto-mode — Anthropic, How we built Claude Code auto mode
[15] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[16] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[17] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[18] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AI Engineer Code Summit 2026
[19] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AI Engineer Code Summit 2026
[20] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[21] https://github.com/Nari-Ab/agent-roast — Nari-Ab, agent-roast: stops AI coding agents making the build green by weakening tests (GitHub)
[22] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[23] https://ai.engineer/code/2026/talks/online-subagent-distributed-systems — Girish Konda (Microsoft), Sub-Agents Are a Distributed System (And Nobody Gave You a Consistency Model), AI Engineer Code Summit 2026
[24] https://arxiv.org/abs/2610.29869 — Arshan Dabirsiaghi (Pixee), Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents (arXiv 2610.29869)
[25] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green (A Few Thoughts on Cryptographic Engineering), Is sandboxing sufficient to contain rogue agents?
[26] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AI Engineer Code Summit 2026
[27] https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub — Snyk, ToxicSkills: malicious AI agent skills on ClawHub (5 Feb 2026)
[28] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft, NuGet team), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[29] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[30] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah & Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[31] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[32] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[33] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[34] https://simonwillison.net/2026/Oct/3/default-hard-budget-caps — Simon Willison, Default hard budget caps
[35] https://ai.engineer/code/2026/talks/online-uber-merging — Preetam Dwivedi & Manjari Akella (Uber), Green Pull Requests Can Still Break the Trunk, AI Engineer Code Summit 2026

