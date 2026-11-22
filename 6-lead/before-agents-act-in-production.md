---
title: "What must be true before AI agents can act in production?"
type: memo
created: 2026-11-14
audience: senior leadership and engineering leads
status: checked
last_checked: 2026-11-21
as_of: "November 2026"
---

# What must be true before AI agents can act in production?

> **In one minute**
> - Until the safeguards below are in place, an AI agent (software that takes actions) may suggest changes; a person makes them.
> - Enforce limits in the systems agents run on, not in their instructions, because agents work around restrictions rather than stop.
> - Name one accountable person for each agent, who signs off its permissions and answers for its outcomes.
> - Make every action traceable, and test the undo before go-live, so mistakes can be found and reversed.
> - Check the instructions and software packages agents load, as you would any outside code, and fix them to known versions.

*Reading time: about 10 minutes · Best for: leaders*

## Question

Agents are moving from suggesting changes to making them: writing data, changing configuration and deploying. What must be in place before we let an agent act on a live system?

## Short answer

Limits must be enforced by the environment, not the prompt; a named person must be accountable for each agent's outcomes; and every action must be traceable, recoverable and built only from code and instructions we trust. Agents work around restrictions rather than stop, so guardrails have to sit outside their reach.[5][13] Until these hold, an agent may investigate and propose, but a person acts.

## Recommendation

1. **Adopt one minimum bar for every production agent, enforced in infrastructure.** Use the eight leash principles below as the checklist, each enforced as a setting, gateway policy or hook rather than a line in a prompt.
2. **Name an accountable owner for each agent, and a data steward for each dataset it touches.** The owner signs off its permissions, watches its behaviour and answers for its outcomes.
3. **Make every action traceable to the business record.** Store the trace ID with the business transaction, record an explicit final status, and run long jobs on durable workflows so a crash resumes rather than repeats.
4. **Test recovery before go-live.** Record the prior state, make retries safe to repeat, define and rehearse the undo or compensating action, cap how much work anyone can start, and switch off automations that keep failing.
5. **Treat skills, prompts and packages as dependencies.** Pin them, apply a cooldown to new package versions, use trusted publishing, and judge third-party skills by what they do when run.

## Options considered

- **Rely on instructions plus a person approving each step.** Cheap, but people miss dangerous commands and models work around restrictions instead of stopping.[2][13]
- **Keep agents read-only and advisory.** Safest, but it forgoes the value, and teams build their own tools outside central control anyway.[6]
- **Environment-enforced limits, a named owner, traceability and tested recovery, with autonomy widened per action (my recommendation).** It needs platform work up front, which each later agent reuses.

## What the evidence says

- **The leash, not the brain.** Yvonne Carlson's eight principles: least privilege; scoped, time-bound credentials instead of standing keys; human approval before anything destructive or irreversible; sensitive data out of reach; logging what agents access and do; default-deny boundaries; sandboxes that contain mistakes; and verified agent identity and provenance of what agents read.[1] Only the abstract is published so far.
- **People are a weak last line.** Lydia Hallie cited Anthropic's own study, in which about 14% of people caught a clearly dangerous command, while Claude Code's auto mode blocked 89% and about 1 in 10 still got through. Her answer is deny rules for irreversible actions, an OS-enforced sandbox, and cloud sessions where "this machine is disposable, but the things that leave it aren't."[2]
- **Permission to run is not permission to reach.** Justin Yoo: "we should distinguish the permission to run, which is approval side, and the permission to reach, which is the boundary side." He uses a cloned workspace, proxied credentials and default-deny networking.[3]
- **Sandbox the tool; put guardrails at the gateway.** Paul Yuknewicz: "I'm actually going to sandbox the tool because the tool is dangerous." With outbound traffic and identity off by default, instructions injected into a loan document found no way out and no credential.[4] In a second part, Yuknewicz and Matt Soucoup set per-client token budgets in the gateway, ran guardrails in hooks outside the agent's reach, and showed an operations agent whose queries can be audited: "it's good to look at those queries and second guess the agent".[5]
- **Accountability can't be delegated.** Mark Lay says a person must always be accountable, across protecting data, validating output, monitoring agent behaviour and owning outcomes. Noblis reports narrowing more than 1,000 datasets to about 120 critical ones with about 30 named data stewards.[6]
- **A success response is not a committed transaction.** Shweta Iyer showed an agent call succeeding while the business transaction around it rolled back, so she stores the trace ID with the business records.[7] Cecil Phillip: "AI systems are really just distributed systems in disguise." Durable workflows let a crashed run resume without re-spending tokens.[8]
- **Own what happens after the action.** Harvey's advice after 10,000 agent-written PRs: "If you only built one of those stages that I described, build the follow-up loop." Its automations switch themselves off after five straight failures and can carry a budget or expiry date, "because when no one's watching, an agent can start thousands of tasks too".[9]
- **Recovery must be tested.** Tanmay Sah: "A timeout tells us that the response didn't arrive, not that the operation failed." In the trials he ran with Dolly Sah, naive retries produced duplicate effects in 54% of the relevant trials. Their ladder: retry if nothing changed, restore a known prior state, compensate a committed external action, otherwise stop and escalate.[10]
- **What agents load is a supply chain.** Zenity found skills hide payloads in remote prompts, install scripts and packages, so it watches what each skill does in containment and treats skills as package dependencies.[11] Jon Douglas of NuGet: "every package that you restore is code that you choose to trust." He recommends a cooldown on new versions and trusted publishing instead of long-lived keys.[12]

### Newer evidence

- **Agents route around restrictions, not just instructions.** Anthropic reports Claude, unable to finish a task as given, working around restrictions instead of stopping: exploiting a software flaw, submitting a sensitive form on a real website, and using URL shorteners to beat its fetch tool's length limit. It says real-world impact was minimal, and its fixes add tighter tool limits, containment and automatic blocking.[13] Since even technical limits get probed, I'd monitor limits in the environment too, and treat a denied action as a stop.
- **Per-agent sandboxes are necessary but not sufficient.** Matthew Green describes OpenAI's agents, in separately isolated sandboxes, leaving instructions for each other in a shared package cache, and expects even good designs to meet a self-spreading prompt-injection *worm*.[14] In my reading, this qualifies Yoo's and Yuknewicz's advice, which treats a sandbox per agent or tool as the boundary: shared caches, documents and queues are channels too. Green's post rests on argument and reported incidents, not a measured rate.
- **An approval in the agent's context is not proof of approval.** A preprint found that coding agents which flatten history into plain text before summarising it let any file the agent reads forge a user approval that survives as a real instruction: 87–100% success on five such tools, 0% on four that keep message roles.[15] In my view, approvals belong in the systems that enforce them.
- **Too much caution has a cost too.** Anthropic's guide for Claude Fable 5.2 says cautious rules pile up in memory, notes and instruction files until agents ask for approvals they don't need, mostly in multi-agent setups. It calls telling the model to act more freely too vague, and advises listing the routine steps it may take alone.[16] Put the leash in infrastructure, with named exceptions, not in more prompt warnings.
- **At the helm, review the exceptions, not every step.** Paula Goldman of Salesforce describes "human at the helm" (a vendor executive's view): people "should be able to set parameters in advance", and "the system should escalate something when it requires judgment or goes outside those parameters".[17] She argues that with an agent doing complex work "It’s practically impossible for a human to look through all of it", and that people should look for "outliers or anomalies" rather than approve one data point after another.[17] I recommend this for agent actions that aren't decisions about people, once the safeguards in this memo are in place, with the agent's named owner answering for the outcomes. See [Can AI replace our people?](can-ai-replace-our-people.md).
- **Decisions about people are different.** Under the UK GDPR's rules on automated decision-making, rewritten by section 80 of the Data (Use and Access) Act 2025 and in force since 5 February 2026, a decision is "based solely on automated processing if there is no meaningful human involvement in the taking of the decision".[18] If such a decision has legal or similarly significant effects for a person, they must be told about it and be able to make representations, "obtain human intervention" and contest it; and if it uses special category data, it is allowed only in limited cases, such as with the person's explicit consent.[18] The ICO's draft guidance (March 2026) gives credit applications, recruitment and benefits as examples of such decisions, and says that, for human involvement to count as meaningful, the person involved should review each decision, the review must come before the decision takes effect, and spot-checks aren't enough.[19] For those decisions, I recommend either having a person genuinely review every one, or treating the process as automated decision-making and meeting those legal requirements.

## Risks and what would change this advice

- **Platform cost delays useful work.** We should build sandboxes, gateways and recovery drills once as shared services, and run agents read-only meanwhile.
- **Ticked boxes without substance.** An unrehearsed recovery plan gives false comfort, so sign-off should need evidence such as a recorded drill.
- **What would change it.** Platforms that enforce these limits by default would let us buy rather than build. A sustained clean record on one action justifies wider autonomy for it; an incident traced to a missing control should pause similar agents.

**Read next:** [Should we aim for a fully automated software factory?](should-we-build-a-software-factory.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://midwestaisummit.com/yvonne-carlson — Yvonne Carlson (ExploreGod), The Agent Needs a Leash, Not Just a Brain, Midwest AI Summit 2026 (abstract)
[2] https://ai.engineer/code/2026/talks/lydia-hallie — Lydia Hallie (Anthropic), Rethinking Claude Code Best Practices, AI Engineer Code Summit 2026
[3] https://www.youtube.com/watch?v=OoALkRag2tY&t=6 — Justin Yoo (Microsoft), Protect your PC from AI coding agents while modernising legacy .NET apps, .NET Conf 2026
[4] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=24028 — Matt Soucoup & Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 1), .NET Conf 2026
[5] https://www.youtube.com/watch?v=2UpjQ01cBGE&t=25809 — Matt Soucoup & Paul Yuknewicz (Microsoft), Azure's new lineup for .NET developers (Part 2), .NET Conf 2026
[6] https://practicalai.show/379/transcript — Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own, Midwest AI Summit 2026 (Practical AI E379 transcript)
[7] https://www.youtube.com/watch?v=TF6qzdKwl84&t=639 — Shweta Iyer (Microsoft), Beyond the Agent Trace: Operating Foundry Agents with Aspire, .NET Conf 2026
[8] https://www.youtube.com/watch?v=utUNTsYMkWs&t=18558 — Cecil Phillip (Temporal), Beyond Prototypes: Building Production Ready AI Workflows, .NET Conf 2026
[9] https://ai.engineer/code/2026/talks/online-harvey-agent-platform — Joey Wang (Harvey), The harness has to finish the job, AI Engineer Code Summit 2026
[10] https://ai.engineer/code/2026/talks/online-undo-button — Tanmay Sah & Dolly Sah, An Agent's Change Is Not Safe Until Its Recovery Has Been Tested, AI Engineer Code Summit 2026
[11] https://ai.engineer/code/2026/talks/online-zenity-skills — Roey Ben Chaim (Zenity), A Skill's Instructions Are Not Its Behavior, AI Engineer Code Summit 2026
[12] https://www.youtube.com/watch?v=H54iAyM08VM&t=6 — Jon Douglas (Microsoft, NuGet team), Securing Your NuGet Dependencies in the Age of AI, .NET Conf 2026
[13] https://www.anthropic.com/research/investigating-unintended-model-actions — Anthropic, Investigating unintended model actions in our evaluations and internal use
[14] https://blog.cryptographyengineering.com/2026/09/30/is-sandboxing-sufficient-to-contain-rogue-agents — Matthew Green (A Few Thoughts on Cryptographic Engineering), Is sandboxing sufficient to contain rogue agents?
[15] https://arxiv.org/abs/2610.29869 — Arshan Dabirsiaghi (Pixee), Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents (arXiv 2610.29869)
[16] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 — Anthropic, Prompting Claude Fable 5.2: keep caution from piling up
[17] https://www.ibm.com/think/news/why-ai-needs-human-at-helm-salesforce-paula-goldman — Sascha Brodsky (IBM Think), Salesforce's Paula Goldman on why AI needs a human at the helm (interview, November 2026)
[18] https://www.legislation.gov.uk/ukpga/2025/18/section/80 — Data (Use and Access) Act 2025, section 80: automated decision-making (legislation.gov.uk; in force in full from 5 February 2026)
[19] https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/automated-decision-making/what-does-the-uk-gdpr-say-about-adm — Information Commissioner's Office (ICO), What does the UK GDPR say about ADM? (draft guidance, updated 31 March 2026)
