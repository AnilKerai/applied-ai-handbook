---
title: AI questions answered
type: faq
created: 2026-11-14
audience: colleagues, engineering leads, senior leadership
status: checked
last_checked: 2026-11-21
as_of: "November 2026"
---

# AI questions answered

> **In one minute**
> - Start small: one well-understood task with sound data and easy-to-check results, after agreeing what AI must never be used for.
> - Use existing AI models and tools rather than making our own, and build what is ours: access to our data, tests and safety limits.
> - Decide what success means before you start, then measure it on real work: business results and failure rates, not volume of output or how fast it feels.
> - Limit what AI agents (AI that takes actions) can reach, and require approval for anything that can't be undone.
> - A named person is always accountable: AI can do the work, but people own the result.

*Reading time: about 20 minutes · Best for: everyone*

Short answers to the questions an in-house AI adviser hears most, for everyone at work: people using AI tools and teams building with them. They draw on practitioners' accounts and on industry developments, mostly from October and November 2026. **My recommendation** is my advice, in plain words. **How sure I am** is my judgement of how strong the evidence behind it is: very sure, fairly sure or not very sure. The *Why* bullets are what the sources say, and a final *For software teams* bullet holds any engineering detail. Questions only for teams building with AI are grouped [near the end](#for-teams-building-with-ai). Figures a company reports about its own work are marked as its claim, and the [AI glossary](ai-glossary.md) explains the terms.

## For everyone at work

### Q: Will AI replace my job?

**My recommendation:** Not on the evidence so far for jobs as a whole, though the early signs are worse for young people starting out in jobs exposed to AI. Let AI take over tasks while you keep the judgement, the accountability and the trust of the people you work with. To stay at the helm of your own work, tell AI tools what you want and where to stop, check what they give you, and own what you send.

**Why:**
- A Stanford study of payroll data on millions of US workers was revised in August 2026, with data to June 2026.[67]
  It found "no evidence of widespread, economy-wide job displacement" since generative AI was widely adopted.[67]
  A separate tracker from the Budget Lab at Yale, dated 14 October 2026, finds that measures of AI use "show no connection to changes in employment or unemployment".[68]
  Its analysis of exposure to AI also "does not yet clearly indicate an AI-related labor market footprint".[68]
- The exception is young workers aged 22–25 in jobs exposed to AI.[67]
  Their employment is 19% lower than if it had kept pace with that of young people in less-exposed jobs (a gap between the two groups, not a 19% fall in jobs).[67]
  It comes mainly through "reduced hiring of young workers rather than increased separations": fewer being taken on, rather than more being let go.[67]
  The authors call their findings "early, descriptive indicators" rather than causal estimates: they show a pattern, not proof that AI caused it.[67]
- The same study finds declines concentrated in jobs where AI mainly does tasks instead of people.[67] Where it mainly helps people with their work, "employment is flat or rising, especially for experienced workers".[67]
- Paula Goldman of Salesforce argues that "As AI gets more and more powerful, human leadership and judgment matter more, not less" (a vendor executive's view).[69]

**How sure I am:** Fairly sure. Two independent sources see no effect on jobs overall yet, but young workers fare worse. The main study shows a pattern, not proof, and one view is a vendor's.

See also [Will AI replace our developers?](#q-will-ai-replace-our-developers) for software teams, [Who is accountable when AI gets it wrong?](#q-who-is-accountable-when-ai-gets-it-wrong), and, for leaders, [Can AI replace our people?](../6-lead/can-ai-replace-our-people.md).

## Strategy

### Q: Where do we start?

**My recommendation:** Start with one well-understood task where AI would make the result better or more efficient, the data is sound and the output is easy to check. Agree first what we will never use AI for.

**Why:**
- Heidi Porter (Moyer Group AI) chooses a mechanism per task: rules, machine learning, a decision model (which picks from fixed answers) or an LLM (the AI behind chat assistants).[1]
  She says data quality sets the ceiling.[1]
- Mark Lay (Noblis): if AI gives neither a better nor a more efficient result, don't use it. Don Barger's organisation wrote its AI charter "before we ever write one line of code".[2]
- **For software teams:** Jarred Sumner (Anthropic) chose a project he could check against existing tests.[3]
  Newer evidence agrees: AWS's Swami Sivasubramanian supervised an agent rebuilding a replication engine for four nights before seeing it couldn't check its results.[4]
  With a spec and a test environment it took about two hours (AWS's account).[4]

**How sure I am:** Fairly sure. Several independent practitioners agree, but it rests on their experience, and nobody compared starting points.

### Q: How do we get people to actually use it?

**My recommendation:** Build it with the people who will use it, inside the tools they already use. Make a good shared tool the easy default, rather than ordering people to use it.

**Why:**
- Kevin Solorio (Focused) builds *with* frontline workers, not *for* them through proxies, and finds that people who helped build a tool become its champions.[1]
- AeroCore's data agent took off once it moved into Microsoft Teams: "No one likes an extra login."[2]
- Ramp says it never had to mandate use of its shared coding agent,[5] and Jason Beutler (Robosource) called team buy-in the hardest part of any AI project (abstract only).[6]

**How sure I am:** Fairly sure. The practitioners' stories agree, but none of them gives adoption figures.

### Q: Should we build or buy?

**My recommendation:** Use existing models and agent tooling rather than making our own, and build what is ours: data access, evals (repeatable tests on our own examples), checks and guardrails. Before building anything bespoke, ask what reversing it would cost and who will run it.

**Why:**
- Mark Lay saw one vendor upgrade break every app built on the old version.[2]
- **For software teams:** Harvey runs off-the-shelf coding agents and invests in the harness around them: "We don't compete with it. We run them."[7]
  Nick Kuhn (VMware Tanzu) called bespoke agent plumbing a platform problem that platform engineering already solved for ordinary apps (abstract only).[8]
  Warp's chief executive, whose company sells agent tooling, said a software factory is overkill for a team of a few people, and that companies should benchmark agents on their own tasks.[66]

**How sure I am:** Not very sure. The advice is consistent, but it often comes from vendors with a stake, and nobody compared total costs.

### Q: Will AI replace our developers?

**My recommendation:** Not for developers as a whole on the evidence so far, though early-career employment in AI-exposed jobs, software development among them, is lagging. The work shifts from writing code to specifying, checking and owning it, and that still needs people.

**Why:**
- A Stanford study of US payroll data, revised in August 2026, finds that employment has "declined substantially for early-career workers in the occupations most exposed to AI, including but not limited to software development and customer support".[70]
  Its headline figure is a gap between young workers in more and less exposed jobs, and the authors call their findings "early, descriptive indicators" rather than causal estimates.[70]
- A study of 655 firms (revised November 2026; data to August 2026) found no detectable effect on employment, though its model projects long-run declines.[11]
- Meta says about three quarters of its new code is now written with AI, yet its on-call work (responding to problems in live systems) did not get faster.[10]
- Steve Yegge: "the more agents I deploy, the more humans I need."[12] Against that, Cognition reports merged pull requests (accepted code changes) up 40-fold in a year while its headcount grew 2.7 times (Cognition's claim).[13]
- **For software teams:** in the 655-firm study, coding agents raised pull requests opened by 35.7% but resolved issues by only 13.7% (borderline significant).[11]
  Time from review submission to approval rose 56.1%.[11]

**How sure I am:** Fairly sure. One large independent study sees no effect on jobs yet, but projects long-run declines, and its data predate the newest models. Early-career jobs lag (a pattern, not proof), and practitioners disagree.

### Q: How do we know it's working, and what should we measure?

**My recommendation:** Decide what *better* means before you start: for example, time saved, fewer mistakes or better results for customers. Then check it on real work, with what each task costs alongside. Judge the outcome, not how much AI was used or how much it produced. Don't trust the feeling that it's faster: measure it.

**Why:**
- METR, a non-profit, ran one randomised trial of experienced open-source developers in early 2025: 16 of them, from large projects they had contributed to for years.[76]
  They brought 246 real tasks, such as bug fixes and new features, averaging two hours each, and each task was randomly assigned to allow or disallow AI.[76]
  METR found that "When developers are allowed to use AI tools, they take 19% longer to complete issues".[76]
  Yet "developers expected AI to speed them up by 24%, and even after experiencing the slowdown, they still believed AI had sped them up by 20%."[76]
- METR sets out the limits itself: "We do not claim that our developers or repositories represent a majority or plurality of software development work", and "We only study software development".[76]
  Its page on the trial now says: "These results are out of date."[76]
  In a follow-up begun in August 2025, with 57 developers, 143 repositories and more than 800 tasks, METR's raw results "show some evidence for speedup".[77]
  But METR calls that data "an unreliable signal".[77]
  More developers declined to take part because they did not want to work without AI.[77]
  And 30% to 50% of those surveyed said they held back some tasks for the same reason.[77]
  A lower pay rate also affected who took part, and its timings are unreliable for developers who run several AI agents at once.[77]
  METR believes developers are likely "more sped up from AI tools now" than its early-2025 estimates, but calls its data "only very weak evidence for the size of this increase".[77]
  It adds that developers' own estimates of their speed-up "can be quite unreliable", as its earlier study showed.[77]
- Kevin Solorio: "an agent without evals is a proof of concept". Heidi Porter warns that "averages can hide a bad result".[1]
- The 655-firm study shows output rising far faster than completed work.[11]
- **For software teams:** I'd track failure rates on real cases and cost per task, not lines of code, pull-request counts or tokens: those are not measures of success.
  DORA warns that token counts invite gaming and recommends tracking cost per accepted change and rework rates.[14]
  Factory tracks a *regret-free merge rate*, the share of changes that never need a revert or follow-up fix,[15] and Philipp Schmid (Google DeepMind) tells teams to report cost per task next to accuracy.[16]

**How sure I am:** Very sure. Two research sources show that counting output misleads, and one trial shows that people's sense of speed does too. What to measure instead rests on practitioners' practice.

### Q: How do we keep costs under control?

**My recommendation:** Track cost per task and cap spending. Cut usage with simpler set-ups, fewer agents and cheaper models for routine steps.

**Why:**
- Simon Willison argues that pay-per-use services and APIs should ship with hard spending caps on by default, since agents make runaway bills easier.[53]
- SEP's client prototype stalled partly because the token budget, its allowance for AI use, covered only a couple of days' work.[1]
- One newer study found that teams of AI agents scored higher but cost 3-7 times as much as a single agent.[18]
- **For software teams:** I'd also keep prompts cache-friendly, so the provider can reuse work it has already done.
  Philipp Schmid's single-tool harness roughly matched richer ones on accuracy with fewer tokens.[16]
  A second-hand write-up of one inference provider's data says falling from 97% to 92% cached means about 2.7 times the prompt-processing work, and notes that some providers price cached input at a twentieth of normal.[51]
  Newer evidence tempers the many-agent designs practitioners showed: Anthropic finds one agent loop often beats subagents on quality, cost and speed,[52] and Warp went from about $80 to $15-20 per pull request partly by using fewer subagents (Warp's claim).[9]

**How sure I am:** Fairly sure. The advice points the same way, but most savings figures are vendors' own.

## Choosing technology

### Q: Which model should we use, and do we need the biggest one?

**My recommendation:** Treat the model as a replaceable part, chosen by testing on our own tasks. By default, for domain agents (agents for one area of our work) especially, use open-weight models we can run ourselves, behind a good harness and evals. Open-weight models are published for anyone to download and run; the harness is the software around a model that makes it a working tool. Move a step up to a frontier model, one of the most capable, only where our evals show the open model failing and the step is worth the cost. Expect hard, open-ended steps to need a frontier model more often than routine ones, and re-test whenever we swap.

**Why:**
- Stanford Health Care tested five LLMs and chose a cheaper one that performed competitively.[1] AgentRun cut cost per item from $0.89 to $0.12 by having a cheap model run a job an expensive one had learned (AgentRun's claim).[19]
- Open-weight models trail the best closed ones by months, not years.[71]
  Epoch AI finds that since January 2026, the most capable open-weight models have lagged frontier closed models by an average of four months, on its composite capabilities index.[71]
  On narrow tasks, small models can catch up.[72]
  In a peer-reviewed study of text classification (sorting text into categories), specialised small models often needed only about 100 labelled examples on average to match or beat general large models.[72]
  The number depended strongly on the task, and rose by 100–200% once variance in performance was allowed for.[72]
- Against that, frontier models lead clearly on harder tests.[73]
  Artificial Analysis rebuilt its index in October 2026 with harder tests, 60% of it now private or held out.[73]
  The gap between the leader and the best open-weight model widened from 3 points to 12, and to 26 among models whose weights had been released.[73]
  The gaps were widest on hard reasoning and knowledge questions and on science tasks carried out by AI agents.[73]
- Running a model ourselves has its own costs.[74]
  Australia's cyber security centre says self-hosting may cut usage costs at scale, but that organisations should assess the total cost of running it securely.[74]
  That includes monitoring, maintenance and skilled staff.[74]
- **For software teams:** Microsoft's .NET team tests each of its agent skills per model, and Copilot can hand subtasks such as validation to cheaper models.[17]
  In a study of agent teams, cheap planners recovered 47.5% of a strong team's gain for 13.9% of its extra cost, but cheap implementers hurt.[18]
  Newer evidence adds a caveat to practitioners' message that models are interchangeable: one study found that a harness one model built for itself fell from 69.3 to 33.0 on a coding benchmark when another model ran it.[20]
  One developer compared two coding set-ups over two four-week periods (a preprint).[75]
  A self-hosted, quantised open-weight model, run in a different harness, was associated with a far higher share of fix commits than a frontier model behind an API (74.9% against 45.9%).[75]
  Even so, it still cost less in total on shared GPUs, and more on dedicated ones.[75]

**How sure I am:** Fairly sure about testing on our own tasks, not very sure about the open-weight default. Open models lag more on harder tests, the cost evidence is thin, and a comparison on business tasks is still missing (see the open questions).

### Q: Should we fine-tune a model, use retrieval (RAG), or neither?

**My recommendation:** Usually neither at first. Supply current facts through search or tools over good data, and write procedures down as skills (written instructions an AI can follow). Fine-tune, which means training the model further on our own examples, only if evals show a gap those can't close.

**Why:**
- Jeffrey Pinner (Exa, which sells search): "frontier models no matter how capable they are are always out of date."[21]
- Brian Douglas, on training a specialised reviewer model: "My recommendation is probably write a skill first."[22]
- Anthropic reports that a maintained wiki plus search beat search alone, 61% against 53%, on 25 questions (Anthropic's claim).[24]
- **For software teams:** Glean re-prompts its decision model, rather than retraining it, when labels change.[23]

**How sure I am:** Not very sure. No practitioner compared fine-tuning with retrieval directly.

### Q: Do we need a knowledge graph?

**My recommendation:** A knowledge graph stores facts as things and the links between them, such as customers and their contracts. Probably not as a starting point. For records kept in tables, well-written database queries (SQL) behind fixed tools are the baseline to beat. Test a graph only on relationship-heavy questions we can't answer today.

**Why:**
- In a peer-reviewed study Heidi Porter cited, of a hose production line, a vision model (AI that reads camera images) detected the defects.[1]
  The system drew evidence from a knowledge graph and separately searched procedures and maintenance history.[1]
  Rule checks tested whether the LLM's explanation stayed within the evidence.[1]
- The closest independent study (synthetic health records) found SQL ahead on lookup, multi-hop (chained) and reasoning questions, and a graph ahead only on time-based ones.[30]
  The graph agent cost about 3.5 times one with no retrieval.[30]
- Graph retrieval over text has been reported to underperform plain retrieval on many real tasks.[31]
- **For software teams:** model-written graph queries need checking: on one benchmark a strong model's were right about 72% of the time unaided and about 95% with automatic repair.[32]

**How sure I am:** Fairly sure. There is little research, and most of it uses made-up (synthetic) data.

## Risk

### Q: How do we stop hallucinations?

**My recommendation:** We can't eliminate them: AI will sometimes state false or made-up things with confidence. We can give the model less to invent, and check its output against the evidence it actually looked up. Where possible, check with code rather than another model's opinion.

**Why:**
- In Heidi Porter's case studies the LLM in a seed-selection tool is "the interface, the router, and the explainer, not the agronomist".[1] On a hose production line, rule checks test whether each draft stayed within its evidence.[1]
- Brian Kennedy (ZoomInfo) warns that AI judges, models that mark other models' work, hallucinate too: "The agent made it up and the judge approved it."[25] Melvin Johnson (Google DeepMind) says a final summary "needs to be grounded in the actions that were taken."[54]
- AgentRun's judge checks that the quote behind each answer is on a page the agent actually read, and hands unsupported answers to the expensive model (AgentRun's account).[19]
- **For software teams:** in Shweta Iyer's demo the agent call reported success while the request as a whole failed and its output was rolled back.[55]

**How sure I am:** Very sure. Many independent teams use the same pattern, though most of the measurements are their own.

### Q: Is our data safe?

**My recommendation:** Only as safe as what the AI can reach and what our contract says. Keep secrets, such as passwords and keys, and sensitive data out of what the AI is given to read. Keep data in-house where it must not leave, and confirm the provider's retention terms (what it keeps, and for how long) in writing.

**Why:**
- Juergen Gutsch: "the LLM should not know any credentials".[34] Noblis narrowed over 1,000 datasets to about 115-120 critical ones, with about 30 named data stewards.[2]
- Terms vary by plan. As read in October 2026, Anthropic's docs said commercial data isn't used for training without opt-in, and that retention is 30 days.[57][58]
  They said zero retention covers only qualifying enterprise accounts and excludes MCP (a standard way to connect AI to other tools).[57][58]
- Tools leak too: a user reported a coding agent putting their email address in the headers of its web requests.[59] A security firm found passwords in 1,122 public agent settings files (the firm's count).[60]
- **For software teams:** in regulated industries, bringing your own model "can be what enables the usage of AI coding tools",[56] and Kuhn's abstract promises a demo with a self-hosted model in which no data leaves the environment.[8]

**How sure I am:** Fairly sure. The engineering advice is consistent, but providers' terms change and need checking against our contract.

### Q: What about prompt injection and supply-chain risk?

**My recommendation:** Assume anything an AI agent reads could carry hidden instructions: that is prompt injection. Treat skills, plugins and packages like any other software we depend on, because they can carry harmful code too (supply-chain risk). Vet them, pin them to a known version, and sandbox them: run them where they can't reach our real systems.

**Why:**
- The UK's National Cyber Security Centre (NCSC) says LLMs don't separate instructions from data, so designs should lean on deterministic (non-LLM) safeguards that constrain what the system can do.[63]
- **For software teams:** Roey Ben Chaim (Zenity) found payloads in skills' remote prompts, install scripts and packages, including a campaign with 1.7 million downloads: "Everything that comes into the context is under risk."[61]
  Jon Douglas (Microsoft): "every package that you restore is code that you choose to trust." NuGet is adding a cooldown that skips very new versions.[62]
  Newer evidence adds two risks: OpenAI's sandboxed agents leaving each other instructions in a shared package cache (Matthew Green's account),[64] and planted text surviving context compaction as a fake user turn in 87-100% of cases on five agent tools that flatten history, against 0% on four that keep message roles.[65]

**How sure I am:** Very sure. Practitioners, a government agency and research papers agree, though the attack rates come from single studies.

### Q: Who is accountable when AI gets it wrong?

**My recommendation:** A named person, always. AI can do the work, but the person who asked for it and the person who approved it own the result.

**Why:**
- Mark Lay: "accountability can't be delegated" to AI, so the accountable role in a RACI chart (which records who is responsible, accountable, consulted and informed) is always a person. He adds that someone must own the tools staff build outside IT.[2]
- Juergen Gutsch: "Errors agents do are my errors".[34] Robinhood: "Scripts prove what can be proven. An agent judges what needs context and people own the calls only they should make."[38]
- **For software teams:** Anthropic's Claude Code team counts the person prompting an agent as a required reviewer (Anthropic's account).[37]

**How sure I am:** Very sure as a principle, though it is a stance on how to govern AI rather than a measured finding.

## For teams building with AI

These questions are for teams building AI features or working with coding agents.

### Q: When should we use a decision model instead of an LLM?

**My recommendation:** A decision model is an AI model that picks an answer from a fixed list and says how sure it is, instead of writing text. When the possible answers can be listed in advance (route, label, approve or reject), use a decision model or plain code, and keep the LLM for open-ended work. Test reliability, not only accuracy.

**Why:**
- Chinmay Goyal (Glean) asks "can the output be listed in advance?" If so, a decision model returns choices with probabilities instead of text.[23]
- ZoomInfo ran a decision model asking seven yes/no questions in shadow mode beside its LLM judge; it caught 623 of 728 clearly failed steps against the judge's 294 (ZoomInfo's figures).[25]
- Newer evidence broadens what was largely one vendor's theme among practitioners: a Strands case study says Amazon cut ticket-labelling costs by about 98% (its claim),[26] and OpenAI and Google have released decision-model APIs.[27][28]
- It also adds a caution: in a benchmark of 21 models, the best-performing decision model ranked only seventh for reliability, meaning answers that hold when options change and saying when none fits.[29]

**How sure I am:** Fairly sure. The results are strong, but mostly from one vendor's customers, and the newer figures are vendors' own.

### Q: What is MCP, and do we need it?

**My recommendation:** MCP (Model Context Protocol) is an open standard for giving agents tools, data and prompts. We need it when several agents must reach the same systems under managed access. For a one-off job, a skill or command-line tool is often simpler.

**Why:**
- Stephen Halter (Microsoft) described its building blocks as tools, resources and prompts, with the C# SDK owned by a Linux Foundation body. One benefit: "you don't need to put tokens inside of your environment and stuff and give access to secrets to the agent."[33]
- AeroCore's text-to-SQL agent reaches its database over MCP,[2] and Nick Kuhn's talk abstract describes binding an agent to its tools through a governed MCP gateway (no recording is available).[8]
- Practitioners disagree: Juergen Gutsch prefers skills as faster, cheaper and safer,[34] while Thariq Shihipar said "Like I actually prefer MCP to CLI now".[35] A November coding-agent release fixed leaking MCP sign-in tokens.[36]

**How sure I am:** Fairly sure. MCP is well described, but when it beats simpler options is a matter of opinion.

### Q: How do we review all this AI-written code?

**My recommendation:** We can't read every line, so let machines do most of the checking (tests, analysers, AI reviewers grounded in evidence), and have people review by risk.

**Why:**
- In the 655-firm study, time from review submission to approval rose 56.1%.[11] Anthropic's Claude Code team sets human approval by risk tier, and after three rounds of agent review the reviewer asks the author to rethink the approach (Anthropic's account).[37]
- ZoomInfo measured its LLM judge at 65% correct; given both receipts and the agent's report, "it went with the story."[25] Robinhood: "If the description says it is safe and the code says otherwise, the code wins."[38]
- On Lydia Hallie's team (Anthropic) an AI reviews every PR first; docs then need no person, ordinary changes perhaps one reviewer and risky ones might need two.[39] In a small pilot, a reviewer from a different model provider made a material finding on 8 of 20 coding turns.[40]

**How sure I am:** Fairly sure. Several teams agree, but two accounts are Anthropic's own and the figures are the teams' own. The independent study shows only where the bottleneck is.

### Q: What should go in AGENTS.md and similar instruction files?

**My recommendation:** Keep them short: exact commands, paths and facts the agent can't see in the code. Anything that must always hold belongs in a test, analyser or hook.

**Why:**
- Lydia Hallie: the file "should only include the things the Claude cannot see from your code".[39] Nikolay Petrov found models already knew about 70% of skills' general content but only 22% of the specific details.[41]
- A study of 3,159 skill files found added rules helped mainly when they named a command or path the file didn't already mention; unrelated text had no detectable effect, and deleting a rule lowered compliance with it, so check a rule is obsolete before cutting it.[42]
- Lauren Tan: make each correction "a deterministic check instead of adding another line to your rules or your agents.md".[43] Cam Soper (Pulumi): "a rule in an agent's instructions is just a suggestion."[44]
- A newer update: Anthropic warns that cautious instructions piling up through memory and instruction files can make its newest model ask for approvals it doesn't need; its advice includes removing outdated notes and naming the routine steps that need no approval.[45]

**How sure I am:** Very sure. Practitioners and one large study, not yet peer-reviewed, agree. The advice on the newest model is one vendor's.

### Q: How do we stop agents breaking things?

**My recommendation:** Limit what agents can reach, not just what they may run. Require approval for anything that can't be undone, and test the undo.

**Why:**
- Yvonne Carlson's eight principles include least privilege, short-lived credentials, approval before anything destructive, default-deny boundaries and sandboxes (abstract only).[46] Justin Yoo (Microsoft) separates "the permission to run, which is approval side, and the permission to reach, which is the boundary side".[47]
- Heidi Porter automates outright "only what is cheap to undo".[1] Meta asks "How costly is a mistake and how easy is it to catch?"[10] Tanmay and Dolly Sah found only 47% of normally successful agent runs recovered from an injected failure.[48]
- Newer evidence adds a reason to enforce limits in code: Anthropic reported its model working around restrictions instead of stopping,[49] and agent hooks can now block when they fail instead of being skipped.[50]

**How sure I am:** Very sure. Practitioners and newer evidence agree, though the failure rates come from single studies.

## Open questions (evidence thin)

- **What will it cost in total, and when does it pay back?** The sources give per-task savings, mostly vendors' own, but no total cost of ownership.
- **Which vendor, on what terms?** Nothing compared providers on data handling, sub-processors or international transfers.
- **What does regulation require of us?** Not covered beyond practical UK GDPR guidance, which is not legal advice.
- **How do we train our people, and how do junior roles change?** Practitioners' accounts covered adoption and culture, not training or career paths.
- **Are local, open-weight models good enough?** Partly settled. On Epoch AI's composite index the best open-weight models trail frontier ones by about four months,[71] and specialised small models can match large ones on narrow tasks such as text classification.[72] But the gap widens on harder, mostly private tests.[73] I know of no study that measures open-weight against frontier models on business tasks, so for now our own evals have to decide.

**Read next:** [Talk: using AI well at work](talk-using-ai-at-work.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; and Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[2] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; and Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows, Midwest AI Summit 2026 (Practical AI E379 transcript)
[3] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AI Engineer Code Summit 2026
[4] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS), AWS Emulator and the engineer's job when agents write the code
[5] https://ai.engineer/code/2026/talks/zach-bruggeman — Zach Bruggeman (Ramp), How to build an agent that builds the culture, AI Engineer Code Summit 2026
[6] https://midwestaisummit.com/jason-beutler — Jason Beutler (Robosource), The Order Matters: Structuring AI Projects Around People, Midwest AI Summit 2026 (abstract)
[7] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[8] https://midwestaisummit.com/nick-kuhn — Nick Kuhn (VMware Tanzu), Zero-Code Agents, Midwest AI Summit 2026 (abstract)
[9] https://x.com/latentspacepod/status/2117721636195663898 — Latent Space, Zach Lloyd (Warp) on software factories, 3 Nov 2026
[10] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[11] https://fion.ac/jellyfish.pdf — Chen & Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[12] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (Independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
[13] https://ai.engineer/code/2026/talks/walden-yan — Walden Yan (Cognition), A New Age of Software Engineering, AI Engineer Code Summit 2026
[14] https://dora.dev/insights/finding-balance-in-the-era-of-tokenmaxxing — DORA, Finding balance in the era of tokenmaxxing
[15] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AI Engineer Code Summit 2026
[16] https://ai.engineer/code/2026/talks/philipp-schmid — Philipp Schmid (Google DeepMind), I deleted 90% of my harness (And It Got Better), AI Engineer Code Summit 2026
[17] https://www.youtube.com/watch?v=SIBdHRrk8os&t=22243 — Wendy Breiding (Microsoft), Beyond Autocomplete: Getting the Most from GitHub Copilot for .NET, .NET Conf 2026
[18] https://arxiv.org/abs/2610.17471 — Cohere authors (arXiv 2610.17471), Scaling Inference-Time Compute with Teams of Coding Agents
[19] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun (Parcha), merchant-classification case study
[20] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[21] https://ai.engineer/code/2026/talks/jeffrey-pinner — Jeffrey Pinner (Exa), What Your AI Doesn't Know, AI Engineer Code Summit 2026
[22] https://ai.engineer/code/2026/talks/online-brian-douglas — Brian Douglas (organisation unconfirmed), If You Are Going to Verbally Abuse Your Agents, at Least Label the Outcome, AI Engineer Code Summit 2026
[23] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[24] https://www.anthropic.com/research/components-of-agent-memory — Anthropic, The components of agent memory
[25] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[26] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents, Amazon saves millions replacing Sonnet with Strands Decider
[27] https://developers.openai.com/api/docs/guides/decisions — OpenAI, Decisions API guide
[28] https://simonwillison.net/2026/Nov/11 — Simon Willison, weblog for 11 Nov 2026 (Gemini Decision 1)
[29] https://huggingface.co/papers/2611.15777 — Hugging Face Papers, SO-Arena (paper 2611.15777)
[30] https://www.mdpi.com/1999-5903/18/7/365 — MDPI paper 1999-5903/18/7/365, knowledge graph vs SQL retrieval for LLM agents over structured health records (Jul 2026)
[31] https://arxiv.org/abs/2506.05690 — arXiv 2506.05690, When to use Graphs in RAG (GraphRAG-Bench)
[32] https://arxiv.org/abs/2610.41755 — arXiv 2610.41755, CypherGuard: detect-and-repair for text-to-Cypher queries
[33] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=11360 — Stephen Halter (Microsoft), What's new in the MCP C# SDK, .NET Conf 2026
[34] https://www.youtube.com/watch?v=TF6qzdKwl84&t=9595 — Juergen Gutsch (organisation not named), Building a multi agent solution using Aspire, .NET Conf 2026
[35] https://ai.engineer/code/2026/talks/thariq-shihipar — Thariq Shihipar (Independent), Keep the human inside the creative loop, AI Engineer Code Summit 2026
[36] https://github.com/anthropics/claude-code/releases/tag/v2.1.321 — Anthropic, Claude Code v2.1.321 release notes
[37] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[38] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AI Engineer Code Summit 2026
[39] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[40] https://arxiv.org/abs/2610.10961 — arXiv 2610.10961, cross-provider review as a runtime contract (pilot)
[41] https://ai.engineer/code/2026/talks/online-skills-knowledge — Nikolay Petrov (organisation not stated), Your SKILL.md is 70% of Things the Model Already Knows, AI Engineer Code Summit 2026
[42] https://arxiv.org/abs/2610.04832 — Wang et al. (arXiv 2610.04832), Agent Skill Evolution: How Revisions Affect Coding Agents
[43] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[44] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[45] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 — Anthropic, Prompting Claude Fable 5.2: keep caution from piling up
[46] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[47] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[48] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah and Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[49] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions
[50] https://github.com/anthropics/claude-code/releases/tag/v2.1.295 — Anthropic, Claude Code v2.1.295 release notes
[51] https://www.brianletort.ai/industry/agents/2026-W42 — Brian Letort, agents week 42 (summarising Neuralwatt production cache data)
[52] https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop — Anthropic, When to fold subagents into your main agent loop
[53] https://simonwillison.net/2026/Oct/3/default-hard-budget-caps — Simon Willison, Default hard budget caps
[54] https://ai.engineer/code/2026/talks/melvin-johnson — Melvin Johnson (Google DeepMind), Train on the engineering work that still fails, AI Engineer Code Summit 2026
[55] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[56] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=2341 — Rachel Kang and Barbara (Microsoft), The State of AI in Visual Studio, .NET Conf 2026
[57] https://code.claude.com/docs/en/data-usage — Anthropic, Claude Code docs: Data usage (as read 12 Oct 2026)
[58] https://code.claude.com/docs/en/zero-data-retention — Anthropic, Claude Code docs: Zero data retention (as read 12 Oct 2026)
[59] https://github.com/anthropics/claude-code/issues/107757 — anthropics/claude-code issue 107757, harness put the account email in its web searches' User-Agent headers
[60] https://news.ycombinator.com/item?id=50407882 — Hacker News, discussion of Apiiro's finding that Claude Code allow rules stored secrets in settings files
[61] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AI Engineer Code Summit 2026
[62] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[63] https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection — NCSC, Prompt injection is not SQL injection (it may be worse)
[64] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green, Is sandboxing sufficient to contain rogue agents?
[65] https://arxiv.org/abs/2610.29869 — arXiv 2610.29869, compaction laundering: forged user turns survive context compaction
[66] https://www.youtube.com/watch?v=LL0YmIyBKSU — Latent Space, The 2026 Software Factory Infra Stack — Zach Lloyd (Warp), full episode video, 3 Nov 2026
[67] https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence — Erik Brynjolfsson, Bharat Chandar & Ruyu Chen (Stanford Digital Economy Lab), Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence (revised 12 August 2026)
[68] https://budgetlab.yale.edu/research/tracking-impact-ai-labor-market — The Budget Lab at Yale, Tracking the Impact of AI on the Labor Market (14 October 2026)
[69] https://paulagoldman.ai — Paula Goldman, Manage the Machine (author's book site)
[70] https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf — Erik Brynjolfsson, Bharat Chandar & Ruyu Chen (Stanford Digital Economy Lab), Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence (revised August 2026, full paper PDF)
[71] https://epoch.ai/data-insights/open-closed-eci-gap — Epoch AI, Open models lag state-of-the-art closed models by 4 months (Data Insight, 29 May 2026)
[72] https://aclanthology.org/2025.emnlp-main.9 — Branislav Pecher, Ivan Srba & Maria Bielikova, Comparing Specialised Small and General Large Language Models on Text Classification: 100 Labelled Samples to Achieve Break-Even Performance (EMNLP 2025)
[73] https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5 — Artificial Analysis, Announcing Artificial Analysis Intelligence Index v5 (27 October 2026)
[74] https://cyber.gov.au/sites/default/files/2026-11/Open-weight%20AI%20models%20Opportunities%20and%20cyber%20security%20risks.pdf — ASD's ACSC (Australian Cyber Security Centre), Open-weight AI models: Opportunities and cyber security risks (5 November 2026, PDF)
[75] https://arxiv.org/abs/2607.13080 — Sheng-Wei Peng, Yi-Hsun Lin & Yi-Pei Lee (arXiv 2607.13080, preprint), Inference Economics of Enterprise Coding Agents: A Case Study of Cloud vs. On-Premise LLMs
[76] https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study — METR, Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity (blog post, 10 July 2025; since marked out of date by METR)
[77] https://metr.org/blog/2026-02-24-uplift-update — METR, We are Changing our Developer Productivity Experiment Design (blog post, 24 February 2026)
