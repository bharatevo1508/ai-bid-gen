# ai-bid-gen

Write winning bids and proposals from information you already have — case studies,
projects, accepted sample bids, and profiles. You paste a job description, pick a
profile, and it drafts a proposal that **strictly follows the format of your
accepted sample bids**, backed by the most relevant case studies and projects.

## Model-agnostic

This plugin is **not tied to Claude**. All of its logic lives in plain Markdown
instruction files, so **any AI coding assistant can use it** — Claude Code, Codex,
Cursor, or anything else that can read files and follow instructions.

- **Claude Code:** install it as a plugin (below) — you get the `/ai-bid-gen:init`
  command and the `write-bid` skill automatically.
- **Any other model/tool:** point the model at the instruction files directly
  (below). The behavior is identical because the files are the source of truth.

## How it works

```
1. Set up the knowledge base   →  creates bid-resources/ with 4 folders
2. Populate it                 →  drop in your case studies, projects, sample bids, profiles
3. Write a bid                 →  paste a job description → get a tailored proposal
```

### The knowledge base

```
bid-resources/
├── case-studies/   # problems you've solved — matched to a job by PROBLEM TYPE
├── projects/       # overview, responsibilities, tech stack, production URLs — matched by TECH
├── sample-bids/    # bids you already submitted AND won — the exact FORMAT to mirror
└── profiles/       # each profile's URL, intro, description, hourly rate, skills — the VOICE + rate
```

Each folder has a `README.md` explaining what goes there and a `_template.md`
showing the fields to fill in.

### What the bid generator does

1. Verifies `bid-resources/` exists.
2. Asks you to **paste** the job description (no URL crawling — paste is reliable).
3. **You choose the profile** to bid as.
4. Picks the **sample bid to mirror** (asks which one if you have several).
5. Analyzes the job and matches relevant **case studies** (by problem) and
   **projects** (by tech stack).
6. **Warns you** if evidence is missing (e.g. no case study backs the problem, no
   project uses the tech) and **asks clarifying questions** when anything is unclear.
7. Drafts the bid — **strictly following the sample bid's exact format and length**,
   in the chosen profile's voice. Pricing is included **only if the job asked** about
   rate/budget/hours.
8. Refines on your feedback and saves to `bids/<job-slug>/bid.md`.

> **The one hard rule:** the generated bid mirrors your chosen sample bid's format
> exactly — same structure, sections, ordering, and style. Only the content changes.

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

To write a bid, just ask: *"write a bid for this job"* and paste the description —
the `write-bid` skill takes over.

### Any other model (Codex, Cursor, etc.) — manual use

1. Clone this repo (or copy it) next to your bid materials:
   ```
   git clone https://github.com/bharatevo1508/ai-bid-gen.git
   ```
2. **Set up the knowledge base** — tell your model:
   > "Follow the instructions in `ai-bid-gen/commands/init.md`."

   It will create `bid-resources/` with the four folders and templates.
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
│   └── plugin.json          # plugin manifest
├── commands/
│   └── init.md              # scaffolds the bid-resources/ knowledge base
├── skills/
│   └── write-bid/
│       └── SKILL.md         # writes a bid from the knowledge base
└── README.md
```
