---
description: Write a bid/proposal from a job description (pasted or a file) using your bid-resources knowledge base
argument-hint: [pasted job description | path to a .md/.txt file]
---

Write a bid for the user by following the **write-bid** skill.

Load and follow the instructions in `skills/write-bid/SKILL.md` exactly — every step
and checkpoint, in order. That skill is the source of truth for how a bid is generated,
and it runs in two parts with a **required pause between them**:

1. **Score first** (Step 1) — runs the `score` skill if this job hasn't been scored yet
   (or reads its existing result), then **stops and asks the user whether to proceed**
   with drafting a bid at all. Do not treat this command as a single uninterrupted
   pipeline that ends in a saved bid — it does not draft anything until the user
   explicitly confirms at this checkpoint.
2. **Draft, if the user confirms** (Steps 2 onward) — pick the profile, choose mimic vs.
   inspiration mode, gap-check, draft in a human voice, refine, and save `bid.txt` plus
   the rest of `notes.md`.

The job description supplied with this command is: $ARGUMENTS

Use it as the job description in Step 1. It may be pasted text, or a path / `@file`
reference to a file holding the post — in that case read the file and use its contents.
A URL is not accepted; ask for a paste or a file instead. If nothing was supplied, ask
the user for the post.
