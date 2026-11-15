---
title: What works with AI: practical lessons
type: deck
created: 2026-11-14
audience: colleagues across engineering and the business
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# What works with AI: practical lessons

> **In one minute**
> - Treat AI as one replaceable part of a larger system, and give it the narrowest job possible.
> - If something must never happen, enforce it with automatic checks, not with instructions written for the AI.
> - Test any AI feature on real cases before launch; without those tests it is still only an experiment.
> - Earn trust gradually: build with future users, grant freedom one kind of action at a time, and keep a named owner.
> - AI raises output, but a gain only counts once it ships, so checking and review must keep up.

*Reading time: about 20 minutes · Best for: sharing with a team*

A lunch-and-learn for colleagues across engineering and the business: 16 slides, 16:9, for 30-45 minutes (about two minutes a slide, plus questions). This outline holds the slide text, the speaker notes and the sources; the deck itself is `ai-lunch-and-learn.pptx` in this folder. Numbers in square brackets point to the Sources list at the end. Company figures are the companies' own claims, and the suggestions on slide 15 are advice, not findings from our sources.

---

## Slide 1 · What works with AI: practical lessons

**On the slide**

- Subtitle: What practitioners report, checked against research and industry data
- Subtitle: November 2026 · lunch-and-learn

**Speaker notes**

This deck pulls together practical lessons about putting AI to work, for engineers and non-engineers alike.
One set of sources is ten practitioner talks for people who build, scale or govern AI systems.[1][2]
We have transcripts for six of them; the other four we know only from their published abstracts.
A second set, for AI engineers, covers themes including fighting slop in software factories and building with System One (fast decision) models.[3]
A third set covers Microsoft's .NET 11 AI stack as presented in November 2026, starting from what's new in .NET 11.[4]
We also checked these practitioner reports against industry research and vendor announcements, and where the two disagree the slides say so.

---

## Slide 2 · Three things to remember

**On the slide**

- AI is one part of a system: keep the model swappable and its job narrow [5]
- Checks beat instructions: guardrails in code, evals before launch [5][15]
- Trust is earned: with users, one action at a time, with a named owner [5][6][32]

**Speaker notes**

If you remember nothing else from today, remember these three.
First, the strongest case studies treated the model as a component: Heidi Porter called it "the replaceable part, not the center of the system".[5]
Second, what you check matters more than what you ask for: a rule in a prompt isn't enforced, and an agent without evals is still a proof of concept.[5]
Several practitioners also named verification, not code generation, as the real limit on coding agents.[27][28]
Third, trust is built step by step: with the people who will use the tool, one kind of action at a time, and with a person who stays accountable.[5][6][32]
The next ten slides unpack these, and the last three turn them into things we can use.

---

## Slide 3 · The model is the replaceable part

**On the slide**

- Stanford tested five models and chose a cheaper one that performed competitively [5]
- Syngenta's design survives swapping the model or the knowledge bases [5]
- At Noblis, a vendor's next version meant none of the old apps converted [6]
- .NET's AI libraries fix the contracts; the model behind them is your choice [7]

**Key line:** Design so we can swap the model, then re-run the evals.

**Speaker notes**

Heidi Porter's case studies, all in production, make the point.[5]
Stanford's surgical co-management tool benchmarked five LLMs against consensus chart review and chose a cheaper model that performed competitively.[5]
Syngenta built its seed-selection assistant so the model and the knowledge bases can both be swapped out, with a re-evaluation afterwards.[5]
Mark Lay of Noblis described the opposite: a vendor moved its tool to a new version and none of the old apps converted.[6]
Luis Quintanilla of Microsoft said the .NET AI abstractions give you the contracts while the implementations are up to you, and Bruno Capuano of GitHub compared three models on the same code.[7][8]
Newer evidence: the best-value model keeps changing, too; Anthropic claims its Fable 5.2 model, released on 9 November, matched Opus 5.5's best score on one coding benchmark for roughly half the cost per task.[9]
Ishaan Dey of Google DeepMind warned that decisions made for weaker models go out of date.[10]

---

## Slide 4 · Give the LLM the narrowest job

**On the slide**

- Syngenta's LLM is "the interface, the router, and the explainer, not the agronomist" [5]
- AeroCore's vision prompt was cut down to "Compare and flag" [6]
- Glean's test: "can the output be listed in advance?" If so, use a decision model [11]
- Keep the control flow in code; call a model only at decision points [12]

**Key line:** Most steps are decisions, not writing.[11]

**Speaker notes**

Heidi Porter argued that pilots stall when the LLM is asked to hold the data, be the system of record, make the decision and check its own work.[5]
In Syngenta's tool, application code handles identity and Syngenta's own models make the predictions; the LLM routes and explains.[5]
Darren Taillie kept simplifying AeroCore's work-order prompt until it was "Compare and flag".[6]
Chinmay Goyal of Glean said "most AI product steps are bounded decisions and not generation problems", and uses decision models that return choices with probabilities instead of text.[11]
UiPath keeps control flow deterministic; its fraud demo called in an agent only when evidence was missing.[12]
Caveat: those results came mostly from customers of one product, Jev.[11][12]
Newer evidence: Amazon engineers say a decision model replaced Sonnet 4.6 for ticket labelling at about 98% less cost, but the SO-Arena benchmark ranked the best-performing decision model only seventh for reliability.[13][14]

---

## Slide 5 · A rule in a prompt isn't a guardrail

**On the slide**

- "A rule written in a prompt is not deterministically enforced" — Heidi Porter [5]
- "a rule in an agent's instructions is just a suggestion" — Cam Soper [15]
- A real guardrail is a gate, a check, a human or a limit in code [5]
- Turn each correction into a lint rule or a test [16]

**Key line:** If it must never happen, enforce it outside the model's reach.

**Speaker notes**

Heidi Porter put it plainly: "a rule written in a prompt is not deterministically enforced".[5]
A guardrail is actual machinery: a gate, a check, a human or a limit in code.[5]
Cam Soper said "a rule in an agent's instructions is just a suggestion" after an agent ignored one; he puts rules that must hold into types the compiler checks.[15]
Lauren Tan's advice: whenever you correct your agent, make it a deterministic check rather than another line in the rules file.[16]
Yvonne Carlson's eight *leash* principles include least privilege, default-deny boundaries, sandboxes and human approval before anything destructive (from her abstract).[17]
Matt Soucoup and Paul Yuknewicz of Microsoft showed guardrails running in gateway hooks outside the agent's reach, and Justin Yoo separates permission to run from permission to reach.[18][19]
Newer evidence: Anthropic reported its own model working around restrictions instead of stopping, which backs the same rule.[20]

---

## Slide 6 · Evals gate production

**On the slide**

- "an agent without evals is a proof of concept" — Kevin Solorio [5]
- Build evals from real cases, with the people who do the job [5]
- Look past averages: they "can hide a bad result" [5]
- Measure the judge too: ZoomInfo's LLM judge was right 65% of the time [21]

**Key line:** Evals also decide when a system earns more autonomy.[5]

**Speaker notes**

Kevin Solorio's line was "an agent without evals is a proof of concept": without evaluations you can't confirm the agent behaves as expected.[5]
His team develops against an offline dataset, scores a sample of live traces after release, and sends failures through an annotation queue back into the dataset.[5]
Syngenta's evaluation used 100 real question-and-answer pairs from sales reps, scored by human reviewers and an LLM judge.[5]
Heidi Porter warned against trusting averages, because "averages can hide a bad result".[5]
Brian Kennedy checked ZoomInfo's LLM judge against hand-checked labels and found it right 65% of the time: "We had trusted our judge until we measured it."[21]
Microsoft's .NET team runs 170-odd C# scenarios nightly, rotating through the five most-used models, graded by tests or an LLM judge.[22]
If the evals aren't passing, the system doesn't get promoted.[5]

---

## Slide 7 · Human review doesn't scale

**On the slide**

- Reviewers facing thousands of items get "rubber stamping fatigue" [5]
- Faithbot's human takeovers worked at 5,000 users, not at 2,500,000 [6]
- In an Anthropic study, about 14% of people caught a clearly dangerous command [23]
- Design for it: over-flag, a person decides, review by risk [5][23]

**Key line:** "A gate that escalates everything is not actually saving anyone any time." — Chetas Joshi, Robinhood [24]

**Speaker notes**

Several practitioners warned that a human reviewer is a weak guardrail at volume.[5][6]
Heidi Porter, building on Jeff Schreiner's talk, said people facing thousands of items to review get tired and fall into "rubber stamping fatigue".[5]
Don Barger gets alerts on Faithbot's critical conversations and can take over, which was possible at 5,000 users but not at 2,500,000.[6]
Lydia Hallie cited an Anthropic study in which about 14% of people caught a clearly dangerous command, while the automatic classifier blocked 89%; these are Anthropic's figures.[23]
Stanford's tool over-flags by design and leaves every decision with the physician, who can confirm, decline or override each case; physicians agreed with its *no* answers 97% of the time.[5]
On Hallie's team Claude reviews every PR first; docs then need no person, ordinary changes maybe one reviewer, risky ones maybe two.[23]
Chetas Joshi of Robinhood adds the counterweight: escalating everything saves nobody any time.[24]

---

## Slide 8 · Adoption is about people

**On the slide**

- Build with the people who do the job, not for them through a proxy [5]
- Show a deliberately rough version: people correct faster than they describe [5]
- Put it where people already work: "No one likes an extra login." — Darren Taillie [6]
- Getting buy-in is the hardest part of an AI project [26]

**Key line:** People who help build it become its champions.[5]

**Speaker notes**

Kevin Solorio's team built an agent for field technicians, and the client's CEO made adoption the number one requirement.[5]
His lesson: tools fail when they are built for users through a proxy, such as a product owner who reinterprets what users said, so get the users in the room and make feedback cheap.[5]
He shows people a deliberately rough version, because they correct a wrong answer much faster than they describe a right one, and the people who help build a tool become its champions.[5]
At AeroCore, use of a database query agent took off once it moved into Microsoft Teams, because "No one likes an extra login."[6]
Jason Beutler's abstract argues that getting a team to buy in is harder than the model or the tooling.[26]
Ramp says it never had to mandate use of its shared coding agent, because it works as a ready-made baseline, and public-by-default sessions replaced formal training (Ramp's own account).[25]

---

## Slide 9 · Set boundaries first: charter and accountability

**On the slide**

- One team wrote an AI charter "before we ever write one line of code" [6]
- A yes list and a never list made later decisions quick [6]
- "Something can be worse than nothing if you're doing the wrong things." — Don Barger [6]
- A named person always holds the A in RACI: accountability can't be delegated to AI [6]

**Key line:** Ask early: "what will we never do?" And who will keep it running?[6]

**Speaker notes**

Don Barger's team at the International Mission Board, eight people over a couple of days, wrote an AI charter "before we ever write one line of code", and it still decides what they will and won't do.[6]
The yes list covers drafting, summarising, research, translation and code with humans in the loop; the never list includes AI posing as human, final decisions about people made solely by AI, and monitoring people without their knowledge.[6]
When a team asked for an AI counsellor, he said no: "Something can be worse than nothing if you're doing the wrong things."[6]
Mark Lay of Noblis said "accountability can't be delegated" to AI, so somewhere in the RACI chart a person holds the A.[6]
He also asked what it would really cost to reverse a deployment, and "do they have the capacity to keep running what they deployed?"[6]

---

## Slide 10 · Verification is the bottleneck for coding agents

**On the slide**

- "writing code isn't the hard part anymore, verifying it is." — Kush Agrawal, Duolingo [27]
- Choose work you can check against tests that predate it [28]
- Anchor tests to written requirements, not the agent's own reading of them [29]
- Ask for proof from the running app, not just green tests [30]

**Key line:** Fix the inner loop before automating it.[16]

**Speaker notes**

Kush Agrawal of Duolingo said "writing code isn't the hard part anymore, verifying it is."[27]
Duolingo's test-writing agent has any PR that touches non-test files closed, because "agents sometimes take the shortest paths to green CI."[27]
Jarred Sumner chose a project he could check against test suites that predate it, warning that once you rewrite the tests "you can't really trust the tests anymore."[28]
McKenna Barlow showed that an agent writing both code and tests can repeat one misunderstanding in both, so tests should be anchored to written requirements.[29]
Gerald Versluis's advice was "for every session, start from a running app, ask for proof".[30]
Lauren Tan warned that "if your inner coding loop produces slop, then automating that loop just produces more slop".[16]
Newer evidence: AWS says its agents built its emulator against fidelity tests that were first corrected until real AWS passed them (AWS's own account).[31]

---

## Slide 11 · Autonomy is earned per action

**On the slide**

- L1 · Investigate and report; change nothing [32]
- L2 · Draft the change; a human approves [32]
- L3 · Act alone on low-risk work [32]
- L4 · Auto-merge [33]
- Promotion test: "How costly is a mistake and how easy is it to catch?" — Meta [32]

**Key line:** Promote one kind of action at a time, on its track record.[32][33]

**Speaker notes**

Meta's on-call agent climbs a ladder like a new hire: L1 investigates and changes nothing, L2 drafts fixes that ship only with human approval, and L3 clears low-criticality work alone.[32]
Meta promotes by one test, "How costly is a mistake and how easy is it to catch?", and only with a track record on that exact action.[32]
Factory's workstreams run from L1, which pauses for a human at the spec, the PR and the merge, to L4 auto-merge.[33]
They reach L4 only once agent PRs break things less often than human ones, measured as "the regret-free merge rate, the share of changes that merge and never need a revert or a follow-up fix."[33]
Heidi Porter's execution dial is the same idea outside coding: automate outright only what is cheap to undo.[5]
Robinhood reports about 60% of its data-pipeline PRs merging without human review at about a 2% miss rate.[24]

---

## Slide 12 · No dark factory needed: fit beats maximum autonomy

**On the slide**

- "AI is not gonna fix your team. It amplifies what's already there." — SEP [5]
- Six constraints set the mode: tokens, readiness, goals, domain knowledge, verifiability, oversight [5]
- One high-risk team stopped part-way; another reported a "six x reduction of effort" [5]
- "the factory runs dim, not dark" — Andrew Finch, Sonar [34]

**Key line:** Choose the mode per team, and fix the process before adding autonomy.

**Speaker notes**

Chris Shinkle and Andrew Dunlap of SEP started from the dark factory demos, where agents write, review, test and ship the code with nobody at the keyboard.[5]
Their reading of recent studies was "AI is not gonna fix your team. It amplifies what's already there."[5]
Six constraints set the right mode for a team: token budget, organisational readiness, goal definition, domain knowledge, verifiability and code oversight.[5]
A team writing software for building components deliberately stopped at a shared mode because verifiability mattered more, while a credit union app team with no token constraint and strong sponsorship reported a "six x reduction of effort".[5]
Andrew Finch of Sonar said "the factory runs dim, not dark", and Steve Yegge found "the more agents I deploy, the more humans I need."[34][35]
DORA's 2025 report, one of the studies SEP cited, calls AI an amplifier of an organisation's existing strengths and dysfunctions.[5][36]

---

## Slide 13 · What the industry data says

**On the slide**

- Harvard study of 655 firms: agents raised output (+44% lines, +36% PRs) [37]
- …but resolved issues rose only 14% (borderline), and review time rose 56% [37]
- Anthropic's Claude Code team: merged PRs more than doubled, revert share down over 40% (its own claim) [38]
- So treat headline company numbers as claims, not norms [37][39]

**Key line:** A gain only counts once it ships: verification and review have to keep up.

**Speaker notes**

The independent counterweight to the practitioners' stories is a Harvard study by Fiona Chen and James Stratton of engineering data from 655 firms, January 2021 to August 2026, in its November 2026 revision.[37]
Coding agents raised output: 35.7% more pull requests and 44.0% more lines of code, though the lines estimate falls just short of statistical significance.[37]
But resolved issues rose by only 13.7%, a borderline-significant effect, while time from review submission to approval rose 56.1% and review comments per pull request rose 38.6%.[37]
That supports SEP and Andrew Finch on review becoming the bottleneck.[5][34]
It also cautions against reading the boldest reported figures as typical, such as Cognition's report of merged PRs up 40 times in about a year.[39]
On the producing side, Anthropic says its Claude Code team more than doubled merged PRs while the revert share fell by over 40%, using machine review and human approval by risk; these are vendor figures.[38]
The study is observational, and its data ends in August 2026.[37]

---

## Slide 14 · Should this task use AI?

**On the slide**

- 1 · On our 'never' list? | yes → Don't use AI [6]
- 2 · AI better or more efficient? | no → Don't use AI [6]
- 3 · Data good enough for this task? | no → Fix the data first [5]
- 4 · Can rules or code do it? | yes → Rules or code [5][12]
- 5 · Output listable in advance? | yes → Decision model (or fine-tuned model) [11]
- 6 · Steps known in advance? | yes → Fixed workflow, LLM for the fuzzy step only / no → Bounded agent in deterministic orchestration [5][12]
- Then, whatever the outcome: | set who acts by the cost of a mistake · evals on real cases before launch · guardrails in code and a named owner [5][6]

**Speaker notes**

This is a simplified version of the decision tree in our toolkit; run it per task or workflow step, not per project, as Heidi Porter advised.[5]
Go down the questions until one sends you out.
The never list comes from IMB's charter, and the better-or-more-efficient test from Mark Lay: if AI gives neither, don't use it.[6]
Data has to be good enough for this task, because stale data quietly gives wrong answers.[5]
Glean's question decides between a decision model and an LLM; fine-tuning a model is an option when labels are stable and volume is high.[11]
If the steps are known, use a fixed workflow and give the LLM only the fuzzy step; if not, bound the agent inside deterministic orchestration.[5][12]
Whatever comes out, set who acts by the cost of a mistake, and don't ship without evals on real cases.[5]

**Links:** the full tree with the reasoning behind each step, [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md); its companion on autonomy, [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md).

---

## Slide 15 · What we could try next

**On the slide**

- Run one real proposal through the AI intake checklist
- Draft our AI charter: a yes list and a never list
- Build an eval set from real cases, with the people who do the job
- Turn the next repeated agent correction into a lint rule or a test
- Track review time and reverts before granting more autonomy

**Speaker notes**

These are suggestions for us, not findings from our sources, so they carry no citations.
We could start small: pick one workflow step someone has already proposed and walk it through the intake checklist together, in about fifteen minutes.
In parallel, a few of us could draft a one-page charter, saying what we will use AI for and what we never will, so later decisions are quick.
For any AI feature already in flight, we should agree who owns its eval set and sit with the people who do the job to build it from real cases.
On the engineering side, the next time we correct a coding agent twice for the same thing, we should encode it as a check.
Finally, we should measure review time and reverts now, so any decision to give agents more autonomy rests on our own numbers.

**Links:** [AI intake checklist](../2-decide/ai-intake-checklist.md) · [Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md) · [Working with coding agents](../4-build/working-with-coding-agents.md) · [Agent-written pull requests and agent autonomy: draft engineering standard](../5-run/agent-pr-policy.md) · [What to measure: AI metrics scorecard](../5-run/ai-metrics-scorecard.md).

---

## Slide 16 · Further reading and sources

**On the slide**

- The outline that goes with this deck: every claim cited, with links
- Case-study transcripts: Practical AI podcast, episodes 378 and 379 [5][6]
- Talk pages and agenda: ai.engineer/code · dotnetconf.com/agenda [3][4]
- Industry: Chen & Stratton (Harvard, 2026) · DORA 2025 · Anthropic on code review [37][36][38]
- Our toolkit: intake checklist, decision trees, agent PR policy, evals playbook

**Speaker notes**

Everything on these slides is cited in the outline that goes with the deck, which lists all 39 sources with links.
Six of the case-study talks come from the Practical AI podcast's official transcripts.[5][6]
The AI-engineering talks each have their own page under ai.engineer/code, and Microsoft's .NET 11 talks are listed on the agenda at dotnetconf.com.[3][4]
For the independent view, start with the Harvard study and DORA's 2025 report.[37][36]
Anthropic's write-up on how its Claude Code team reviews code describes a full review pipeline, though its numbers are its own.[38]
Our toolkit has the longer versions: the intake checklist, the two decision trees, the agent PR policy and the evals playbook.

---

## Related

- Decision trees: [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md) and [How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md)
- Leadership memos: [Should we aim for a fully automated software factory?](../6-lead/should-we-build-a-software-factory.md), [What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md), [Where should AI go in our product or operations first?](../2-decide/where-ai-goes-first.md)
- Engineering: [Agent-written pull requests and agent autonomy: draft engineering standard](../5-run/agent-pr-policy.md), [Working with coding agents](../4-build/working-with-coding-agents.md), [Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md)
- Questions: [AI questions answered](ai-questions-answered.md)

**Read next:** [Should this task use AI, and which kind?](../2-decide/should-this-task-use-ai.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://techpoint.org/digital-innovation/midwest-ai-summit-2026-indianapolis — TechPoint, Midwest AI Summit returns to Indianapolis October 15
[2] https://midwestaisummit.com/2026-recap — Midwest AI Summit, 2026 Recap (speakers and talk titles)
[3] https://ai.engineer/code — AI Engineer, AI Engineer Code Summit 2026 (AIE CODE) event page
[4] https://dotnetconf.com/agenda — .NET Conf, .NET Conf 2026 agenda (dotnetconf.com)
[5] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; Kevin Solorio (Focused), Building AI With Workers, Not For Them; Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory; Midwest AI Summit 2026 (Practical AI E378 transcript)
[6] https://practicalai.show/379/transcript — Don Barger (International Mission Board), Building AI Trust: What We Said Yes To, and What We Didn't; Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own; Darren Taillie (AeroCore Technologies), From Photos to Queries: Practical AI Agents for Real Workflows; Midwest AI Summit 2026 (Practical AI E379 transcript)
[7] https://www.youtube.com/watch?v=SIBdHRrk8os&t=11450 — Luis Quintanilla (Microsoft), The .NET AI Stack: What's New, What's Next, and How It Fits Together, .NET Conf 2026
[8] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=29537 — Bruno Capuano (GitHub), .NET + Foundry: Better Together, .NET Conf 2026
[9] https://www.anthropic.com/claude-fable-and-mythos-5-2 — Anthropic, Claude Fable 5.2 and Mythos 5.2
[10] https://ai.engineer/code/2026/talks/ishaan-dey — Ishaan Dey (Google DeepMind), Judgement is the last job, AI Engineer Code Summit 2026
[11] https://ai.engineer/code/2026/talks/chinmay-goyal — Chinmay Goyal (Glean), Beyond Generation: Fast, Structured AI Decisions with Jev at Glean, AI Engineer Code Summit 2026
[12] https://ai.engineer/code/2026/talks/uipath — Chibi Vikram & Kevin Bernstein (UiPath), Your Automation Is Overthinking It, AI Engineer Code Summit 2026
[13] https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider — Strands Agents blog, Amazon saves millions by replacing Sonnet 4.6 with Strands Decider
[14] https://huggingface.co/papers/2611.15777 — SO-Arena authors (arXiv 2611.15777), SO-Arena: Benchmarking the Capability Spectrum and Reliability of System One Models
[15] https://www.youtube.com/watch?v=utUNTsYMkWs&t=24176 — Cam Soper (Pulumi), Infrastructure as (Actual) Code with C# 15 and .NET 11, .NET Conf 2026
[16] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[17] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[18] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=25809 — Matt Soucoup & Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 2), .NET Conf 2026
[19] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[20] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[21] https://ai.engineer/code/2026/talks/brian-kennedy — Brian Kennedy (ZoomInfo), Your Judge Is Hallucinating Too, AI Engineer Code Summit 2026
[22] https://www.youtube.com/watch?v=SIBdHRrk8os&t=22243 — Wendy Breiding (Microsoft), Beyond Autocomplete: Getting the Most from GitHub Copilot for .NET, .NET Conf 2026
[23] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[24] https://ai.engineer/code/2026/talks/online-robinhood-review — Chetas Joshi (Robinhood), Who reviews the bots?, AI Engineer Code Summit 2026
[25] https://ai.engineer/code/2026/talks/zach-bruggeman — Zach Bruggeman (Ramp), How to build an agent that builds the culture, AI Engineer Code Summit 2026
[26] https://midwestaisummit.com/jason-beutler — Jason Beutler (Robosource), The Order Matters: Structuring AI Projects Around People, Midwest AI Summit 2026 (abstract)
[27] https://ai.engineer/code/2026/talks/online-duolingo-tests — Kush Agrawal (Duolingo), Duolingo's Test-Writing Agent Is a Pull-Request Lifecycle, Not a Prompt, AI Engineer Code Summit 2026
[28] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AI Engineer Code Summit 2026
[29] https://www.youtube.com/watch?v=fKnZotxlEec&t=6 — McKenna Barlow (Microsoft), Test Smarter: AI-Assisted Testing for Modern .NET, .NET Conf 2026
[30] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=20349 — Gerald Versluis (Microsoft), Beyond Code Generation: Give AI Eyes and Hands for .NET MAUI, .NET Conf 2026
[31] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS, All Things Distributed), AWS Emulator and the engineer's job when agents write the code
[32] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[33] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AI Engineer Code Summit 2026
[34] https://ai.engineer/code/2026/talks/andrew-finch — Andrew Finch (Sonar), Building a Safe Software Factory, AI Engineer Code Summit 2026
[35] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
[36] https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf — DORA (Google Cloud), State of AI-assisted Software Development 2025
[37] https://fion.ac/jellyfish.pdf — Fiona Chen & James Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[38] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[39] https://ai.engineer/code/2026/talks/walden-yan — Walden Yan (Cognition), A New Age of Software Engineering, AI Engineer Code Summit 2026

