# Changelog

All notable changes to this gradio_chatbot workspace will be documented in this file.
This log intentionally avoids sensitive information (no secrets, tokens, or personal data).

## 2025-08-11

### Added
- Created `requirements.txt` with core dependencies for a Gradio + Transformers chatbot:
  - gradio, transformers, accelerate, torch, safetensors, numpy, pydantic, python-dotenv, requests
- Initialized Python virtual environment at `.venv_chatbot` and installed dependencies from `requirements.txt`.
- Scaffolded `basic_chatbot/` demo subproject:
  - `basic_chatbot/app.py`: Gradio ChatInterface wired to a simple generation function.
  - `basic_chatbot/utils/model.py`: Utilities for loading model/tokenizer and generating replies; auto-selects device (MPS/CUDA/CPU).
  - `basic_chatbot/.env.example`: Example configuration for model and generation parameters.
  - `basic_chatbot/README.md`: Usage and setup instructions.
  - `basic_chatbot/run.sh`: Convenience script to run with the workspace virtual environment.

### Changed
- Updated `requirements.txt` to remove `sentencepiece` due to build failure on macOS with Python 3.13 (requires CMake). Left a comment indicating how to install later if needed.

### Notes
- No secrets were created or stored. Any environment variables should be placed in a local `.env` file based on `.env.example` and kept out of version control as appropriate.
- If models requiring SentencePiece are needed (e.g., T5/MT5 or some chat models), install build tools first (e.g., `brew install cmake`) and then `pip install sentencepiece` within `.venv_chatbot`.
- To run the basic chatbot without activating the venv: `../../.venv_chatbot/bin/python basic_chatbot/app.py`.
-
## 2025-08-12

### Added
- Created root-level `.gitignore` with comprehensive ignores for Python projects on macOS, including:
  - macOS files (e.g., `.DS_Store`)
  - Python bytecode and caches (e.g., `__pycache__`, `*.pyc`)
  - Virtual environments (e.g., `.venv/`, `venv/`, `env/`, including nested variants like `*/.venv/`)
  - Build/packaging artifacts (e.g., `build/`, `dist/`, `*.egg-info`)
  - Test/coverage directories (e.g., `.tox/`, `.pytest_cache/`, coverage files)
  - Type checker caches (e.g., `.mypy_cache/`, `.pytype/`, `.pyre/`, `.ruff_cache/`)
  - Jupyter checkpoints, IDE settings, logs, and temp files
  - Gradio cached examples (`gradio_cached_examples/`)
  - Node-related directories (`node_modules/`, `*.tsbuildinfo`)

### Notes
- A `.gitignore` also exists at `gradio_chatbot/educative_chatbot/.gitignore` from an earlier step.
- Updated the root `.gitignore` to allow tracking `CHANGELOG.md` while still ignoring `changelog.md` lowercase variant.

### Changed
- Adjusted `.gitignore` rule order so `!CHANGELOG.md` takes effect on case-insensitive filesystems (e.g., macOS), ensuring the changelog is tracked.

### Added (recent)
- gradio_chatbot/educative_chatbot/basic_input_bot.py
- gradio_chatbot/educative_chatbot/pattern-matching_bot.py
- gradio_chatbot/educative_chatbot/rule_based_bot.py
- gradio_chatbot/educative_chatbot/streaming_chatbot.py

### Removed
- gradio_chatbot/educative_chatbot/main.py (superseded by individual bot entry points)
