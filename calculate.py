#!/usr/bin/env python3
"""
calculate.py - Combine CNN predictions with Knowledge Base for calibrated metrics
"""
import argparse
import csv
import numpy as np
import sys
from collections import defaultdict


def load_support(support_file):
    """Load support patterns from CSV."""
    patterns = {}
    try:
        with open(support_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pattern = row['pattern']
                support = float(row['support'])
                patterns[pattern] = support
        return patterns
    except FileNotFoundError:
        print(f"[WARN] Support file not found: {support_file}")
        return {}


def calculate_kb_support(text, patterns, limit=20):
    """Calculate knowledge base support for text."""
    words = set(text.lower().split())
    total_support = 0.0
    matches = 0
    
    for pattern, support in list(patterns.items())[:limit]:
        pattern_words = set(pattern.split())
        if pattern_words.issubset(words):
            total_support += support
            matches += 1
    
    return total_support, matches


def main():
    parser = argparse.ArgumentParser(description='Calculate calibrated metrics')
    parser.add_argument('combined_csv', help='Combined CSV with text and label columns')
    parser.add_argument('--probabilities', required=True, help='CNN probabilities .npy file')
    parser.add_argument('--fake_support', required=True, help='Fake news support patterns CSV')
    parser.add_argument('--real_support', required=True, help='Real news support patterns CSV')
    parser.add_argument('--limit', type=int, default=20, help='Top-K patterns to use')
    parser.add_argument('--out_dir', default='.', help='Output directory')
    
    args = parser.parse_args()
    
    print("[INFO] Loading CNN predictions...")
    try:
        cnn_probs = np.load(args.probabilities)
        print(f"  Loaded {len(cnn_probs)} predictions")
    except FileNotFoundError:
        print(f"[ERROR] Probabilities file not found: {args.probabilities}")
        sys.exit(1)
    
    print("[INFO] Loading support patterns...")
    fake_patterns = load_support(args.fake_support)
    real_patterns = load_support(args.real_support)
    print(f"  Real patterns: {len(real_patterns)}")
    print(f"  Fake patterns: {len(fake_patterns)}")
    
    print("[INFO] Loading combined data...")
    texts = []
    labels = []
    try:
        with open(args.combined_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                texts.append(row['text'])
                labels.append(int(row['label']))
    except FileNotFoundError:
        print(f"[ERROR] Combined CSV not found: {args.combined_csv}")
        sys.exit(1)
    
    if len(cnn_probs) != len(texts):
        print(f"[ERROR] Mismatch: {len(cnn_probs)} predictions vs {len(texts)} texts")
        sys.exit(1)
    
    print(f"[INFO] Processing {len(texts)} samples...")
    
    # Calculate metrics
    results = []
    for i, (text, label, cnn_prob) in enumerate(zip(texts, labels, cnn_probs)):
        real_support, real_matches = calculate_kb_support(text, real_patterns, args.limit)
        fake_support, fake_matches = calculate_kb_support(text, fake_patterns, args.limit)
        
        # Simple fusion: weighted average
        kb_signal = real_support - fake_support
        # Normalize kb_signal to [0, 1] range (simple approach)
        kb_prob = 0.5 + (kb_signal * 0.5)  # Scale to 0-1
        kb_prob = max(0.0, min(1.0, kb_prob))  # Clamp
        
        # Fuse CNN and KB (simple average)
        fused_prob = (cnn_prob + kb_prob) / 2.0
        
        # Predictions
        cnn_pred = 1 if cnn_prob > 0.5 else 0
        fused_pred = 1 if fused_prob > 0.5 else 0
        
        results.append({
            'text': text[:50] + '...',  # Truncate for display
            'label': label,
            'cnn_prob': cnn_prob,
            'kb_prob': kb_prob,
            'fused_prob': fused_prob,
            'cnn_pred': cnn_pred,
            'fused_pred': fused_pred,
            'real_matches': real_matches,
            'fake_matches': fake_matches
        })
    
    # Calculate accuracy
    cnn_correct = sum(1 for r in results if r['cnn_pred'] == r['label'])
    fused_correct = sum(1 for r in results if r['fused_pred'] == r['label'])
    
    cnn_accuracy = cnn_correct / len(results)
    fused_accuracy = fused_correct / len(results)
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Total samples: {len(results)}")
    print(f"\nCNN Accuracy:   {cnn_accuracy:.3f} ({cnn_correct}/{len(results)})")
    print(f"Fused Accuracy: {fused_accuracy:.3f} ({fused_correct}/{len(results)})")
    print(f"Improvement:    {(fused_accuracy - cnn_accuracy):.3f}")
    
    # Per-class metrics
    real_samples = [r for r in results if r['label'] == 1]
    fake_samples = [r for r in results if r['label'] == 0]
    
    if real_samples:
        real_cnn_acc = sum(1 for r in real_samples if r['cnn_pred'] == 1) / len(real_samples)
        real_fused_acc = sum(1 for r in real_samples if r['fused_pred'] == 1) / len(real_samples)
        print(f"\nReal News (n={len(real_samples)}):")
        print(f"  CNN:   {real_cnn_acc:.3f}")
        print(f"  Fused: {real_fused_acc:.3f}")
    
    if fake_samples:
        fake_cnn_acc = sum(1 for r in fake_samples if r['cnn_pred'] == 0) / len(fake_samples)
        fake_fused_acc = sum(1 for r in fake_samples if r['fused_pred'] == 0) / len(fake_samples)
        print(f"\nFake News (n={len(fake_samples)}):")
        print(f"  CNN:   {fake_cnn_acc:.3f}")
        print(f"  Fused: {fake_fused_acc:.3f}")
    
    # Sample results
    print("\n" + "="*60)
    print("SAMPLE PREDICTIONS")
    print("="*60)
    for i, r in enumerate(results[:5], 1):
        print(f"\n{i}. {r['text']}")
        print(f"   True Label: {'REAL' if r['label'] == 1 else 'FAKE'}")
        print(f"   CNN:   prob={r['cnn_prob']:.3f} → {'REAL' if r['cnn_pred']==1 else 'FAKE'}")
        print(f"   KB:    prob={r['kb_prob']:.3f} (R:{r['real_matches']} F:{r['fake_matches']})")
        print(f"   Fused: prob={r['fused_prob']:.3f} → {'REAL' if r['fused_pred']==1 else 'FAKE'}")
    
    print("\n" + "="*60)


if __name__ == '__main__':
    main()
