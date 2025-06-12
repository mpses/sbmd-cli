#!/usr/bin/env python3
"""
Convert Scrapbox (Cosense) markup in the macOS clipboard to Obsidian‑friendly Markdown and copy result back to clipboard.

Usage:
    1. Copy Scrapbox text (Cmd‑C)
    2. python3 sb_to_md.py
    3. Paste (Cmd‑V) wherever you want.
"""

import re
import subprocess
import sys


def convert_inline(text: str) -> str:
    """Convert inline-level Scrapbox markup to Markdown."""

    # Math: [$ formula ] → $formula$
    text = re.sub(r"\[\$ ([^\]]+?) \]", lambda m: f"${m.group(1)}$", text)

    # Bold: [[text]] or [* text]
    text = re.sub(r"\[\* ([^\]]+?)\]", lambda m: f"**{m.group(1)}**", text)
    text = re.sub(r"\[\[\s*([^\]\n]+?)\s*\]\]",
                  lambda m: f"**{m.group(1)}**", text)

    # Italic: [/ text]
    text = re.sub(r"\[/ ([^\]]+?)\]", lambda m: f"*{m.group(1)}*", text)

    # Strikethrough: [- text]
    text = re.sub(r"\[- ([^\]]+?)\]", lambda m: f"~~{m.group(1)}~~", text)

    # External labelled links: [url label] or [label url]
    def link_repl(match: re.Match) -> str:
        a, b = match.group(1), match.group(2)
        if re.match(r"https?://", a):
            return f"[{b}]({a})"
        if re.match(r"https?://", b):
            return f"[{a}]({b})"
        # Fallback: treat as internal link with space in title
        return f"[[{a} {b}]]"

    text = re.sub(r"\[([^\]\s]+?) ([^\]]+?)\]", link_repl, text)

    # Internal links: [Page] → [[Page]]
    text = re.sub(r"\[([^\]]+?)\]", lambda m: f"[[{m.group(1)}]]", text)

    return text


def convert(text: str) -> str:
    """Full‑document conversion."""
    lines = text.splitlines()
    out: list[str] = []
    in_code = False

    for line in lines:
        # Handle code block body
        if in_code:
            if line.strip() == "":
                out.append("```")
                in_code = False
                continue
            out.append(line)
            continue

        stripped = line.lstrip()

        # Start of code block: code:filename.ext
        if stripped.startswith("code:"):
            filename = stripped[5:].strip()
            lang = filename.split(".")[-1] if "." in filename else ""
            out.append(f"```{lang}")
            in_code = True
            continue

        # Block quote lines
        if stripped.startswith(">"):
            out.append("> " + convert_inline(stripped[1:].lstrip()))
            continue

        # Headings like [*** Heading]
        hmatch = re.match(r"\[(\*{1,6})\s+(.+?)\]", stripped)
        if hmatch:
            star_count = len(hmatch.group(1))
            # Mapping: **** → h1, *** → h2, ** → h3, * → h4
            level = max(1, min(6, 5 - star_count))
            out.append("#" * level + " " + convert_inline(hmatch.group(2)))
            continue

        # Bullet list (Scrapbox treats every non‑blank line as bullet)
        indent_size = len(line) - len(stripped)
        depth = indent_size // 2  # 2‑space indent per level
        prefix = "  " * depth + "- "
        out.append(prefix + convert_inline(stripped))

    if in_code:
        # Close un‑terminated code fence
        out.append("```")

    return "\n".join(out)


def main() -> None:
    original = subprocess.run(
        ["pbpaste"], capture_output=True, text=True).stdout
    if not original:
        print("📋 クリップボードが空です。まず Scrapbox のテキストをコピーしてね。", file=sys.stderr)
        sys.exit(1)

    converted = convert(original)
    subprocess.run(["pbcopy"], input=converted, text=True)
    print("✅ Scrapbox → Markdown 完了！結果をクリップボードに入れたよ。")


if __name__ == "__main__":
    main()
