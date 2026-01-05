# Change: Add Translation Script for System Prompts

## Why

This repository contains AI tool system prompts in English. To make these prompts accessible to Chinese-speaking users, we need an automated translation tool. Manual translation is time-consuming and inconsistent. An automated script using LLM APIs will ensure consistent, high-quality translations while avoiding redundant work.

## What Changes

- Add a new Python translation script using Poetry for dependency management
- Integrate with OpenAI SDK for LLM-based translation
- Implement smart skip logic to avoid re-translating existing files (`*_zh.md` files)
- Support environment variable configuration (`OPENAI_API_BASE`, `OPENAI_API_KEY`)
- Use a specialized prompt optimized for translating technical documentation and system prompts

## Impact

- Affected specs: `specs/translation-tool/` (new capability)
- Affected code: New files in project root
  - `pyproject.toml` - Poetry configuration
  - `translate.py` - Main translation script
- No breaking changes to existing functionality
