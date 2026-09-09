---
description: Write a bid/proposal from a job description (pasted or a file) using your bid-resources knowledge base
argument-hint: [pasted job description | path to a .md/.txt file]
---

Write a bid for the user by following the **write-bid** skill.

Load and follow the instructions in `skills/write-bid/SKILL.md` exactly — every step
and checkpoint, in order. That skill is the source of truth for how a bid is
generated (verify the knowledge base, pick the profile, choose mimic vs. inspiration
mode, analyze the job, match projects, gap-check, draft in a human voice, refine, and
save).

The job description supplied with this command is: $ARGUMENTS

Use it as the job description in Step 2. It may be pasted text, or a path / `@file`
reference to a file holding the post — in that case read the file and use its contents.
A URL is not accepted; ask for a paste or a file instead. If nothing was supplied, ask
the user for the post.
