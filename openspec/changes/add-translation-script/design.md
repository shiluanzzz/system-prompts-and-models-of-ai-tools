# Design: Translation Script

## Context

The repository contains system prompts from various AI tools in English. Users have started manually translating some files to Chinese (suffix `_zh.md`). We need an automated solution to:
1. Scale translations efficiently
2. Maintain consistency across translations
3. Avoid redundant API calls for already translated files

## Goals / Non-Goals

**Goals:**
- Automate English-to-Chinese translation of markdown files
- Use LLM APIs for high-quality translation of technical content
- Support custom API endpoints (for proxy or alternative providers)
- Be idempotent - skip files that already have translations

**Non-Goals:**
- Multi-language support (only Chinese for now)
- Real-time translation service
- Web UI or API server

## Decisions

### Decision 1: Use Poetry for Dependency Management
- **Why**: Modern Python packaging, lockfile support, clean virtual environment management
- **Alternatives**: pip + venv (less reproducible), pipenv (slower)

### Decision 2: Use OpenAI SDK with configurable base URL
- **Why**: Industry standard, supports alternative providers via `OPENAI_API_BASE`
- **Alternatives**: Direct HTTP calls (more code), provider-specific SDKs (less flexible)

### Decision 3: File naming convention `{name}_zh.md`
- **Why**: Follows existing pattern in repository, clear and consistent
- **Alternatives**: `zh/{name}.md` subdirectories (more complex, harder to discover)

### Decision 4: Skip existing translations by default
- **Why**: Avoid unnecessary API costs and preserve manual edits
- **Alternatives**: Always overwrite (wasteful), version comparison (complex)

## Translation Prompt Design

The prompt should:
1. Preserve markdown formatting exactly
2. Keep code blocks, URLs, and technical terms unchanged
3. Translate natural language content to simplified Chinese
4. Maintain the tone and style appropriate for technical documentation

## Risks / Trade-offs

- **Risk**: API rate limits or costs
  - Mitigation: Process files sequentially, add optional delay between requests

- **Risk**: Translation quality varies by model
  - Mitigation: Use well-tested prompt, allow model configuration via env var

## Migration Plan

No migration needed - this is a new tool that doesn't affect existing files unless explicitly run.

## Open Questions

- Should we add a `--force` flag to re-translate existing files?
- Should we support batch processing with progress tracking?
