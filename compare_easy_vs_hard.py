#!/usr/bin/env python3
"""
compare_easy_vs_hard.py - Compare performance on easy vs hard examples
"""
import csv
import numpy as np


def load_results(probs_file, csv_file, real_patterns_file, fake_patterns_file):
    """Load all data for analysis."""
    # Load predictions
    probs = np.load(probs_file)
    
    # Load patterns
    real_patterns = {}
    fake_patterns = {}
    
    try:
        with open(real_patterns_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                real_patterns[row['pattern']] = float(row['support'])
    except:
        pass
    
    try:
        with open(fake_patterns_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fake_patterns[row['pattern']] = float(row['support'])
    except:
        pass
    
    # Load texts
    texts = []
    labels = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['text'])
            labels.append(int(row['label']))
    
    return probs, texts, labels, real_patterns, fake_patterns


def calculate_metrics(probs, labels):
    """Calculate accuracy and confidence metrics."""
    predictions = (probs > 0.5).astype(int)
    accuracy = np.mean(predictions == labels)
    
    # Confidence metrics
    avg_confidence = np.mean(np.abs(probs - 0.5))  # Distance from 0.5
    min_confidence = np.min(np.maximum(probs, 1 - probs))
    
    # Per-class confidence
    real_indices = [i for i, l in enumerate(labels) if l == 1]
    fake_indices = [i for i, l in enumerate(labels) if l == 0]
    
    real_confidence = np.mean(probs[real_indices]) if real_indices else 0
    fake_confidence = 1 - np.mean(probs[fake_indices]) if fake_indices else 0
    
    return {
        'accuracy': accuracy,
        'avg_confidence': avg_confidence,
        'min_confidence': min_confidence,
        'real_confidence': real_confidence,
        'fake_confidence': fake_confidence
    }


def analyze_patterns(real_patterns, fake_patterns):
    """Analyze pattern overlap and distinctiveness."""
    real_words = set()
    for pattern in real_patterns.keys():
        real_words.update(pattern.split())
    
    fake_words = set()
    for pattern in fake_patterns.keys():
        fake_words.update(pattern.split())
    
    overlap = real_words & fake_words
    real_only = real_words - fake_words
    fake_only = fake_words - real_words
    
    return {
        'real_patterns': len(real_patterns),
        'fake_patterns': len(fake_patterns),
        'total_real_words': len(real_words),
        'total_fake_words': len(fake_words),
        'overlap_words': len(overlap),
        'real_only_words': len(real_only),
        'fake_only_words': len(fake_only),
        'overlap_ratio': len(overlap) / max(len(real_words | fake_words), 1)
    }


def main():
    print("\n" + "="*80)
    print("EASY vs HARD EXAMPLES COMPARISON")
    print("="*80 + "\n")
    
    # Load easy examples
    print("Loading EASY examples...")
    easy_probs, easy_texts, easy_labels, easy_real_pat, easy_fake_pat = load_results(
        'fnn_all_clean_cnn_prob.npy',
        'fnn_all_clean.csv',
        'real_support.csv',
        'fake_support.csv'
    )
    
    # Load hard examples
    print("Loading HARD examples...")
    hard_probs, hard_texts, hard_labels, hard_real_pat, hard_fake_pat = load_results(
        'fnn_all_hard_cnn_prob.npy',
        'fnn_all_hard_clean.csv',
        'real_hard_support.csv',
        'fake_hard_support.csv'
    )
    
    # Calculate metrics
    easy_metrics = calculate_metrics(easy_probs, easy_labels)
    hard_metrics = calculate_metrics(hard_probs, hard_labels)
    
    # Analyze patterns
    easy_patterns = analyze_patterns(easy_real_pat, easy_fake_pat)
    hard_patterns = analyze_patterns(hard_real_pat, hard_fake_pat)
    
    # Display comparison
    print("\n" + "="*80)
    print("DATASET STATISTICS")
    print("="*80)
    
    print(f"\n{'Metric':<30} {'EASY':<20} {'HARD':<20} {'Difference':<20}")
    print("-" * 80)
    print(f"{'Total samples':<30} {len(easy_probs):<20} {len(hard_probs):<20} {len(hard_probs)-len(easy_probs):<20}")
    print(f"{'Real samples':<30} {sum(easy_labels):<20} {sum(hard_labels):<20} {sum(hard_labels)-sum(easy_labels):<20}")
    print(f"{'Fake samples':<30} {len(easy_labels)-sum(easy_labels):<20} {len(hard_labels)-sum(hard_labels):<20} {(len(hard_labels)-sum(hard_labels))-(len(easy_labels)-sum(easy_labels)):<20}")
    
    print("\n" + "="*80)
    print("CNN PERFORMANCE")
    print("="*80)
    
    print(f"\n{'Metric':<30} {'EASY':<20} {'HARD':<20} {'Difference':<20}")
    print("-" * 80)
    print(f"{'Accuracy':<30} {easy_metrics['accuracy']:.3f}{' ':<16} {hard_metrics['accuracy']:.3f}{' ':<16} {hard_metrics['accuracy']-easy_metrics['accuracy']:+.3f}")
    print(f"{'Avg Confidence':<30} {easy_metrics['avg_confidence']:.3f}{' ':<16} {hard_metrics['avg_confidence']:.3f}{' ':<16} {hard_metrics['avg_confidence']-easy_metrics['avg_confidence']:+.3f}")
    print(f"{'Min Confidence':<30} {easy_metrics['min_confidence']:.3f}{' ':<16} {hard_metrics['min_confidence']:.3f}{' ':<16} {hard_metrics['min_confidence']-easy_metrics['min_confidence']:+.3f}")
    print(f"{'Real News Confidence':<30} {easy_metrics['real_confidence']:.3f}{' ':<16} {hard_metrics['real_confidence']:.3f}{' ':<16} {hard_metrics['real_confidence']-easy_metrics['real_confidence']:+.3f}")
    print(f"{'Fake News Confidence':<30} {easy_metrics['fake_confidence']:.3f}{' ':<16} {hard_metrics['fake_confidence']:.3f}{' ':<16} {hard_metrics['fake_confidence']-easy_metrics['fake_confidence']:+.3f}")
    
    print("\n" + "="*80)
    print("KNOWLEDGE BASE PATTERNS")
    print("="*80)
    
    print(f"\n{'Metric':<30} {'EASY':<20} {'HARD':<20} {'Difference':<20}")
    print("-" * 80)
    print(f"{'Real patterns found':<30} {easy_patterns['real_patterns']:<20} {hard_patterns['real_patterns']:<20} {hard_patterns['real_patterns']-easy_patterns['real_patterns']:+20}")
    print(f"{'Fake patterns found':<30} {easy_patterns['fake_patterns']:<20} {hard_patterns['fake_patterns']:<20} {hard_patterns['fake_patterns']-easy_patterns['fake_patterns']:+20}")
    print(f"{'Unique real words':<30} {easy_patterns['real_only_words']:<20} {hard_patterns['real_only_words']:<20} {hard_patterns['real_only_words']-easy_patterns['real_only_words']:+20}")
    print(f"{'Unique fake words':<30} {easy_patterns['fake_only_words']:<20} {hard_patterns['fake_only_words']:<20} {hard_patterns['fake_only_words']-easy_patterns['fake_only_words']:+20}")
    print(f"{'Overlapping words':<30} {easy_patterns['overlap_words']:<20} {hard_patterns['overlap_words']:<20} {hard_patterns['overlap_words']-easy_patterns['overlap_words']:+20}")
    print(f"{'Overlap ratio':<30} {easy_patterns['overlap_ratio']:.3f}{' ':<16} {hard_patterns['overlap_ratio']:.3f}{' ':<16} {hard_patterns['overlap_ratio']-easy_patterns['overlap_ratio']:+.3f}")
    
    # Key insights
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80 + "\n")
    
    print("✓ CNN Performance:")
    if hard_metrics['accuracy'] >= easy_metrics['accuracy']:
        print(f"  • CNN maintains {hard_metrics['accuracy']:.1%} accuracy on hard examples")
    else:
        print(f"  • CNN accuracy drops from {easy_metrics['accuracy']:.1%} to {hard_metrics['accuracy']:.1%}")
    
    if hard_metrics['avg_confidence'] < easy_metrics['avg_confidence']:
        print(f"  • CNN is LESS confident on hard examples ({hard_metrics['avg_confidence']:.3f} vs {easy_metrics['avg_confidence']:.3f})")
        print(f"  • This is GOOD - it shows the examples are more challenging!")
    else:
        print(f"  • CNN confidence similar or higher on hard examples")
    
    print("\n✓ Knowledge Base:")
    if hard_patterns['overlap_ratio'] > easy_patterns['overlap_ratio']:
        print(f"  • HARD examples have MORE pattern overlap ({hard_patterns['overlap_ratio']:.1%} vs {easy_patterns['overlap_ratio']:.1%})")
        print(f"  • Real and fake news use more similar language")
        print(f"  • This makes KB discrimination HARDER but more realistic")
    else:
        print(f"  • Pattern overlap decreased - examples may not be challenging enough")
    
    if hard_patterns['real_patterns'] > easy_patterns['real_patterns']:
        print(f"  • Found MORE patterns in hard examples ({hard_patterns['real_patterns']} vs {easy_patterns['real_patterns']} real)")
        print(f"  • More linguistic diversity in dataset")
    
    # Recommendations
    print("\n✓ Recommendations:")
    if hard_metrics['accuracy'] == 1.0:
        print("  • CNN still achieves 100% - need EVEN HARDER examples!")
        print("  • Try: satire, sophisticated propaganda, context manipulation")
    
    if hard_patterns['overlap_ratio'] > 0.5:
        print("  • High pattern overlap - KB filtering is critical")
        print("  • Focus on unique discriminative patterns only")
    
    if hard_metrics['min_confidence'] > 0.6:
        print(f"  • Lowest confidence is still {hard_metrics['min_confidence']:.1%} - examples not ambiguous enough")
        print("  • Add more borderline cases")
    
    # Show most challenging examples
    print("\n" + "="*80)
    print("MOST CHALLENGING HARD EXAMPLES (lowest CNN confidence)")
    print("="*80 + "\n")
    
    # Get lowest confidence predictions
    hard_real_probs = [(i, p, hard_texts[i]) for i, (p, l) in enumerate(zip(hard_probs, hard_labels)) if l == 1]
    hard_fake_probs = [(i, 1-p, hard_texts[i]) for i, (p, l) in enumerate(zip(hard_probs, hard_labels)) if l == 0]
    
    hard_real_probs.sort(key=lambda x: x[1])
    hard_fake_probs.sort(key=lambda x: x[1])
    
    print("REAL news with lowest confidence:")
    for i, (idx, conf, text) in enumerate(hard_real_probs[:5], 1):
        print(f"{i}. CNN confidence: {conf:.3f}")
        print(f"   {text[:70]}...")
        print()
    
    print("FAKE news with lowest confidence:")
    for i, (idx, conf, text) in enumerate(hard_fake_probs[:5], 1):
        print(f"{i}. CNN confidence: {conf:.3f}")
        print(f"   {text[:70]}...")
        print()
    
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
