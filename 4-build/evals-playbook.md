---
title: "Evals playbook: how to build and run evals for an AI feature or agent"
type: playbook
created: 2026-11-14
audience: "Engineering teams and product owners building AI features"
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Evals playbook

> **In one minute**
> - Treat evals (repeatable tests of whether the AI did the job) as the gate into production.
> - Start small with real cases from the people who do the job, include the worst cases, and add each new failure.
> - Report worst cases, not just averages; any failure on something that must never happen blocks release.
> - Use fixed automatic checks first; any AI that marks results must see what actually happened and be checked against people.
> - Run each case several times, and re-run the whole set whenever the model, instructions, data or marking method changes.

*Reading time: about 20 minutes · Best for: engineers and product owners*

*How to build and run evals for an AI feature or agent, end to end.* An eval is a repeatable test of whether the AI did the job. The [AI intake checklist](../2-decide/ai-intake-checklist.md) asks whether we have evals; this says how to build them. Rules are my recommendations; company and vendor figures are their own claims.

## 1. Why evals gate production

Kevin Solorio (Focused) puts it bluntly: "an agent without evals is a proof of concept", however it is deployed.[1] Heidi Porter (Moyer Group AI) says evals tell us whether a system works and "they gate everything towards more autonomy", and the matching principle at SEP, a firm that builds software for clients, is "verification before velocity".[1] So, in my view, a passing eval run is the ticket into production and onto each rung of [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md). As Duolingo puts it, "writing code isn't the hard part anymore, verifying it is."[3]

## 2. Build the eval set

**Build it with the people who do the job.**
- Solorio shows workers a deliberately rough version built on synthetic data, because people are quick to say what is wrong, and makes labelling cheap, for example with a shared spreadsheet.[1]
- He widens the circle once the first few experts have shaped it, because they "might not see every case".[1]

**Use real cases.**
- Syngenta evaluated against 100 real question-and-answer pairs from sales reps, scored by human reviewers and an LLM judge (Syngenta's figures, as Porter reported them).[1]
- Microsoft built its own C# benchmark of about 170 scenarios, each a prompt plus an expected result, because public suites contain no C#.[5]
- Zach Lloyd (Warp): "The only way to answer those questions for real is to test on your own data."[4]

**Include edge and worst cases.**
- Anthropic's Claude Code team turns every incident into an eval case, with each bug confirmed by engineers who know the code, and runs its reviewer against the set daily.[6]
- It also runs the reviewer on PRs known to be clean, to count false alarms (Anthropic's account).[6]
- In reinforcement learning (RL) training rather than evals, Melvin Johnson (Google DeepMind) turns failures from internal use into new training tasks and prunes tasks the model always solves, because "Easy task give you zero learning signal".[7]

**How big to start.**
- Solorio's sets are small and curated: "You're not gonna have millions of them."[1]
- The examples run from about 100 cases (Syngenta) to about 170 (Microsoft), and ZoomInfo hand-checked 500 production steps to test one judge.[1][5][13]
- Susan Chang (Elastic), citing advice from Eugene Yan's blog, says a first test dataset can in some situations start at 20 to 50 records and grow later.[37]
- I recommend starting with 30-50 real cases, at least a quarter of them edge or worst cases, then growing the set from real failures. Coverage matters more than count.

## 3. What to score

**Task success, defined per case.** Exa's benchmark counts a row as correct only if every field in it is right.[8] Define "correct" per case before running anything.

**Worst cases, not averages.**
- Porter: "averages can hide a bad result", and we need to know how bad the bad result is so we can fix it.[1]
- Diogo Almeida (TypeSafe AI) puts the risk of automating with LLMs as "you get Einstein 95% of the time, but Mr. Bean 5% of the time."[9]
- SO-Arena tested 21 models across 11 domains. The best-scoring decision model ranked only seventh for reliability, meaning giving answers that hold when the options change, and noticing when no option is right.[10]
- Patrick Debois (Tessl) frames going live as a risk call: some evals must pass and others can be more erratic, so he gives some functionality a very limited error budget and other functionality one he can relax.[39]
- I recommend reporting the pass rate, worst-case failures and the single worst result separately. Any failure in a *must never happen* case blocks release.

**Cost and latency per case.**
- Cline grades turns, tokens, latency, tool calls and the path taken separately, plus checks for reward hacking.[11]
- Microsoft's C# benchmark caught a code-search tool's token overuse before release.[5]
- DORA warns that token counts are easy to game and suggests pairing delivery metrics with cost per accepted change and rework rates.[12]
- Glean reports its decision model stayed within a 1.5-2 second budget in 99.2% of cases, against about 90% for an LLM (Glean's claim).[19]

**Per step and end to end.**
- ZoomInfo's judge decides after every agent step whether to accept, redo or stop. The team is adding per-tool post-condition checks, such as whether the message was delivered or the record exists.[13]
- Shweta Iyer (Microsoft) showed an agent call succeeding while saving its results failed and rolled back, so she stores the trace ID with the business record: "the final takeaway was to make any completions explicit".[14]
- I recommend scoring each step that can fail silently and the end-to-end outcome on the business record: one locates the fault, the other says whether the user got what they needed.

**Agents that hold a conversation: simulated users.**
- Zhou Yu (Columbia University; co-founder of Arklex AI, which makes a user simulator for this testing) argues that a static, single-turn benchmark can't test an agent that holds a conversation, because it is hard to predict how the user reacts when the agent says something different.[38]
- In her approach, each test is a scenario: the user's attributes (a profile), a goal drawn from what the agent can do, and context such as product documents.[38]
  A simulated user plays the scenario against the agent, and a fixed set of scenarios runs in CI.[38]
- Her grade checks the system as well as the reply: for a return, whether the databases and environment show the product was actually returned following the business's process, which rules can check automatically.[38]
- For softer qualities such as helpfulness or brand voice, she seeds LLM judges with good examples and tricky bad ones, which experts can pick from the simulated conversations.[38]
- She grows the fixed set from production logs, adding scenarios for the kinds of user, goal and context the simulation missed.[38]
- In her example, simulating 10,000 conversations on every CI run would cost a couple of thousand dollars each time (her figure), so she aims for the fewest scenarios that give the most coverage.[38]
- τ-bench (section 5) also has language models play the user, and grades by comparing the database state at the end of the conversation with the annotated goal state.[33]
- I'd reserve simulated-user runs for agents that hold a conversation, and run them nightly or before a release rather than on every change, because of the cost.
  I'd still grade them on the end state with deterministic checks first, and keep judges for what code can't check.

## 4. Graders

**Deterministic checks first.**
- Robinhood: "Scripts prove what can be proven. An agent judges what needs context and people own the calls only they should make." Its reviewer agent is told what the scripted checks already cover.[15]
- Duolingo runs a deterministic rule (close any PR touching a non-test file) before its LLM judge.[3]
- Susan Chang (Elastic) pairs LLM judges with programmatic checks for anything with a deterministic answer, such as a product ID or a required format, because judges can struggle with formats and internal facts.[37]

**LLM judges read the tool output, not the agent's story.**
- ZoomInfo measured its LLM judge on 500 hand-checked production steps. It was right 65% of the time and accepted 118 bad steps (ZoomInfo's figures).[13]
- When an agent claimed it had scheduled an email though the CRM write had failed, the judge, shown both, "went with the story".[13]
- Robinhood's rule: "If the description says it is safe and the code says otherwise, the code wins."[15]
- Johnson: "when the agent says I'm done and gives you a summary that needs to be grounded in the actions that were taken."[7]
- AgentRun's judge checks that the quote behind each answer is on a page the agent actually read (AgentRun's case study).[16]

**Yes/no rubric questions, not *is this good?***
- ZoomInfo rewrote its open judgement as seven yes/no questions answered from the evidence, which explain each verdict and feed the redo instructions, and trialled it in shadow mode beside its LLM judge.[13]
- Its recipe: rewrite one judgement as yes/no questions that evidence can answer, build it, ship it in shadow mode and read the disagreements.[13]

**Calibrate judges against people.**
- Brian Kennedy (ZoomInfo): "We had trusted our judge until we measured it."[13]
- Nikolay Petrov uses a judge or panel, ideally from a different model family, and checks that questions don't leak their answers.[17]
- Susan Chang (Elastic) reports that a judge from the same model family, such as Llama grading Llama, rated that family's models higher, as Meta and CrowdStrike also found.[37]
- Chang leaves calibration to each team rather than Elastic's shared eval framework, because checking that judges agree with human evaluators, and give a repeated scenario roughly the same score, rests on domain expertise and each team's own expertise.[37]
- A small, agent-authored pilot of cross-provider review found a material finding in 8 of 20 coding turns (95% interval about 19-64%).[18]
- It also found plumbing bugs: a false pass on truncated input, and a reviewer that exited with an error but a valid verdict counted as complete.[18]
- I recommend hand-labelling at least 50 cases and measuring the judge's chance-corrected agreement with people (section 5) before it gates anything, then re-checking monthly and logging each grader's input size and exit status.

**Decision models as graders.**
- ZoomInfo's typed decision model (Jev) was confident on about 7 in 10 of the same steps; among those, it caught 74 of the 82 bad steps the LLM judge had accepted. Uncertain cases still go to the LLM (ZoomInfo's figures).[13]
- Glean says its citation-checking decision model was consistent enough that repeat runs weren't needed: only one run differed across about 30 use cases (Glean's claim).[19]
- Newer evidence cuts the other way: in SO-Arena (section 3), the best-scoring decision model was not the most reliable.[10] I'd give a decision-model grader the same calibration, including cases where no option is right.

## 5. Measurement rigour

The practitioner sources in this playbook say little about statistics, so this section draws on published practice. A pass rate from a handful of runs can look far more precise than it is.

**Run each case several times.**
- Model outputs vary between runs, so Anthropic runs several trials of each task and measures how often the agent succeeds.[32]
- Two numbers come out of that: pass@k, the chance that at least one of k trials succeeds, and pass^k, the chance that all k succeed.[32]
- An agent that succeeds on 75% of trials passes all of three trials only about 42% of the time.[32]
- pass^k comes from τ-bench, where even strong function-calling agents succeeded on under half the tasks and passed all eight trials in the retail domain less than 25% of the time.[33]
- Anthropic recommends pass^k where users expect the same behaviour every time, and pass@k where one success is enough.[32]
- Capability and reliability rank models differently. A study of long-horizon agents found the two rankings diverging as tasks lengthened, with reliability falling fastest in software engineering and barely at all in document processing.[36] SO-Arena found the same split for decision models.[10]
- I recommend at least three runs per case, with pass^k as the headline for anything customer-facing.

**Put error bars on every number.**
- Evan Miller (Anthropic) argues that evals are experiments and should report standard errors, as other sciences do.[34]
- When questions come in related groups, he recommends clustered standard errors.[34]
- Anthropic also warns that trials which fail for the same shared cause are not independent.[32]
- Repeated runs of one case, and several checks on one case, form such groups: if every check in every run counts as a separate observation, the interval comes out narrower than the evidence supports.[34] I recommend clustering by case, or computing intervals over cases rather than checks.

**Compare like with like.**
- When two configurations run on the same questions, Miller recommends analysing the per-question differences rather than comparing the two overall rates.[34]
- Pairing reduces the variance whenever the two configurations agree on which questions are hard.[34]
- I recommend this for every with-and-without comparison: with or without a skill, old model or new. Run both on the same cases and test the paired difference.

**Size the set for the question.**
- Early on, 20-50 tasks drawn from real failures are a good start, because each change tends to have a large, visible effect.[32]
- More mature agents may need larger and harder sets to detect smaller effects.[32]
- Miller recommends a power analysis to check whether an eval can detect the difference that matters at all.[34]

**Calibrate judges with chance-corrected agreement.**
- The Judge's Verdict benchmark found that correlation alone is not enough to evaluate a judge, and measured agreement with humans using Cohen's kappa; 27 of 54 judge models reached its top tier.[35]
- Kappa discounts the agreement a judge would get by chance, such as by always answering pass on a set that is mostly passes.[35] A calibration set labelled entirely pass cannot show whether a judge catches failures: there are none to catch, and kappa comes out at zero or undefined whatever the judge does.
- Anthropic builds balanced sets, covering cases where a behaviour should happen and cases where it shouldn't.[32]
- It also recommends giving judges a way out, such as answering Unknown when the evidence is missing, and grading each dimension with a separate judge.[32]

**Keep regression and capability evals apart.**
- Regression evals should pass nearly 100% of the time, so a drop is an alarm; capability evals start low and give a hill to climb.[32]
- Capability tasks that reach high pass rates can graduate into the regression suite, and an eval at 100% gives no signal for improvement.[32]
- Melvin Johnson (Google DeepMind) prunes always-solved tasks from his RL training data (not from an eval suite) for a similar reason: they carry no learning signal.[7]

**Test the eval before trusting the score.**
- Anthropic recommends a reference solution for each task, to prove it is solvable and the graders are set up correctly, and treats 0% across many trials as a likely sign of a broken task.[32]
- An Anthropic researcher found rigid grading, ambiguous specs and irreproducible tasks that held Opus 4.5 at 42% on CORE-Bench; after fixes and a less constrained scaffold it scored 95% (Anthropic's account).[32]
- Grade what the agent produced rather than one fixed sequence of steps, because agents find valid paths the designers didn't anticipate.[32]
- Start each trial from a clean environment: shared state causes correlated failures, and in one internal eval Claude read git history left by earlier trials.[32]
- Read the transcripts. Anthropic does not take a score at face value until someone has.[32]
- The mutation check in section 7 and the break-it-on-purpose pitfall in section 9 test the same thing from the other side: an eval that never goes red is not measuring anything.

## 6. Offline and online

**Run Solorio's data flywheel.** Develop against an offline dataset. Once live, online evaluators (code checks or an LLM judge) score a sample of traces, and flagged cases go to an annotation queue; people work out what went wrong and the case joins the offline set.[1] Keep the loop running, he says, because new cases turn up at every stage of release.[1]

**Shadow mode before switching.**
- ZoomInfo ran its new judge in shadow mode over 37,000 decisions. Of 728 clearly failed tool steps, the LLM judge caught 294 and the decision model 623 (ZoomInfo's figures).[13]
- Amazon engineers ran Sonnet and a decision model on the same tickets in parallel, applying Sonnet's labels and comparing, before switching. They report about 98% lower cost (Strands' claim).[20]
- Glean gates changes with golden eval sets, then internal use by about 1,500 staff, then customer A/B tests.[19]

**Score live traffic and feed the results back.**
- Warp records every run centrally and runs online scorers over them, such as one for redundant tests.[4]
- Robinhood collects reasoned human replies daily; misses become new rules, and false escalations reveal missing context.[15]
- Ara Khan (Cline) treats each human correction as a capability gap to cover, and buckets eval failures by type before fixing the harness.[11]

**Current practice: tools that help a coding agent write evals from traces.** NVIDIA's tooling reads stored traces against a short file of expected behaviour, ranks the issues, helps a coding agent write evals, and compares the fix on held-out tasks. It reports malformed tool calls falling from 142 to zero with accuracy unchanged (NVIDIA's claim).[21] That automates the triage Solorio runs with people, but it does not answer his point that workers know cases no trace shows.[1] I recommend letting tooling fill the queue and keeping people deciding what enters the set. Live operation is in [Running AI in production](../5-run/ai-in-production-runbook.md).

## 7. Evals for coding agents and their context

**Use test suites that predate the agent as oracles.**
- Jarred Sumner (Anthropic) chose the project that existing test suites could check: "as soon as you're like rewriting the tests then you can't really trust the tests anymore."[22]
- AWS's agents correct each *fidelity test* until it passes against real AWS, then build the emulator until it passes the same test.[23]
- Swami Sivasubramanian (AWS) supervised a Kiro agent rebuilding Alf's replication engine for four nights before seeing it had no way to check its results; with a spec and a test environment the rebuild took about two hours (his account).[23]
- McKenna Barlow (Microsoft) makes the written requirement the oracle, because a misread requirement "can actually show up in both places", code and tests.[26]

**Keep the checks out of the agent's reach.**
- Duolingo closes any PR touching a non-test file, because "agents sometimes take the shortest path to green CI."[3]
- Factory's risk judge "reads its policy from our mainline branch so that the change can't rewrite the rules that it's being judged by."[25]
- Johnson's graders hide the tests and git history until the agent submits, because agents had peeked at tests and resubmitted.[7]
- Google's /teamwork checks agents' results against unmodified test suites, with critics working from a clean context (Google's account).[24]
- The agent PR policy, [Agent-written pull requests and agent autonomy](../5-run/agent-pr-policy.md), turns these into merge rules.

**Test skills and AGENTS.md with and without, per model.**
- Petrov runs each skill's tasks with and without it, comparing solves, tokens and time; larger models already knew about 70% of skills' general ideas but only 22% of the details.[17]
- Microsoft scores each skill per model on activation, tokens, speed and pass rate with and without it, and runs its benchmark nightly, rotating through the five models users use most.[5]
- Patrick Debois (Tessl) recommends testing context by running a skill's task without the context and with it, or with the old context and the new, repeating each test (say, five times) because results vary.[39]
  When a coding agent goes wrong during a working session, he suggests turning that into a test case and running it without and with the improved context.[39]
- The browser vendors' Modern Web Guidance skill uses evals to prune content models already know.[29]
- An ETH Zurich study found context files did not generally improve task success but raised inference cost by over 20%.[27] A study of skill revisions found added rules helped mainly when they named a command or path the skill had not mentioned.[28] In my reading, both support the practitioners above: keep only lines an eval shows help.
- Dmitry Buykin (Maersk) mutated sentences in his prose instructions and almost no tests went red, so he now checks that evals notice.[31]

See also [Working with coding agents](working-with-coding-agents.md) and [Building AI features in .NET](dotnet-ai-engineering-guide.md).

## 8. When to re-run

Re-run the full set and compare against the last baseline whenever one of these changes:

- **The model or platform.** Porter, on Syngenta's swappable models and knowledge bases: "you have to reevaluate afterwards".[1] In ByteDance Seed's HarnessDev study, one harness fell from 69.3 to 33.0 when a different model ran it (the paper's numbers).[30] Mark Lay (Noblis) saw a vendor's new version where "none of the old apps converted".[2]
- **A prompt, skill, context file or tool.** Warp replays a benchmark of its own tasks before switching model, harness or skill.[4] Petrov re-runs task evals after every trim, and Buykin replays frozen real tasks old against new.[17][31]
- **The data.** Porter warns that stale data will "quietly give you the wrong answers", so a knowledge-base refresh is a trigger like a model swap.[1]
- **The grader.** Recalibrate a new judge model or prompt against the hand-labelled cases before comparing scores (my recommendation).
- **The calendar.** Anthropic runs its incident set daily and Microsoft runs its benchmark nightly.[6][5]

## 9. Pitfalls

- **Trusting the average.** It hides the bad result.[1]
- **An unmeasured judge.** Kennedy likened ZoomInfo's judge, once measured (section 4), to a coin flip.[13]
- **Evals that cannot fail.** Barlow breaks something on purpose before trusting a green suite.[26] Sumner: "it's really easy to fool yourself that it's finding bugs when it's not finding bugs."[22]
- **Letting the agent edit its checks.** It may take the shortest path to green.[3]
- **Cases written by a proxy.** Developers or product owners guessing on users' behalf can miss what workers know.[1]
- **Vendor scores as a forecast.** One model scored 77.5% in Cline's harness against its release paper's claim of up to 85% or more.[11]
- **Silent grader failures.** Truncated input or a reviewer that exited with an error can still count as a completed review.[18]
- **A gate that escalates everything.** Robinhood: "A gate that escalates everything is not actually saving anyone any time."[15]
- **A set that never changes.** Graduate capability cases that always pass into the regression suite, and add each new failure.[32][7]
- **One run per case.** A single pass can be luck, so run several trials.[32]
- **Error bars that treat every check as independent.** Runs and checks on the same case are related, so cluster them.[34]

## 10. First two weeks: a starter plan

*My recommendation, uncited.*

Week 1:

1. **Day 1.** Pick one feature or workflow step and name an owner. Write down what a correct result is, and the outcomes that must never happen.
2. **Days 2-3.** With two or three people who do the job, collect 30-50 real cases, including past failures, at least a quarter of them edge or worst cases (section 2), and have them label the expected results.
3. **Day 4.** Write deterministic checks first: format, required fields, post-conditions on the business record.
4. **Day 5.** Build a runner recording pass or fail, cost and latency per case across at least three runs, and baseline the current system or human process.

Week 2:

5. **Days 6-7.** Add an LLM judge only for what code cannot check. Phrase it as yes/no questions, feed it the tool output, and measure its agreement with people on the labelled cases.
6. **Day 8.** Put the run in CI, with the set and judge prompts out of the agent's reach. For coding agents, run with and without each skill or context file, per model.
7. **Day 9.** Shadow a sample of live traffic, set up the annotation queue, and book a weekly review slot.
8. **Day 10.** Report pass^k with confidence intervals, worst-case failures, cost, latency and the judge's kappa, and record the re-run triggers in the [AI feature spec template](../2-decide/ai-feature-spec.md).

Related: [What to measure: AI metrics scorecard](../5-run/ai-metrics-scorecard.md), [AI failure modes: a pre-mortem checklist](../2-decide/ai-failure-modes-premortem.md), [What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md), [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md).

As a talk: [Talk: building AI features](talk-building-ai-features.md), slides and speaker notes for engineers, ending with writing eval cases from real examples.

**Read next:** [Working with coding agents](working-with-coding-agents.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs; Kevin Solorio (Focused), Building AI With Workers, Not For Them; Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026
[2] https://practicalai.show/379/transcript — Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own, Midwest AI Summit 2026
[3] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AIE CODE 2026
[4] https://ai.engineer/code/2026/talks/zach-lloyd — Zach Lloyd (Warp), Software Engineering Is Becoming Factory Engineering, AIE CODE 2026
[5] https://www.youtube.com/watch?v=SIBdHRrk8os&t=22243 — Wendy Breiding (Microsoft), Beyond Autocomplete: Getting the Most from GitHub Copilot for .NET, .NET Conf 2026
[6] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[7] https://ai.engineer/code/2026/talks/melvin-johnson — Melvin Johnson (Google DeepMind), Train on the engineering work that still fails, AIE CODE 2026
[8] https://ai.engineer/code/2026/talks/jeffrey-pinner — Jeffrey Pinner (Exa), What Your AI Doesn't Know, AIE CODE 2026
[9] https://ai.engineer/code/2026/talks/diogo-almeida — Diogo Almeida (TypeSafe AI), Beyond Better Assistants: Software That Can Make a Decision, AIE CODE 2026
[10] https://huggingface.co/papers/2611.15777 — SO-Arena: Benchmarking the Capability Spectrum and Reliability of System One Models (arXiv 2611.15777)
[11] https://ai.engineer/code/2026/talks/online-cline-rsi — Ara Khan (Cline), The Improvement Loop Is the Product, AIE CODE 2026
[12] https://dora.dev/insights/finding-balance-in-the-era-of-tokenmaxxing — DORA, Finding balance in the era of tokenmaxxing
[13] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AIE CODE 2026
[14] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[15] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AIE CODE 2026
[16] https://github.com/Parcha-ai/agentrun/blob/main/docs/case-studies/merchant-classification.md — AgentRun, Merchant classification case study
[17] https://ai.engineer/code/2026/talks/online-skills-knowledge — Nikolay Petrov, Your SKILL.md is 70% of Things the Model Already Knows, AIE CODE 2026
[18] https://arxiv.org/abs/2610.10961 — Bowen Xu & Boyu Chen, Cross-Provider Review as a Runtime Contract for Coding Agents: A Controlled Pilot and Fault-Injection Study (arXiv 2610.10961)
[19] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AIE CODE 2026
[20] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents, Amazon saves millions replacing Sonnet with Strands Decider
[21] https://developer.nvidia.com/blog/use-nvidia-nemo-to-turn-agent-failures-into-tests-and-harness-fixes — NVIDIA, Turn agent failures into tests and harness fixes
[22] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AIE CODE 2026
[23] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS), AWS Emulator and the engineer's job when agents write the code
[24] https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature — Google Research, Advancing science & engineering with Antigravity's /teamwork
[25] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AIE CODE 2026
[26] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[27] https://arxiv.org/abs/2602.11988 — ETH Zurich, Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (arXiv 2602.11988)
[28] https://arxiv.org/abs/2610.04832 — arXiv 2610.04832, Agent Skill Evolution: How Revisions Affect Coding Agents
[29] https://github.com/GoogleChrome/modern-web-guidance — Google Chrome, Modern Web Guidance (coding-agent skill, GitHub)
[30] https://arxiv.org/abs/2609.01437 — ByteDance Seed, HarnessDev (arXiv 2609.01437)
[31] https://ai.engineer/code/2026/talks/online-dmitry-maintenance — Dmitry Buykin (Maersk), Agents Made Code Free. Maintaining It Didn't Get Cheaper., AIE CODE 2026
[32] https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents — Anthropic, Demystifying evals for AI agents
[33] https://arxiv.org/abs/2406.12045 — Yao, Shinn, Razavi & Narasimhan (Sierra), τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (arXiv 2406.12045)
[34] https://arxiv.org/abs/2411.00640 — Evan Miller (Anthropic), Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations (arXiv 2411.00640)
[35] https://arxiv.org/abs/2510.09738 — Han, Titericz Junior, Balough & Zhou (NVIDIA), Judge's Verdict: A Comprehensive Analysis of LLM Judge Capability Through Human Agreement (arXiv 2510.09738)
[36] https://arxiv.org/abs/2603.29231 — Khanal, Tao & Zhou, Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents (arXiv 2603.29231)
[37] https://www.infoq.com/presentations/elastic-ai-agent-evaluations — Susan Chang (Elastic), Building Reusable Evaluation Frameworks for Agentic AI Products, QCon AI Boston 2026
[38] https://www.infoq.com/presentations/ai-agent-testing-evaluation — Zhou Yu (Arklex AI; Columbia University), From AI Agent Demo to Production: Automated Testing and Evaluation, QCon AI Boston 2026
[39] https://www.infoq.com/presentations/context-as-code-devops-agents — Patrick Debois (Tessl), Context is the New Code, QCon London 2026
