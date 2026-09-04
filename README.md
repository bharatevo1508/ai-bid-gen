# ai-bid-gen

Write winning bids and proposals from information you already have — projects
(each doubling as a case study), accepted sample bids, and profiles. You paste a
job description (or point it at a file), pick a profile, and it drafts a proposal that **strictly follows
the format of your accepted sample bids**, backed by your most relevant projects.

## Model-agnostic

This plugin is **not tied to Claude**. All of its logic lives in plain Markdown
instruction files, so **any AI coding assistant can use it** — Claude Code, Codex,
Cursor, or anything else that can read files and follow instructions.

- **Claude Code:** install it as a plugin (below) — you get the `/ai-bid-gen:init`,
  `/ai-bid-gen:organize-kb`, `/ai-bid-gen:write-bid`, and `/ai-bid-gen:md-to-txt`
  commands (plus the `write-bid`, `find-evidence`, `humanize`, `enrich-kb`,
  `build-index`, `lint-kb`, and `md-to-txt` skills) automatically.
- **Any other model/tool:** point the model at the instruction files directly
  (below). The behavior is identical because the files are the source of truth.

## How it works

```
1. Set up the knowledge base   →  creates bid-resources/ with 3 folders
2. Populate it                 →  drop in your projects, sample bids, profiles (plain prose)
3. Organize it                 →  auto-adds frontmatter + builds an index for fast retrieval
4. Write a bid                 →  paste a job description (or point at a file) → get a proposal
```

You write your projects as plain prose — you never author frontmatter yourself.
Step 3 reads that prose and structures it for you.

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
2. Takes the job description — **pasted, or a file** you point it at (`@jds/jd-001.md`).
   No URL crawling: job boards block crawlers, so a link is not accepted.
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
8. Tells you **which portfolio pieces to attach** — the items already published on the
   profile you bid as that back the projects the bid cites.
9. Refines on your feedback and saves to `bids/<NNN>/` — a sequential numbered folder
   holding `jd.md` (the post, verbatim), `bid.md` (the bid text alone, ready to copy and
   send) and `notes.md` (context, decisions, and a *gaps to fix in the knowledge base*
   list naming the exact files to add or improve before the next bid).
10. Need a paste-ready version? Run `/ai-bid-gen:md-to-txt bids/<NNN>/bid.md` — it writes
    `bid.txt` beside the source with the markdown stripped and paragraphs unwrapped, so
    it pastes cleanly into Google Docs or an application form. Saving a bid never
    produces a `.txt` on its own.

If the post carries its own block of screening questions, the bid keeps the cover letter
short and answers them as a verbatim `Q:` / `A:` list below the salutation, so each answer
can go straight into its field. Questions asked inside the post's prose are answered by
the letter itself.

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
/ai-bid-gen:init         # scaffold bid-resources/
# ...populate the folders with plain-prose projects, bids, profiles...
/ai-bid-gen:organize-kb  # structure the KB: auto-add frontmatter + build the index
```

Re-run `/ai-bid-gen:organize-kb` any time you add or edit projects — it only enriches
new/changed files and refreshes the index. **Already have a v1.0 knowledge base?** Just
reload the plugin and run it once to upgrade your existing projects.

To write a bid, run `/ai-bid-gen:write-bid` (or just ask: *"write a bid for this
job"*) and paste the description — or hand it a file: `/ai-bid-gen:write-bid @jds/jd-001.md`.
The `write-bid` skill takes over from there.

### Any other model (Codex, Cursor, etc.) — manual use

1. Clone this repo (or copy it) next to your bid materials:
   ```
   git clone https://github.com/bharatevo1508/ai-bid-gen.git
   ```
2. **Set up the knowledge base** — tell your model:
   > "Follow the instructions in `ai-bid-gen/commands/init.md`."

   It will create `bid-resources/` with the three folders and templates.
3. **Populate** the folders with your real content (plain prose is fine).
4. **Organize the knowledge base** — tell your model:
   > "Follow the instructions in `ai-bid-gen/commands/organize-kb.md`."

   It reads your project prose, adds retrieval frontmatter, builds the index, and
   reports any gaps.
5. **Write a bid** — tell your model:
   > "Follow the instructions in `ai-bid-gen/skills/write-bid/SKILL.md` to write a
   > bid for this job:" and paste the job description (or point it at a file holding it).

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
│   ├── organize-kb.md       # orchestrator: enrich + index + lint the knowledge base
│   ├── write-bid.md         # runs the write-bid skill
│   └── md-to-txt.md         # converts one .md file to paste-ready .txt beside it
├── skills/
│   ├── write-bid/
│   │   └── SKILL.md         # orchestrator: runs the full bid flow
│   ├── find-evidence/
│   │   └── SKILL.md         # find & rank relevant projects/profile for any input
│   ├── humanize/
│   │   └── SKILL.md         # make any output read human, not AI-generated
│   ├── enrich-kb/
│   │   └── SKILL.md         # read project prose → add structured frontmatter
│   ├── build-index/
│   │   └── SKILL.md         # generate projects/INDEX.md for fast retrieval
│   ├── lint-kb/
│   │   └── SKILL.md         # audit the KB and report gaps (never fills them)
│   └── md-to-txt/
│       ├── SKILL.md         # markdown → paste-ready plain text
│       └── scripts/
│           └── md_to_txt.py # the converter (verifies no word changed)
├── LICENSE
└── README.md
```

The plugin uses an **orchestrator + reusable skills** pattern:
- `write-bid` composes `find-evidence` (the "find & fetch" retrieval step) and
  `humanize` (the anti-AI-tell voice rules).
- `organize-kb` composes `enrich-kb`, `build-index`, and `lint-kb` to turn a
  plain-prose knowledge base into a retrieval-ready one.

`md-to-txt` stands alone: point it at any markdown file and it writes a paste-ready
`.txt` next to it, verifying that not one word changed.

The reusable skills are useful on their own and are the foundation for future outputs
(cover letters, resumes) that draw from the same knowledge base.
