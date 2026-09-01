# ai-bid-gen

Write winning bids and proposals from information you already have — projects
(each doubling as a case study), accepted sample bids, and profiles. You paste a
job description, pick a profile, and it drafts a proposal that **strictly follows
the format of your accepted sample bids**, backed by your most relevant projects.

## Model-agnostic

This plugin is **not tied to Claude**. All of its logic lives in plain Markdown
instruction files, so **any AI coding assistant can use it** — Claude Code, Codex,
Cursor, or anything else that can read files and follow instructions.

- **Claude Code:** install it as a plugin (below) — you get the `/ai-bid-gen:init`
  and `/ai-bid-gen:write-bid` commands (plus the `write-bid`, `find-evidence`, and
  `humanize` skills) automatically.
- **Any other model/tool:** point the model at the instruction files directly
  (below). The behavior is identical because the files are the source of truth.

## How it works

```
1. Set up the knowledge base   →  creates bid-resources/ with 3 folders
2. Populate it                 →  drop in your projects, sample bids, profiles
3. Write a bid                 →  paste a job description → get a tailored proposal
```

### The knowledge base

```
bid-resources/
├── projects/       # each project is both a case study AND a credibility signal —
│                   # problem, solution, tech stack, outcome, production URL.
│                   # Matched to a job by PROBLEM TYPE and/or TECH.
├── sample-bids/    # bids you already submitted AND won — the exact FORMAT to mirror
└── profiles/       # each profile's URL, intro, description, hourly rate, skills — the VOICE + rate
```

Each folder has a `README.md` explaining what goes there and a `_template.md`
showing the fields to fill in.

### What the bid generator does

1. Verifies `bid-resources/` exists.
2. Asks you to **paste** the job description (no URL crawling — paste is reliable).
3. **You choose the profile** to bid as.
4. Asks **how to use your samples** — either **mimic one specific sample** (copy its
   exact format) or **take inspiration from all of them** and craft a fresh, catchy
   bid with a strong hook from the pattern they share.
5. Analyzes the job and matches relevant **projects** — by problem type and/or by
   tech stack (each project doubles as a case study). It also **flags any hidden
   "prove you're human" instructions** planted in the job post and asks you how to
   handle them.
6. **Warns you** if evidence is missing (e.g. no project backs the problem or uses
   the tech) and **asks clarifying questions** when anything is unclear.
7. Drafts the bid in the chosen profile's voice, written to **read as human, not
   AI-generated**. Pricing is included **only if the job asked** about
   rate/budget/hours.
8. Refines on your feedback and saves to `bids/<job-slug>/bid.md`.

> **Mimic mode** reproduces your chosen sample's format exactly — same structure,
> sections, ordering, and style; only the content changes. **Inspiration mode**
> builds its own best-of structure from the shared DNA of all your winning samples.

## Install

### Claude Code (as a plugin)

```
/plugin marketplace add bharatevo1508/ai-bid-gen
/plugin install ai-bid-gen
```

Then, inside the project where you keep your bid materials:

```
/ai-bid-gen:init      # scaffold bid-resources/
# ...populate the folders...
```

To write a bid, run `/ai-bid-gen:write-bid` (or just ask: *"write a bid for this
job"*) and paste the description — the `write-bid` skill takes over.

### Any other model (Codex, Cursor, etc.) — manual use

1. Clone this repo (or copy it) next to your bid materials:
   ```
   git clone https://github.com/bharatevo1508/ai-bid-gen.git
   ```
2. **Set up the knowledge base** — tell your model:
   > "Follow the instructions in `ai-bid-gen/commands/init.md`."

   It will create `bid-resources/` with the three folders and templates.
3. **Populate** the folders with your real content.
4. **Write a bid** — tell your model:
   > "Follow the instructions in `ai-bid-gen/skills/write-bid/SKILL.md` to write a
   > bid for this job:" and paste the job description.

That's it — the Markdown files drive the whole process regardless of which model
you use.

## Structure

```
ai-bid-gen/
├── .claude-plugin/
│   ├── marketplace.json     # marketplace manifest (required for remote install)
│   └── plugin.json          # plugin manifest
├── commands/
│   ├── init.md              # scaffolds the bid-resources/ knowledge base
│   └── write-bid.md         # runs the write-bid skill
├── skills/
│   ├── write-bid/
│   │   └── SKILL.md         # orchestrator: runs the full bid flow
│   ├── find-evidence/
│   │   └── SKILL.md         # find & rank relevant projects/profile for a job
│   └── humanize/
│       └── SKILL.md         # make any output read human, not AI-generated
├── LICENSE
└── README.md
```

The `write-bid` skill is an **orchestrator** — it composes two reusable skills:
`find-evidence` (the "find & fetch" retrieval step) and `humanize` (the anti-AI-tell
voice rules). Both are useful on their own and are the foundation for future outputs
(cover letters, resumes) that draw from the same knowledge base.
