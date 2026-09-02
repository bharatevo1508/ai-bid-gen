---
description: Organize the bid-resources knowledge base — read your prose projects, add structured frontmatter, build the retrieval index, and report gaps
---

Organize the user's `bid-resources/` knowledge base so bids retrieve faster and more
reliably. The user does **not** write any frontmatter themselves — you read their
existing project prose and structure it for them. This is the one command an existing
user runs (after reloading the plugin) to upgrade a plain-prose KB into a retrieval-ready
one.

This command is an **orchestrator** that composes three skills, in order. Follow each
skill's instructions exactly.

## Step 1 — Verify the knowledge base

Check that `bid-resources/` exists with `projects/`, `sample-bids/`, and `profiles/`. If
it's missing, tell the user to run `/ai-bid-gen:init` first, then stop.

## Step 2 — Enrich projects with frontmatter

Run the **`enrich-kb`** skill (`skills/enrich-kb/SKILL.md`). It reads each real project's
prose and adds/completes its YAML frontmatter (tech, domain, problem_tags, has_outcome,
url), non-destructively and idempotently. It never invents values and never rewrites the
prose body.

## Step 3 — Build the index

Run the **`build-index`** skill (`skills/build-index/SKILL.md`) to (re)generate
`bid-resources/projects/INDEX.md` from the enriched frontmatter. This is the compact file
`find-evidence` reads first to shortlist projects.

## Step 4 — Lint and report

Run the **`lint-kb`** skill (`skills/lint-kb/SKILL.md`) and present its findings. Give the
user a short, honest summary: how many projects were enriched and indexed, and where the
KB is weak (projects with no measured outcome, no live URL, thin content, or still on the
template). These gaps are for the **user** to fill — do not invent content to close them.

## Notes

- Safe to re-run any time the user adds or edits projects — enrichment skips files that
  already have complete frontmatter, and the index is regenerated fresh.
- Profiles and sample-bids are read in full at bid time and are not enriched here; they
  are still health-checked in Step 4.
