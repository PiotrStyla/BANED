#!/usr/bin/env python3
"""
compare_results.py - Detailed comparison showing KB impact on predictions
"""
import csv
import numpy as np
from collections import defaultdict


def load_patterns(pattern_file):
    """Load support patterns."""
    patterns = {}
    try:
        with open(pattern_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                patterns[row['pattern']] = float(row['support'])
    except FileNotFoundError:
        pass
    return patterns


def calculate_kb_support(text, patterns, limit=20):
    """Calculate KB support for text."""
    words = set(text.lower().split())
    total_support = 0.0
    matches = []
    
    for pattern, support in list(patterns.items())[:limit]:
        pattern_words = set(pattern.split())
        if pattern_words.issubset(words):
            total_support += support
            matches.append(pattern)
    
    return total_support, matches


def main():
    # Load data
    print("\n" + "="*80)
    print("BANED RESULTS - DETAILED COMPARISON")
    print("="*80 + "\n")
    
    # Load CNN predictions
    cnn_probs = np.load('fnn_all_clean_cnn_prob.npy')
    
    # Load patterns
    real_patterns = load_patterns('real_support.csv')
    fake_patterns = load_patterns('fake_support.csv')
    
    print(f"Knowledge Base Loaded:")
    print(f"  Real patterns: {len(real_patterns)}")
    print(f"  Fake patterns: {len(fake_patterns)}")
    
    # Load texts and labels
    texts = []
    labels = []
    with open('fnn_all_clean.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['text'])
            labels.append(int(row['label']))
    
    # Calculate all metrics
    results = []
    for i, (text, label, cnn_prob) in enumerate(zip(texts, labels, cnn_probs)):
        real_support, real_matches = calculate_kb_support(text, real_patterns, 20)
        fake_support, fake_matches = calculate_kb_support(text, fake_patterns, 20)
        
        kb_signal = real_support - fake_support
        kb_prob = 0.5 + (kb_signal * 0.5)
        kb_prob = max(0.0, min(1.0, kb_prob))
        
        fused_prob = (cnn_prob + kb_prob) / 2.0
        
        kb_impact = fused_prob - cnn_prob
        
        results.append({
            'idx': i,
            'text': text,
            'label': label,
            'cnn_prob': cnn_prob,
            'kb_prob': kb_prob,
            'fused_prob': fused_prob,
            'kb_impact': kb_impact,
            'real_matches': real_matches,
            'fake_matches': fake_matches,
            'cnn_correct': (cnn_prob > 0.5) == label,
            'fused_correct': (fused_prob > 0.5) == label
        })
    
    # Overall stats
    print(f"\n{'='*80}")
    print("OVERALL STATISTICS")
    print(f"{'='*80}\n")
    
    total = len(results)
    cnn_acc = sum(1 for r in results if r['cnn_correct']) / total
    fused_acc = sum(1 for r in results if r['fused_correct']) / total
    
    print(f"Total samples: {total}")
    print(f"CNN Accuracy:   {cnn_acc:.2%} ({sum(1 for r in results if r['cnn_correct'])}/{total})")
    print(f"Fused Accuracy: {fused_acc:.2%} ({sum(1 for r in results if r['fused_correct'])}/{total})")
    print(f"Improvement:    {(fused_acc - cnn_acc):.2%}")
    
    # KB impact analysis
    avg_impact = np.mean([r['kb_impact'] for r in results])
    print(f"\nAverage KB impact: {avg_impact:+.4f}")
    
    positive_impact = [r for r in results if r['kb_impact'] > 0.01]
    negative_impact = [r for r in results if r['kb_impact'] < -0.01]
    neutral_impact = [r for r in results if abs(r['kb_impact']) <= 0.01]
    
    print(f"  Positive impact (KB helps):  {len(positive_impact)} cases")
    print(f"  Negative impact (KB hurts):  {len(negative_impact)} cases")
    print(f"  Neutral (no KB effect):      {len(neutral_impact)} cases")
    
    # Most confident KB signals
    print(f"\n{'='*80}")
    print("TOP 10 CASES WHERE KB HAD STRONGEST POSITIVE IMPACT")
    print(f"{'='*80}\n")
    
    sorted_positive = sorted(results, key=lambda x: x['kb_impact'], reverse=True)[:10]
    for i, r in enumerate(sorted_positive, 1):
        label_str = "REAL" if r['label'] == 1 else "FAKE"
        print(f"{i}. [{label_str}] {r['text'][:60]}...")
        print(f"   CNN: {r['cnn_prob']:.3f} → Fused: {r['fused_prob']:.3f} (KB impact: +{r['kb_impact']:.3f})")
        if r['real_matches']:
            print(f"   Real patterns: {', '.join(r['real_matches'])}")
        if r['fake_matches']:
            print(f"   Fake patterns: {', '.join(r['fake_matches'])}")
        print()
    
    # Cases where KB had negative impact
    print(f"{'='*80}")
    print("TOP 10 CASES WHERE KB HAD STRONGEST NEGATIVE IMPACT")
    print(f"{'='*80}\n")
    
    sorted_negative = sorted(results, key=lambda x: x['kb_impact'])[:10]
    for i, r in enumerate(sorted_negative, 1):
        label_str = "REAL" if r['label'] == 1 else "FAKE"
        print(f"{i}. [{label_str}] {r['text'][:60]}...")
        print(f"   CNN: {r['cnn_prob']:.3f} → Fused: {r['fused_prob']:.3f} (KB impact: {r['kb_impact']:.3f})")
        if r['real_matches']:
            print(f"   Real patterns: {', '.join(r['real_matches'])}")
        if r['fake_matches']:
            print(f"   Fake patterns: {', '.join(r['fake_matches'])}")
        print()
    
    # Pattern frequency in correct classifications
    print(f"{'='*80}")
    print("PATTERN USAGE IN CLASSIFICATIONS")
    print(f"{'='*80}\n")
    
    real_news = [r for r in results if r['label'] == 1]
    fake_news = [r for r in results if r['label'] == 0]
    
    print(f"REAL NEWS ({len(real_news)} samples):")
    print(f"  Average real patterns matched: {np.mean([len(r['real_matches']) for r in real_news]):.2f}")
    print(f"  Average fake patterns matched: {np.mean([len(r['fake_matches']) for r in real_news]):.2f}")
    
    print(f"\nFAKE NEWS ({len(fake_news)} samples):")
    print(f"  Average real patterns matched: {np.mean([len(r['real_matches']) for r in fake_news]):.2f}")
    print(f"  Average fake patterns matched: {np.mean([len(r['fake_matches']) for r in fake_news]):.2f}")
    
    # Most common patterns used
    print(f"\n{'='*80}")
    print("MOST FREQUENTLY MATCHED PATTERNS")
    print(f"{'='*80}\n")
    
    all_real_matches = defaultdict(int)
    all_fake_matches = defaultdict(int)
    
    for r in results:
        for pattern in r['real_matches']:
            all_real_matches[pattern] += 1
        for pattern in r['fake_matches']:
            all_fake_matches[pattern] += 1
    
    print("Real patterns (in actual usage):")
    for pattern, count in sorted(all_real_matches.items(), key=lambda x: x[1], reverse=True):
        pct = count / total * 100
        print(f"  '{pattern}': {count} times ({pct:.1f}% of texts)")
    
    print("\nFake patterns (in actual usage):")
    for pattern, count in sorted(all_fake_matches.items(), key=lambda x: x[1], reverse=True):
        pct = count / total * 100
        print(f"  '{pattern}': {count} times ({pct:.1f}% of texts)")
    
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()
