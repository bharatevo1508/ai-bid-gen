---
name: md-to-txt
description: Convert a markdown file to paste-ready plain text saved alongside it as .txt — markdown syntax stripped, paragraphs unwrapped so Google Docs and web forms reflow them, blank lines between list items, URLs left bare so they auto-link. Use when the user wants a bid, document, or any .md made copy-pasteable, or asks for a .txt version of a markdown file.
---

# Markdown to plain text

Produce a `.txt` next to a `.md` that pastes cleanly into Google Docs, a Word document,
an Upwork form, or an email. **The words never change.** Only the formatting does.

## Why it exists

Pasting markdown into a rich-text editor carries the syntax through as literal
characters: `**bold**` stays starred, `#` sits at the top of the page, `- ` bullets stay
dashes. Worse, a file hard-wrapped at 90 columns pastes with those line breaks made
permanent, so the text will not reflow to the page width and looks broken on any other
column width.

## Run it

```
python3 scripts/md_to_txt.py <file.md>
```

Writes `<file>.txt` beside the source and prints the word count it verified. The script
lives at `scripts/md_to_txt.py` inside this skill directory.

Options:

- `-o PATH` — write somewhere other than the default sibling `.txt`.
- `--stdout` — print instead of writing. Use this to preview before committing to a file.
- `--unwrap` / `--no-unwrap` — override paragraph unwrapping. Auto-detection needs at
  least three lines bunched near the file's widest line to conclude the file is
  hard-wrapped, so a short document with a single wrapped paragraph may need `--unwrap`.
- `--force` — write even when verification fails. Do not use this without telling the
  user exactly which words changed.

## What it does to the text

- Strips `#` headings, `**bold**`, `*italic*`, `` `code` ``, and blockquote `>` markers.
- `[text](url)` becomes `text (url)`, so the address survives the paste. A link whose
  text is already the URL collapses to the bare URL.
- `- `, `* `, `+ ` bullets become `• `, with a blank line between items so editors do not
  collapse them together. Numbered lists keep their numbers.
- Horizontal rules are dropped.
- Paragraphs hard-wrapped at a fixed column are joined back into one line each.
- Fenced code blocks and tables are passed through verbatim, keeping their spacing.
- URLs are left bare so the target application auto-links them.

## The verification step

Before writing, the script compares the word sequence of the output against the word
sequence of the source, ignoring list markers and whitespace. If a single word was
dropped, added, or reordered it **refuses to write** and reports where the drift began.

This matters because the failure mode here is silent. A conversion that quietly loses a
sentence looks fine until the client reads it. Never bypass the check with `--force` to
make an error go away — fix the input or report the problem.

## Reporting back

Tell the user the formatting changes you made and anything they should expect on paste.
Two worth mentioning:

- Docs auto-links bare URLs and may keep the source font. Paste-without-formatting
  (Ctrl+Shift+V) gives clean body text.
- A document that starts lines with `1.` will trigger the editor's auto-numbering, which
  then fights the later items. Ctrl+Z immediately after the paste undoes just that
  autoformat.

## Scope

Formatting only. This skill never rewrites, shortens, improves, or re-orders the text —
if the wording should change, that is a separate edit to the markdown source, made first
and then converted, never the other way round.

It works on **any** markdown file, not just bids. It is invoked on demand, by the user,
through `/ai-bid-gen:md-to-txt <path>` — no other skill produces a `.txt` as a side
effect, and `write-bid` in particular never calls it while saving a bid.

**Where the output goes.** Same directory as the source, same basename, `.txt` extension:
`bids/001/bid.md` becomes `bids/001/bid.txt`. Do not write it anywhere else and do not
rename it (`-o` exists for the rare case where the user names a different path
themselves). The source `.md` is never modified.
