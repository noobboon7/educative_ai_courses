Basic Gradio Chatbot

This is a minimal Gradio chatbot scaffold using Hugging Face Transformers. It defaults to the small model `distilgpt2` for fast CPU demos.

Structure
- app.py: Gradio app entrypoint
- utils/model.py: Model loading and response generation helpers
- .env.example: Example environment variables
- run.sh: Helper script to run with the repository's virtual environment

Requirements
- Python 3.10+
- The parent project already has a virtual environment `.venv_chatbot` with required dependencies installed.

Setup
1) Optionally create a .env based on example:
   cp .env.example .env
   # edit values as desired

2) Run the app (without activating venv):
   ../../.venv_chatbot/bin/python app.py

   Or, if you've activated the venv:
   python app.py

Environment Variables (.env)
- MODEL_NAME: HF model to use (default: distilgpt2). Choose a small, causal LM for CPU.
- MAX_NEW_TOKENS: Max tokens to generate (default: 128)
- TEMPERATURE: Sampling temperature (default: 0.7)
- TOP_P: Nucleus sampling p (default: 0.9)

Notes
- distilgpt2 is not chat-tuned, but works for basic generation. Swap MODEL_NAME to a chat-tuned model if desired (e.g., TinyLlama/TinyLlama-1.1B-Chat-v1.0). Some chat models may require extra dependencies (like sentencepiece) or significant RAM/VRAM.
- On Apple Silicon, PyTorch will prefer MPS if available.

