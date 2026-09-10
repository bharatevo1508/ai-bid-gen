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
  `/ai-bid-gen:organize-kb`, `/ai-bid-gen:score`, and `/ai-bid-gen:write-bid` commands
  (plus the `score`, `write-bid`, `find-evidence`, `humanize`, `enrich-kb`,
  `build-index`, and `lint-kb` skills) automatically.
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

It runs in two stages, each backed by files in `bids/<NNN>-<slug>/` — a numbered, titled
folder (e.g. `bids/001-realtime-dashboard/`) that gets created the moment you score a
job, whether or not you go on to bid.

**Stage 1 — Score** (`/ai-bid-gen:score`, or automatic as `write-bid`'s first step):

1. Verifies `bid-resources/` exists.
2. Takes the job description — **pasted, or a file** you point it at (`@jds/jd-001.md`).
   No URL crawling: job boards block crawlers, so a link is not accepted.
3. **Flags any hidden "prove you're human" instructions** planted in the job post and
   asks you how to handle them.
4. Saves the post verbatim to `jd.md`.
5. Analyzes the job and matches relevant **projects** — by problem type and/or by
   tech stack (each project doubles as a case study).
6. Writes a **0-10 confidence score** for how well your knowledge base backs this
   specific job, with the reasoning behind it, plus a *gaps to fix in the knowledge
   base* list naming the exact files to add or improve — both into `notes.md`. Low
   confidence isn't a stop sign; it's information for you to weigh before deciding
   whether to bid at all.

Between the stages, `write-bid` **pauses and asks whether to continue** — the score and
top gaps are shown, and you decide whether this job is worth drafting a bid for at all
before anything else happens.

**Stage 2 — Write** (`/ai-bid-gen:write-bid`, picks up from Stage 1's files):

1. **You choose the profile** to bid as.
2. Asks **how to use your samples** — either **mimic one specific sample** (copy its
   exact format) or **take inspiration from all of them** and craft a fresh, catchy
   bid with a strong hook from the pattern they share.
3. **Warns you** if the gap list from Stage 1 flags missing evidence and **asks
   clarifying questions** when anything is unclear.
4. Drafts the bid in the chosen profile's voice, written to **read as human, not
   AI-generated** — and to **read simply**: short sentences, outcome before tech, light on
   jargon, so a client skimming in seconds gets it on the first pass. Pricing is included
   **only if the job asked** about rate/budget/hours. In Inspiration mode, checks the
   draft actually follows the proof pattern it deduced from your samples — by quoting the
   draft itself, not just asserting it — the same way Mimic mode checks it against the one
   sample it's copying.
5. **Writes every draft straight to `bid.txt`**, from the first one — so you review and
   verify it by opening the file, not by scrolling chat. Refines on your feedback by
   editing that same file, and appends `notes.md` with which profile/mode you used, the
   pricing decision, and the evidence drawn on.

The number in `<NNN>-<slug>` keeps bids ordered; the slug keeps them scannable.

### The `bid.txt` file

`bid.txt` always has **three sections, separated by `---`**, present even when a section
has nothing in it — so an empty section reads as "considered, nothing here," not
"forgotten":

1. **The cover letter** — paste-ready plain text: no markdown syntax, each paragraph on
   one line so it reflows on paste, bare URLs that auto-link. This is the **only** part
   you paste into the Upwork proposal box, a Google Doc, or an email — nothing to clean
   up first.
2. **Suggested attachments** — the portfolio pieces already published on the profile you
   bid as that back the projects the letter cites, written in the same name / URL / short
   description / why-it-fits shape as a project cited in the letter, or `None.` if
   there's nothing to attach.
3. **Q&A** — if the post has a *list* of questions (Upwork's own screening block, or a
   numbered list embedded in the post itself), **you're always asked where to answer
   them** — inside the cover letter, or here as verbatim `Q:` / `A:` pairs so each one
   can be lifted straight into its own form field. Whichever you pick, this section
   always says so explicitly, rather than silently going quiet. A single one-off question
   mixed into the post's own prose (not a list) is answered inline in Section 1 either
   way — no need to ask about those.

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

To just check how well your knowledge base backs a job before committing to a bid, run
`/ai-bid-gen:score` and paste the description (or hand it a file). It writes `jd.md` and
a scored `notes.md` into `bids/<NNN>-<slug>/` and stops there — no bid is drafted.

To write a bid, run `/ai-bid-gen:write-bid` (or just ask: *"write a bid for this
job"*) and paste the description — or hand it a file: `/ai-bid-gen:write-bid @jds/jd-001.md`.
The `write-bid` skill takes over from there, running `score` first automatically if you
haven't already.

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
5. **Score a job (optional, standalone)** — tell your model:
   > "Follow the instructions in `ai-bid-gen/skills/score/SKILL.md` to score this
   > job:" and paste the job description (or point it at a file holding it).
6. **Write a bid** — tell your model:
   > "Follow the instructions in `ai-bid-gen/skills/write-bid/SKILL.md` to write a
   > bid for this job:" and paste the job description (or point it at a file holding it).
   > It runs the `score` skill first automatically if the job hasn't been scored yet.

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
│   ├── score.md             # runs the score skill
│   └── write-bid.md         # runs the write-bid skill
├── skills/
│   ├── score/
│   │   └── SKILL.md         # scores how well the KB backs a JD; writes jd.md + notes.md
│   ├── write-bid/
│   │   └── SKILL.md         # orchestrator: drafts the bid once a job is scored
│   ├── find-evidence/
│   │   └── SKILL.md         # find & rank relevant projects/profile for any input
│   ├── humanize/
│   │   └── SKILL.md         # make any output read human, not AI-generated, and easy to skim
│   ├── enrich-kb/
│   │   └── SKILL.md         # read project prose → add structured frontmatter
│   ├── build-index/
│   │   └── SKILL.md         # generate projects/INDEX.md for fast retrieval
│   └── lint-kb/
│       └── SKILL.md         # audit the KB and report gaps (never fills them)
├── LICENSE
└── README.md
```

The plugin uses an **orchestrator + reusable skills** pattern:
- `write-bid` depends on `score` having run for the job (auto-invoking it if not), and
  composes `humanize` (the anti-AI-tell voice rules) directly while drafting.
- `score` composes `find-evidence` (the "find & fetch" retrieval step) to work out what's
  relevant before turning it into a confidence score.
- `organize-kb` composes `enrich-kb`, `build-index`, and `lint-kb` to turn a
  plain-prose knowledge base into a retrieval-ready one.

The reusable skills are useful on their own and are the foundation for future outputs
(cover letters, resumes) that draw from the same knowledge base.
