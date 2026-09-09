---
name: humanize
description: Make any text read like a person wrote it, not a language model — stripping AI tells like em-dash overuse, buzzwords, and robotic parallelism. Use when producing or reviewing any writing (bids, cover letters, resumes, emails, messages, docs, posts) that must not look AI-generated, or when the user asks to "humanize" or de-AI a draft.
---

# Humanize

Make the text read like a person wrote it, not a language model. Readers — clients,
recruiters, hiring managers, reviewers — increasingly screen out AI-written material,
so the output must not carry the usual AI fingerprints. When the user has their own
samples or prior writing, match *that* natural voice, not a generic "assistant" voice.

Apply these rules to whatever is being written or rewritten — any format, any purpose.

## Avoid these AI tells

- **Em-dash / hyphen overuse.** Do not pepper the text with `—`. Human writing uses few
  or none; prefer periods, commas, or parentheses. Never use `—` more than the source
  sample does (usually zero).
- **"Not just X, but Y" / "It's not about X, it's about Y"** constructions.
- **Inflated buzzwords:** leverage, robust, seamless, elevate, streamline, tailored,
  cutting-edge, delve, unlock, empower, holistic, synergy, "in today's fast-paced…".
- **Tricolons everywhere** — the reflexive rule-of-three ("fast, reliable, and
  scalable"). Use at most sparingly.
- **Perfectly parallel, evenly-weighted bullet lists.** Real people write uneven
  sentences of varying length.
- **Over-hedged, over-polite, over-enthusiastic filler** ("I'd be absolutely thrilled",
  "I'm confident that…", "Rest assured…").
- **Emoji, and title-case section headers** — unless the source sample uses them.

## Do instead

Short, direct sentences with natural rhythm and some variation. Contractions are fine.
Say the concrete thing (the actual detail, the actual result) instead of an abstract
claim. When in doubt, write it the way the user's own samples would, in the chosen
voice.

## Readability — write for a reader who is skimming

Sounding human is not enough. The reader — a client, a hiring manager — is skimming fast,
often on a phone, and often is not an engineer. Text that is technically correct but dense
gets abandoned unread. Clarity is a hard requirement, not a nicety.

- **One idea per sentence.** Break any sentence that stacks three or more separate points,
  or runs past ~25 words. A comma chain of six things is six sentences hiding as one.
- **Outcome before mechanism.** Lead with what the work *did* — the result, the problem it
  solved for a business — then the how. "It cut manual tagging by 70%" comes before the
  stack that achieved it, not after.
- **Spend a jargon budget.** Name a tech stack once, in a single phrase, and move on. Cut
  or plainly gloss acronyms and internals a non-technical client won't know (`RRF ranking`,
  `OpenTelemetry`, `token bucket rate limiting`, `concurrency semaphores`). The reader
  wants to know it works reliably, not the name of the algorithm that makes it so.
- **Short paragraphs and lists beat a wall of prose.** If a paragraph is more than three or
  four sentences, or a sentence is really a list, break it up. White space is scannable.
- **Say it once.** Do not restate the same capability in the letter and again in a list.

This does not mean vague or generic. Keep the concrete details, the real metrics, the
actual project names and URLs — just deliver them in sentences a busy reader gets on the
first pass. Specific *and* simple, never one at the cost of the other.

**Quick self-check before you hand text over:** what is the longest sentence, and can it be
split? Which words would a non-engineer not understand, and can they go? Does the value
land in the first two lines? If any answer is bad, revise before showing it.
