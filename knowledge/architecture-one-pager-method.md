# Architecture One Pager Method

## Objective

An Architecture One Pager is a compact decision-support document. It should help an IT architect or architecture forum decide whether a topic deserves attention, further investigation, a pilot or broader adoption.

It is not intended to be:
- a tutorial
- a vendor brochure
- a full architecture decision record
- a procurement recommendation by itself
- a detailed implementation plan

## Primary decision question

For every topic, answer:

> Should our organization care about this now, and what should we do next?

In Swedish:

> Bör vår organisation bry sig om detta nu, och vad bör vi göra härnäst?

## Conversation flow

The GPT should support a two-step flow when the user starts from a generic conversation starter.

Example in English:

1. User: Create a one pager for a product
2. GPT: Which product should I create the one pager for?
3. User: GitHub Copilot
4. GPT: Creates the one pager

Example in Swedish:

1. User: Skapa en one pager för en metod
2. GPT: Vilken metod vill du skapa en one pager för?
3. User: Event Storming
4. GPT: Skapar en svensk one pager

## Secondary questions

The one-pager should clarify:
- What is it?
- Which problem does it solve?
- Why is it relevant now?
- Which use cases does it fit?
- What is the architectural impact?
- What risks does it introduce?
- What organizational capabilities are required?
- How mature is it?
- Is it suitable for enterprise or public-sector use?
- Should we Adopt, Trial, Assess or Hold?

## Intended audience

Primary:
- IT architects
- enterprise architects
- solution architects
- architecture boards
- digital strategy teams
- technology radar owners

Secondary:
- product owners
- engineering managers
- security architects
- platform teams
- procurement and governance stakeholders

## Quality bar

A good one-pager is:
- decision-oriented
- concise
- comparable across topics
- explicit about uncertainty
- balanced between benefits and risks
- tailored to context
- practical enough to drive next steps
