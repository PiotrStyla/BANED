#!/usr/bin/env python3
"""
api_double_power.py - Double Power Fake News Detection API
Combines BANED (CNN) with LIMM-inspired logical verification
Neural proof-based sound verification system
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
import sys

# Add verification module to path
sys.path.append(os.path.dirname(__file__))
from verification.logical_consistency import DoublePowerVerifier, LogicalConsistencyChecker, FactDatabase

# Initialize FastAPI
app = FastAPI(
    title="BANED Double Power Fake News Detection API",
    description="Neural Network + Logical Verification for Sound Fake News Detection",
    version="4.0.0-double-power"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class DoublePowerRequest(BaseModel):
    text: str
    use_double_power: bool = True
    language: Optional[str] = None  # 'pl' or 'en', auto-detect if None

class DoublePowerResponse(BaseModel):
    text: str
    prediction: str
    confidence: float
    fake_probability: float
    language: str
    method: str
    cnn_score: Optional[Dict] = None
    verification: Optional[Dict] = None
    explanation: List[str]

class BatchRequest(BaseModel):
    texts: List[str]
    use_double_power: bool = True

# CNN Model (same as BANED)
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

# Global state
models = {}  # Will hold 'pl' and 'en' models
vocabs = {}
double_power_verifier = DoublePowerVerifier()
device = 'cpu'

# Language detection
POLISH_CHARS = set('ąćęłńóśźż')
POLISH_COMMON_WORDS = {
    'jest', 'się', 'nie', 'że', 'jak', 'ale', 'dla', 'jego', 'przez',
    'na', 'do', 'po', 'przed', 'bardzo', 'może', 'może', 'tylko'
}

def detect_language(text: str) -> str:
    """Auto-detect Polish or English"""
    text_lower = text.lower()
    
    # Check for Polish diacritics
    if any(char in POLISH_CHARS for char in text_lower):
        return 'pl'
    
    # Check for common Polish words
    words = set(re.findall(r'\b\w+\b', text_lower))
    polish_word_count = len(words & POLISH_COMMON_WORDS)
    
    if polish_word_count >= 2 or (polish_word_count > 0 and len(words) < 10):
        return 'pl'
    
    return 'en'

def preprocess_text(text: str) -> str:
    """Clean and normalize text"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'[^a-ząćęłńóśźż\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def text_to_indices(text: str, vocab: dict, max_len: int = 100) -> torch.Tensor:
    """Convert text to tensor indices"""
    words = preprocess_text(text).split()
    indices = [vocab.get(w, vocab.get('<UNK>', 0)) for w in words[:max_len]]
    
    # Pad to max_len
    if len(indices) < max_len:
        indices += [0] * (max_len - len(indices))
    
    return torch.tensor([indices], dtype=torch.long)

def load_model(model_path: str, vocab_path: str, lang: str):
    """Load CNN model and vocabulary"""
    global models, vocabs
    
    # Load vocabulary
    vocab = {'<PAD>': 0, '<UNK>': 1}
    if os.path.exists(vocab_path):
        with open(vocab_path, 'r', encoding='utf-8') as f:
            for idx, line in enumerate(f, start=2):
                word = line.strip()
                if word:
                    vocab[word] = idx
    
    # Load model
    model = SimpleCNN(vocab_size=len(vocab))
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
    
    models[lang] = model
    vocabs[lang] = vocab

def predict_with_cnn(text: str, lang: str) -> Dict:
    """Get CNN prediction"""
    if lang not in models:
        return None
    
    model = models[lang]
    vocab = vocabs[lang]
    
    # Convert text to tensor
    x = text_to_indices(text, vocab)
    
    # Get prediction
    with torch.no_grad():
        prob = model(x).item()
    
    # MC Dropout for uncertainty (5 samples)
    model.train()  # Enable dropout
    mc_probs = []
    with torch.no_grad():
        for _ in range(5):
            mc_probs.append(model(x).item())
    model.eval()
    
    mean_prob = np.mean(mc_probs)
    std_prob = np.std(mc_probs)
    
    return {
        'probability': mean_prob,
        'uncertainty': std_prob,
        'prediction': 'FAKE' if mean_prob > 0.5 else 'REAL',
        'confidence': abs(mean_prob - 0.5) * 2.0
    }

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    # Try to load Polish model
    pl_model_path = 'models/model_pl.pth'
    pl_vocab_path = 'models/vocab_pl.txt'
    if os.path.exists(pl_model_path):
        load_model(pl_model_path, pl_vocab_path, 'pl')
    
    # Try to load English model
    en_model_path = 'models/model.pth'
    en_vocab_path = 'models/vocab.txt'
    if os.path.exists(en_model_path):
        load_model(en_model_path, en_vocab_path, 'en')

@app.get("/")
async def root():
    """API status"""
    return {
        "name": "BANED Double Power API",
        "version": "4.0.0",
        "status": "online",
        "models_loaded": list(models.keys()),
        "features": [
            "CNN Neural Network",
            "Logical Consistency Checking",
            "Fact Database Verification",
            "Double Power Verification",
            "Bilingual (PL/EN)"
        ],
        "inspiration": "LIMM + Neural Proofs for Sound Verification"
    }

@app.post("/predict", response_model=DoublePowerResponse)
async def predict(request: DoublePowerRequest):
    """
    Double Power Prediction:
    1. CNN Neural Network (pattern recognition)
    2. Logical Verification (consistency + fact checking)
    """
    text = request.text
    
    if not text or len(text) < 10:
        raise HTTPException(status_code=400, detail="Text too short (min 10 chars)")
    
    # Detect language
    lang = request.language or detect_language(text)
    
    explanation = []
    cnn_result = None
    verification_result = None
    
    # Power 1: CNN Neural Network
    if lang in models and request.use_double_power:
        cnn_result = predict_with_cnn(text, lang)
        explanation.append(f"CNN ({lang.upper()}): {cnn_result['prediction']} with {cnn_result['confidence']:.2%} confidence")
    
    # Power 2: Logical Verification
    if request.use_double_power:
        cnn_prob = cnn_result['probability'] if cnn_result else None
        verification_result = double_power_verifier.verify(text, cnn_prob)
        explanation.append(f"Verification: {verification_result['verdict']} (score: {verification_result['verification_score']})")
        
        if verification_result['all_issues']:
            explanation.append(f"Issues found: {len(verification_result['all_issues'])}")
            for issue in verification_result['all_issues'][:3]:
                explanation.append(f"  • {issue}")
    
    # Determine final prediction
    if request.use_double_power and verification_result:
        # Use double power result
        final_prediction = verification_result['verdict']
        final_confidence = verification_result['confidence']
        final_prob = verification_result['fake_probability']
        method = "DOUBLE_POWER"
    elif cnn_result:
        # Use CNN only
        final_prediction = cnn_result['prediction']
        final_confidence = cnn_result['confidence']
        final_prob = cnn_result['probability']
        method = "CNN_ONLY"
    else:
        # No model available - use verification only
        if verification_result:
            final_prediction = verification_result['verdict']
            final_confidence = verification_result['confidence']
            final_prob = verification_result['fake_probability']
            method = "VERIFICATION_ONLY"
        else:
            raise HTTPException(status_code=503, detail="No models available")
    
    return DoublePowerResponse(
        text=text[:200],
        prediction=final_prediction,
        confidence=final_confidence,
        fake_probability=final_prob,
        language=lang,
        method=method,
        cnn_score=cnn_result,
        verification=verification_result,
        explanation=explanation
    )

@app.post("/batch")
async def batch_predict(request: BatchRequest):
    """Batch prediction with double power"""
    results = []
    
    for text in request.texts:
        try:
            result = await predict(DoublePowerRequest(
                text=text,
                use_double_power=request.use_double_power
            ))
            results.append(result.dict())
        except Exception as e:
            results.append({
                "text": text[:100],
                "error": str(e)
            })
    
    return {
        "total": len(request.texts),
        "results": results
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": list(models.keys()),
        "verification_active": True,
        "double_power_enabled": True
    }

@app.get("/verify-demo")
async def verification_demo():
    """Demo endpoint showing verification capabilities"""
    test_cases = [
        "Scientists reveal 200% effective cure!",
        "Government announces new research program",
        "COVID-19 started in 2015 according to experts",
    ]
    
    results = []
    for text in test_cases:
        result = double_power_verifier.verify(text)
        results.append({
            "text": text,
            "verdict": result['verdict'],
            "score": result['verification_score'],
            "issues": result['all_issues'][:3]
        })
    
    return {
        "demo": "Double Power Verification System",
        "test_cases": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
