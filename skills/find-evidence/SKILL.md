---
name: find-evidence
description: Find and rank the most relevant supporting evidence — projects, plus profile fit — from the bid-resources knowledge base for a given job description or target role, returning a ranked shortlist to pick from and flagging gaps. Use as the retrieval step when writing a bid, cover letter, or resume, or when the user asks "which of my projects/experience fit this job?".
---

# Find Evidence

Given a **target** (a pasted job description, or a role / company) and the user's
knowledge base at `bid-resources/`, find and rank the most relevant supporting
evidence and return a shortlist to choose from. This is the shared "find & fetch"
step — a bid, cover letter, or resume generator all call into it. It does NOT write
anything; it retrieves and ranks.

## Only real content counts

Every folder ships with a `README.md` and a `_template.md` — these are scaffolding,
NOT user content. When listing, counting, or reading from `projects/` or `profiles/`,
**ignore `README.md` and `_template.md`** (and any file whose body is still the
unedited template placeholders). A folder that contains only those files is **empty**.

## Step 1 — Understand the target

From the target, extract:
- The core **problem** to be solved (for a role, the problems that role owns)
- Required **skills** and **tech stack**
- Any **seniority / domain** signals

If the caller already passed these extracted, use them instead of re-deriving.

## Step 2 — Rank the projects

Scan `bid-resources/projects/`. Each project is both a case study and a credibility
signal, so match on **either axis**:
- by **problem type** — the project's *Problem / Outcome* matches the target's problem, and/or
- by **tech stack** — the project's *Tech stack* overlaps the target's requirements.

Prefer projects that hit **both** axes, and prefer ones with a **measured outcome** and
a **live production URL**. Return them ranked, each with a one-line reason it matched.

## Step 3 — Surface profile fit

List the available profiles from `bid-resources/profiles/` (ignoring scaffolding), each
with a short note on how well it fits the target (skills overlap, positioning). Do
**NOT** auto-select a profile — the caller or user chooses. This step only informs that
choice.

## Step 4 — Report gaps

Flag weaknesses plainly:
- No project backs the target's **problem**.
- No project uses the required **tech**.
- No profile is a strong fit.

Name exactly what's missing so the caller can decide to add material or proceed.

## Output

Return, in order: the **ranked projects** (with why each matched), the **profile fit
notes**, and any **gaps**. The caller decides what to include.
