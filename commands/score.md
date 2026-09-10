---
description: Score how well your knowledge base backs a job description (pasted or a file) before deciding whether to write a bid
argument-hint: [pasted job description | path to a .md/.txt file]
---

Score the given job description against the user's knowledge base by following the
**score** skill.

Load and follow the instructions in `skills/score/SKILL.md` exactly, step by step. That
skill is the source of truth for how a job gets scored (verify the knowledge base, read
the job description, detect embedded traps, save the record, find supporting evidence,
compute a 0-10 confidence score, write the gaps, report back).

The job description supplied with this command is: $ARGUMENTS

Use it as the job description in Step 2. It may be pasted text, or a path / `@file`
reference to a file holding the post — in that case read the file and use its contents.
A URL is not accepted; ask for a paste or a file instead. If nothing was supplied, ask
the user for the post.

This command only scores the job — it does not draft a bid. To write a bid, run
`/ai-bid-gen:write-bid`, which calls this skill automatically if the job hasn't been
scored yet.
