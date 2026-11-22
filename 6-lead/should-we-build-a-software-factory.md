---
title: "Should we aim for a fully automated software factory?"
type: memo
created: 2026-11-14
audience: senior leadership and engineering leads
status: checked
last_checked: 2026-11-22
as_of: "November 2026"
---

# Should we aim for a fully automated software factory?

> **In one minute**
> - A fully automated software factory (AI agents building and shipping code with nobody involved) should not be a goal in itself.
> - Choose how much to automate team by team, according to each team's constraints, not one target for everyone.
> - Make every change checkable by machine, and fix checking and review before giving agents more freedom.
> - Let agents earn freedom one kind of action at a time, based on a measured track record.
> - Point early automation at existing products, such as small bug fixes, and keep new-product discovery led by people.

*Reading time: about 5 minutes · Best for: leaders*

## Question

Demos of *dark factories*, where agents write, review, test and ship code with nobody involved, raise an obvious question for leadership.[1] Should that be our goal, and how fast should we move towards it?

## Short answer

No: a fully automated factory should not be a goal in itself. The evidence says to match agent autonomy to our constraints, and to let each kind of action earn more autonomy from a measured track record.[1][3] Even Andrew Finch (Sonar), who argues for automating review, keeps people auditing risky code, reviewing architecture and engineering the factory itself: the factory "runs dim, not dark".[4]

## Recommendation

1. **Choose a mode per team, not one target for the whole organisation.** A mode is how a team works with agents, from each developer working with their own agent up to a fully automated factory.
   Score each team against the six constraints below; regulated or safety-critical work will stay closer to individual, human-checked use.
2. **Fix verification and review before adding autonomy.** Make every change checkable by machine, with tests that predate the work and that agents can't edit. Turn repeated agent corrections into lint rules or tests, and gate merges on recorded evidence.
3. **Grant autonomy per kind of action, on a ladder.** Agents investigate and report (L1), then draft changes for approval (L2), then act alone on low-risk work (L3), and only then auto-merge (L4). Promote an action when its mistakes are cheap and caught early, and a track record backs it; allow auto-merge only once its regret-free merge rate (changes that never need a revert or follow-up fix) beats our engineers'.
4. **Point early factory-style automation at brownfield work.** Good first targets are flaky tests and small bug fixes on products we already run. Agents can draft dependency updates too, but the [agent PR policy](../5-run/agent-pr-policy.md) makes those Risky-tier: two human reviewers, and never beyond drafting for a person to approve (L2). Keep new-product discovery human-led.
5. **Budget for people and tokens, not just licences.** Name an owner for each automated workstream, keep humans on architecture and high-risk review, and review token spend monthly.

## Options considered

- **Aim for a dark factory now.** Highest potential throughput, but it needs a generous token budget, written-down domain knowledge and automated verification; without them AI amplifies whatever is weak today.[1]
- **Keep agents as individual assistants, with humans reading every line.** Lowest risk and least disruption, but Doug Clauson reports that Amazon teams bolting AI onto an unchanged process saw 10–20% gains, and a person acting as the agent's feedback loop becomes the bottleneck.[6]
- **Match autonomy to constraints and earn it per action (my recommendation).** Slower headline gains and up-front investment in measurement and verification, but gains are kept and risk stays in proportion to the work.

## What the evidence says

- **Fit beats maximum autonomy.** SEP, a firm that builds software for clients, finds its teams working in four modes, spread along a scale of agent autonomy from individual agentic coding to a dark factory (Chris Shinkle and Andrew Dunlap).[1]
  Shinkle sums up three recent studies as "AI is not gonna fix your team. It amplifies what's already there."[1]
  Six constraints set a team's mode: token budget, organisational readiness, goal definition, domain knowledge, verifiability and code oversight.[1]
  A two-day prototype stalled on the way to production because tokens ran out, knowledge sat in people's heads and millions of input parameters left outputs unverifiable at scale.[1]
  Dunlap's own building-components team chose to stop part-way ("Buildings don't fall down"), while a team rebuilding a credit union's mobile banking app, with no token limit, reported a "six x reduction of effort".[1]
- **Autonomy is earned per action.** Meta's on-call agent climbs from investigating and reporting, to drafting fixes that ship only with approval, to clearing low-criticality work alone. Promotion turns on "How costly is a mistake and how easy is it to catch?"[3] Factory's workstreams run from L1, which pauses for a human at the spec, the PR and the merge, to L4 auto-merge, reached only when agent PRs break things less often than human ones, measured as "the regret-free merge rate".[2]
  These are Factory's own levels: in my reading, its L1 is close to L2 on the ladder in recommendation 3, since it already drafts work for a person to approve.
- **Review moves; it doesn't vanish.** Andrew Finch argues that once coding is automated the bottleneck moves to review, so the merge gate should judge recorded evidence against criteria the team writes down, letting low-risk PRs be auto-approved.[4] Lydia Hallie says her Anthropic team tiers human review by risk: no person for docs or copy, perhaps one reviewer for ordinary changes, and maybe two for risky ones.[5] Kiro's team uses six specialised agent reviewers and says "we've stopped reviewing code a long time ago", but people own the review record and fix the process.[6]
- **Unattended automation multiplies slop.** Dexter Horthy describes a factory as the existing delivery pipeline with an agent doing the build, plus forward pressure (what starts work) and back pressure (agent review and testing, CI, linters) that improves quality without humans.[7] Lauren Tan: "if your inner coding loop produces slop, then automating that loop just produces more slop".[8] Jarred Sumner picked work he could check against test suites that predate it, and warns that once a project means rewriting its tests, you can no longer trust them.[9]
- **Start with brownfield.** Justin McCarthy advises against pushing uncertain greenfield ideas through a factory. Point it at existing products instead, and write their *promises* (features, performance, cost, security) as loops that agents keep continuously.[10]
- **One team rebuilt around its agent.** Cognition runs its lifecycle on its own agent by default, escalating to people for judgement, after rebuilding its infrastructure and team shape. It reports merged PRs up 40x in about a year while headcount grew 2.7x.[11]
- **People remain the limit.** Steve Yegge, running about 50 agents, found "the more agents I deploy, the more humans I need", and that after he yelled at his factory, its agents piled on so many rules that "nothing ever happened".[12] Armin Ronacher: "human attention is for me at least the limiting factor".[13]

### Newer evidence

- **Independent data tempers the throughput claims.** A Harvard study of engineering data from 655 firms (revised November 2026) found coding agents raised output (44.0% more lines of code, an estimate the paper calls marginally insignificant, and 35.7% more pull requests) but resolved issues by only 13.7%, a borderline-significant rise, while time from review submission to approval rose 56.1%.[14] In my reading, this supports SEP and Finch on review as the bottleneck, and contradicts any claim that Cognition's or Kiro's figures are typical: on average, the extra code has not turned into proportional gains in shipped software. The data is observational and ends in August 2026.[14]
- **Risk-tiered review is now documented practice.** Anthropic's Claude Code team moves most reading to machines and uses a risk classifier to set how many people must approve (none, one or two). It reports merged PRs more than doubling from June to September while the revert share fell by over 40%, but admits it has no automatic brake yet that tightens approval when reverts rise.[15] These are vendor figures, from a team with unusual tooling.
- **Autonomous agents lean on checks they can't edit.** AWS's agents build its emulator against fidelity tests first corrected until real AWS passes them, behind security-agent merge gates and deterministic checks that stop agents touching code they shouldn't. Swami Sivasubramanian supervised a Kiro agent rebuilding a replication engine for four nights before seeing it had no way to check its results; with a spec and a test environment it took about two hours (AWS's account).[16] DeepMind had Lean check every agent proof about Signal's protocol code, while the agents flagged about 1% of the codebase for human review, and Google's /teamwork filters parallel attempts through falsifiers such as unmodified test suites (both their own claims).[17][18]
  In my reading, all three cases, AWS's, DeepMind's and Google's, support Sumner and Tan.

## Risks and what would change this advice

- **Moving too slowly.** Rivals with fewer constraints may gain speed, so we should revisit each team's mode quarterly; budget and sponsorship are ours to change.
- **False confidence.** Most figures above are the companies' own claims, without controlled baselines. Our own revert, incident and regret-free merge data should outweigh them.
- **What would change it.** If a team's agent changes break things less often than human ones on our own metrics for a sustained period, with verification automated end to end, its low-risk work can get wider autonomy. Rising reverts or incidents should move an action back down a rung.

**Read next:** [Can AI replace our people?](can-ai-replace-our-people.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://practicalai.show/378/transcript — Chris Shinkle & Andrew Dunlap (SEP), Not Every Team Needs a Dark Factory, Midwest AI Summit 2026 (Practical AI E378 transcript)
[2] https://ai.engineer/code/2026/talks/luke-alvoeiro — Luke Alvoeiro (Factory), Earning Autonomy: From Missions to Workstreams, AI Engineer Code Summit 2026
[3] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula and Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[4] https://ai.engineer/code/2026/talks/andrew-finch — Andrew Finch (Sonar), Building a Safe Software Factory, AI Engineer Code Summit 2026
[5] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[6] https://ai.engineer/code/2026/talks/doug-clauson — Doug Clauson (AWS, Kiro), Ship More as a Team of One with Kiro Crew, AI Engineer Code Summit 2026
[7] https://ai.engineer/code/2026/talks/dexter-horthy — Dexter Horthy (Factory), A software factory needs pressure in both directions, AI Engineer Code Summit 2026
[8] https://ai.engineer/code/2026/talks/lauren-tan — Lauren Tan, All Code Is Slop (Except Mine), AI Engineer Code Summit 2026
[9] https://ai.engineer/code/2026/talks/jarred-sumner — Jarred Sumner (Anthropic), Choose the project you can verify, AI Engineer Code Summit 2026
[10] https://ai.engineer/code/2026/talks/justin-mccarthy — Justin McCarthy (Diffusion), Brownfield factories keep the promises you already made, AI Engineer Code Summit 2026
[11] https://ai.engineer/code/2026/talks/walden-yan — Walden Yan (Cognition), A New Age of Software Engineering, AI Engineer Code Summit 2026
[12] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
[13] https://ai.engineer/code/2026/talks/armin-ronacher — Armin Ronacher (Earendil), The Software Atelier, AI Engineer Code Summit 2026
[14] https://fion.ac/jellyfish.pdf — Fiona Chen & James Stratton (Harvard), Artificial Intelligence in the Firm: Bottlenecks in Software Production
[15] https://claude.dev/blog/solving-code-review-at-anthropic — Anthropic (Claude Code team), How the Claude Code team does code review
[16] https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html — Swami Sivasubramanian (AWS, All Things Distributed), AWS Emulator and the engineer's job when agents write the code
[17] https://deepmind.google/blog/introducing-alphaproof-code — Google DeepMind, Introducing AlphaProof Code: a breakthrough in verifying complex software at depth
[18] https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature — Google Research, Advancing science & engineering with Antigravity's /teamwork

