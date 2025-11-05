#!/usr/bin/env python3
"""
calculate_optimized.py - OPTIMIZED fusion with filtered patterns and confidence weighting
"""
import argparse
import csv
import numpy as np
import sys
from collections import defaultdict


# Common words that appear in both real and fake news - filter these out
COMMON_WORDS_BLACKLIST = {
    'in', 'to', 'for', 'of', 'and', 'the', 'a', 'an', 'on', 'at', 'by', 'with',
    'from', 'about', 'as', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
}


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


def filter_distinctive_patterns(patterns, blacklist=COMMON_WORDS_BLACKLIST):
    """Filter out patterns containing common words."""
    filtered = {}
    removed = 0
    
    for pattern, support in patterns.items():
        pattern_words = set(pattern.split())
        # Keep pattern only if it doesn't contain blacklisted words
        if not pattern_words & blacklist:
            filtered[pattern] = support
        else:
            removed += 1
    
    if removed > 0:
        print(f"  Filtered out {removed} common patterns")
    
    return filtered


def calculate_kb_support(text, patterns, limit=20):
    """Calculate knowledge base support for text."""
    words = set(text.lower().split())
    total_support = 0.0
    matches = 0
    matched_patterns = []
    
    for pattern, support in list(patterns.items())[:limit]:
        pattern_words = set(pattern.split())
        if pattern_words.issubset(words):
            total_support += support
            matches += 1
            matched_patterns.append(pattern)
    
    return total_support, matches, matched_patterns


def weighted_fusion(cnn_prob, kb_signal, cnn_confidence):
    """
    Weighted fusion: give more weight to CNN when it's very confident
    
    Args:
        cnn_prob: CNN probability (0-1)
        kb_signal: KB signal (-inf to +inf, where positive = real, negative = fake)
        cnn_confidence: How confident CNN is (distance from 0.5)
    
    Returns:
        Fused probability (0-1)
    """
    # Normalize kb_signal to probability
    kb_prob = 0.5 + (kb_signal * 0.5)
    kb_prob = max(0.0, min(1.0, kb_prob))
    
    # CNN weight based on confidence
    # If CNN is very confident (>0.4 from center), trust it more
    # If CNN is uncertain (<0.2 from center), trust KB more
    cnn_weight = min(1.0, cnn_confidence / 0.4)  # 0 to 1 scale
    kb_weight = 1.0 - cnn_weight
    
    # Weighted average
    fused_prob = (cnn_prob * cnn_weight) + (kb_prob * kb_weight)
    
    return fused_prob


def main():
    parser = argparse.ArgumentParser(description='Calculate OPTIMIZED calibrated metrics')
    parser.add_argument('combined_csv', help='Combined CSV with text and label columns')
    parser.add_argument('--probabilities', required=True, help='CNN probabilities .npy file')
    parser.add_argument('--fake_support', required=True, help='Fake news support patterns CSV')
    parser.add_argument('--real_support', required=True, help='Real news support patterns CSV')
    parser.add_argument('--limit', type=int, default=20, help='Top-K patterns to use')
    parser.add_argument('--out_dir', default='.', help='Output directory')
    parser.add_argument('--no_filter', action='store_true', help='Disable common word filtering')
    
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
    
    # OPTIMIZATION 1: Filter common words
    if not args.no_filter:
        print("\n[INFO] Filtering distinctive patterns...")
        print(f"  Blacklist: {len(COMMON_WORDS_BLACKLIST)} common words")
        real_patterns = filter_distinctive_patterns(real_patterns)
        fake_patterns = filter_distinctive_patterns(fake_patterns)
        print(f"  After filtering:")
        print(f"    Real patterns: {len(real_patterns)}")
        print(f"    Fake patterns: {len(fake_patterns)}")
    
    print("\n[INFO] Loading combined data...")
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
    
    print(f"[INFO] Processing {len(texts)} samples with OPTIMIZED fusion...")
    
    # Calculate metrics with both methods
    results_baseline = []
    results_optimized = []
    
    for i, (text, label, cnn_prob) in enumerate(zip(texts, labels, cnn_probs)):
        real_support, real_matches, real_patterns_matched = calculate_kb_support(text, real_patterns, args.limit)
        fake_support, fake_matches, fake_patterns_matched = calculate_kb_support(text, fake_patterns, args.limit)
        
        # BASELINE: Simple fusion (original method)
        kb_signal_baseline = real_support - fake_support
        kb_prob_baseline = 0.5 + (kb_signal_baseline * 0.5)
        kb_prob_baseline = max(0.0, min(1.0, kb_prob_baseline))
        fused_prob_baseline = (cnn_prob + kb_prob_baseline) / 2.0
        
        # OPTIMIZED: Weighted fusion
        kb_signal_optimized = real_support - fake_support
        cnn_confidence = abs(cnn_prob - 0.5)
        fused_prob_optimized = weighted_fusion(cnn_prob, kb_signal_optimized, cnn_confidence)
        
        # Predictions
        cnn_pred = 1 if cnn_prob > 0.5 else 0
        fused_pred_baseline = 1 if fused_prob_baseline > 0.5 else 0
        fused_pred_optimized = 1 if fused_prob_optimized > 0.5 else 0
        
        results_baseline.append({
            'text': text[:50] + '...',
            'label': label,
            'cnn_prob': cnn_prob,
            'fused_prob': fused_prob_baseline,
            'cnn_pred': cnn_pred,
            'fused_pred': fused_pred_baseline,
            'cnn_confidence': cnn_confidence,
            'real_matches': real_matches,
            'fake_matches': fake_matches
        })
        
        results_optimized.append({
            'text': text[:50] + '...',
            'label': label,
            'cnn_prob': cnn_prob,
            'fused_prob': fused_prob_optimized,
            'cnn_pred': cnn_pred,
            'fused_pred': fused_pred_optimized,
            'cnn_confidence': cnn_confidence,
            'real_matches': real_matches,
            'fake_matches': fake_matches
        })
    
    # Calculate accuracy for both methods
    cnn_correct = sum(1 for r in results_baseline if r['cnn_pred'] == r['label'])
    baseline_correct = sum(1 for r in results_baseline if r['fused_pred'] == r['label'])
    optimized_correct = sum(1 for r in results_optimized if r['fused_pred'] == r['label'])
    
    cnn_accuracy = cnn_correct / len(results_baseline)
    baseline_accuracy = baseline_correct / len(results_baseline)
    optimized_accuracy = optimized_correct / len(results_optimized)
    
    print("\n" + "="*80)
    print("RESULTS COMPARISON: BASELINE vs OPTIMIZED FUSION")
    print("="*80)
    print(f"Total samples: {len(results_baseline)}")
    print(f"\nCNN Accuracy:            {cnn_accuracy:.3f} ({cnn_correct}/{len(results_baseline)})")
    print(f"Baseline Fusion:         {baseline_accuracy:.3f} ({baseline_correct}/{len(results_baseline)})")
    print(f"Optimized Fusion:        {optimized_accuracy:.3f} ({optimized_correct}/{len(results_optimized)})")
    print(f"\nImprovement over CNN:")
    print(f"  Baseline:  {(baseline_accuracy - cnn_accuracy):+.3f}")
    print(f"  Optimized: {(optimized_accuracy - cnn_accuracy):+.3f}")
    print(f"\nOptimized vs Baseline:   {(optimized_accuracy - baseline_accuracy):+.3f}")
    
    # Show cases where optimized differs from baseline
    differences = []
    for b, o in zip(results_baseline, results_optimized):
        if b['fused_pred'] != o['fused_pred']:
            differences.append((b, o))
    
    if differences:
        print(f"\n{len(differences)} cases where OPTIMIZED differs from BASELINE:")
        print("-" * 80)
        for i, (baseline_result, opt_result) in enumerate(differences[:10], 1):
            label_str = "REAL" if baseline_result['label'] == 1 else "FAKE"
            print(f"\n{i}. [{label_str}] {baseline_result['text']}")
            print(f"   CNN: {baseline_result['cnn_prob']:.3f} (confidence: {baseline_result['cnn_confidence']:.3f})")
            print(f"   Baseline:  {baseline_result['fused_prob']:.3f} → {'REAL' if baseline_result['fused_pred']==1 else 'FAKE'} {'✓' if baseline_result['fused_pred']==baseline_result['label'] else '✗'}")
            print(f"   Optimized: {opt_result['fused_prob']:.3f} → {'REAL' if opt_result['fused_pred']==1 else 'FAKE'} {'✓' if opt_result['fused_pred']==opt_result['label'] else '✗'}")
    else:
        print("\n[INFO] Optimized fusion produces same predictions as baseline")
    
    # Confidence analysis
    baseline_confidences = [abs(r['fused_prob'] - 0.5) for r in results_baseline]
    optimized_confidences = [abs(r['fused_prob'] - 0.5) for r in results_optimized]
    
    print(f"\n{'='*80}")
    print("CONFIDENCE ANALYSIS")
    print(f"{'='*80}")
    print(f"{'Method':<20} {'Avg Conf':<15} {'Min Conf':<15} {'Max Conf':<15}")
    print("-" * 80)
    print(f"{'CNN':<20} {np.mean([r['cnn_confidence'] for r in results_baseline]):.3f}{' '*11} {np.min([r['cnn_confidence'] for r in results_baseline]):.3f}{' '*11} {np.max([r['cnn_confidence'] for r in results_baseline]):.3f}")
    print(f"{'Baseline Fusion':<20} {np.mean(baseline_confidences):.3f}{' '*11} {np.min(baseline_confidences):.3f}{' '*11} {np.max(baseline_confidences):.3f}")
    print(f"{'Optimized Fusion':<20} {np.mean(optimized_confidences):.3f}{' '*11} {np.min(optimized_confidences):.3f}{' '*11} {np.max(optimized_confidences):.3f}")
    
    print("\n" + "="*80)
    print("OPTIMIZATION SUMMARY")
    print("="*80)
    print("\n✓ Applied optimizations:")
    if not args.no_filter:
        print(f"  1. Filtered {len(COMMON_WORDS_BLACKLIST)} common words from patterns")
    print("  2. Weighted fusion based on CNN confidence")
    print("     - High CNN confidence → Trust CNN more")
    print("     - Low CNN confidence → Trust KB more")
    
    print("\n✓ Key findings:")
    if optimized_accuracy > baseline_accuracy:
        print(f"  • Optimized fusion IMPROVES accuracy by {(optimized_accuracy-baseline_accuracy):.3f}")
    elif optimized_accuracy == baseline_accuracy:
        print(f"  • Optimized fusion maintains same accuracy as baseline")
    else:
        print(f"  • Optimized fusion slightly decreases accuracy by {(optimized_accuracy-baseline_accuracy):.3f}")
        print(f"  • This may indicate CNN is already very reliable")
    
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()
