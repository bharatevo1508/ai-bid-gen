---
name: fetch-upwork-jobs
description: Pull candidate jobs directly from Upwork (via a connected Upwork MCP server) that match the tech stacks in your knowledge base, and save each as a raw, sectioned job file under jobs/. Use whenever the user asks to find, fetch, pull, or search for Upwork jobs/leads, wants new jobs matching their stack (MERN, MERN + LLM, WordPress, Laravel, Shopify/CMS, or a custom skill list), or asks about job-presets.md. This is the sourcing step that runs BEFORE score/write-bid — it never scores or drafts a bid itself, only saves raw job posts to disk.
---

# Fetch Upwork Jobs

Pull job leads straight from Upwork and save each one, raw but clearly sectioned, to
`jobs/<jobid>-slug.md` — so the user has a pile of candidate posts to run through
`/ai-bid-gen:score` later. This skill never scores a job or drafts a bid; it only
sources and saves.

## Step 1 — Verify an Upwork MCP is connected

This skill depends entirely on an Upwork MCP server being connected — there is no
built-in Upwork access. Check for it before doing anything else:

1. Look at the tools already visible in context for anything with `upwork` in the name.
2. If none are visible, run `ToolSearch` with query `"upwork"` to check for a deferred
   Upwork tool that hasn't been loaded into context yet.

If a matching tool (or tools) is found, note its exact name(s) — you'll call it in Step 5.
Tool names vary by MCP server, so don't assume a specific one; use whatever you actually
find.

If nothing is found, **stop here**. Tell the user plainly that no Upwork MCP server is
connected, that this skill can't fetch real jobs without one, and that they need to
connect an Upwork MCP server first. Do not fabricate, guess, or hallucinate job listings
to fill the gap — an empty, honest stop is correct behavior here.

## Step 2 — Load or create `job-presets.md`

This file lives at the **repo root** (not inside `bid-resources/`) and holds reusable
search criteria so the user doesn't have to re-answer the same questions every run.

**If it already exists:** read it as-is. Never overwrite or reformat a preset the user
has edited — treat their content as authoritative.

**If it doesn't exist:** create it with this exact structure — a `default` preset, two
more example presets covering different stacks/locations, and a `_template` block the
user can copy to add their own:

```md
# Job Presets

Reusable search criteria for `/ai-bid-gen:fetch-upwork-jobs`. Pick one by name when
prompted, or copy `_template` below to add your own.

## default
- Jobs to fetch: 1
- Tech stack: MERN
- Experience level: Intermediate
- Experience years: 2-5
- Client location: USA

## mern-llm-usa
- Jobs to fetch: 5
- Tech stack: MERN + LLM Integration
- Experience level: Expert
- Experience years: 5+
- Client location: USA

## wordpress-foreign
- Jobs to fetch: 5
- Tech stack: WordPress
- Experience level: Intermediate
- Experience years: 2-5
- Client location: Foreign

## _template
- Jobs to fetch: <1-10, hard capped at 10 per run>
- Tech stack: <MERN | MERN + LLM Integration | WordPress | Laravel | CMS (Shopify etc.) | comma-separated custom skills>
- Experience level: <Entry | Intermediate | Expert>
- Experience years: <e.g. 2-5, or 5+>
- Client location: <USA | UK | Foreign | India>
```

Report to the user that you created it, so they know it's now theirs to edit.

## Step 3 — Choose criteria and run parameters

Present the presets found in `job-presets.md` (name + a one-line summary of its
criteria) and ask the user to either pick one, or supply custom criteria for this run
only (a one-off customization is not saved back to `job-presets.md` unless they ask you
to add it as a new preset).

Also resolve two run parameters, defaulting sensibly but always confirming with the user
rather than silently assuming:

- **Number of jobs to fetch** — default **1**, offer **5** as a second option, and allow
  a custom number. **Hard limit: never fetch more than 10 jobs in a single run**, no
  matter what the preset or the user asks for — Upwork can IP-block scraping-shaped
  traffic, and this cap exists specifically to avoid that. If the resolved number is
  above 10, clamp it to 10 and tell the user why.
- **Output location** — default `jobs/` at the repo root (files land at
  `jobs/<jobid>-slug.md`). Ask the user to confirm this default or name a different
  target directory before fetching anything.

## Step 4 — Search Upwork

Using the Upwork MCP tool(s) found in Step 1, search for jobs matching the resolved tech
stack, experience level/years, and client location, requesting the clamped job count from
Step 3.

## Step 5 — Save each job, raw but sectioned

For every job returned, save it as its own file at
`<output-dir>/<jobid>-slug.md` (default `jobs/<jobid>-slug.md`):

- **`<jobid>`** — Upwork's own job ID for that posting (not a locally-generated sequence
  like the `bids/<NNN>-...` numbering elsewhere in this plugin — the Upwork ID is what
  makes this file traceable back to the source and prevents re-saving the same job twice).
- **`slug`** — three or four lowercase hyphenated words from the job title.

Use this exact section structure. The **Description** and **Screening Questions**
sections are copied **verbatim** — no summarizing or reformatting, same rule `score`
follows for `jd.md`:

```md
# <Job Title>

## Job Info
- Job ID: <upwork job id>
- URL: <job posting URL>
- Posted: <posted date>
- Budget/Rate: <fixed price or hourly range>
- Duration: <estimated duration/length, if given>

## Client Info
- Location: <client's country>
- Rating: <client rating, if shown>
- Hire history: <jobs posted / hire rate, if shown>
- Payment verified: <yes/no, if shown>

## Description
<the job post text, verbatim>

## Skills / Tags
- <skill 1>
- <skill 2>

## Screening Questions
<verbatim, only if the post has them — omit this whole section if it doesn't>
```

Leave a field blank (don't invent a value) if Upwork didn't return it.

**Never overwrite** a file for a job ID that's already been saved in the target
directory — skip it and note the skip in Step 6's report. This makes re-running the same
preset later safe: it naturally dedupes against jobs already pulled.

The `Job ID:` line under `## Job Info` is also the dedup key downstream: `score` records
it as the `Source:` in `notes.md` and refuses to score the same job into a second
`bids/<NNN>-…` folder. Always populate it when Upwork returns it — an empty Job ID
defeats dedup at both layers.

## Step 6 — Report back

Tell the user, in one short list:
- Each job saved: title + file path.
- Any job skipped because it was already saved (job ID match).
- Whether the job count was clamped to the 10-job hard limit, and from what.

Close by pointing at the next step: running `/ai-bid-gen:score` on any of these files to
check knowledge-base fit before drafting a bid. This skill's job ends at saving raw files
— it never scores or drafts anything itself.
