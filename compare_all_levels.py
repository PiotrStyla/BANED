#!/usr/bin/env python3
"""
compare_all_levels.py - Compare EASY vs HARD vs EXTREME examples
"""
import csv
import numpy as np


def load_dataset(name, probs_file, csv_file, real_pat_file, fake_pat_file):
    """Load a complete dataset."""
    probs = np.load(probs_file)
    
    texts = []
    labels = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['text'])
            labels.append(int(row['label']))
    
    real_patterns = {}
    fake_patterns = {}
    
    try:
        with open(real_pat_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                real_patterns[row['pattern']] = float(row['support'])
    except:
        pass
    
    try:
        with open(fake_pat_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                fake_patterns[row['pattern']] = float(row['support'])
    except:
        pass
    
    return {
        'name': name,
        'probs': probs,
        'texts': texts,
        'labels': labels,
        'real_patterns': real_patterns,
        'fake_patterns': fake_patterns
    }


def analyze_dataset(dataset):
    """Analyze a dataset."""
    probs = dataset['probs']
    labels = np.array(dataset['labels'])
    
    predictions = (probs > 0.5).astype(int)
    accuracy = np.mean(predictions == labels)
    
    # Confidence metrics
    avg_confidence = np.mean(np.abs(probs - 0.5))
    min_confidence = np.min(np.maximum(probs, 1 - probs))
    max_confidence = np.max(np.maximum(probs, 1 - probs))
    std_confidence = np.std(np.maximum(probs, 1 - probs))
    
    # Per-class
    real_mask = labels == 1
    fake_mask = labels == 0
    
    real_confidence = np.mean(probs[real_mask]) if real_mask.sum() > 0 else 0
    fake_confidence = 1 - np.mean(probs[fake_mask]) if fake_mask.sum() > 0 else 0
    
    # Pattern analysis
    real_words = set()
    for pattern in dataset['real_patterns'].keys():
        real_words.update(pattern.split())
    
    fake_words = set()
    for pattern in dataset['fake_patterns'].keys():
        fake_words.update(pattern.split())
    
    overlap = real_words & fake_words
    overlap_ratio = len(overlap) / max(len(real_words | fake_words), 1)
    
    # Find hardest examples
    real_probs_idx = [(i, probs[i], dataset['texts'][i]) for i in range(len(labels)) if labels[i] == 1]
    fake_probs_idx = [(i, 1-probs[i], dataset['texts'][i]) for i in range(len(labels)) if labels[i] == 0]
    
    real_probs_idx.sort(key=lambda x: x[1])
    fake_probs_idx.sort(key=lambda x: x[1])
    
    return {
        'accuracy': accuracy,
        'avg_confidence': avg_confidence,
        'min_confidence': min_confidence,
        'max_confidence': max_confidence,
        'std_confidence': std_confidence,
        'real_confidence': real_confidence,
        'fake_confidence': fake_confidence,
        'n_samples': len(labels),
        'n_real': real_mask.sum(),
        'n_fake': fake_mask.sum(),
        'n_real_patterns': len(dataset['real_patterns']),
        'n_fake_patterns': len(dataset['fake_patterns']),
        'n_real_words': len(real_words),
        'n_fake_words': len(fake_words),
        'n_overlap': len(overlap),
        'overlap_ratio': overlap_ratio,
        'hardest_real': real_probs_idx[:3],
        'hardest_fake': fake_probs_idx[:3]
    }


def print_comparison(datasets, analyses):
    """Print detailed comparison."""
    print("\n" + "="*100)
    print("COMPREHENSIVE COMPARISON: EASY vs HARD vs EXTREME")
    print("="*100 + "\n")
    
    # Dataset sizes
    print("="*100)
    print("DATASET STATISTICS")
    print("="*100)
    print(f"\n{'Metric':<35} {'EASY':<20} {'HARD':<20} {'EXTREME':<20}")
    print("-" * 100)
    
    metrics = ['n_samples', 'n_real', 'n_fake']
    labels = ['Total samples', 'Real news', 'Fake news']
    
    for metric, label in zip(metrics, labels):
        print(f"{label:<35} {analyses[0][metric]:<20} {analyses[1][metric]:<20} {analyses[2][metric]:<20}")
    
    # CNN Performance
    print("\n" + "="*100)
    print("CNN PERFORMANCE")
    print("="*100)
    print(f"\n{'Metric':<35} {'EASY':<20} {'HARD':<20} {'EXTREME':<20}")
    print("-" * 100)
    
    metrics = ['accuracy', 'avg_confidence', 'min_confidence', 'max_confidence', 'std_confidence', 
               'real_confidence', 'fake_confidence']
    labels = ['Accuracy', 'Avg Confidence', 'Min Confidence', 'Max Confidence', 'Std Confidence',
              'Real Confidence', 'Fake Confidence']
    
    for metric, label in zip(metrics, labels):
        e_val = analyses[0][metric]
        h_val = analyses[1][metric]
        x_val = analyses[2][metric]
        print(f"{label:<35} {e_val:.3f}{' ':<16} {h_val:.3f}{' ':<16} {x_val:.3f}")
    
    # Knowledge Base
    print("\n" + "="*100)
    print("KNOWLEDGE BASE PATTERNS")
    print("="*100)
    print(f"\n{'Metric':<35} {'EASY':<20} {'HARD':<20} {'EXTREME':<20}")
    print("-" * 100)
    
    metrics = ['n_real_patterns', 'n_fake_patterns', 'n_real_words', 'n_fake_words', 
               'n_overlap', 'overlap_ratio']
    labels = ['Real patterns', 'Fake patterns', 'Unique real words', 'Unique fake words',
              'Overlapping words', 'Overlap ratio']
    
    for metric, label in zip(metrics, labels):
        e_val = analyses[0][metric]
        h_val = analyses[1][metric]
        x_val = analyses[2][metric]
        if 'ratio' in metric:
            print(f"{label:<35} {e_val:.3f}{' ':<16} {h_val:.3f}{' ':<16} {x_val:.3f}")
        else:
            print(f"{label:<35} {e_val:<20} {h_val:<20} {x_val:<20}")
    
    # Hardest examples from each level
    print("\n" + "="*100)
    print("MOST CHALLENGING EXAMPLES (lowest CNN confidence)")
    print("="*100)
    
    for dataset, analysis in zip(datasets, analyses):
        print(f"\n{dataset['name'].upper()} Dataset:")
        print("-" * 100)
        print("\nReal news (3 hardest):")
        for i, (idx, conf, text) in enumerate(analysis['hardest_real'], 1):
            print(f"  {i}. Confidence: {conf:.3f} - {text[:70]}...")
        
        print("\nFake news (3 hardest):")
        for i, (idx, conf, text) in enumerate(analysis['hardest_fake'], 1):
            print(f"  {i}. Confidence: {conf:.3f} - {text[:70]}...")
    
    # Key insights
    print("\n" + "="*100)
    print("KEY INSIGHTS & CONCLUSIONS")
    print("="*100 + "\n")
    
    print("1. CNN PERFORMANCE TREND:")
    print(f"   • Accuracy: {analyses[0]['accuracy']:.1%} (easy) → {analyses[1]['accuracy']:.1%} (hard) → {analyses[2]['accuracy']:.1%} (extreme)")
    
    if analyses[2]['min_confidence'] > 0.85:
        print(f"   • PROBLEM: Even hardest example has {analyses[2]['min_confidence']:.1%} confidence!")
        print("   • CNN is TOO CONFIDENT - needs truly ambiguous cases")
    else:
        print(f"   • Min confidence dropped to {analyses[2]['min_confidence']:.1%} ✓")
    
    print(f"\n2. CONFIDENCE DISTRIBUTION:")
    print(f"   • Avg confidence: {analyses[0]['avg_confidence']:.3f} → {analyses[1]['avg_confidence']:.3f} → {analyses[2]['avg_confidence']:.3f}")
    print(f"   • Std confidence: {analyses[0]['std_confidence']:.3f} → {analyses[1]['std_confidence']:.3f} → {analyses[2]['std_confidence']:.3f}")
    
    if analyses[2]['std_confidence'] < 0.05:
        print("   • Low std = CNN very consistent (good or bad depending on accuracy)")
    
    print(f"\n3. KNOWLEDGE BASE COMPLEXITY:")
    print(f"   • Pattern overlap: {analyses[0]['overlap_ratio']:.1%} → {analyses[1]['overlap_ratio']:.1%} → {analyses[2]['overlap_ratio']:.1%}")
    
    if analyses[2]['overlap_ratio'] > analyses[1]['overlap_ratio']:
        print("   • EXTREME has MORE overlap = more realistic!")
    
    total_patterns = [a['n_real_patterns'] + a['n_fake_patterns'] for a in analyses]
    print(f"   • Total patterns: {total_patterns[0]} → {total_patterns[1]} → {total_patterns[2]}")
    
    print(f"\n4. RECOMMENDATIONS:")
    if all(a['accuracy'] == 1.0 for a in analyses):
        print("   ⚠️  CNN achieves 100% on ALL levels - model may be overfitting")
        print("   → Try: Larger test set, cross-validation, or truly adversarial examples")
    
    if analyses[2]['min_confidence'] > 0.9:
        print("   ⚠️  Lowest confidence still >90% - need TRULY ambiguous cases")
        print("   → Try: Real satire vs fake satire, propaganda with facts, deep fakes")
    
    if analyses[2]['overlap_ratio'] < 0.5:
        print("   ℹ️  Pattern overlap <50% - languages still quite distinct")
        print("   → KB can still provide useful signal for disambiguation")
    
    print("\n" + "="*100 + "\n")


def main():
    print("Loading datasets...")
    
    datasets = [
        load_dataset('EASY', 'fnn_all_clean_cnn_prob.npy', 'fnn_all_clean.csv',
                    'real_support.csv', 'fake_support.csv'),
        load_dataset('HARD', 'fnn_all_hard_cnn_prob.npy', 'fnn_all_hard_clean.csv',
                    'real_hard_support.csv', 'fake_hard_support.csv'),
        load_dataset('EXTREME', 'fnn_all_extreme_cnn_prob.npy', 'fnn_all_extreme_clean.csv',
                    'real_extreme_support.csv', 'fake_extreme_support.csv')
    ]
    
    print("Analyzing...")
    analyses = [analyze_dataset(d) for d in datasets]
    
    print_comparison(datasets, analyses)




if __name__ == '__main__':
    main()
