#!/usr/bin/env python3
"""
api.py - REST API for BANED Fake News Detection
FastAPI-based production-ready API with automatic documentation
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import torch
import torch.nn as nn
import csv
import re
from typing import List, Dict, Optional
import os

# Initialize FastAPI
app = FastAPI(
    title="BANED Fake News Detection API",
    description="Bayesian-Augmented News Evaluation and Detection - Production API",
    version="3.0.0"
)

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class PredictionRequest(BaseModel):
    text: str
    use_fusion: bool = True

class PredictionResponse(BaseModel):
    text: str
    prediction: str
    confidence: float
    cnn_probability: float
    kb_match: Optional[Dict[str, List[str]]] = None
    method: str

class BatchPredictionRequest(BaseModel):
    texts: List[str]
    use_fusion: bool = True

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    kb_loaded: bool
    version: str

# Simple CNN Model (same as training)
class SimpleCNN(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, num_filters=100, dropout_p=0.5):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.conv1 = nn.Conv1d(embed_dim, num_filters, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(embed_dim, num_filters, kernel_size=4, padding=2)
        self.conv3 = nn.Conv1d(embed_dim, num_filters, kernel_size=5, padding=2)
        self.dropout = nn.Dropout(dropout_p)
        self.fc = nn.Linear(num_filters * 3, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        x = self.embedding(x)
        x = x.transpose(1, 2)
        c1 = torch.relu(self.conv1(x))
        c2 = torch.relu(self.conv2(x))
        c3 = torch.relu(self.conv3(x))
        c1 = torch.max(c1, dim=2)[0]
        c2 = torch.max(c2, dim=2)[0]
        c3 = torch.max(c3, dim=2)[0]
        concat = torch.cat([c1, c2, c3], dim=1)
        concat = self.dropout(concat)
        out = self.fc(concat)
        return self.sigmoid(out).squeeze()
    
    def predict(self, x):
        """Prediction mode - returns probabilities"""
        return self.forward(x)

# Global state
model = None
vocab = None
real_patterns = []
fake_patterns = []
device = 'cpu'
MODEL_LOADED = False
KB_LOADED = False

# Common words blacklist for filtering
COMMON_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should'
}

def clean_text(text):
    """Clean text (same as prep_data.py)"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_model(model_dir='models'):
    """Load trained CNN model and vocabulary"""
    global model, vocab, device, MODEL_LOADED
    
    try:
        # Load vocabulary
        vocab_path = os.path.join(model_dir, 'vocab.txt')
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab = {word.strip(): idx for idx, word in enumerate(f.readlines())}
        
        # Initialize model
        model = SimpleCNN(len(vocab), dropout_p=0.5).to(device)
        
        # Load weights
        weights_path = os.path.join(model_dir, 'model.pth')
        model.load_state_dict(torch.load(weights_path, map_location=device))
        model.eval()
        
        MODEL_LOADED = True
        print(f"[INFO] Model loaded: {len(vocab)} words in vocabulary")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        MODEL_LOADED = False
        return False

def load_knowledge_base(kb_dir='kb'):
    """Load Apriori knowledge base patterns"""
    global real_patterns, fake_patterns, KB_LOADED
    
    try:
        # Load real patterns
        real_path = os.path.join(kb_dir, 'real_patterns.csv')
        if os.path.exists(real_path):
            with open(real_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                real_patterns = [row[0] for row in reader if row[0] not in COMMON_WORDS]
        
        # Load fake patterns
        fake_path = os.path.join(kb_dir, 'fake_patterns.csv')
        if os.path.exists(fake_path):
            with open(fake_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                fake_patterns = [row[0] for row in reader if row[0] not in COMMON_WORDS]
        
        KB_LOADED = True
        print(f"[INFO] KB loaded: {len(real_patterns)} real, {len(fake_patterns)} fake patterns")
        return True
    except Exception as e:
        print(f"[WARN] Failed to load KB: {e}")
        KB_LOADED = False
        return False

def predict_cnn(text, mc_samples=10):
    """Predict using CNN with MC Dropout"""
    if not MODEL_LOADED:
        raise ValueError("Model not loaded")
    
    # Clean and tokenize
    cleaned = clean_text(text)
    tokens = cleaned.split()[:50]  # Max 50 tokens
    
    # Convert to indices
    indices = [vocab.get(token, 0) for token in tokens]
    
    # Pad
    if len(indices) < 50:
        indices += [0] * (50 - len(indices))
    
    # Convert to tensor
    x = torch.tensor([indices], dtype=torch.long).to(device)
    
    # MC Dropout inference
    model.train()  # Keep dropout active
    predictions = []
    with torch.no_grad():
        for _ in range(mc_samples):
            pred = model(x).item()
            predictions.append(pred)
    
    # Average predictions
    avg_pred = np.mean(predictions)
    return avg_pred

def match_patterns(text):
    """Match text against knowledge base patterns"""
    if not KB_LOADED:
        return None
    
    cleaned = clean_text(text)
    tokens = set(cleaned.split())
    
    # Find matches
    real_matches = [p for p in real_patterns if p in tokens]
    fake_matches = [p for p in fake_patterns if p in tokens]
    
    return {
        'real': real_matches,
        'fake': fake_matches
    }

def fuse_predictions(cnn_prob, kb_matches):
    """Fuse CNN and KB predictions (optimized method)"""
    if not kb_matches or (not kb_matches['real'] and not kb_matches['fake']):
        return cnn_prob
    
    # KB probability
    real_count = len(kb_matches['real'])
    fake_count = len(kb_matches['fake'])
    total_count = real_count + fake_count
    
    if total_count == 0:
        kb_prob = 0.5
    else:
        kb_prob = real_count / total_count
    
    # Confidence-based weighting
    cnn_confidence = abs(cnn_prob - 0.5)
    cnn_weight = min(1.0, cnn_confidence / 0.4)
    kb_weight = 1.0 - cnn_weight
    
    # Weighted fusion
    fused_prob = (cnn_prob * cnn_weight) + (kb_prob * kb_weight)
    return fused_prob

@app.on_event("startup")
async def startup_event():
    """Load model and KB on startup"""
    print("[INFO] Starting BANED API...")
    load_model()
    load_knowledge_base()
    print(f"[INFO] API ready - Model: {MODEL_LOADED}, KB: {KB_LOADED}")

@app.get("/", response_model=HealthResponse)
async def root():
    """API health check"""
    return {
        "status": "online",
        "model_loaded": MODEL_LOADED,
        "kb_loaded": KB_LOADED,
        "version": "3.0.0"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Predict if text is real or fake news"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # CNN prediction
        cnn_prob = predict_cnn(request.text)
        
        # KB matching
        kb_matches = match_patterns(request.text) if KB_LOADED else None
        
        # Fusion
        if request.use_fusion and KB_LOADED and kb_matches:
            final_prob = fuse_predictions(cnn_prob, kb_matches)
            method = "fusion"
        else:
            final_prob = cnn_prob
            method = "cnn_only"
        
        # Classify
        prediction = "REAL" if final_prob > 0.5 else "FAKE"
        confidence = abs(final_prob - 0.5) * 2  # Convert to 0-1 scale
        
        return {
            "text": request.text[:100] + "..." if len(request.text) > 100 else request.text,
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "cnn_probability": round(cnn_prob, 4),
            "kb_match": kb_matches,
            "method": method
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Predict multiple texts at once"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for text in request.texts:
        try:
            pred_req = PredictionRequest(text=text, use_fusion=request.use_fusion)
            result = await predict(pred_req)
            results.append(result)
        except Exception as e:
            results.append({
                "text": text[:50] + "...",
                "error": str(e)
            })
    
    return {"results": results, "total": len(results)}

@app.get("/stats")
async def get_stats():
    """Get model and KB statistics"""
    return {
        "model": {
            "loaded": MODEL_LOADED,
            "vocabulary_size": len(vocab) if vocab else 0,
            "device": device
        },
        "knowledge_base": {
            "loaded": KB_LOADED,
            "real_patterns": len(real_patterns),
            "fake_patterns": len(fake_patterns),
            "total_patterns": len(real_patterns) + len(fake_patterns)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
