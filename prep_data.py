#!/usr/bin/env python3
"""
prep_data.py - Simple data preprocessing for BANED
Cleans text data by removing special characters, lowercasing, etc.
"""
import argparse
import re
import csv
import sys


def clean_text(text):
    """Clean and normalize text data."""
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def process_file(input_file, output_file):
    """Process CSV file and clean text column."""
    print(f"[INFO] Reading from: {input_file}")
    print(f"[INFO] Writing to: {output_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in)
            
            # Get fieldnames
            fieldnames = reader.fieldnames
            if not fieldnames or 'text' not in fieldnames:
                print("[ERROR] Input file must have a 'text' column")
                sys.exit(1)
            
            rows = []
            for row in reader:
                if 'text' in row:
                    row['text'] = clean_text(row['text'])
                    if row['text']:  # Only keep non-empty rows
                        rows.append(row)
        
        # Write cleaned data
        with open(output_file, 'w', encoding='utf-8', newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"[INFO] Processed {len(rows)} rows successfully")
        
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Preprocess text data for BANED')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    
    args = parser.parse_args()
    
    process_file(args.input, args.output)


if __name__ == '__main__':
    main()
