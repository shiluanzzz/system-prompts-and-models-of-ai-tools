## ADDED Requirements

### Requirement: Translation Script Core Functionality
The system SHALL provide a Python script that translates markdown files from English to Simplified Chinese using LLM APIs.

#### Scenario: Translate single markdown file
- **WHEN** the script is run with a valid markdown file path
- **THEN** it SHALL create a translated file with `_zh.md` suffix in the same directory

#### Scenario: Skip existing translation
- **WHEN** the script encounters a file that already has a corresponding `_zh.md` translation
- **THEN** it SHALL skip translation and log that the file was skipped

#### Scenario: Preserve markdown formatting
- **WHEN** translating a file containing code blocks, URLs, and markdown syntax
- **THEN** the translated file SHALL preserve all formatting, code blocks, and URLs unchanged

### Requirement: Environment Variable Configuration
The system SHALL use environment variables for API configuration.

#### Scenario: Use custom API base URL
- **WHEN** `OPENAI_API_BASE` environment variable is set
- **THEN** the script SHALL use this URL as the API endpoint

#### Scenario: Use API key from environment
- **WHEN** `OPENAI_API_KEY` environment variable is set
- **THEN** the script SHALL authenticate using this key

#### Scenario: Missing API key error
- **WHEN** `OPENAI_API_KEY` is not set
- **THEN** the script SHALL exit with a clear error message

### Requirement: Poetry Dependency Management
The system SHALL use Poetry for Python dependency management.

#### Scenario: Install dependencies
- **WHEN** user runs `poetry install` in the project directory
- **THEN** all required dependencies SHALL be installed in a virtual environment

#### Scenario: Run script via Poetry
- **WHEN** user runs `poetry run python translate.py`
- **THEN** the script SHALL execute with the correct dependencies
