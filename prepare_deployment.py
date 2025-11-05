#!/usr/bin/env python3
"""
prepare_deployment.py - Prepare trained model for API deployment
Extracts vocabulary and copies model/KB files to deployment directories
"""
import os
import shutil
import torch
import csv

def create_directories():
    """Create necessary directories"""
    os.makedirs('models', exist_ok=True)
    os.makedirs('kb', exist_ok=True)
    print("[INFO] Created deployment directories")

def extract_vocabulary_from_dataset(dataset_path='fnn_all_10k_clean.csv'):
    """Extract vocabulary from cleaned dataset"""
    print(f"[INFO] Extracting vocabulary from {dataset_path}...")
    
    words = set()
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('text'):
                    words.update(row['text'].split())
        
        # Sort by frequency if possible, otherwise alphabetically
        vocab = {word: idx for idx, word in enumerate(sorted(words))}
        
        # Save vocabulary
        with open('models/vocab.txt', 'w', encoding='utf-8') as f:
            for word in sorted(vocab.keys(), key=lambda w: vocab[w]):
                f.write(f"{word}\n")
        
        print(f"[INFO] Saved vocabulary: {len(vocab)} words -> models/vocab.txt")
        return len(vocab)
    except FileNotFoundError:
        print(f"[WARN] Dataset not found: {dataset_path}")
        return 0

def copy_kb_patterns():
    """Copy knowledge base patterns"""
    print("[INFO] Copying knowledge base patterns...")
    
    # Try different KB files
    kb_files = [
        ('real_10k_support.csv', 'kb/real_patterns.csv'),
        ('fake_10k_support.csv', 'kb/fake_patterns.csv'),
        ('real_support.csv', 'kb/real_patterns.csv'),
        ('fake_support.csv', 'kb/fake_patterns.csv'),
    ]
    
    copied = 0
    for src, dst in kb_files:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✓ {src} -> {dst}")
            copied += 1
    
    if copied == 0:
        print("  [WARN] No KB files found. API will work with CNN only.")
    
    return copied > 0

def create_example_model_loader():
    """Create a script to save model during training"""
    script = """
# Add this to your cnn.py training script:

# After training completes, add:
print("[INFO] Saving model for deployment...")
torch.save(model.state_dict(), 'models/model.pth')
print("[INFO] Model saved to models/model.pth")

# Save vocabulary
with open('models/vocab.txt', 'w', encoding='utf-8') as f:
    for word in sorted(vocab.keys(), key=lambda w: vocab[w]):
        f.write(f"{word}\\n")
print("[INFO] Vocabulary saved to models/vocab.txt")
"""
    
    with open('save_model_snippet.txt', 'w') as f:
        f.write(script)
    
    print("[INFO] Created save_model_snippet.txt with code to save model during training")

def check_model_exists():
    """Check if model weights exist"""
    if os.path.exists('models/model.pth'):
        print("[INFO] ✓ Model weights found: models/model.pth")
        return True
    else:
        print("[WARN] ✗ Model weights not found: models/model.pth")
        print("       Run your training script and save the model with:")
        print("       torch.save(model.state_dict(), 'models/model.pth')")
        return False

def main():
    print("=" * 60)
    print("BANED DEPLOYMENT PREPARATION")
    print("=" * 60)
    print()
    
    # Step 1: Create directories
    create_directories()
    print()
    
    # Step 2: Extract vocabulary
    vocab_size = extract_vocabulary_from_dataset()
    print()
    
    # Step 3: Copy KB patterns
    kb_loaded = copy_kb_patterns()
    print()
    
    # Step 4: Check model
    model_exists = check_model_exists()
    print()
    
    # Step 5: Create helper script
    create_example_model_loader()
    print()
    
    # Summary
    print("=" * 60)
    print("DEPLOYMENT STATUS")
    print("=" * 60)
    print(f"Vocabulary:    {'✓' if vocab_size > 0 else '✗'} ({vocab_size} words)")
    print(f"Knowledge Base: {'✓' if kb_loaded else '✗'}")
    print(f"Model Weights:  {'✓' if model_exists else '✗'}")
    print()
    
    if not model_exists:
        print("⚠️  MODEL WEIGHTS REQUIRED!")
        print()
        print("To train and save the model:")
        print("  1. Run: python cnn.py -r fnn_real_10k_clean.csv -f fnn_fake_10k_clean.csv")
        print("  2. After training, add to cnn.py:")
        print("     torch.save(model.state_dict(), 'models/model.pth')")
        print("  3. Or use an existing trained model")
        print()
    
    if vocab_size > 0 and model_exists:
        print("✅ Deployment ready!")
        print()
        print("Next steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Start API: python api.py")
        print("  3. Open web interface: static/index.html")
        print("  4. API docs: http://localhost:8000/docs")
    else:
        print("⚠️  Deployment incomplete - see warnings above")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
