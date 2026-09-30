import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Which model to load — an env var, so we can change it without editing code
MODEL_ID = os.getenv("MODEL_ID", "distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# Use GPU 0 if PyTorch can see one, else fall back to CPU
DEVICE = 0 if torch.cuda.is_available() else -1

# Load the model ONCE, when the server starts (slow), not on every request
classifier = pipeline("sentiment-analysis", model=MODEL_ID, device=DEVICE)

app = FastAPI(title="sentiment-api")

class PredictRequest(BaseModel):   # defines the expected input: {"text": "..."}
    text: str

@app.get("/healthz")               # health check — also tells us if GPU is being used
def healthz():
    return {
        "status": "ok",
        "model": MODEL_ID,
        "device": "cuda" if DEVICE == 0 else "cpu",
        "gpu": torch.cuda.get_device_name(0) if DEVICE == 0 else None,
        "torch": torch.__version__,
    }

@app.post("/predict")              # the actual model endpoint
def predict(req: PredictRequest):
    return classifier(req.text)[0]
