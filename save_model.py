#!/usr/bin/env python3
"""
save_model.py - Save trained model and vocabulary for API deployment
"""
import torch
import csv
import os
import argparse

def save_model_for_api(model_path, vocab_dict, output_dir='models'):
    """Save model and vocabulary for API"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save vocabulary
    vocab_file = os.path.join(output_dir, 'vocab.txt')
    with open(vocab_file, 'w', encoding='utf-8') as f:
        for word in sorted(vocab_dict.keys(), key=lambda w: vocab_dict[w]):
            f.write(f"{word}\n")
    
    print(f"[INFO] Saved vocabulary: {len(vocab_dict)} words -> {vocab_file}")
    
    # Note: Model weights should be saved during training
    print(f"[INFO] Place model weights at: {output_dir}/model.pth")
    print("[INFO] Use torch.save(model.state_dict(), 'models/model.pth') during training")

def save_kb_patterns(real_patterns_csv, fake_patterns_csv, output_dir='kb'):
    """Copy KB patterns for API"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy real patterns
    if os.path.exists(real_patterns_csv):
        with open(real_patterns_csv, 'r', encoding='utf-8') as fin:
            with open(os.path.join(output_dir, 'real_patterns.csv'), 'w', encoding='utf-8') as fout:
                fout.write(fin.read())
        print(f"[INFO] Saved real patterns -> {output_dir}/real_patterns.csv")
    
    # Copy fake patterns
    if os.path.exists(fake_patterns_csv):
        with open(fake_patterns_csv, 'r', encoding='utf-8') as fin:
            with open(os.path.join(output_dir, 'fake_patterns.csv'), 'w', encoding='utf-8') as fout:
                fout.write(fin.read())
        print(f"[INFO] Saved fake patterns -> {output_dir}/fake_patterns.csv")

def main():
    parser = argparse.ArgumentParser(description='Prepare model for API deployment')
    parser.add_argument('--real_support', default='real_10k_support.csv', help='Real patterns CSV')
    parser.add_argument('--fake_support', default='fake_10k_support.csv', help='Fake patterns CSV')
    args = parser.parse_args()
    
    print("[INFO] Preparing model for API deployment...")
    print("[INFO] This script helps organize files for the API")
    print()
    print("Steps:")
    print("1. Train your model and save it with:")
    print("   torch.save(model.state_dict(), 'models/model.pth')")
    print()
    print("2. Save vocabulary during training:")
    print("   Use the save_model_for_api() function with your vocab dict")
    print()
    print("3. Run this script to copy KB patterns:")
    
    # Copy KB patterns
    save_kb_patterns(args.real_support, args.fake_support)
    
    print()
    print("[INFO] Setup complete!")
    print("[INFO] API structure:")
    print("  models/")
    print("    ├── model.pth        ← Model weights (from training)")
    print("    └── vocab.txt        ← Vocabulary (from training)")
    print("  kb/")
    print("    ├── real_patterns.csv ← Real news patterns")
    print("    └── fake_patterns.csv ← Fake news patterns")

if __name__ == '__main__':
    main()
