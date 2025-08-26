import os
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
)

INTENT_DIR = os.environ.get("INTENT_MODEL_DIR", "ismaelfericha/intent-model")
STORY_DIR  = os.environ.get("STORY_MODEL_DIR",  "ismaelfericha/t5-user-story")
ACCEPT_DIR = os.environ.get("ACCEPT_MODEL_DIR", "ismaelfericha/flan-acceptance")

DEVICE_STR = os.environ.get("MODEL_DEVICE", "cpu").lower()
DEVICE = torch.device("cuda" if DEVICE_STR == "cuda" and torch.cuda.is_available() else "cpu")

NUM_THREADS = int(os.environ.get("NUM_THREADS", "4"))
torch.set_num_threads(NUM_THREADS)

class ModelRegistry:
    intent_tok = None
    intent_model = None
    story_tok = None
    story_model = None
    accept_tok = None
    accept_model = None
    id2label = None

REG = ModelRegistry()

def _load_intent():
    REG.intent_tok = AutoTokenizer.from_pretrained(INTENT_DIR)
    REG.intent_model = AutoModelForSequenceClassification.from_pretrained(INTENT_DIR)
    REG.intent_model.to(DEVICE)
    cfg = REG.intent_model.config
    if getattr(cfg, "id2label", None):
        REG.id2label = {int(k): v for k, v in cfg.id2label.items()}
    else:
        REG.id2label = {0: "BUG FIX", 1: "Feature"}

def _load_story():
    REG.story_tok = AutoTokenizer.from_pretrained(STORY_DIR)
    REG.story_model = AutoModelForSeq2SeqLM.from_pretrained(STORY_DIR)
    REG.story_model.to(DEVICE)

def _load_accept():
    REG.accept_tok = AutoTokenizer.from_pretrained(ACCEPT_DIR)
    REG.accept_model = AutoModelForSeq2SeqLM.from_pretrained(ACCEPT_DIR)
    REG.accept_model.to(DEVICE)

def init_models():
    _load_intent()
    _load_story()
    _load_accept()
    return {
        "device": str(DEVICE),
        "threads": NUM_THREADS,
        "intent_dir": INTENT_DIR,
        "story_dir": STORY_DIR,
        "accept_dir": ACCEPT_DIR,
    }
