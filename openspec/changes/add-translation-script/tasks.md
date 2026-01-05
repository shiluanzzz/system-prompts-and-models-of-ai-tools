# Implementation Tasks

## 1. Project Setup
- [x] 1.1 Initialize Poetry project with `pyproject.toml`
- [x] 1.2 Add dependencies: `openai`, `python-dotenv`

## 2. Core Implementation
- [x] 2.1 Create `translate.py` with main translation logic
- [x] 2.2 Implement file discovery (find all `.md` and `.txt` files excluding `*_zh.*`)
- [x] 2.3 Implement skip logic for existing translations
- [x] 2.4 Implement OpenAI API integration with env var configuration
- [x] 2.5 Add translation prompt optimized for system prompts

## 3. Testing & Validation
- [x] 3.1 Install dependencies with Poetry
- [x] 3.2 Run script on test file to verify translation quality
- [x] 3.3 Verify skip logic works for existing translations
- [x] 3.4 Test error handling for missing API keys
