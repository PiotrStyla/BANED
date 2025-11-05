#!/usr/bin/env python3
"""
analyze_patterns.py - Detailed analysis of Knowledge Base patterns
Shows which texts match which patterns
"""
import csv
import sys


def load_patterns(pattern_file):
    """Load patterns from CSV."""
    patterns = []
    with open(pattern_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            patterns.append({
                'pattern': row['pattern'],
                'support': float(row['support']),
                'count': int(row['count'])
            })
    return patterns


def load_texts(text_file):
    """Load texts from CSV."""
    texts = []
    with open(text_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'text' in row:
                texts.append(row['text'])
    return texts


def find_matches(texts, pattern):
    """Find texts that match the pattern."""
    pattern_words = set(pattern.split())
    matches = []
    
    for idx, text in enumerate(texts):
        text_words = set(text.lower().split())
        if pattern_words.issubset(text_words):
            matches.append((idx, text))
    
    return matches


def analyze_class(class_name, text_file, pattern_file):
    """Analyze patterns for a class."""
    print(f"\n{'='*80}")
    print(f"{class_name.upper()} NEWS - KNOWLEDGE BASE PATTERNS")
    print(f"{'='*80}\n")
    
    texts = load_texts(text_file)
    patterns = load_patterns(pattern_file)
    
    print(f"Total texts: {len(texts)}")
    print(f"Total patterns found: {len(patterns)}\n")
    
    for i, pattern_info in enumerate(patterns[:15], 1):  # Show top 15
        pattern = pattern_info['pattern']
        support = pattern_info['support']
        count = pattern_info['count']
        
        print(f"{i}. Pattern: '{pattern}'")
        print(f"   Support: {support:.3f} ({count}/{len(texts)} texts)")
        
        # Find example matches
        matches = find_matches(texts, pattern)
        print(f"   Example matches:")
        for match_idx, match_text in matches[:3]:
            print(f"      [{match_idx+1}] {match_text[:70]}...")
        
        if len(matches) > 3:
            print(f"      ... and {len(matches)-3} more")
        print()


def main():
    print("\n" + "="*80)
    print("BANED KNOWLEDGE BASE - DETAILED PATTERN ANALYSIS")
    print("="*80)
    
    analyze_class("REAL", "fnn_real_clean.csv", "real_support.csv")
    analyze_class("FAKE", "fnn_fake_clean.csv", "fake_support.csv")
    
    # Comparison
    print(f"\n{'='*80}")
    print("KEY INSIGHTS")
    print(f"{'='*80}\n")
    
    real_patterns = load_patterns("real_support.csv")
    fake_patterns = load_patterns("fake_support.csv")
    
    print(f"✓ Real news patterns ({len(real_patterns)}):")
    for p in real_patterns[:10]:
        print(f"   - '{p['pattern']}' ({p['support']:.1%})")
    
    print(f"\n✓ Fake news patterns ({len(fake_patterns)}):")
    for p in fake_patterns[:10]:
        print(f"   - '{p['pattern']}' ({p['support']:.1%})")
    
    # Find distinctive patterns
    real_words = set()
    for p in real_patterns:
        real_words.update(p['pattern'].split())
    
    fake_words = set()
    for p in fake_patterns:
        fake_words.update(p['pattern'].split())
    
    only_real = real_words - fake_words
    only_fake = fake_words - real_words
    shared = real_words & fake_words
    
    print(f"\n✓ Distinctive to REAL news: {', '.join(sorted(only_real))}")
    print(f"✓ Distinctive to FAKE news: {', '.join(sorted(only_fake))}")
    print(f"✓ Shared words: {', '.join(sorted(shared))}")
    
    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()
