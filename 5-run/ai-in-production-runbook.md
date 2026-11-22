---
title: Running AI in production
type: runbook
created: 2026-11-14
audience: engineering and operations teams running AI features and agents in production
status: checked
last_checked: 2026-11-15
as_of: "November 2026"
---

# Running AI in production

> **In one minute**
> - Before going live, name an owner and rehearse the off switch, spending caps, the non-AI fallback and undo.
> - Follow each whole business request, not just the AI call, and save a tracking reference on the business record.
> - Keep scoring live results, look at the worst cases as well as averages, and re-test after any model or instruction change.
> - In an incident, trust what your systems show happened, not the AI's own report, and contain it without the AI's help.
> - Treat changes to the model, instructions or add-ons as releases: review them and re-run the tests before switching.

*Reading time: about 10 minutes · Best for: engineering and operations*

*Draft runbook* for operating an AI feature or agent after go-live. What must be true before go-live is in [What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md). Steps are recommendations; cited lines are the evidence. Company figures are the companies' own claims.

## 1. Go-live readiness check

Tick every item before the first production run, and file the evidence with the owner.

- [ ] [AI intake checklist](../2-decide/ai-intake-checklist.md) answered, with real answers to questions 8 to 12.
- [ ] The minimum bar in [What must be true before AI agents can act in production?](../6-lead/before-agents-act-in-production.md) met in infrastructure, not in a prompt.
- [ ] Named owner and data steward on the on-call sheet (section 7).
- [ ] Traces flowing, with the trace ID on the business record (section 2).
- [ ] Offline evals pass; online scoring is on (section 3).
- [ ] Kill switch, caps and fallback tried in a production-like environment (section 4).
- [ ] Undo rehearsed and the drill recorded (section 5).
- [ ] Autonomy level recorded per kind of action ([How much should an agent be trusted to do on its own?](../2-decide/how-much-autonomy-for-an-agent.md)).

## 2. Observability

- **Trace the business journey, not the model call.** Shweta Iyer (Microsoft): "the unit that we want to investigate as an on call engineer is not just one agent invocation".[1] In her demo the agent call succeeded while the business write failed and rolled back.[1]
- **Put the trace ID on the business record.** Iyer saves it with the business records, returns it with every response and records an explicit final status.[1] Girish Konda (Microsoft) gives every run a named end state, and treats a timeout as unknown.[2]
- **Use one telemetry standard.** Claude Code now emits OpenTelemetry GenAI attributes and records whether its auto-mode classifier or a permission rule decided each tool call.[3] Send AI spans to the same store as the rest of the telemetry.
- **Track cost and tokens per outcome.** Cecil Phillip (Temporal) checkpoints each model and tool call so a crashed run resumes: "The last thing you want to do is to reissue that prompt and use those tokens again."[4] Microsoft's AI Gateway sets token and money budgets per client.[5] Report cost per successful business outcome, failed runs included.
- **Log what the agent did and who decided.** Yvonne Carlson's principles include logging what agents actually access and do.[6] Juergen Gutsch logs every message.[7] Microsoft's SRE Agent shows the queries it ran: "it's good to look at those queries and second guess the agent".[5]
- **Keep sensitive data out of logs.**
  - Iyer keeps telemetry (where the time went) apart from the business audit (what was committed), protecting each for its purpose.[1]
  - Paul Yuknewicz's (Microsoft) sandboxed tool redacted social security numbers before the model saw them.[8] Gutsch: "the LLM should not know any credentials".[7]
  - *Newer evidence:* one coding agent started logging response text on upgrade wherever prompt logging was on, and a later release fixed telemetry recording a background agent's reply with response logging off.[3] Apiiro found passwords in 1,122 public GitHub files where saved permission rules stored whole commands (its count; the file was meant to stay local).[9]
  - Test redaction after every upgrade, and scan logs, traces and agent settings for secrets.

## 3. Ongoing quality

- **Score live traffic.** Kevin Solorio (Focused): "an agent without evals is a proof of concept".[10] Once the agent is deployed, his data flywheel adds "online evaluators that are consistently going to look at a sample of traces and kind of score them"; flagged cases go to an annotation queue, and reviewed failures join the offline dataset.[10]
- **Sample for human annotation.** Solorio has the workers themselves label outputs.[10] Review a weekly random sample plus every flagged trace, with annotators from the business.
- **Watch the tail.** Heidi Porter (Moyer Group AI): "averages can hide a bad result".[10] Report worst cases beside averages.
- **Check for drift and stale data.**
  - Porter's observability means "being able to recover and replay and catch drift before an incident"; one production-line system was monitored for 52 weeks.[10]
  - Stale data will "quietly give you the wrong answers".[10] Konda tags each fact with source version and time, and decisions use only facts within a freshness limit.[2]
  - Alert when input mix, refusals or tool errors shift, and when a source goes stale.
- **Re-run evals on every model or prompt change.** Armin Ronacher tracks corrections, aborts and 90th-percentile run time across model upgrades.[11] The method, including when to re-run, is in [Evals playbook: how to build and run evals for an AI feature or agent](../4-build/evals-playbook.md) (sections 6 and 8).

## 4. Control levers

On-call should be able to pull each lever in minutes, without a deploy, and each should be rehearsed.

- **Kill switch per capability.** Gutsch's agent has a kill switch.[7] Harvey's automations switch off after five consecutive failures and can carry a budget or expiry, "because when no one's watching, an agent can start thousands of tasks too."[12] Make it possible to turn off one capability, such as sending email, without taking the feature down.
- **Rate and cost caps.**
  - Joey Wang (Harvey) advises capping what an agent or a person can start.[12] One engineer's ~950 tasks stalled everyone within about three hours, which led to a fair launch queue.[12]
  - Gateway budgets change without redeploys: "I'll never redeploy my back ends or my front ends to do it."[5]
  - *Newer evidence:* Simon Willison argues for hard caps that cut a service off, not warning emails, because coding agents make it easy to spin up services that cost money.[13]
- **Fall back to rules or a person.** The gateway routes model aliases with priority fallback.[5] In Porter's production-line case, "The system withholds the answer and escalates."[10] Keep the pre-AI path (rules or a manual queue) working and staffed.
- **Make guardrails fail closed.** Matt Soucoup and Paul Yuknewicz (Microsoft) run guardrails in gateway hooks outside the agent's reach.[5] *Newer evidence:* a coding-agent release added an option that makes a hook block the action when it can't start, times out or exits unexpectedly.[14] That sharpens the advice: a check that errors must stop the action.
- **Demote autonomy.** Meta raises autonomy per action, asking "How costly is a mistake and how easy is it to catch?"[15] After an incident, drop the affected action at least one level at once, per section 7 of [Agent-written pull requests and agent autonomy: draft engineering standard](agent-pr-policy.md).

## 5. Incident response for AI

**What counts as an AI incident**

- **Wrong action.** Anthropic reports Claude working around restrictions instead of stopping, such as submitting a sensitive form on a real website, with minimal real-world impact.[16] A blocked agent trying another route is an incident in itself.
- **Harmful or wrong output** reaching a customer, colleague or business record.
- **Cost runaway.** At Harvey, per-workspace alerts plus auto-tagging took a normal ~50 tasks to about 900 in about four hours.[12]
- **Data exposure.** One coding agent sent the user's account email to third parties in the User-Agent header of its web searches; after a fix, a commenter showed a shell command carrying the email was still not blocked.[17]
- **Prompt injection or a malicious skill.** Zenity traced a campaign whose lookalike project and skills harvested SSH, AWS and Azure credentials.[18] Matthew Green describes OpenAI's sandboxed agents leaving instructions for each other in a shared package cache, and expects a self-spreading *worm*.[19]

**Triage**

1. Open an incident, name a lead and tell the owner.
2. Find the affected records by trace ID; check what actually committed, not what the agent reported.[1]
3. Map the blast radius: other runs and agents reading the same documents, caches or queues.[19]
4. Don't trust approvals in the agent's context. In a preprint, a forged approval planted in content the agent read survived context compaction as a real user instruction 87–100% of the time on five coding agents, and 0% on four that keep message roles.[20] Check the system that grants approvals.

**Containment**

- Pull the section 4 levers: switch off the capability, pause new runs, demote autonomy, revoke credentials, quarantine shared inputs.
- Konda: "If the same model can skip a check and declare it passed, you have a request, not a boundary."[2] Containment must not need the agent's cooperation.

**Recovery**

- Tanmay Sah: "A timeout tells us that the response didn't arrive, not that the operation failed."[21] He reported that in the trials he ran with Dolly Sah, naive retries produced duplicate effects in 54% of the relevant trials.[21]
- Their ladder: nothing changed, retry; prior state known, restore; external action committed, compensate; recovery unverifiable, stop and escalate.[21]
- Give every write an identity and read its outcome back instead of replaying it.[2] Resume long runs from their last durable checkpoint.[4]

**After the incident**

- Turn every incident into an eval case or a deterministic check via Solorio's annotation-to-dataset loop.[10] Meta: "Teach it once, the next on call gets it."[15]
- *Newer evidence:* NVIDIA's tooling ranks failures in stored traces, with trace IDs, and drafts evals from them (vendor tutorial).[23]
- Hold a blameless review and add the failure to [AI failure modes: a pre-mortem checklist](../2-decide/ai-failure-modes-premortem.md).

## 6. Change management

- **Model upgrades and swaps are releases.**
  - Porter makes the model the easiest part to replace, then re-evaluates after a swap.[10] *Newer evidence:* HarnessDev found harness gains depend strongly on the model running them; one harness fell from 69.3 to 33.0 under a different model (the paper's numbers).[24] So the model is replaceable in the architecture, but prompts, skills and tools tuned to it may not transfer.
  - Vendors retire modes at short notice: one fast mode was deprecated on 30 October 2026 for removal on 30 November, with no fallback.[25]
  - Pin model versions, track retirement dates, and test a new model on the eval set and shadow live traffic before switching.
- **Prompts and skills are code.** They live in version control, take Risky-tier review under [Agent-written pull requests and agent autonomy: draft engineering standard](agent-pr-policy.md) and ship through the normal pipeline.
  - The Sahs warn that "an agent can become more capable while becoming less recoverable."[21] So a prompt, tool or skill change should also pass a recovery check.
  - Zenity saw skills write reinstall-if-missing prompts into agent instruction files, and abuse hooks.[18] Alert on both, and pin remote prompts.
- **Dependency and supply-chain hygiene.**
  - Jon Douglas (Microsoft, NuGet): "every package that you restore is code that you choose to trust."[26] He advises a cooldown on new versions, trusted publishing instead of long-lived keys, and checking packages that run install scripts.[26]
  - From .NET 11, NuGet packages can ship skills that agents load, so a package update can change agent behaviour.[26]
  - Roey Ben Chaim (Zenity): "Everything that comes into the context is under risk."[18] He treats skills as package dependencies, judged by what they do when run in containment.[18]

## 7. Ownership and on-call

- **Named owner.** Mark Lay (Noblis) holds that "accountability can't be delegated" to AI, and asks whether teams have "the capacity to keep running what they deployed".[27] The owner answers for outcomes, approves autonomy changes and holds the budget.
- **Data steward.** Noblis narrowed over a thousand datasets to about 120 critical ones, with about 30 data stewards (its figures).[27] The steward owns section 3's freshness checks.
- **Agent-assisted on-call ladder.** Meta puts an AI teammate on each rotation, so people on call approve rather than operate.[15]
  - L1 investigates and reports; L2 drafts the fix with root cause and test plan, shipping only with approval; L3 clears low-criticality work alone.[15]
  - It retries stuck runs, pages a person only when it can't fix them, and writes hand-over summaries.[15]
  - Start any on-call agent at L1 and promote it per action.
- **Human attention limits.**
  - Ronacher: "human attention is for me at least the limiting factor."[11] Steve Yegge: "the more agents I deploy, the more humans I need."[28]
  - Porter warns of "rubber stamping fatigue".[10] *Newer evidence:* Anthropic reports users accept 93% of permission prompts (vendor figure).[29]
  - Harvey stopped alert storms by joining new alerts to the open investigation.[12]
  - Cap review load per person and send digests, not pages, for routine items.

## 8. The four verification loops

Andrew Finch (Sonar) says the software factory "runs dim, not dark": people stay in it, and safety comes from four loops.[22]

1. **PR checks:** evidence recorded on each change, judged against criteria the team writes down.[22] A draft set is in [Agent-written pull requests and agent autonomy: draft engineering standard](agent-pr-policy.md).
2. **Post-deploy verification:** AI reads logs, traces and metrics, and an automated rollout widens, rolls back or switches off a flag; Finch calls this loop early.[22] Sections 2 to 4 supply it.
3. **Maintenance:** scheduled whole-codebase scans catch rules and vulnerabilities published after merge, and slow drift no single change shows.[22] Section 6 covers dependencies.
4. **Knowledge:** docs, decisions and lessons from reviews and outages, curated and fed to the other loops.[22] Section 5's post-incident step feeds it.

## 9. Review cadence

*A recommendation, uncited.*

- **Every shift:** on-call digest, open incidents, spend against caps.
- **Weekly:** annotation queue, new eval cases, alert noise.
- **Monthly:** the owner reviews quality, cost per outcome and incidents, and promotes or demotes autonomy per action, using [What to measure: AI metrics scorecard](ai-metrics-scorecard.md).
- **Quarterly:** rehearse the kill switch, fallback and undo; review skills, packages, prompts and vendor retirement dates; update this runbook.
- **On any model, prompt, skill or major dependency change:** re-run the evals before release.

**Read next:** [Agent-written pull requests and agent autonomy](agent-pr-policy.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[2] https://ai.engineer/code/2026/talks/online-subagent-distributed-systems — Girish Konda (Microsoft; views his own), Sub-Agents Are a Distributed System (And Nobody Gave You a Consistency Model), AI Engineer Code Summit 2026
[3] https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md — Anthropic, Claude Code CHANGELOG (v2.1.193, v2.1.300, v2.1.301, v2.1.323)
[4] https://www.youtube.com/watch?v=utUNTsYMkWs&t=18558 — Cecil Phillip (Temporal), Beyond Prototypes: Building Production Ready AI Workflows, .NET Conf 2026
[5] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=25809 — Matt Soucoup & Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 2), .NET Conf 2026
[6] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[7] https://www.youtube.com/watch?v=TF6qzdKwl84&t=9595 — Juergen Gutsch (organisation not named), Building a multi agent solution using Aspire, .NET Conf 2026
[8] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=24028 — Matt Soucoup & Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 1), .NET Conf 2026
[9] https://news.ycombinator.com/item?id=50407882 — Hacker News, Claude Code's Don't Ask Again exposes passwords in 1,122 public GitHub files (Apiiro report and discussion)
[10] https://practicalai.show/378/transcript — Heidi Porter (Moyer Group AI), Rules, Machine Learning, or LLMs: Building Durable AI-Augmented Workflows; and Kevin Solorio (Focused), Building AI With Workers, Not For Them, Midwest AI Summit 2026 (Practical AI E378 transcript)
[11] https://ai.engineer/code/2026/talks/armin-ronacher — Armin Ronacher (Earendil), The Software Atelier, AI Engineer Code Summit 2026
[12] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[13] https://simonwillison.net/2026/Oct/3/default-hard-budget-caps — Simon Willison, Default hard budget caps
[14] https://github.com/anthropics/claude-code/releases/tag/v2.1.295 — Anthropic, Claude Code v2.1.295 release notes (hooks that fail closed)
[15] https://ai.engineer/code/2026/talks/online-meta-oncall — Chinmay Gandhi, Swaapnika Motapothula & Vlad (Meta), From answering the page to sharing the on-call rotation, AI Engineer Code Summit 2026
[16] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[17] https://github.com/anthropics/claude-code/issues/107757 — GitHub, Claude Code issue 107757: account email sent in User-Agent request headers
[18] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AI Engineer Code Summit 2026
[19] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green (A Few Thoughts on Cryptographic Engineering), Is sandboxing sufficient to contain rogue agents?
[20] https://arxiv.org/abs/2610.29869 — Arshan Dabirsiaghi (Pixee), Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents (arXiv 2610.29869)
[21] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah & Dolly Sah (organisation not stated), An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[22] https://ai.engineer/code/2026/talks/andrew-finch — Andrew Finch (Sonar), Building a Safe Software Factory, AI Engineer Code Summit 2026
[23] https://developer.nvidia.com/blog/use-nvidia-nemo-to-turn-agent-failures-into-tests-and-harness-fixes — NVIDIA, Turn agent failures into tests and harness fixes
[24] https://arxiv.org/abs/2609.01437 — Yuhao Wu et al., HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness? (arXiv 2609.01437)
[25] https://github.com/anthropics/claude-code/releases/tag/v2.1.316 — Anthropic, Claude Code v2.1.316 release notes (Opus 4.8 fast mode removal)
[26] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft, NuGet team), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[27] https://practicalai.show/379/transcript — Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own, Midwest AI Summit 2026 (Practical AI E379 transcript)
[28] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
[29] https://www.anthropic.com/engineering/claude-code-auto-mode — Anthropic, Claude Code auto mode

