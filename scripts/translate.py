#!/usr/bin/env python3
"""Translate Hugo blog posts between English and Vietnamese using the Claude API.

Scans content/en/posts and content/vi/posts for missing counterparts and
creates them. Run locally or from GitHub Actions (needs ANTHROPIC_API_KEY).
"""

import sys
from pathlib import Path
import anthropic

client = anthropic.Anthropic()

CONTENT_EN = Path("content/en")
CONTENT_VI = Path("content/vi")

LANG_NAMES = {"en": "English", "vi": "Vietnamese"}


def translate(text: str, source: str, target: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        messages=[{
            "role": "user",
            "content": (
                f"Translate this Hugo blog post from {LANG_NAMES[source]} to {LANG_NAMES[target]}.\n\n"
                "Rules:\n"
                "- Preserve ALL Hugo front matter YAML (between ---) but translate the values of 'title' and 'description'\n"
                "- Preserve ALL markdown formatting exactly (headers, bold, italic, links, code blocks, blockquotes)\n"
                "- Do NOT translate code blocks, technical terms, proper nouns, or brand names\n"
                "- Keep the same writing style and tone\n"
                "- Output ONLY the translated markdown, nothing else\n\n"
                f"{text}"
            ),
        }],
    )
    return response.content[0].text


def sync_translations() -> list[Path]:
    new_files: list[Path] = []

    pairs = [
        (CONTENT_VI, CONTENT_EN, "vi", "en"),
        (CONTENT_EN, CONTENT_VI, "en", "vi"),
    ]

    for src_dir, tgt_dir, src_lang, tgt_lang in pairs:
        src_posts = src_dir / "posts"
        if not src_posts.exists():
            continue

        for src_file in sorted(src_posts.glob("*.md")):
            tgt_file = tgt_dir / "posts" / src_file.name
            if tgt_file.exists():
                continue

            print(f"Translating {src_lang}→{tgt_lang}: {src_file.name}")
            content = src_file.read_text(encoding="utf-8")
            translated = translate(content, src_lang, tgt_lang)
            tgt_file.parent.mkdir(parents=True, exist_ok=True)
            tgt_file.write_text(translated, encoding="utf-8")
            new_files.append(tgt_file)

    return new_files


if __name__ == "__main__":
    files = sync_translations()
    if files:
        print(f"\nTranslated {len(files)} new file(s):")
        for f in files:
            print(f"  {f}")
    else:
        print("Nothing to translate.")
    sys.exit(0)
