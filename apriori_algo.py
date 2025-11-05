#!/usr/bin/env python3
"""
apriori_algo.py - Knowledge Base generation using Apriori algorithm
Finds frequent word patterns in text data
"""
import argparse
import csv
import sys
from collections import defaultdict, Counter
from itertools import combinations


def tokenize(text):
    """Split text into words."""
    return text.lower().split()


def get_itemsets(transactions, min_support_count):
    """Generate frequent itemsets using Apriori algorithm."""
    # Count individual items
    item_counts = Counter()
    for transaction in transactions:
        for item in set(transaction):
            item_counts[item] += 1
    
    # Filter by minimum support
    frequent_1_itemsets = {
        frozenset([item]): count 
        for item, count in item_counts.items() 
        if count >= min_support_count
    }
    
    if not frequent_1_itemsets:
        return {}
    
    all_frequent = dict(frequent_1_itemsets)
    current_itemsets = frequent_1_itemsets
    k = 2
    
    # Generate k-itemsets
    while current_itemsets and k <= 3:  # Limit to 3-itemsets for speed
        # Generate candidates
        candidates = set()
        items = list(current_itemsets.keys())
        
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                union = items[i] | items[j]
                if len(union) == k:
                    candidates.add(union)
        
        # Count candidates
        candidate_counts = defaultdict(int)
        for transaction in transactions:
            transaction_set = set(transaction)
            for candidate in candidates:
                if candidate.issubset(transaction_set):
                    candidate_counts[candidate] += 1
        
        # Filter by support
        current_itemsets = {
            itemset: count 
            for itemset, count in candidate_counts.items() 
            if count >= min_support_count
        }
        
        all_frequent.update(current_itemsets)
        k += 1
    
    return all_frequent


def process_file(input_file, min_support, output_file):
    """Process CSV and generate frequent itemsets."""
    print(f"[INFO] Reading from: {input_file}")
    print(f"[INFO] Minimum support: {min_support}")
    
    try:
        # Read transactions
        transactions = []
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'text' in row and row['text']:
                    tokens = tokenize(row['text'])
                    if tokens:
                        transactions.append(tokens)
        
        if not transactions:
            print("[WARN] No transactions found")
            return
        
        total_transactions = len(transactions)
        min_support_count = int(min_support * total_transactions)
        
        print(f"[INFO] Total transactions: {total_transactions}")
        print(f"[INFO] Minimum support count: {min_support_count}")
        
        # Run Apriori
        frequent_itemsets = get_itemsets(transactions, min_support_count)
        
        # Calculate support values and sort
        results = []
        for itemset, count in frequent_itemsets.items():
            support = count / total_transactions
            pattern = ' '.join(sorted(itemset))
            results.append({
                'pattern': pattern,
                'support': support,
                'count': count
            })
        
        # Sort by support descending
        results.sort(key=lambda x: x['support'], reverse=True)
        
        # Write output
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['pattern', 'support', 'count'])
            writer.writeheader()
            writer.writerows(results)
        
        print(f"[INFO] Found {len(results)} frequent patterns")
        print(f"[INFO] Output written to: {output_file}")
        
        # Show top 5
        if results:
            print("\n[INFO] Top 5 patterns:")
            for i, result in enumerate(results[:5], 1):
                print(f"  {i}. '{result['pattern']}' (support: {result['support']:.3f})")
    
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Generate knowledge base using Apriori')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('--min_support', type=float, default=0.3, help='Minimum support (0-1)')
    parser.add_argument('--out', '--output', dest='output', required=True, help='Output CSV file')
    
    args = parser.parse_args()
    
    if args.min_support <= 0 or args.min_support > 1:
        print("[ERROR] min_support must be between 0 and 1")
        sys.exit(1)
    
    process_file(args.input, args.min_support, args.output)


if __name__ == '__main__':
    main()
