import os
from typing import List, Tuple

import gradio as gr
from dotenv import load_dotenv

from utils.model import load_model_and_tokenizer, generate_reply


# Load environment variables if .env exists
load_dotenv(override=True)

MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "128"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
TOP_P = float(os.getenv("TOP_P", "0.9"))

# Lazy globals to hold model/tokenizer after first load
_model = None
_tokenizer = None

def _ensure_model():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        _model, _tokenizer = load_model_and_tokenizer(MODEL_NAME)


def chat_fn(message: str, history: List[Tuple[str, str]]):
    """
    message: latest user message
    history: list of (user, assistant) pairs
    returns: assistant reply string
    """
    _ensure_model()
    reply = generate_reply(
        model=_model,
        tokenizer=_tokenizer,
        message=message,
        history=history,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
    )
    return reply


def build_demo():
    return gr.ChatInterface(
        fn=chat_fn,
        title="Basic Gradio Chatbot (Transformers)",
        description=(
            "A minimal chatbot using Hugging Face Transformers. Default model is "
            f"'{MODEL_NAME}'. You can change it via MODEL_NAME in .env."
        ),
        examples=[
            ["Hello!"],
            ["Write a short haiku about summer."],
            ["Give me 3 creative uses for a paperclip."]
        ],
    )


def main():
    demo = build_demo()
    demo.launch()


if __name__ == "__main__":
    main()

