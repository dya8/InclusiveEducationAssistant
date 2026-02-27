# core/nlp/tokenizer.py
import re

def tokenize(text: str):
    return re.findall(r"\b[a-zA-Z]+\b", text.lower())

def extract_context_and_prefix(text: str):
    words = tokenize(text)

    if text and text[-1].isalpha():
        prefix = words[-1] if words else ""
        context = words[:-1]
    else:
        prefix = ""
        context = words

    return context, prefix