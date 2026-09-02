---
name: enrich-kb
description: Read the prose in each bid-resources project file and add a structured YAML frontmatter block (tech, domain, problem_tags, has_outcome, url) so retrieval is fast and reliable. Use to organize a knowledge base that was written as plain prose, or to backfill frontmatter into projects that don't have it yet. Non-destructive — it only adds frontmatter, never rewrites the case-study prose.
---

# Enrich KB

Turn plain-prose project files into retrieval-ready files by adding a structured
**frontmatter** block to each one. The user is not expected to write frontmatter by
hand — you read what they already wrote and structure it for them.

This is the "structure it for me" step. It does **not** write bids and does **not**
rewrite anyone's prose. It reads each project's existing case-study text and prepends a
YAML frontmatter block that the retrieval step (`find-evidence`) and the index builder
(`build-index`) can rely on.

## The frontmatter schema (this file is the authority)

Every real project file in `bid-resources/projects/` should carry this block at the very
top, before the `# <Project name>` heading:

```yaml
---
title: Acme Realtime Dashboard
tech: [react, node, postgres, websockets]
domain: [fintech]
problem_tags: [dashboard, real-time, data-viz]
has_outcome: true
url: https://acme.example.com
---
```

Field rules:
- **`title`** — the project name (from the `#` heading).
- **`tech`** — a flat list of concrete technologies named in the *Tech stack* section
  (and elsewhere in the prose). Lowercase, canonical names (`postgres`, not
  `PostgreSQL DB`). This is the tech-axis match key.
- **`domain`** — industry/domain signals (`fintech`, `healthcare`, `ecommerce`). Empty
  list `[]` if the prose gives no clear domain. Do not guess.
- **`problem_tags`** — short kebab tags for the *kind of problem* solved
  (`dashboard`, `migration`, `real-time`, `payments`, `search`). This is the
  problem-axis match key.
- **`has_outcome`** — `true` only if the prose contains a **measured** result (a number,
  %, time saved, revenue, scale, uptime). If the *Outcome / Results* section is empty or
  vague, set `false`. Do not invent an outcome to justify `true`.
- **`url`** — the live production URL if one is present in the prose; otherwise leave it
  empty (`url:`). Never fabricate a URL.

## Only real content counts

Ignore `README.md` and `_template.md`, and skip any file whose body is still unedited
template placeholders — those are not real projects and must not be enriched. If a file
is only placeholders, leave it and let `lint-kb` report it.

## Never invent — same honesty rule as the rest of the plugin

Frontmatter must be **derived from the prose, not imagined**. If you cannot tell a
field's value from what the user wrote:
- lists (`domain`, `problem_tags`, `tech`) → include only what the text supports;
- `has_outcome` → `false`;
- `url` → empty.

It is correct for a thin project to get a thin frontmatter block. `lint-kb` will surface
those gaps for the user to fill; you must not paper over them.

## Idempotent — safe to re-run

Users add projects over time and re-run the organizer.

- A file that **already has a complete, valid frontmatter block** → leave it untouched
  (do not clobber values the user may have hand-tuned), unless the caller explicitly
  asks for a full re-enrich.
- A file with **no frontmatter, or an incomplete block** → add or complete it.
- Never rewrite, reorder, or trim the prose body. You only touch the frontmatter block
  at the top.

## Steps

1. List the real project files in `bid-resources/projects/` (skip scaffolding and
   placeholder-only files).
2. For each file that needs it, read the prose, derive the schema fields above, and
   write the frontmatter block at the very top of the file, immediately followed by the
   existing content unchanged.
3. Report what you enriched, what you skipped (already had frontmatter), and which files
   came out thin (e.g. `has_outcome: false`, empty `url`, empty `domain`) so the caller
   can pass that to the user.

> Profiles and sample-bids are few and are read in full at bid time, so they do **not**
> need frontmatter. This skill enriches `projects/` only.
