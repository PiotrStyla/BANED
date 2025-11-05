#!/usr/bin/env python3
"""
merge_data.py - Merge real and fake CSV files into combined file with labels
"""
import csv
import sys


def merge_files(real_file, fake_file, output_file):
    """Merge real (label=1) and fake (label=0) CSV files."""
    print(f"[INFO] Merging {real_file} and {fake_file}")
    
    rows = []
    
    # Read real news
    try:
        with open(real_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'text' in row:
                    rows.append({'text': row['text'], 'label': '1'})
    except FileNotFoundError:
        print(f"[ERROR] File not found: {real_file}")
        sys.exit(1)
    
    real_count = len(rows)
    
    # Read fake news
    try:
        with open(fake_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'text' in row:
                    rows.append({'text': row['text'], 'label': '0'})
    except FileNotFoundError:
        print(f"[ERROR] File not found: {fake_file}")
        sys.exit(1)
    
    fake_count = len(rows) - real_count
    
    # Write merged file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'label'])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"[INFO] Merged {real_count} real + {fake_count} fake = {len(rows)} total")
    print(f"[INFO] Output: {output_file}")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python merge_data.py <real_clean.csv> <fake_clean.csv> <output.csv>")
        sys.exit(1)
    
    merge_files(sys.argv[1], sys.argv[2], sys.argv[3])
