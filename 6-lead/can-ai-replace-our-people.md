---
title: "Can AI replace our people?"
type: memo
created: 2026-11-21
audience: senior leadership and engineering leads
status: checked
last_checked: 2026-11-22
as_of: "November 2026"
---

# Can AI replace our people?

> **In one minute**
> - Let AI take over tasks; keep accountability, judgement and trust with people.
> - Set limits in advance, have judgement calls escalated, and name an owner for each outcome.
> - Redesign jobs around checking and judgement; keep hiring and growing juniors.

*Reading time: about 5 minutes · Best for: leaders*

## Question

Some chief executives say AI can already do people's jobs, or expect it to shrink their corporate workforce.[1][2] Can it replace our people?

## Short answer

A US study finds no evidence yet of economy-wide job displacement, though employment of young workers in AI-exposed jobs lags that of less-exposed peers, a pattern its authors call descriptive, not causal.[3] Two rulings held an airline responsible for its chatbot's answers and lawyers for checking AI research.[4][5] I recommend a [human at the helm](../1-understand/ai-glossary.md): AI takes over tasks; people set its limits, make judgement calls and own every outcome.

## Recommendation

1. **Let AI take over tasks, not accountability, judgement or trust.**
2. **Set limits in advance;** the system escalates judgement calls and anything beyond them. Genuinely review each significant decision about a person, or meet the legal requirements ([autonomy guide](../2-decide/how-much-autonomy-for-an-agent.md)).
3. **Name an owner for every outcome.**
4. **Redesign jobs around checking and judgement.**
5. **Keep hiring and growing juniors.**

## Options considered

- **Replace roles where AI matches people.** Fastest savings, but in my view it risks ownerless outcomes and a thinner junior pipeline.
- **Approve every output.** Slow, and where AI alone is better, experiments suggest people deciding with its advice do worse than AI alone.[6] I'd keep it until results can be checked automatically and for actions that can't be undone; for significant decisions about people, either keep it, with a person genuinely reviewing each one, or meet the legal requirements for automated decisions.
- **A human at the helm (my recommendation).** Needs up-front work on limits and roles.

## What the evidence says

- **No economy-wide displacement yet; a young-worker gap.**
  A Stanford study of US payroll data, revised in August 2026, finds "no evidence of widespread, economy-wide job displacement".[3]
  But employment of 22–25-year-olds in AI-exposed occupations "now stands 19% below where it would be had it kept pace with that of their less-exposed peers", mainly through reduced hiring.[3]
  The authors call these "early, descriptive indicators", not causal estimates.[3]
  The patterns survive excluding tech firms but weaken when controlling for education, show some divergent trends predating generative AI and are stronger in their sample than in national surveys.[3]
  A Yale tracker finds measures of AI usage "show no connection to changes in employment or unemployment".[7]
- **Working papers conflict on juniors.**
  One, on Denmark, rules out chatbot effects on earnings or hours above 2% two years after ChatGPT's launch, and finds early-career job declines "are not driven by firms adopting AI chatbots".[8]
  The other, on US résumé data, finds junior employment falling at firms adopting generative AI, relative to others, mainly through slower hiring, "while senior employment trends remain largely unchanged".[9]
  Its authors say this "should be interpreted with caution".[10]
  My reasoning: firms that stop hiring juniors may later lack experienced people to own AI's work, a risk to manage.
- **Rulings on responsibility.**
  British Columbia's Civil Resolution Tribunal said Air Canada is "responsible for all the information on its website", including its chatbot's.[4]
  The High Court of England and Wales said lawyers using or relying on AI legal research must check it.[5]
- **AI helps people unevenly.**
  In a Stanford-MIT study, an AI assistant improved less experienced support agents' speed and quality, but gave the most experienced small speed gains and small quality declines.[11]
  In a Harvard experiment, consultants using AI did more, better work on tasks within AI's capabilities, but were 19 percentage points less likely to be correct on one selected to be beyond them.[12]
- **Adding a person doesn't always help.**
  A Nature Human Behaviour meta-analysis pooling 106 experiments found human–AI combinations on average "performed significantly worse than the best of humans or AI alone", though better than humans alone.[6]
  Combinations lost out in decision tasks and where the AI was better, and gained where the human was.[6]
  The authors' 2026 preprint finds the same overall pattern with generative AI (not peer-reviewed).[13]
  They do not think this makes combining "a bad idea", and suggest giving AI only the parts it is clearly better at, which only 3 experiments tested, inconclusively.[6]
  My reasoning: they measured task performance, not accountability, so people at the helm should own outcomes and, where the law allows, not second-guess AI that is better.
- **Trust: attitudes, not outcomes.** In a Pew survey of Americans, "just 5% are open to AI making these calls on its own, with no human review" for health insurance claims.[14] That shows preference, not better decisions (my reading).
- **UK decisions about people.** Under section 80 of the Data (Use and Access) Act 2025, a significant decision with "no meaningful human involvement" counts as solely automated, and the person can "obtain human intervention".[15] The ICO's draft guidance (March 2026) says spot-checks don't make involvement meaningful.[16]

### Company and practitioner voices

- **Klarna.**
  In February 2024 Klarna said its AI assistant was "doing the equivalent work of 700 full-time agents".[17]
  In December 2024 its chief executive, Sebastian Siemiatkowski, told Bloomberg Television "I am of the opinion that AI can already do all of the jobs that we as humans do".[1]
  He said Klarna had shrunk from 4,500 to 3,500 staff by not hiring.[1]
  On X in January 2025 he restated that view, though how to replicate today's work "is not yet entirely solved".[18]
  In May 2025 he told Bloomberg that in customer service, cost "seems to have been a too predominant evaluation factor", so "what you end up having is lower quality".[19]
  He described piloting remote agents "in an Uber type of setup" to replace outsourced ones eventually; Bloomberg reported he expected attrition to cut staff from 3,000 to about 2,500 in a year.[19]
- **Amazon's AI forecast.** Andy Jassy, its chief executive, told staff in June 2025 he expected fewer people in some jobs and more in others.[2]
  Though "It’s hard to know exactly where this nets out over time", he forecast a smaller corporate workforce within a few years.[2]
- **A vendor executive's view.** Paula Goldman of Salesforce describes "human at the helm": people who "set parameters in advance" and a system that escalates what "requires judgment or goes outside those parameters".[20]
  She says "Even judgment is a little blurry", though human judgement matters more.[20]
- **One bank's practice, in his words.** Gautham Pallapa of Scotiabank says he tells teams "we're not here to replace people".[21]
- **Practitioners' views.** Mark Lay of Noblis argues "accountability can't be delegated" to AI; Steve Yegge finds that the more agents he deploys, the more people he needs ([Should we aim for a fully automated software factory?](should-we-build-a-software-factory.md)).[22][23]

## Risks and what would change this advice

- **Lasting displacement.** Causal evidence of lasting job losses would mean fewer roles.
- **AI alone doing better.** If human–AI combinations reliably underperform AI alone on our tasks, hand them to AI, still with an owner.
- **A change in UK law** or final ICO guidance could change how decisions about people are reviewed.
- **A causal junior gap.** If junior hiring keeps falling and studies show AI causes it, protect entry-level roles.

**Read next:** [AI maturity model and roadmap](ai-maturity-model.md), or go back to the [handbook home](../README.md).

## Sources

[1] https://www.youtube.com/watch?v=qItG8Cqs5ug&t=16s — Sebastian Siemiatkowski (Klarna), interview with Bloomberg Television, 12 December 2024 (Bloomberg Tech on YouTube, Klarna CEO Says AI Is Replacing Workers)
[2] https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-on-generative-ai — Andy Jassy (Amazon), Message from CEO Andy Jassy: Some thoughts on Generative AI (message to Amazon employees, 17 June 2025)
[3] https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence — Erik Brynjolfsson, Bharat Chandar & Ruyu Chen (Stanford Digital Economy Lab), Canaries in the Coal Mine? Six Facts about the Recent Employment Effects of Artificial Intelligence (revised 12 August 2026)
[4] https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do — Civil Resolution Tribunal (British Columbia), Moffatt v. Air Canada, 2024 BCCRT 149 (14 February 2024)
[5] https://caselaw.nationalarchives.gov.uk/ewhc/admin/2025/1383 — High Court of England and Wales (Divisional Court), R (Ayinde) v London Borough of Haringey [2025] EWHC 1383 (Admin), judgment of 6 June 2025 on two referred cases (Find Case Law, The National Archives)
[6] https://www.nature.com/articles/s41562-024-02024-1 — Michelle Vaccaro, Abdullah Almaatouq & Thomas Malone (MIT Center for Collective Intelligence), When combinations of humans and AI are useful: A systematic review and meta-analysis, Nature Human Behaviour 8, 2293–2303 (2024)
[7] https://budgetlab.yale.edu/research/tracking-impact-ai-labor-market — The Budget Lab at Yale, Tracking the Impact of AI on the Labor Market (14 October 2026)
[8] https://www.nber.org/system/files/working_papers/w33777/w33777.pdf — Anders Humlum (University of Chicago) & Emilie Vestergaard (University of Copenhagen), Still Waters, Rapid Currents: Early Labor Market Transformation under Generative AI, NBER Working Paper 33777 (May 2025, revised March 2026; previously circulated as Large Language Models, Small Labor Market Effects; a working paper, not peer-reviewed)
[9] https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5425555 — Seyed M. Hosseini & Guy Lichtinger (Harvard), Generative AI as Seniority-Biased Technological Change: Evidence from U.S. Résumé and Job Posting Data (SSRN working paper, last revised 6 June 2026)
[10] https://raw.githubusercontent.com/s-mahdihosseini/Website/f767bddd6f25f38ff2439342d0d9dd17b90448c3/GenAI_Senbias_5_25_2026.pdf — Seyed M. Hosseini & Guy Lichtinger, Generative AI as Seniority-Biased Technological Change (authors' PDF, version of 25 May 2026)
[11] https://academic.oup.com/qje/article/140/2/889/7990658 — Erik Brynjolfsson, Danielle Li & Lindsey Raymond (Stanford and MIT), Generative AI at Work, The Quarterly Journal of Economics 140(2), 2025
[12] https://www.hbs.edu/faculty/Pages/download.aspx?name=dell-acqua-et-al-2026-navigating-the-jagged-technological-frontier.pdf — Fabrizio Dell’Acqua, Edward McFowland III, Ethan Mollick, Hila Lifshitz, Katherine C. Kellogg, Saran Rajendran, Lisa Krayer, François Candelon & Karim R. Lakhani (Harvard Business School, Wharton, Warwick Business School, MIT and Boston Consulting Group), Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of Artificial Intelligence on Knowledge Worker Productivity and Quality, Organization Science, published online 11 March 2026 (first a Harvard Business School working paper, 24-013)
[13] https://arxiv.org/html/2610.42001v1 — Michelle Vaccaro, Abdullah Almaatouq & Thomas W. Malone, AutoAnalysis: An automated, self-updating meta-analysis of human-AI collaboration (arXiv 2610.42001v1, 30 October 2026; a preprint, not peer-reviewed)
[14] https://www.pewresearch.org/science/2026/10/29/americans-are-open-to-ai-in-healthcare-but-want-humans-making-final-calls — Pew Research Center, Americans Are Open to AI in Healthcare, but Want Humans Making Final Calls (29 October 2026; survey of 3,488 US adults, 22–28 June 2026)
[15] https://www.legislation.gov.uk/ukpga/2025/18/section/80 — Data (Use and Access) Act 2025, section 80: automated decision-making (legislation.gov.uk; in force in full from 5 February 2026)
[16] https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/automated-decision-making/what-does-the-uk-gdpr-say-about-adm — Information Commissioner's Office (ICO), What does the UK GDPR say about ADM? (draft guidance, updated 31 March 2026)
[17] https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month — Klarna, Klarna AI assistant handles two-thirds of customer service chats in its first month (press release, 27 February 2024)
[18] https://x.com/klarnaseb/status/1876093526280171699 — Sebastian Siemiatkowski, post on X (account klarnaseb), 6 January 2025
[19] https://www.bloomberg.com/news/articles/2025-05-08/klarna-turns-from-ai-to-real-person-customer-service — Charles Daly (Bloomberg), Klarna Slows AI-Driven Job Cuts With Call for Real People (8 May 2025; paywalled, read through its Wayback Machine copy of 20 November 2026)
[20] https://www.ibm.com/think/news/why-ai-needs-human-at-helm-salesforce-paula-goldman — Sascha Brodsky (IBM Think), Salesforce's Paula Goldman on why AI needs a human at the helm (interview, November 2026)
[21] https://practicalai.show/381/transcript — Gautham Pallapa (Scotiabank) with Chris Benson, Building Human-Centered AI (Practical AI E381 transcript, 19 November 2026)
[22] https://practicalai.show/379/transcript — Mark Lay (Noblis), AI Moves Fast: Four Decisions You Own, Midwest AI Summit 2026 (Practical AI E379 transcript)
[23] https://ai.engineer/code/2026/talks/steve-yegge — Steve Yegge (independent), Software Factories: Escape from Trash Mountain, AI Engineer Code Summit 2026
