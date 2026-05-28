# Cognitive Design

Why this dashboard looks and works the way it does.

## The Core Problem

Two collaborators, both unreliable:
- The **human** has aphantasia — cannot mentally visualize the project state. Must see it externally. Cannot hold multiple threads in working memory simultaneously.
- The **AI** has amnesia — forgets everything between sessions. Must be re-oriented each time.

The dashboard is the externalized working memory they share. It must be:
- Always correct (never stale)
- Always visual (figures rendered, not described)
- Always structured (fixed categories that don't move)
- Immediately verifiable (one glance tells you if something is wrong)

## Fixed Structure, Never Sprawl

The navigation never changes. The tab groups never change. The order never changes. This is deliberate — for someone who cannot hold the project structure in memory, a moving interface is an interface that doesn't exist. The structure must be as reliable as furniture.

New content flows into existing categories. New hypotheses go into the Hypotheses tab. New figures go into the Figures tab. The categories absorb growth without structural change.

## One Question At A Time

The audit protocol asks one question, waits for an answer, acts on it, then moves to the next. This is not arbitrary pacing — it matches sequential processing. The user cannot evaluate five dimensions simultaneously. One at a time, resolved before moving forward.

## Color As Cognition

Colors are never decorative. They encode exactly one dimension: status.
- **Green** = done, confirmed, fresh, safe
- **Yellow** = in progress, testing, stale, needs attention
- **Red** = failed, missing, complicated, problem
- **Grey** = not started, pending, orphaned

A glance at the Code tab tells you pipeline health without reading a word. A glance at the Hypotheses tab tells you which claims are earned. This is vision-as-verification.

## Figures Are Primary, Not Supplementary

For someone who trusts pictures over numbers (and who cannot mentally recall a figure when looking at a different tab), the Figures tab is the most important evidence surface. Every figure must:
- Be visible as a thumbnail (not just a filename)
- Show its provenance (which script made it)
- Show its freshness (is it current?)
- Be self-explanatory to a stranger (clear title, labeled axes)

## The Narrative Opens The Dashboard

The default tab is Narrative, not Overview. This is deliberate: orientation starts with "what do we currently believe?" not "what is the status of the machinery?" The story is primary. The machinery serves the story.

## Filing As Ontological Gate

If something isn't filed, it doesn't exist in this system. This isn't bureaucracy — it's the mechanism that prevents the narrative from containing unearned claims. The courtroom can only reference filed insights. Filed insights must trace to pipeline scripts. Pipeline scripts must produce fresh outputs. The chain is: reality → pipeline → figure → insight → courtroom → narrative. Any break in the chain means the claim is unearned.
