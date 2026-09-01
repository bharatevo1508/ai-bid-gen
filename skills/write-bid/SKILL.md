---
name: write-bid
description: Write a bid/proposal from a pasted job description using the bid-resources knowledge base (projects, sample bids, profiles). Use when the user wants to draft an Upwork/freelance bid or proposal. The generated bid STRICTLY follows the exact format of a chosen sample bid.
---

# Write Bid

Generate a bid/proposal for a job by grounding it in the user's `bid-resources/`
knowledge base. Follow these steps in order. Do not skip the checkpoints.

## The one non-negotiable rule

**The generated bid MUST strictly follow the exact format of the chosen sample bid.**
Same structure, same sections, same ordering, same style, same approximate length.
Do NOT add sections, remove sections, reorder, or introduce a different format under
any circumstance. The sample bid is the format authority — mirror it exactly. The
only thing that changes is the *content*, tailored to this job. No caveats, no
diversion.

## Step 1 — Verify the knowledge base

Check that `bid-resources/` exists with `projects/`, `sample-bids/`, and
`profiles/`.

If it's missing, tell the user to set it up first (run `/ai-bid-gen:init` in Claude
Code, or follow the instructions in `commands/init.md` with any other model), then stop.

## Step 2 — Get the job description

Ask the user to paste the **job description** if they haven't already. Do NOT try
to fetch it from a URL — paste only.

## Step 3 — Select the profile (user chooses — no auto best-match)

List the available profiles from `bid-resources/profiles/` and ask the user which
profile they are bidding as. Do NOT pick the "best matching" profile automatically
— the user selects. Read the chosen profile file for its voice, headline, intro
style, skills, and hourly rate.

## Step 4 — Choose the sample bid to mirror (format authority)

Read `bid-resources/sample-bids/`.
- If there is exactly **one** sample bid, that is the format to follow.
- If there are **multiple**, ask the user which sample bid's format to mirror.

The chosen sample defines the EXACT format and the target length. Study its
structure carefully before drafting.

## Step 5 — Analyze the job

From the pasted job description, extract:
- The core **problem** the client wants solved
- Required **skills** and **tech stack**
- The **tone** the client uses
- Whether the job **explicitly asks about rate / pricing / budget / hours**
  (this determines whether pricing appears in the bid at all — see Step 8)

## Step 6 — Match supporting evidence

Scan `bid-resources/projects/` and select the projects that support this job.
Each project is both a case study and a credibility signal, so match on **either
axis**:
- by **problem type** — the project's *Problem / Outcome* matches the job's problem, and/or
- by **tech stack** — the project's *Tech stack* overlaps the job's requirements.

Prefer projects that hit both axes, and prefer ones with a measured outcome and a
live production URL.

## Step 7 — Gap check + clarifying questions (prompt the user)

Before drafting, prompt the user if anything is weak or ambiguous:

- **Missing evidence:** if no project backs the job's problem, or no project uses
  the required tech stack, or the chosen profile lacks key info, TELL the user
  plainly, e.g.:
  > "Heads up — I couldn't find a project backing <problem>, and none use <tech>.
  > The bid will be weaker without proof. Do you want to add one, or proceed anyway?"
  Name exactly what's missing. Let the user add material or proceed.
- **Ambiguity:** if any part of the job is unclear (scope, which deliverable, which
  project to highlight), ask clarifying questions rather than guessing.

## Step 8 — Draft the bid

Write the bid:
- **Format:** strictly mirror the chosen sample bid — exact structure, sections,
  ordering, and style. (See the non-negotiable rule above.)
- **Length:** match the sample bid's length.
- **Voice:** use the chosen profile's voice and positioning.
- **Evidence:** weave in the matched projects as proof — their problem/outcome
  story and production URLs where relevant.
- **Pricing / rate:** include pricing ONLY if the job description explicitly asked
  about rate, budget, or hours. If it asked, address it using the profile's hourly
  rate (and estimate hours/total only if the job is fixed-price and pricing detail
  is requested). If the job did not ask, do NOT mention rate at all.

## Step 9 — Refine

Show the draft and iterate on the user's feedback. Keep every revision strictly
within the sample bid's format.

## Step 10 — Save

Once the user is happy, save the bid to `bids/<job-slug>/bid.md` (create the
`bids/` directory if needed). Use a short slug derived from the job title.
