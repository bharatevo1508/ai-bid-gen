---
description: Convert a markdown file to paste-ready plain text, saved as .txt beside it
argument-hint: <path to the .md file>
---

Convert a markdown file to plain text by following the **md-to-txt** skill.

Load and follow `skills/md-to-txt/SKILL.md`. Run the script it points at rather than
converting the file by hand — it verifies that no word changed and refuses to write if
one did.

The path of the file to convert is: $ARGUMENTS

If that is empty, ask the user which file to convert. Do not guess a file, and do not
convert a whole folder — one file per run.

The output goes **next to the source**: same directory, same basename, `.txt` extension
(`bids/001/bid.md` → `bids/001/bid.txt`). Never modify the source markdown.

When it's done, tell the user where the `.txt` was written and mention the paste tips
from the skill's *Reporting back* section.
