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

## 2025-08-14

### Changed
- gradio_chatbot/requirements.txt: add Rasa entries gated to `python_version < "3.12"` to avoid installation on Python 3.12+.

### Added
- gradio_chatbot/requirements-rasa.txt: optional Rasa 3.x requirements for demos (pins rasa and rasa-sdk to >=3.6,<4.0).
- Scaffolded `gradio_chatbot/Rasa_demo/` Rasa 3.x project for a simple assistant, including:
  - `actions/actions.py`
  - `config.yml`, `domain.yml`, `endpoints.yml`, `credentials.yml`
  - `data/nlu.yml`, `data/rules.yml`, `data/stories.yml`
  - `tests/test_stories.yml`
  - `main.py` entry point

### Operations
- Installed uv via Homebrew (upgraded to uv 0.8.10).
- Created Python 3.10 virtual environment at `gradio_chatbot/.venv_rasa` using uv and installed Rasa and Rasa SDK successfully from `requirements-rasa.txt`.

### Housekeeping
- Updated `.gitignore` to exclude Rasa cache and model artifacts:
  - `gradio_chatbot/Rasa_demo/.rasa/`
  - `gradio_chatbot/Rasa_demo/models/`
  - `gradio_chatbot/Rasa_demo/*.tar.gz`
  - `gradio_chatbot/Rasa_demo/story_graph.dot`

### Notes
- Rasa 3.x is not available for Python 3.12+; keep `.venv_chatbot` on Python 3.13 for Gradio/Transformers and use `.venv_rasa` (3.10) for Rasa demos.
- The Rasa demo includes generated cache/model files locally; they are ignored from version control to keep the repo lean.

## 2025-08-15

### Added

- added ollama to gradio app demo
