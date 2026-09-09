---
name: lint-kb
description: Audit the bid-resources knowledge base and report what's weak — placeholder-only files, projects missing frontmatter, missing live URLs or measured outcomes, thin content, and frontmatter that contradicts the prose. Reports gaps for the user to fix; it does not invent or fill them. Use to health-check a knowledge base.
---

# Lint KB

Audit the knowledge base and tell the user, plainly, what is weak so **they** can fix it.
This skill only reports — it never invents content, fabricates a URL or outcome, or edits
a file to hide a gap. A KB that honestly reports "12 projects have no measured outcome"
is more useful than one that quietly papers over it.

## Only real content counts

Ignore `README.md` and `_template.md`. A folder that contains only those is **empty** —
report it as such.

## What to check

Across `bid-resources/projects/`, `profiles/`, and `sample-bids/`:

**Existence / emptiness**
- Any of the three folders empty (only scaffolding) → the user can't write a bid yet.
- Files still full of unedited `_template.md` placeholders → not real content; list them.

**Projects — retrieval readiness**
- Projects with **no frontmatter** (need `enrich-kb`).
- Frontmatter that **contradicts the prose** — e.g. `has_outcome: true` but the
  *Outcome* section is empty, a `url:` that doesn't appear in the body, or `tech`/`domain`
  tags the prose never mentions. Flag these; frontmatter is the retrieval index and must
  match the narrative it indexes.
- `INDEX.md` missing or stale (fewer/more entries than real project files) → recommend
  `build-index`.

**Projects — strength (report as counts, not errors)**
- How many projects have `has_outcome: false` (no measured result).
- How many have an empty `url` (no live link).
- Thin projects (little prose beyond the template headings).

**Profiles & sample-bids**
- Profiles missing a rate, headline, or skills.
- `## Portfolio items` entries that match no file in `projects/` — a rename or a typo,
  since every entry must name a real project file (report under **Retrieval**).
- Projects that appear in no profile's `## Portfolio items` — nothing attachable proves
  them (report as a count under **Strength**).
- Profiles with no `## GitHub / website` link — posts ask for one often enough that a
  missing link costs applications. The section left empty or still holding the template
  placeholder counts as missing; an explicit "none" satisfies the check. Report it, never
  fill it in — a guessed URL is worse than no URL.
- Fewer than ~2 sample bids (mimic/inspiration modes work far better with variety).

## Output

Group findings by severity:
- **Blocking** — anything that stops a bid being written (empty folder, no real samples).
- **Retrieval** — missing frontmatter / stale index / frontmatter-vs-prose contradictions.
- **Strength** — counts of missing outcomes/URLs and thin content, so the user knows
  where the portfolio is weak.

For each item, name the exact file(s) and say what to add. Recommend the fix skill where
one applies (`enrich-kb`, `build-index`). Do not change any file.
