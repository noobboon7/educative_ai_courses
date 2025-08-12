import os
from typing import List, Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)


def get_device() -> torch.device:
    # Prefer MPS on Apple Silicon if available, then CUDA, else CPU
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_model_and_tokenizer(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    device = get_device()
    model = model.to(device)
    model.eval()
    return model, tokenizer


def format_history(history: List[Tuple[str, str]], user: str) -> str:
    # Very simple chat prompt builder for casual LM; not chat-tuned.
    # For chat-tuned models, switch to their specific chat templates.
    lines: List[str] = []
    for u, a in history:
        if u:
            lines.append(f"User: {u}")
        if a:
            lines.append(f"Assistant: {a}")
    lines.append(f"User: {user}")
    lines.append("Assistant:")
    return "\n".join(lines)


def generate_reply(
    model,
    tokenizer,
    message: str,
    history: List[Tuple[str, str]],
    max_new_tokens: int = 128,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    device = next(model.parameters()).device

    prompt = format_history(history, message)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    full_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Extract only the assistant's latest turn: split on 'Assistant:' and take last piece
    if "Assistant:" in full_text:
        reply = full_text.split("Assistant:")[-1].strip()
    else:
        # Fallback: remove the prompt from the front if possible
        if full_text.startswith(prompt):
            reply = full_text[len(prompt):].strip()
        else:
            reply = full_text.strip()
    # Be nice and limit runaway outputs
    reply = reply[:2000]
    return reply

