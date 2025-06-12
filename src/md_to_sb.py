#!/usr/bin/env python3
"""
Convert Obsidian-style Markdown in the macOS clipboard to Scrapbox markup and copy the result back to the clipboard.

Usage:
    1. Copy Markdown text (Cmd-C)
    2. python3 md_to_sb.py
    3. Paste (Cmd-V) into Scrapbox
"""
import re
import subprocess
import sys


def md_inline_to_sb(text: str) -> str:
    """Convert Markdown inline elements to Scrapbox."""

    # Math: $formula$ → [$ formula ]
    text = re.sub(r"\$(.+?)\$", lambda m: f"[$ {m.group(1)} ]", text)

    # External link: [label](url) → [url label]
    def link_repl(match: re.Match) -> str:
        label, url = match.group(1), match.group(2)
        return f"[{url} {label}]"

    text = re.sub(r"\[([^\]]+?)\]\((https?://[^)]+?)\)", link_repl, text)

    # Internal link: [[Page]] → [Page]
    text = re.sub(r"\[\[([^\]]+?)\]\]", lambda m: f"[{m.group(1)}]", text)

    # Bold: **text** → [* text]
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"[* {m.group(1)}]", text)

    # Italic: *text* (but not **bold**) → [/ text]
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
                  lambda m: f"[/ {m.group(1)}]", text)

    # Strikethrough: ~~text~~ → [- text]
    text = re.sub(r"~~(.+?)~~", lambda m: f"[- {m.group(1)}]", text)

    return text


def convert_md_to_sb(text: str) -> str:
    """Convert full Markdown document to Scrapbox."""
    lines = text.splitlines()
    out = []
    in_code = False

    for line in lines:
        # Inside a code block
        if in_code:
            if line.strip().startswith("```"):
                out.append("")  # blank line ends Scrapbox code block
                in_code = False
                continue
            out.append(line)
            continue

        stripped = line.lstrip()

        # Code block start
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            out.append(f"code:{lang}" if lang else "code:")
            in_code = True
            continue

        # Block quote
        if stripped.startswith(">"):
            out.append("> " + md_inline_to_sb(stripped[1:].lstrip()))
            continue

        # Heading
        hmatch = re.match(r"(#{1,6})\s+(.+)", stripped)
        if hmatch:
            level = len(hmatch.group(1))
            heading_text = md_inline_to_sb(hmatch.group(2))
            stars_map = {1: "****", 2: "***", 3: "**", 4: "*", 5: "*", 6: "*"}
            stars = stars_map.get(level, "*")
            out.append(f"[{stars} {heading_text}]")
            continue

        # List item
        lmatch = re.match(r"(\s*)-\s+(.*)", line)
        if lmatch:
            indent = lmatch.group(1)
            item_text = md_inline_to_sb(lmatch.group(2))
            out.append(f"{indent}{item_text}")
            continue

        # Regular line
        out.append(md_inline_to_sb(line))

    return "\n".join(out)


def main() -> None:
    original = subprocess.run(
        ["pbpaste"], capture_output=True, text=True).stdout
    if not original:
        print("📋 クリップボードが空です。まず Markdown をコピーしてね。", file=sys.stderr)
        sys.exit(1)

    converted = convert_md_to_sb(original)
    subprocess.run(["pbcopy"], input=converted, text=True)
    print("✅ Markdown → Scrapbox 完了！結果をクリップボードに入れたよ。")


if __name__ == "__main__":
    main()
