---
name: write-bid
description: Write a bid/proposal from a job description — pasted or in a file — using the bid-resources knowledge base (projects, sample bids, profiles). Use when the user wants to draft an Upwork/freelance bid or proposal. The user chooses whether to mimic one sample bid's exact format or take inspiration from all samples and craft a fresh, catchy bid.
---

# Write Bid

Generate a bid/proposal for a job by grounding it in the user's `bid-resources/`
knowledge base. This skill is the **orchestrator** — it owns the conversation flow and
composes three shared skills:
- **`score`** (`skills/score/SKILL.md`) — the JD-vs-KB relevance check. Every job must be
  scored before a bid is drafted; this skill's Step 1 runs `score` automatically if it
  hasn't run yet.
- **`find-evidence`** (`skills/find-evidence/SKILL.md`) — the find & fetch / ranking step,
  called by `score`, not by `write-bid` directly.
- **`humanize`** (`skills/humanize/SKILL.md`) — the rules that keep the bid from reading
  as AI-generated.

Follow the steps in order. Do not skip the checkpoints.

## Two modes — the user picks how samples are used

The bid is written in one of two modes, chosen by the user in Step 3:

**Mimic mode — the non-negotiable rule.** When the user picks one specific sample to
mimic, the generated bid MUST strictly follow the exact format of that sample. Same
structure, same sections, same ordering, same style, same approximate length. Do NOT
add sections, remove sections, reorder, or introduce a different format under any
circumstance. That sample is the format authority — mirror it exactly. The only thing
that changes is the *content*, tailored to this job. No caveats, no diversion.

The sample governs the **cover letter**. Step 2 always asks the user where a list of
screening questions should be answered — inside the letter, or in `bid.txt`'s separate
Q&A section. If the user picks the **separate section**, it's not counted as a section
added to the sample's format — the letter above it still mirrors the sample exactly. If
the user picks **inside the letter**, flag the tension plainly before drafting: working a
numbered question list into the letter usually means adding a structural device (numbered
answers) the sample doesn't have, which conflicts with the non-negotiable "no sections
added" rule above. Tell the user this, and let them either confirm they want the
deviation (and accept the mimic checkpoint will report it as a real section-count
mismatch, not paper over it) or switch to the separate section instead.

**Inspiration mode.** When the user picks inspiration-from-all, do NOT copy any one
sample. Instead, study every sample, deduce the winning pattern they share, and craft
your own best-of structure — a strong hook, the persuasion beats they have in common,
natural length. See Step 5 for how to synthesize it, and Step 5a′ for how the draft gets
checked against what you deduced. This mode is allowed to depart from any single sample's
exact format because it is building a new one from the shared DNA of all of them.

In both modes, the bid must read as human **and be easy to skim** — always apply the
**`humanize`** skill, including its **Readability** rules (short sentences, outcome before
mechanism, a jargon budget), on every line. See Step 5.

**Readability vs. the modes.** Readability governs *sentences*; the modes govern
*structure*. They do not conflict. Mimic mode still mirrors the sample's sections,
ordering, and length exactly — readability only decides that, between two phrasings that
fit the sample, you pick the clearer one; it never adds or drops a section. Inspiration
mode applies the Readability rules at full force. A dense sample is not a licence to write
a dense bid: keep the sample's shape, write clearer sentences inside it.

## Step 1 — Ensure the job has been scored

Check whether this job already has a folder in `bids/` with a `notes.md` containing a
`## Score` section.

- **If not** (a brand-new JD, or an existing folder from before scoring existed): run the
  **`score`** skill (`skills/score/SKILL.md`) now, start to finish, using the job
  description the user supplied. It verifies the knowledge base, reads the JD, detects
  embedded traps, creates `bids/<NNN>-<slug>/`, writes `jd.md`, runs `find-evidence`,
  computes the score, and writes `## Job context` / `## Score` / `## Gaps to fix in the
  knowledge base` into `notes.md`. Report its summary to the user as `score` normally
  does.
- **If it has already been scored:** don't re-run `score` or re-derive its findings. Read
  `jd.md` and `notes.md`'s `## Job context`, `## Score`, and `## Gaps` back into context,
  and show the user the existing score + top gaps so they see the same signal they would
  from a fresh run.

### Checkpoint — confirm before drafting

Either way, **STOP here.** This skill is not a single uninterrupted pipeline that runs
straight through to a saved `bid.txt` — it always breaks in two after scoring. Ask the
user whether to proceed, e.g.:

> "Scored **6/10** — see `notes.md` for the full breakdown. Want me to go ahead and draft
> a bid for this job, or stop here?"

and **wait for their reply before doing anything else.** Do not start Step 2 in the same
turn, do not pick a profile, do not assume the answer is "yes" because the user invoked
`write-bid` in the first place — invoking the command starts the scoring stage, not a
commitment to draft. This is the one place in the flow where the user decides whether
this job is worth bidding on at all, now that they have the KB-relevance signal in front
of them — a low score doesn't block them, but it must be a deliberate choice to proceed.
If the user says no, stop: the job folder (`jd.md` + `notes.md`) stays exactly as `score`
left it, which is already a complete, valid record.

## Step 2 — Pricing gate + screening-question classification

From the job description now on disk, determine:

- Whether the job **explicitly asks the applicant to state their rate / quote / hours**
  (this determines whether pricing appears in the bid at all — see Step 5).
  **A posted budget or rate range is NOT such a request.** A client writing "$25–$45/hr"
  or "budget: $2,000" is stating *their* number, not asking for *yours*. The pricing
  gate opens only when the job asks the applicant a direct question like "what's your
  rate?", "how much do you charge?", "include your hourly rate", or "quote a fixed
  price". If the job merely posts a range, mentions a budget, or says it will pay more
  for the right person, the gate stays **closed** — do not volunteer a number.
- Whether the job **requires a link to a GitHub profile, personal website, or portfolio**
  ("send a link to your GitHub and/or website"). Read this the way the pricing gate is
  read: a client linking their *own* site is not a request. When it *is* a request, the
  link comes from the chosen profile's `## GitHub / website` field in Step 3 — and if that
  field is empty, it is a gap for Step 4, never something to paper over with a project URL
  or the Upwork profile link.

(Trap detection already happened in `score`'s Step 3 — it is not repeated here.)

### Classify the questions the post asks

List every question the post puts to the applicant, then split it into two different
kinds:

- **A single, organic question inside the post's prose** — one question mixed into the
  description, not part of a list ("tell me about a time you scaled Postgres", "what
  would your first week look like?"). Too small to be its own section: always answered
  *inline*, worked into the cover letter's own prose in Step 5. No placement choice
  needed here.
- **A list of questions** — several discrete questions presented as a set. This covers
  **both** shapes: Upwork's own separate screening-question block (each with its own
  answer field on the form) **and** a numbered list embedded in the post's own text
  (e.g. "Application Instructions: answer the following 10 questions in order"). Either
  shape counts as a list.

**Whenever there's a list, always ask the user where the answers should go — every time,
never infer it from how the post itself structured the questions.** The post's own
formatting is not the user's preference; a numbered list *in the post* does not mean the
answers must stay numbered *in the letter*. Ask:

> "This job has N questions structured as a list. Where do you want them answered —
> **(a) inside the cover letter itself**, in the letter's own flow, or
> **(b) in `bid.txt`'s separate Q&A section**, after the letter?"

Show the user the full question list either way, before drafting, so they can correct
anything mis-scoped. If there are no questions of either kind, say so in one line and
move on — there's nothing to ask about.

## Step 3 — Select the profile and the sample mode

**Profile (user chooses — no auto best-match).** List **every** real profile from
`bid-resources/profiles/` (ignore scaffolding) — do not silently drop or omit any — and
ask the user which profile they are bidding as. Do NOT pick the "best matching" profile
automatically, and do NOT steer: present each profile's fit **factually** (skills/tech
overlap with the job) without ranking language, superlatives, or a recommendation. Do
not call one the "strongest fit," "best," or "weakest" — those steer the reader toward a
choice that is the user's to make. Once the user picks, read the chosen profile file for
its voice, headline, intro style, skills, hourly rate, its `## GitHub / website` link, and
its `## Portfolio items` array (the projects already published on that Upwork profile,
named by their file in `bid-resources/projects/`). Treat both of those fields as optional
in older knowledge bases: if a section is absent or still holds the template placeholder,
the profile simply has nothing on record there — say so when it matters, and never invent
a link or a portfolio entry.

**Sample mode.** Read `bid-resources/sample-bids/` (real bids only — ignore scaffolding).
A usable sample is a **complete, real bid**. A file that still carries unfilled placeholder
sections (`[PROJECT 1 – insert details]`, `Insert project details…`) is a skeleton, not a
sample: do not mimic it and do not fold it into the inspiration-mode pattern, because its
"format" is a blank to fill, not a format that won work. If a partially-filled skeleton is
the only thing present, treat the folder as having no real sample and say so.
If there are no real samples, stop and tell the user to add at least one won bid first.
Otherwise ask:

> "Do you want me to **(a) mimic one specific sample** — copy its exact format — or
> **(b) take inspiration from all your samples** and craft a fresh, catchy bid from the
> pattern they share?"

**If (a) mimic:** one sample → use it; multiple → ask which. The chosen sample defines
the EXACT format and target length. This is **Mimic mode** — the non-negotiable rule
applies (see top).

**If (b) inspiration:** read all samples and deduce their shared winning pattern (hook,
credibility, problem framing, calls to action, tone, typical length, and specifically the
**device** each sample uses to present past-work proof — e.g. a labeled bulleted list of
bare URLs, one line each). Name that device explicitly; you'll need it verbatim in Step
5a′. This is **Inspiration mode**.

## Step 4 — Gap check + clarifying questions (prompt the user)

Before drafting, prompt the user if anything is weak or ambiguous:

- **Missing evidence:** use the `## Gaps to fix in the knowledge base` that `score`
  already wrote into `notes.md` in Step 1. If no project backs the job's problem, or none
  use the required tech, or the chosen profile lacks key info, TELL the user plainly,
  e.g.:
  > "Heads up — the gap check found no project backing <problem>, and none use <tech>.
  > The bid will be weaker without proof. Do you want to add one, or proceed anyway?"
  Name exactly what's missing. The only routes you may offer are: **add real material**,
  **proceed with honest framing** (acknowledge the gap or lead with adjacent proof), or
  **skip this job**. **Never** offer to fabricate — do not present "claim <tech> without a
  project" or any invented experience as an option. The bid must never assert experience
  the knowledge base does not support.
- **Missing profile link:** if the job requires a GitHub/website/portfolio link (Step 2)
  and the chosen profile's `## GitHub / website` is empty or missing, tell the user
  plainly — an unanswered mandatory screening item usually means the application is
  filtered out. Offer to add the link to the profile file, or to state its absence
  honestly. Do **not** substitute a project URL or the Upwork profile link for it.
- **Ambiguity:** if any part of the job is unclear (scope, which deliverable, which
  project to highlight), ask clarifying questions rather than guessing.

Any *new* gap you find here (beyond what `score` already recorded) gets added to the same
`## Gaps to fix in the knowledge base` list when you save in Step 7 — it covers every kind
of gap, not just missing projects: a missing `## GitHub / website` link, a project with no
measured outcome or no live URL, a cited project that is in no profile's `## Portfolio
items`.

## Step 5 — Draft the bid

**Every draft, including the first one, is written straight to
`bids/<NNN>-<slug>/bid.txt`** — in the exact three-section format specified in Step 7 —
not just pasted into chat. The user verifies a bid by reading the file, not by reading
a chat bubble, so the file is the real draft from the start; chat gets a short pointer to
it plus anything that needs the user's input (checkpoint verdicts, questions), not a
second copy of the text. This applies to the very first draft and to every revision in
Step 6 — there is no "draft in chat, save later" phase.

Write the bid according to the mode chosen in Step 3:

- **Format (Mimic mode):** strictly mirror the chosen sample bid — exact structure,
  sections, ordering, and style. (See the non-negotiable rule above.) Match that
  sample's length within **±15%** of its word count. Before writing the draft to
  `bid.txt`, run the mimic-mode verification checkpoint (Step 5a).
- **Format (Inspiration mode):** build your own structure from the pattern you deduced
  across all samples in Step 3, including the specific past-work-proof device you named
  there. Open with a **strong, specific hook** (not a generic "I'm excited to apply"),
  follow the persuasion beats the samples share (credibility, understanding of the
  client's problem, proof, clear next step), and keep it around the samples' typical
  length. **Keep it tight** — the client is skimming, so a shorter bid that lands beats a
  longer one that has to be waded through; when in doubt, cut. Before writing the draft to
  `bid.txt`, run the inspiration-mode format checkpoint (Step 5a′).
- **Voice:** use the chosen profile's voice and positioning, and apply the
  **`humanize`** skill (`skills/humanize/SKILL.md`) to every line — no em-dash spam, no
  buzzwords, no robotic parallelism. It must not read as AI-written.
- **Readability:** apply `humanize`'s **Readability** rules as you draft, not as an
  afterthought. One idea per sentence; break any sentence stacking three or more points.
  Lead each project with the **outcome** (the result, the problem solved) before the tech.
  Name a stack once, in a phrase; drop or plainly gloss acronyms a non-technical client
  won't know. Short paragraphs over walls of prose. Specific *and* simple.
- **Evidence:** weave in the projects confirmed by `score`'s `find-evidence` call as
  proof — their problem/outcome story and production URLs where relevant.
- **Pricing / rate:** include pricing ONLY if the job explicitly asked the applicant to
  state their rate/quote (see the Step 2 test). If it asked, address it using the
  profile's hourly rate (and estimate hours/total only if the job is fixed-price and
  pricing detail is requested). If the job did not ask — including when it merely posts a
  budget or a range, or says it will pay more for the right person — do NOT mention rate,
  a number, or your positioning on price **at all**, even to say you're a good value or
  won't mark up. A posted range is not an invitation to respond with your own figure.

### Answering the questions from Step 2

**The single organic question** (not a list) is answered by the letter itself, worked
into the prose the way a person would answer it. Before saving the draft, check it's
actually addressed; an unanswered question the client asked in the post reads as a bid
that wasn't read.

**A list of questions** goes wherever the user chose in Step 2's prompt:
- **Inside the cover letter:** work the answers into Section 1 itself, in the letter's own
  flow and numbering (see job-embedded lists like a numbered "Application Instructions"
  block for the shape this usually takes). `bid.txt`'s Section 3 still exists — see Step
  7 for what it says in this case — but the letter itself is where the answers live.
- **In the separate Q&A section:** the letter (Section 1) stays short and does not answer
  them at all; they're answered only in `bid.txt`'s Section 3 (Step 7).

Never split one list across both places — the user picked one location, so every question
in that list goes there.

### Suggested attachments

Alongside the letter, work out which portfolio pieces to attach: the entries in the
chosen profile's `## Portfolio items` that back the projects the bid actually cites, each
named with the claim it proves. Suggest **only** names present in that array — those are
the pieces that already exist on the profile and can be attached. If a cited project is
not in the array, say so plainly ("`realtime-sync` is cited but isn't a portfolio item on
this profile, so there's nothing to attach for it") and record it as a gap for Step 7's
`## Gaps to fix in the knowledge base`. Never invent a portfolio piece, and never suggest
attaching something the array does not list.

Write each suggested attachment in the **same block shape as a project in the cover
letter** — name, URL, short description, then why it fits this job:

```
<Project name> — <https://project-url, or "no public URL" if it doesn't have one>
<one-line description of the project, same as the cover letter would use>
Why it fits: <the specific claim in the letter/Q&A this attachment backs>
```

This list becomes `bid.txt`'s Section 2 in Step 7 — it is not written to `notes.md`.

## Step 5a — Mimic-mode verification checkpoint (Mimic mode only)

Before writing a mimic-mode draft to `bid.txt`, verify it against the chosen sample and
**state the numbers** — never claim parity without measuring it:

1. **Word count.** Count the sample's words and the draft's words — the **letter only**,
   excluding the Q&A section, which the sample has no counterpart for. The draft must be
   within **±15%** of the sample. If it is outside the band, revise (cut or expand) until
   it is inside, then re-count. Do not proceed on a draft that fails the band.
2. **Section parity.** List the sample's sections/blocks in order, then the draft's —
   again the letter only, not the Q&A section. They
   must match **1:1** — same count, same types, same order. No section added, none
   dropped. If they differ, fix the draft.
3. **Report honestly.** When you save the draft, tell the user the actual figures, e.g.
   "sample 287 words / draft 305 words (+6%), 9 blocks in the same order — saved to
   `bids/012-.../bid.txt`." Do NOT write "comparable length" or "same length" unless the
   counts back it up. A false parity claim is worse than a visible miss, because it tells
   the user not to re-check — and now the user can re-check directly, in the file.

## Step 5a′ — Inspiration-mode format checkpoint (Inspiration mode only)

Mimic mode has Step 5a to catch drift between what's claimed and what's delivered.
Inspiration mode needs the same discipline — "deduce the shared pattern" in Step 3 is not
itself a guarantee the draft follows it, and **a narrative summary claiming compliance is
not a check** — "file-ai uses the bulleted-link device" is a claim; only the literal text
of the draft can confirm or refute it. Before writing an inspiration-mode draft to
`bid.txt`:

1. **State the pattern explicitly**, using the concrete vocabulary from Step 3 — not a
   vague paraphrase. "Labeled bulleted project list, bare URL + one-line description" is
   checkable; "a proof section" is not.
2. **Verify per project, by quoting the draft — not by describing it.** List every
   project the letter cites. For each one, quote the exact line(s) from the draft that
   introduce it, then check that literal quote against the stated pattern (is the URL on
   its own line, as its own token, the way the pattern requires — or is it folded into a
   sentence?). Judge the quote, not your memory of what you intended to write. Mark each
   project **PASS** or **FAIL** against the pattern based on that quote.
3. **A project only qualifies for the trade-off exception in step 4 if it genuinely has no
   URL** — cross-check against `score`'s evidence (`notes.md`'s `## Evidence used` /
   `find-evidence`'s findings), not assumption. A project that has a URL and still failed
   its quote check in step 2 is a **drafting defect to fix**, not a trade-off to declare —
   revise the draft so the URL is on its own line, then re-quote and re-check.
4. **If a device genuinely can't be followed** — the project has no URL on record at
   all — that is a **declared trade-off**, stated out loud when you present the draft
   ("Cortex has no public URL on file, so it's introduced in prose instead of the bulleted
   list the other two use"). It is never a silent prose rewrite that quietly drops the
   pattern, and never a label applied to a project that actually had a URL available.
   Record it in Step 7's `## Gaps to fix in the knowledge base`, explicitly linked to the
   format compromise it forced — not just "no URL" on its own.
5. **Report the per-project verdicts before writing the draft to `bid.txt`**, the same
   way Step 5a reports word counts instead of claiming "comparable length" on faith, e.g.:
   "cultbooking: no URL on file, trade-off declared. cortex: no URL on file, trade-off
   declared. file-ai: has a URL — quote check FAILS, URL is inline mid-sentence, not its
   own line — revised." Do not save a draft until every cited project either PASSes the
   quote check or has a genuine, evidence-backed trade-off — not until the numbers merely
   *sound* right.

## Step 5b — Readability checkpoint (both modes)

Before writing **any** draft to `bid.txt`, in either mode, read it once as the client
will — skimming, in a hurry, maybe not an engineer. Fix it if it fails any of these:

1. **Longest sentence.** Find it. If it stacks three or more separate points or runs past
   ~25 words, split it. Repeat until the longest sentence passes.
2. **Jargon.** Flag every acronym or internal term a non-technical client wouldn't know
   (`RRF`, `OpenTelemetry`, `semaphores`). Cut it, or gloss it in plain words. A stack is
   named once, in a phrase.
3. **Outcome first.** Each project leads with what it achieved, not the technology. If the
   first thing about a project is the framework, reorder it.
4. **The five-second test.** Does the value land in the first two lines? If a skimmer would
   not know why to keep reading, rewrite the opening.

This is sentence-level only — it never changes the structure, so it does not disturb the
5a or 5a′ checkpoints above. Keep the concrete details and metrics; just make them land on
the first read.

## Step 6 — Refine

Point the user at `bid.txt` (already saved from Step 5) and iterate on their feedback by
editing that file directly — never hold a newer version only in chat while the file goes
stale. In Mimic mode, keep every revision strictly within the chosen sample's format
**and re-run the Step 5a checkpoint** after any change that could affect length or
sections. In Inspiration mode, keep revisions consistent with the synthesized structure
and hook, **and re-run the Step 5a′ checkpoint** after any change that could affect the
proof device or other structural elements. Keep applying `humanize`, and **re-run the
Step 5b readability checkpoint**, on every revision in either mode — an edit that fixes
one thing often lengthens a sentence or reintroduces jargon. Re-save `bid.txt` after every
revision that passes its checkpoints, so the file on disk is always the current, checked
draft, never a stale one waiting on a final save.

## Step 7 — Finalize

`bid.txt` has already been on disk since Step 5, kept current through every Step 6
revision — this step isn't the first save, it's confirming the version the user just
approved is the version sitting in the file, and closing out `notes.md` to match.

**`bid.txt`** is the complete, self-accounting record of everything ready to send.
**Three sections, `---`-separated, in this order, every time**, whether or not each one
has real content — this is the format Steps 5 and 6 write to the file from the start, not
a shape only applied here at the end:

```
<cover letter>

---

<Upwork project-attachment suggestions>

---

<Q&A block>
```

**Section 1 — Cover letter.** The exact bid text, as **paste-ready plain text**. This is
the only section that gets copied straight into an Upwork form, Google Docs, or an email —
it carries no markdown syntax and nothing a user would have to delete before sending.
Write it plain from the start — do **not** draft markdown and convert it:

- No `#` headings, no `**bold**`, `*italic*`, `` `code` `` or blockquotes. The first line
  of the section is the first line of the bid.
- No job-title heading, no meta about the profile, mode, pricing or evidence.
- **One paragraph per line** — write each paragraph as a single unwrapped line with a blank
  line between paragraphs, so it reflows to any width when pasted rather than carrying hard
  line breaks. Do not hard-wrap at a fixed column.
- URLs are written bare (`https://example.com/work`) so the target form auto-links them.
- The words are exactly the ones approved in Step 6 — saving changes formatting only,
  never wording.

One exception: if the post demands a specific opening line (an anti-bot check such as
"start your application with AI FRONT-END"), that line **is** part of the bid and stays
at the top of Section 1.

**Section 2 — Upwork project-attachment suggestions.** The list worked out in Step 5's
"Suggested attachments" — portfolio-item names from the chosen profile's `## Portfolio
items` that back projects cited in the letter, each with the claim it proves. Write each
one in the **same block shape as a project cited in the cover letter** — name + URL,
short description, then why it fits:

```
<Project name> — <https://project-url, or "no public URL" if it doesn't have one>
<one-line description of the project>
Why it fits: <the specific claim in the letter/Q&A this attachment backs>
```

This section is reference material the user reads before submitting, not text to paste —
a plain descriptive first line (e.g. "Suggested attachments:") is fine here, unlike in
Section 1. If there is nothing to attach, write `None.` — **never omit the section.**

**Before writing this section, check each entry has all three lines** — name + URL,
description, `Why it fits:` — by looking at what you actually wrote, not by intending to
write it that way. A bare `- name — claim` bullet is the old format and fails this check;
if what you're about to write doesn't have three lines per entry, it isn't in the required
shape yet.

**Section 3 — Q&A block.** What goes here depends on Step 2's list-placement choice:

- **User chose the separate Q&A section:** answer the list here —

  ```
  Q: <question 1, verbatim>
  A: <answer>

  Q: <question 2, verbatim>
  A: <answer>
  ```

  - Questions are copied **verbatim** — same wording, same order as the post. Do not
    paraphrase, merge, split, or renumber them.
  - Blank line between every Q/A pair, and the `Q:` / `A:` prefixes on their own lines, so
    each answer can be lifted straight into its own field on the form.
  - Answers use the chosen profile's voice, go through **`humanize`** like the rest, and
    respect any word or character limit the post states.

- **User chose the cover letter:** the list was already answered in Section 1 — this
  section stays present but says so instead of repeating the answers: write `Answered
  inside the cover letter, per your choice — see Section 1.` Do not duplicate the
  answers here.

- **There was no list at all** (only the single organic in-letter question, or no
  questions): write `No screening questions for this job.`

**Never omit the section**, and don't reuse "No screening questions for this job." for
the "answered in the letter instead" case — that phrasing is only accurate when there
genuinely were no questions. The presence of all three sections, each with the *correct*
one-line state when there's nothing to list, is what signals the skill actually
considered attachments and screening questions, not that it skipped them or mislabeled
them.

**Append to `notes.md`** — it already holds `## Job context`, `## Score`, and `## Gaps to
fix in the knowledge base` from `score`'s Step 1 run. Add three more `---`-separated
sections after them, in this order:

```markdown
## Profile and mode
- Which profile you bid as, and which mode (Mimic or Inspiration) you used.
---
## Pricing decision
- The pricing decision and the reason for it.
---
## Evidence used
- Which projects you drew on, and why.
```

Then **merge** any new gaps found in this skill's Step 4 or Step 5a′ into the existing
`## Gaps to fix in the knowledge base` section — don't create a second gaps section.
There is **no** `## Suggested attachments` section in `notes.md` — that list lives only
in `bid.txt`'s Section 2 now, so it isn't duplicated.

This step confirms `bid.txt` (already on disk since Step 5) matches the approved draft and
appends to the existing `notes.md`. `jd.md` is not touched — it was already written
verbatim by `score`.
