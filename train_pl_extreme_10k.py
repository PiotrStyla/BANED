#!/usr/bin/env python3
"""
Train Polish Extreme 10K Model
Hardest cases: Satire, Propaganda, Context Manipulation
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from collections import Counter
import csv
import sys

# Import from existing modules
from cnn import SimpleCNN
from apriori_algo import apriori_algorithm

print("="*80)
print("POLISH EXTREME 10K TRAINING - HARDEST CASES")
print("="*80)

# ============================================================================
# STEP 1: Load and Combine Data
# ============================================================================
print("\n[STEP 1/7] Loading Polish Extreme 10K dataset...")

real_df = pd.read_csv('fnn_pl_real_extreme_5000.csv')
fake_df = pd.read_csv('fnn_pl_fake_extreme_5000.csv')

print(f"  ✓ Loaded {len(real_df)} REAL examples")
print(f"  ✓ Loaded {len(fake_df)} FAKE examples")

# Add labels
real_df['label'] = 1
fake_df['label'] = 0

# Combine
df = pd.concat([real_df, fake_df], ignore_index=True)
print(f"  ✓ Combined: {len(df)} total examples")

# Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save combined file
df.to_csv('fnn_pl_extreme_10k_all.csv', index=False, encoding='utf-8')
print(f"  ✓ Saved: fnn_pl_extreme_10k_all.csv")

# ============================================================================
# STEP 2: Clean Data
# ============================================================================
print("\n[STEP 2/7] Cleaning text data...")

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Convert to lowercase for consistency
    text = text.lower()
    return text

df['text'] = df['text'].apply(clean_text)

# Remove empty or very short texts
df = df[df['text'].str.len() > 10].reset_index(drop=True)

print(f"  ✓ Cleaned {len(df)} examples")
print(f"  ✓ Real: {sum(df['label'] == 1)}, Fake: {sum(df['label'] == 0)}")

# Save cleaned data
df.to_csv('fnn_pl_extreme_10k_clean.csv', index=False, encoding='utf-8')
print(f"  ✓ Saved: fnn_pl_extreme_10k_clean.csv")

# ============================================================================
# STEP 3: Extract Knowledge Base with Apriori
# ============================================================================
print("\n[STEP 3/7] Extracting Knowledge Base patterns with Apriori...")

# Split into real and fake
real_texts = df[df['label'] == 1]['text'].tolist()
fake_texts = df[df['label'] == 0]['text'].tolist()

print(f"  → Running Apriori on {len(real_texts)} REAL texts...")
real_patterns = apriori_algorithm(
    real_texts,
    min_support=0.1,  # 10% minimum support
    max_length=3,
    output_file='real_extreme_10k_support.csv'
)

print(f"  → Running Apriori on {len(fake_texts)} FAKE texts...")
fake_patterns = apriori_algorithm(
    fake_texts,
    min_support=0.1,
    max_length=3,
    output_file='fake_extreme_10k_support.csv'
)

print(f"\n  ✓ REAL patterns found: {len(real_patterns)}")
print(f"  ✓ FAKE patterns found: {len(fake_patterns)}")

# Display top patterns
print("\n  Top 10 REAL patterns:")
for i, (pattern, support) in enumerate(list(real_patterns.items())[:10], 1):
    print(f"    {i}. '{pattern}' (support: {support:.4f})")

print("\n  Top 10 FAKE patterns:")
for i, (pattern, support) in enumerate(list(fake_patterns.items())[:10], 1):
    print(f"    {i}. '{pattern}' (support: {support:.4f})")

# ============================================================================
# STEP 4: Prepare Data for CNN
# ============================================================================
print("\n[STEP 4/7] Preparing data for CNN training...")

# Tokenize
def tokenize(text):
    return text.lower().split()

# Build vocabulary
all_words = []
for text in df['text']:
    all_words.extend(tokenize(text))

word_counts = Counter(all_words)
vocab = {word: idx + 1 for idx, (word, _) in enumerate(word_counts.most_common(5000))}
vocab['<PAD>'] = 0
vocab_size = len(vocab)

print(f"  ✓ Vocabulary size: {vocab_size}")

# Convert texts to sequences
def text_to_sequence(text, max_len=100):
    tokens = tokenize(text)
    sequence = [vocab.get(token, 0) for token in tokens]
    if len(sequence) < max_len:
        sequence += [0] * (max_len - len(sequence))
    else:
        sequence = sequence[:max_len]
    return sequence

X = np.array([text_to_sequence(text) for text in df['text']])
y = df['label'].values

print(f"  ✓ Input shape: {X.shape}")
print(f"  ✓ Labels shape: {y.shape}")

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"  ✓ Train: {len(X_train)} samples")
print(f"  ✓ Test:  {len(X_test)} samples")

# Convert to PyTorch tensors
X_train_t = torch.LongTensor(X_train)
y_train_t = torch.FloatTensor(y_train)
X_test_t = torch.LongTensor(X_test)
y_test_t = torch.FloatTensor(y_test)

# ============================================================================
# STEP 5: Train CNN with MC Dropout
# ============================================================================
print("\n[STEP 5/7] Training CNN with MC Dropout...")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"  → Using device: {device}")

model = SimpleCNN(vocab_size=vocab_size, embed_dim=64, num_filters=100, dropout_p=0.5)
model = model.to(device)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training parameters
batch_size = 32
epochs = 20

print(f"  → Batch size: {batch_size}")
print(f"  → Epochs: {epochs}")
print(f"  → Learning rate: 0.001")

# Training loop
best_loss = float('inf')
for epoch in range(epochs):
    model.train()
    total_loss = 0
    
    # Shuffle training data
    indices = torch.randperm(len(X_train_t))
    
    for i in range(0, len(X_train_t), batch_size):
        batch_indices = indices[i:i+batch_size]
        batch_X = X_train_t[batch_indices].to(device)
        batch_y = y_train_t[batch_indices].to(device)
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / (len(X_train_t) / batch_size)
    
    # Evaluate on test set
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_t.to(device))
        test_loss = criterion(test_outputs, y_test_t.to(device))
        test_preds = (test_outputs.cpu().numpy() > 0.5).astype(int)
        test_acc = accuracy_score(y_test, test_preds)
    
    print(f"  Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f} - Test Loss: {test_loss:.4f} - Test Acc: {test_acc:.4f}")
    
    if avg_loss < best_loss:
        best_loss = avg_loss
        torch.save(model.state_dict(), 'polish_extreme_10k_best_model.pth')

print(f"\n  ✓ Best training loss: {best_loss:.4f}")
print(f"  ✓ Model saved: polish_extreme_10k_best_model.pth")

# ============================================================================
# STEP 6: MC Dropout Predictions
# ============================================================================
print("\n[STEP 6/7] Generating MC Dropout predictions...")

model.eval()
mc_samples = 50

# Enable dropout during inference
for module in model.modules():
    if isinstance(module, nn.Dropout):
        module.train()

all_predictions = []
for _ in range(mc_samples):
    with torch.no_grad():
        preds = model(X_test_t.to(device)).cpu().numpy()
        all_predictions.append(preds)

all_predictions = np.array(all_predictions)
mean_predictions = all_predictions.mean(axis=0)
std_predictions = all_predictions.std(axis=0)

# Save predictions
np.save('fnn_pl_extreme_10k_cnn_prob.npy', mean_predictions)
print(f"  ✓ Saved predictions: fnn_pl_extreme_10k_cnn_prob.npy")

# ============================================================================
# STEP 7: Evaluate Performance
# ============================================================================
print("\n[STEP 7/7] Evaluating model performance...")

final_preds = (mean_predictions > 0.5).astype(int)

# Metrics
accuracy = accuracy_score(y_test, final_preds)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, final_preds, average='binary')
cm = confusion_matrix(y_test, final_preds)

print(f"\n{'='*80}")
print("FINAL RESULTS - POLISH EXTREME 10K")
print(f"{'='*80}")
print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"\nConfusion Matrix:")
print(f"  TN: {cm[0,0]}  FP: {cm[0,1]}")
print(f"  FN: {cm[1,0]}  TP: {cm[1,1]}")
print(f"\nFinal Loss: {best_loss:.4f}")
print(f"\nUncertainty Statistics:")
print(f"  Mean std: {std_predictions.mean():.4f}")
print(f"  Max std:  {std_predictions.max():.4f}")
print(f"{'='*80}\n")

# Save report
report = f"""# POLISH EXTREME 10K TRAINING REPORT
{'='*80}

## Dataset
- Total samples: {len(df)}
- Real: {sum(df['label'] == 1)}
- Fake: {sum(df['label'] == 0)}
- Train/Test split: 80/20

## Knowledge Base
- Real patterns: {len(real_patterns)}
- Fake patterns: {len(fake_patterns)}
- Min support: 0.1 (10%)

## Model Architecture
- Type: SimpleCNN with MC Dropout
- Vocabulary: {vocab_size} words
- Embedding dim: 64
- Filters: 100
- Dropout: 0.5

## Training
- Epochs: {epochs}
- Batch size: {batch_size}
- Optimizer: Adam (lr=0.001)
- Best loss: {best_loss:.4f}

## Results
- **Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)**
- Precision: {precision:.4f}
- Recall: {recall:.4f}
- F1-Score: {f1:.4f}

## Confusion Matrix
```
TN: {cm[0,0]}  FP: {cm[0,1]}
FN: {cm[1,0]}  TP: {cm[1,1]}
```

## MC Dropout (50 samples)
- Mean uncertainty: {std_predictions.mean():.4f}
- Max uncertainty: {std_predictions.max():.4f}

{'='*80}
"""

with open('POLISH_EXTREME_10K_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ Report saved: POLISH_EXTREME_10K_REPORT.md")
print(f"\n🎉 Polish Extreme 10K training completed successfully!\n")