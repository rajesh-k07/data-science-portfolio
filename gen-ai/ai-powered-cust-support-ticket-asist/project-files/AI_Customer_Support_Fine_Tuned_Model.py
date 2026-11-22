"""
Model logic for the AI-Powered Customer Support Ticket Assistant.
Loads the fine-tuned Qwen3-1.7B model, generates the JSON output for a ticket,
and checks the output. Same settings as in the test set evaluation.
"""

import json
import os
import re
import time

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Folder of this file, so paths work from any starting folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "qwen3-ticket-finetuned")
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "project_data", "system_prompt.txt")

# Model information shown in the app
MODEL_VERSION = "v1.0"
FINE_TUNED_DATE = "Nov 1, 2026"

# Same generation settings as in test set evaluation
MAX_NEW_TOKENS = 512

# Allowed label values from dataset
ALLOWED_TYPES = ["Change", "Incident", "Problem", "Request"]
ALLOWED_QUEUES = [
    "Billing and Payments", "Customer Service", "General Inquiry", "Human Resources",
    "IT Support", "Product Support", "Returns and Exchanges", "Sales and Pre-Sales",
    "Service Outages and Maintenance", "Technical Support",
]
ALLOWED_PRIORITIES = ["low", "medium", "high"]

# Apple GPU (MPS) on the Mac, NVIDIA GPU (CUDA) on other computers, else CPU
if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"


def load_system_prompt():
    """
    Read the system prompt (Prompt Experiment 6) that was used for fine-tuning.
    """
    with open(SYSTEM_PROMPT_PATH, encoding="utf-8") as f:
        return f.read()


def load_model():
    """
    Load the fine-tuned model and tokenizer in bfloat16 for inference.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_DIR,
        dtype=torch.bfloat16,
        # default attention crashes on the Apple GPU with PyTorch 2.6
        attn_implementation="eager",
    ).to(DEVICE)
    model.eval()
    return model, tokenizer


def generate(model, tokenizer, system_prompt, subject, body):
    """
    Send one ticket to the model.
    Return the output text and the generation time in seconds.
    """
    # Same message format as in training and evaluation
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Subject: {subject}\nBody: {body}"},
    ]

    # Qwen3 chat template, thinking mode off for a direct answer
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    start = time.time()
    with torch.no_grad():
        # Deterministic generation: the same ticket always gives the same output
        output_ids = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS, do_sample=False)
    seconds = time.time() - start

    # Decoding only the new tokens, not the prompt
    text = tokenizer.decode(output_ids[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return text, seconds


def parse_json(text):
    """
    Extract the JSON object from the model output.
    Return an empty dict if it is invalid.
    """
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return {}
    try:
        result = json.loads(text[start:end + 1])
        return result if isinstance(result, dict) else {}
    except json.JSONDecodeError:
        return {}


def check_labels(result):
    """
    Return a list of warnings for labels that are not allowed values.
    """
    warnings = []
    if str(result.get("type", "")).strip() not in ALLOWED_TYPES:
        warnings.append(f"Type '{result.get('type', '')}' is not an allowed value.")
    if str(result.get("queue", "")).strip() not in ALLOWED_QUEUES:
        warnings.append(f"Queue '{result.get('queue', '')}' is not an allowed value.")
    if str(result.get("priority", "")).strip().lower() not in ALLOWED_PRIORITIES:
        warnings.append(f"Priority '{result.get('priority', '')}' is not an allowed value.")
    return warnings


def find_placeholders(text):
    """
    Find placeholders such as <tel_num> or [Your Name] that the agent must replace.
    """
    return sorted(set(re.findall(r"<[^<>\s]+>|\[[^\[\]]+\]", text)))
