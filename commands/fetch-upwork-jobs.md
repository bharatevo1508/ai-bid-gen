---
description: Fetch candidate jobs from Upwork (via a connected Upwork MCP server) matching your knowledge base's tech stacks, and save each as a raw job file under jobs/
argument-hint: [preset name from job-presets.md | leave blank to choose interactively]
---

Fetch Upwork job leads for the user by following the **fetch-upwork-jobs** skill.

Load and follow the instructions in `skills/fetch-upwork-jobs/SKILL.md` exactly, step by
step. That skill is the source of truth for how jobs get sourced: verify an Upwork MCP is
connected, load or create `job-presets.md` at the repo root, resolve search criteria and
run parameters (respecting the hard 10-jobs-per-run limit), fetch from Upwork, save each
job as a raw sectioned file under `jobs/`, and report back.

The preset name supplied with this command is: $ARGUMENTS

If a preset name was given, use it directly in Step 3 (skip straight to confirming run
parameters for that preset) instead of asking the user to pick one. If nothing was
supplied, present the available presets from `job-presets.md` and ask the user to choose
one or give custom criteria, per the skill's Step 3.

This command only fetches and saves raw job posts — it does not score them against the
knowledge base or draft a bid. Run `/ai-bid-gen:score` on a saved job file next.
