---
name: find-evidence
description: Find and rank the most relevant supporting evidence — projects, plus profile fit — from the bid-resources knowledge base for ANY input: a job description, a role, a topic, a brief, a question, or any piece of text. Returns a ranked shortlist to pick from and flags gaps. Use as the retrieval step when writing a bid, cover letter, or resume, or whenever the user asks "which of my projects/experience relate to X?".
---

# Find Evidence

Given **any input** — a pasted job description, a role, a topic, a client brief, a
question, or free text — and the user's knowledge base at `bid-resources/`, find and
rank the most relevant supporting evidence and return a shortlist to choose from.

This is the shared "find & fetch" step. It is **not** bid-specific: a bid, cover
letter, resume, or a plain "which of my work relates to this?" query all call into it.
It does NOT write anything; it retrieves and ranks.

## Only real content counts

Every folder ships with a `README.md` and a `_template.md` — these are scaffolding,
NOT user content. When listing, counting, or reading from `projects/` or `profiles/`,
**ignore `README.md` and `_template.md`** (and any file whose body is still the
unedited template placeholders). A folder that contains only those files is **empty**.

## Step 1 — Understand the input

Distill the input into what you'll match on. Depending on what the input is, this may
include:
- the core **problem(s)** or need it describes,
- the **skills**, **tech**, or **topics** involved,
- any **domain / seniority / audience** signals.

Use whatever is present — a one-line topic is enough; a full job post gives more. If
the caller already passed these extracted, use them instead of re-deriving.

## Step 2 — Rank the projects

**Use the index if it exists.** If `bid-resources/projects/INDEX.md` is present, read it
first — it carries each project's structured frontmatter (tech, domain, problem_tags,
has_outcome, url). Rank off the index, then open in full **only** the top candidates you
shortlist. This avoids reading every project on a large knowledge base. If there is no
`INDEX.md` (the user hasn't run `/ai-bid-gen:organize-kb` yet), fall back to scanning the
project files directly — behavior is the same, just slower. Either way, ignore any
project that is missing from the index but present as a file, and vice versa; the file is
the source of truth for content, so if in doubt, read the file.

Each project is both a case study and a credibility signal, so match on **any relevant
axis**:
- by **problem / topic** — the project's `problem_tags` / *Problem / Outcome* relate to
  the input, and/or
- by **tech / skills** — the project's `tech` / *Tech stack* overlaps the input.

Prefer projects that match on **multiple** axes, and prefer ones with a **measured
outcome** (`has_outcome: true`) and a **live production URL** (`url` set). Return them
ranked, each with a one-line reason it matched.

## Step 3 — Surface profile fit

List **every** real profile from `bid-resources/profiles/` (ignoring scaffolding) — do
not drop or omit any — each with a short, **factual** note on its fit (which of the
input's skills/tech it overlaps). Do **NOT** auto-select a profile — the caller or user
chooses. Keep the notes neutral: no ranking, no superlatives, no "strongest/best/weakest
fit," no recommendation. State overlap, not a verdict; the choice is the user's. This
step only informs that choice. Skip it if profile fit is irrelevant to the caller's
purpose.

## Step 4 — Report gaps

Flag weaknesses plainly:
- No project relates to the input's **problem / topic**.
- No project uses the relevant **tech / skills**.
- No profile is a strong fit.

Name exactly what's missing so the caller can decide to add material or proceed. Report
gaps as facts — never suggest filling a gap by claiming unsupported experience or
inventing a project. Fabrication is not a remedy.

## Output

Return, in order: the **ranked projects** (with why each matched), the **profile fit
notes** (when relevant), and any **gaps**. The caller decides what to use.
