import re
import torch
from typing import List
from .loader import REG, DEVICE

# Intent
@torch.no_grad()
def infer_intent(requirement: str) -> str:
    enc = REG.intent_tok(
        requirement,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128,
    ).to(DEVICE)
    out = REG.intent_model(**enc)
    pred = int(out.logits.argmax(dim=-1).item())
    return REG.id2label.get(pred, str(pred))

# User story
@torch.no_grad()
def generate_user_story(requirement: str) -> str:
    enc = REG.story_tok(
        requirement,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    ).to(DEVICE)
    gen = REG.story_model.generate(
        **enc,
        max_length=256,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3,
        repetition_penalty=1.2,
        length_penalty=0.9,
    )
    return REG.story_tok.decode(gen[0], skip_special_tokens=True).strip()

# Acceptance criteria processing
def _split_to_items(text: str) -> List[str]:
    raw = re.split(r"(?:\n|^|\s)(?:\d+[\.\):\-]|[-*•])\s+", text)
    parts = [p.strip(" -•\t\r\n") for p in raw if p and p.strip()]
    if len(parts) < 3:
        parts = re.split(r"\.\s+", text)
        parts = [p.strip(" .-•\t\r\n") for p in parts if p and p.strip()]
    seen = set()
    uniq = []
    for p in parts:
        key = re.sub(r"\s+", " ", p.lower())
        if len(key) < 3:
            continue
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq

def _format_numbered(items: List[str], min_items=4, max_items=8) -> List[str]:
    items = [it for it in items if len(it) > 3][:max_items]
    if len(items) < min_items and items:
        extra = []
        for it in items:
            chunks = re.split(r";|, and | and ", it)
            for ch in chunks[1:]:
                ch = ch.strip().rstrip(".")
                if len(ch) > 8:
                    extra.append(ch)
            if len(items) + len(extra) >= min_items:
                break
        items.extend(extra[: max(0, min_items - len(items))])
    out = []
    for i, it in enumerate(items, 1):
        it = it.rstrip(".")
        out.append(f"{i}. {it}.")
    return out

# Acceptance criteria
@torch.no_grad()
def generate_acceptance(requirement: str, intent: str, user_story: str) -> List[str]:
    prompt = (
        f"Requirement: {requirement} "
        f"Intent: {intent} "
        f"User Story: {user_story} -> Acceptance Criteria:"
    )
    enc = REG.accept_tok(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    ).to(DEVICE)
    gen = REG.accept_model.generate(
        **enc,
        max_length=512,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=4,
        repetition_penalty=1.25,
        length_penalty=0.9,
    )
    raw = REG.accept_tok.decode(gen[0], skip_special_tokens=True).strip()
    items = _split_to_items(raw)
    items = _format_numbered(items, min_items=4, max_items=8)
    return items
