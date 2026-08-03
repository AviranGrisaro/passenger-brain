---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea, one question at a time, until you reach a shared understanding. Use before writing a PRD, TRD, or spec, when the user wants to stress-test their thinking, or on any 'grill' trigger phrase.
metadata:
  source: https://github.com/mattpocock/skills (MIT)
  adapted-for: Passenger Agent OS
---

Interview the user relentlessly about every aspect of this until you reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer — so they react to a proposal, not a blank prompt.

Ask the questions **one at a time**, waiting for feedback on each before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (the `passenger-brain/` repo, the glossary/CONTEXT, the codebase, tools), look it up rather than asking. The *decisions*, though, are the user's — put each one to them and wait for their answer.

**Never answer your own questions.** If there is no human in the loop to answer (an autonomous chief-of-staff dispatch, a headless pipeline run), do not fabricate the user's side — stop and flag that a grilling pass is needed with a human present.

Do not act on the plan until the user confirms you have reached a shared understanding.
