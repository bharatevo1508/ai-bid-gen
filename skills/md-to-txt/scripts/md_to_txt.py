#!/usr/bin/env python3
"""Convert a markdown file to paste-ready plain text alongside it.

Strips markdown syntax, unwraps hard-wrapped paragraphs so the target application
reflows them, and puts a blank line between list items. Verifies that the word
sequence is unchanged before writing.

    python3 md_to_txt.py path/to/file.md [-o OUT] [--stdout] [--force]
"""

import argparse
import re
import sys
from pathlib import Path

FENCE = re.compile(r'^\s*(```|~~~)')
BULLET = re.compile(r'^(\s*)([-*+])\s+(.*)$')
ORDERED = re.compile(r'^(\s*)(\d+[.)])\s+(.*)$')
ATX = re.compile(r'^\s{0,3}#{1,6}\s+')
HRULE = re.compile(r'^\s{0,3}([-*_])(\s*\1){2,}\s*$')
QUOTE = re.compile(r'^\s{0,3}>\s?')
LINK = re.compile(r'\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def strip_inline(text):
    """Remove inline markdown syntax, keeping the words themselves."""
    text = IMAGE.sub(r'\1', text)
    text = LINK.sub(lambda m: m.group(2) if m.group(1) in ('', m.group(2))
                    else f'{m.group(1)} ({m.group(2)})', text)
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*|__([^_]+)__', lambda m: m.group(1) or m.group(2), text)
    text = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'\1', text)
    text = re.sub(r'(?<![\w_])_([^_\n]+)_(?![\w_])', r'\1', text)
    return text


def wrap_threshold(lines):
    """Length below which a line break was deliberate rather than caused by wrapping.

    A hard-wrapped file has many lines bunched just under its wrap column. A file
    with one paragraph per line does not, and must never be re-joined.
    """
    widths = [len(l) for l in lines if l.strip() and not l.lstrip().startswith('|')]
    if not widths:
        return None
    longest = max(widths)
    near_max = sum(1 for w in widths if w >= longest - 10)
    return longest - 25 if near_max >= 3 and longest >= 50 else None


def convert(src, unwrap=None):
    lines = src.rstrip('\n').split('\n')
    thresh = wrap_threshold(lines) if unwrap is None else (
        max((len(l) for l in lines), default=0) - 25 if unwrap else None)

    blocks, current, in_fence = [], [], False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue                      # drop the fence markers, keep the code
        if not line.strip() and not in_fence:
            blocks.append((current, False))
            current = []
        else:
            current.append((line, in_fence))
    blocks.append((current, False))

    out = []
    for block, _ in blocks:
        if not block:
            continue
        if any(fenced for _, fenced in block):
            out.append('\n'.join(l for l, _ in block))   # code stays verbatim
            continue
        if all(l.lstrip().startswith('|') for l, _ in block):
            out.append('\n'.join(l for l, _ in block))   # tables stay verbatim
            continue

        # classify each line, undoing hard wraps as we go
        parsed = []
        for raw, _ in block:
            if HRULE.match(raw):
                continue
            text = strip_inline(QUOTE.sub('', ATX.sub('', raw))).strip()
            if not text:
                continue
            bullet = BULLET.match(raw.strip())
            ordered = ORDERED.match(raw.strip())
            if bullet:
                kind, text = 'item', '• ' + strip_inline(bullet.group(3)).strip()
            elif ordered:
                kind = 'item'
            else:
                kind = 'text'
            if (parsed and kind == 'text' and thresh is not None
                    and len(parsed[-1][2]) >= thresh):
                parsed[-1] = (parsed[-1][0], parsed[-1][1], parsed[-1][2] + ' ' + text)
            else:
                parsed.append((kind, len(raw) - len(raw.lstrip()), text))

        # a blank line separates list items; every other break stays attached
        pieces = []
        for kind, _indent, text in parsed:
            if kind == 'item' or not pieces:
                pieces.append([text])
            else:
                pieces[-1].append(text)
        if pieces:
            out.append('\n\n'.join('\n'.join(p) for p in pieces))

    return '\n\n'.join(out) + '\n'


MARKERS = {'-', '*', '+', '•', '|', '>'}


def words(text):
    """Word sequence, ignoring list markers, table pipes and all whitespace."""
    return [w for w in re.split(r'\s+', text) if w and w not in MARKERS]


def source_words(src):
    """The same word sequence, read off the markdown with its syntax removed.

    This is the baseline the conversion is checked against, so it strips exactly
    the syntax the converter strips, and nothing more.
    """
    kept, in_fence = [], False
    for raw in src.split('\n'):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            kept.append(raw)
            continue
        if HRULE.match(raw):
            continue
        line = QUOTE.sub('', ATX.sub('', raw))
        item = BULLET.match(line.strip())
        if item:
            line = item.group(3)
        kept.append(strip_inline(line))
    return words('\n'.join(kept))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', type=Path)
    ap.add_argument('-o', '--out', type=Path, help='default: source with a .txt suffix')
    ap.add_argument('--stdout', action='store_true', help='print instead of writing')
    ap.add_argument('--force', action='store_true', help='write even if verification fails')
    ap.add_argument('--unwrap', dest='unwrap', action='store_true', default=None,
                    help='force paragraph unwrapping (auto-detected by default)')
    ap.add_argument('--no-unwrap', dest='unwrap', action='store_false',
                    help='never join lines; keep every line break as written')
    args = ap.parse_args()

    if not args.source.is_file():
        sys.exit(f'no such file: {args.source}')

    src = args.source.read_text(encoding='utf-8')
    result = convert(src, args.unwrap)

    expected = source_words(src)
    actual = words(result)
    ok = expected == actual
    if not ok:
        drift = next((i for i, (a, b) in enumerate(zip(expected, actual)) if a != b),
                     min(len(expected), len(actual)))
        note = (f'word sequence changed near word {drift + 1}: '
                f'{expected[drift:drift + 6]} -> {actual[drift:drift + 6]}')
        if not args.force:
            sys.exit(f'refusing to write, {note}\nre-run with --force to write anyway')
        print(f'WARNING: {note}', file=sys.stderr)

    if args.stdout:
        sys.stdout.write(result)
    else:
        dest = args.out or args.source.with_suffix('.txt')
        dest.write_text(result, encoding='utf-8')
        print(f'wrote {dest} ({len(actual)} words, verified unchanged)' if ok
              else f'wrote {dest} (UNVERIFIED)')


if __name__ == '__main__':
    main()
