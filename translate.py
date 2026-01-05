#!/usr/bin/env python3
"""
Translation script for AI system prompts.
Translates text files from English to Simplified Chinese using OpenAI API.
Supports .md, .txt, and other text file formats.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file if present
load_dotenv()

# Default file extensions to translate
DEFAULT_EXTENSIONS = {".md", ".txt"}

# Translation prompt optimized for technical documentation and system prompts
TRANSLATION_PROMPT = """You are a professional translator. Your ONLY task is to translate the provided document from English to Simplified Chinese.

CRITICAL RULES:
1. This is a TRANSLATION task - translate the ENTIRE document word by word
2. DO NOT generate new content, code examples, or explanations
3. DO NOT summarize or truncate the document
4. DO NOT add any commentary or notes
5. Output ONLY the complete translated document

## Formatting Rules:
- Preserve ALL markdown/text formatting exactly (headers, code blocks, lists, etc.)
- Keep code snippets, URLs, file paths, and technical terms in English
- Keep placeholder variables like {variable} or {{placeholder}} unchanged
- Maintain original line breaks and structure

## Translation Style:
- Use natural, fluent Simplified Chinese
- Maintain the original tone and style
- This is an AI system prompt document - translate accurately

Now translate the following document completely:"""


def get_openai_client() -> OpenAI:
    """Initialize OpenAI client with environment variables."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    base_url = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")

    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def get_translation_output_path(input_path: Path) -> Path:
    """Generate the output path for translated file."""
    stem = input_path.stem
    # Remove existing _zh suffix if present to avoid double suffix
    if stem.endswith("_zh"):
        stem = stem[:-3]
    return input_path.parent / f"{stem}_zh{input_path.suffix}"


def translation_exists(input_path: Path) -> bool:
    """Check if translation already exists for the given file."""
    output_path = get_translation_output_path(input_path)
    return output_path.exists()


def translate_content(client: OpenAI, content: str, model: str = "gpt-4o") -> str:
    """Translate content using OpenAI API."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": TRANSLATION_PROMPT},
            {"role": "user", "content": content}
        ],
        temperature=0.3,  # Lower temperature for more consistent translations
    )
    return response.choices[0].message.content


def translate_file(client: OpenAI, input_path: Path, force: bool = False, model: str = "gpt-4o", base_path: Path = None) -> bool:
    """
    Translate a single file.

    Returns True if translation was performed, False if skipped.
    """
    output_path = get_translation_output_path(input_path)

    # Calculate display path
    if base_path and input_path.is_relative_to(base_path):
        display_path = input_path.relative_to(base_path)
        output_display = output_path.relative_to(base_path)
    else:
        display_path = input_path
        output_display = output_path

    # Skip if translation exists and force is not set
    if output_path.exists() and not force:
        print(f"  Skipped (translation exists): {output_display}")
        return False

    # Read source file
    content = input_path.read_text(encoding="utf-8")

    if not content.strip():
        print(f"  Skipped (empty file): {display_path}")
        return False

    # Translate
    print(f"  Translating: {display_path} -> {output_display}")
    translated = translate_content(client, content, model)

    # Write translated content
    output_path.write_text(translated, encoding="utf-8")
    print(f"  Done: {output_display}")
    return True


def find_translatable_files(directory: Path, recursive: bool = True, extensions: set = None) -> list[Path]:
    """
    Find all text files that need translation.
    Excludes files that already end with _zh suffix.
    """
    if extensions is None:
        extensions = DEFAULT_EXTENSIONS

    # Filter out _zh files, hidden directories, and special directories
    excluded_dirs = {".git", ".github", "node_modules", "__pycache__", ".venv", "venv", "openspec", ".claude", ".cccc"}

    files_to_translate = []

    for ext in extensions:
        pattern = f"**/*{ext}" if recursive else f"*{ext}"
        all_files = list(directory.glob(pattern))

        for f in all_files:
            # Skip _zh files
            if f.stem.endswith("_zh"):
                continue
            # Skip files in excluded directories
            if any(part in excluded_dirs for part in f.parts):
                continue
            # Skip hidden files/directories
            if any(part.startswith(".") for part in f.parts if part != "."):
                continue
            files_to_translate.append(f)

    return sorted(set(files_to_translate))


def main():
    parser = argparse.ArgumentParser(
        description="Translate text files from English to Simplified Chinese"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or directory to translate (default: current directory)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force re-translation even if translation exists"
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't search subdirectories"
    )
    parser.add_argument(
        "-m", "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o"),
        help="Model to use for translation (default: gpt-4o or OPENAI_MODEL env var)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show files that would be translated without actually translating"
    )
    parser.add_argument(
        "-e", "--ext",
        action="append",
        dest="extensions",
        help="File extensions to translate (can be specified multiple times, default: .md .txt)"
    )

    args = parser.parse_args()

    path = Path(args.path).resolve()

    # Determine extensions to use
    if args.extensions:
        extensions = {ext if ext.startswith(".") else f".{ext}" for ext in args.extensions}
    else:
        extensions = DEFAULT_EXTENSIONS

    # Initialize OpenAI client
    if not args.dry_run:
        client = get_openai_client()
    else:
        client = None

    # Determine files to translate
    if path.is_file():
        if path.suffix not in extensions:
            print(f"Error: {path} has extension {path.suffix}, expected one of {extensions}")
            sys.exit(1)
        files = [path]
    elif path.is_dir():
        files = find_translatable_files(path, recursive=not args.no_recursive, extensions=extensions)
    else:
        print(f"Error: {path} does not exist")
        sys.exit(1)

    if not files:
        print("No files found to translate.")
        return

    print(f"Found {len(files)} file(s) to process")
    print(f"Extensions: {', '.join(sorted(extensions))}")
    print(f"Model: {args.model}")
    print("-" * 50)

    if args.dry_run:
        print("DRY RUN - No translations will be performed")
        print("-" * 50)
        for f in files:
            output = get_translation_output_path(f)
            status = "exists" if output.exists() else "needs translation"
            rel_path = f.relative_to(path) if path.is_dir() else f.name
            print(f"  [{status}] {rel_path}")
        return

    # Translate files
    translated_count = 0
    skipped_count = 0
    error_count = 0

    for f in files:
        try:
            if translate_file(client, f, force=args.force, model=args.model, base_path=path if path.is_dir() else None):
                translated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            rel_path = f.relative_to(path) if path.is_dir() else f.name
            print(f"  Error translating {rel_path}: {e}")
            error_count += 1

    print("-" * 50)
    print(f"Summary: {translated_count} translated, {skipped_count} skipped, {error_count} errors")


if __name__ == "__main__":
    main()
