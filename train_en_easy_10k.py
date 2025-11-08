#!/usr/bin/env python3
"""
Train English Easy 10K Model
Clear distinction between real and fake news
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from collections import Counter
import csv

from cnn import SimpleCNN
from apriori_algo import apriori_algorithm

print("="*80)
print("ENGLISH EASY 10K TRAINING")
print("="*80)

# STEP 1: Load Data
print("\n[STEP 1/7] Loading English Easy 10K dataset...")

real_df = pd.read_csv('fnn_real_1k.csv')
fake_df = pd.read_csv('fnn_fake_1k.csv')

print(f"  ✓ Loaded {len(real_df)} REAL examples")
print(f"  ✓ Loaded {len(fake_df)} FAKE examples")

real_df['label'] = 1
fake_df['label'] = 0

df = pd.concat([real_df, fake_df], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('fnn_en_easy_10k_all.csv', index=False, encoding='utf-8')
print(f"  ✓ Combined: {len(df)} total examples")

# STEP 2: Clean Data
print("\n[STEP 2/7] Cleaning text data...")

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    text = ' '.join(text.split())
    text = text.lower()
    return text

df['text'] = df['text'].apply(clean_text)
df = df[df['text'].str.len() > 10].reset_index(drop=True)

print(f"  ✓ Cleaned {len(df)} examples")
print(f"  ✓ Real: {sum(df['label'] == 1)}, Fake: {sum(df['label'] == 0)}")

df.to_csv('fnn_en_easy_10k_clean.csv', index=False, encoding='utf-8')

# STEP 3: Extract KB Patterns
print("\n[STEP 3/7] Extracting Knowledge Base patterns...")

real_texts = df[df['label'] == 1]['text'].tolist()
fake_texts = df[df['label'] == 0]['text'].tolist()

print(f"  → Running Apriori on {len(real_texts)} REAL texts...")
real_patterns = apriori_algorithm(
    real_texts,
    min_support=0.1,
    max_length=3,
    output_file='real_easy_10k_support.csv'
)

print(f"  → Running Apriori on {len(fake_texts)} FAKE texts...")
fake_patterns = apriori_algorithm(
    fake_texts,
    min_support=0.1,
    max_length=3,
    output_file='fake_easy_10k_support.csv'
)

print(f"\n  ✓ REAL patterns: {len(real_patterns)}")
print(f"  ✓ FAKE patterns: {len(fake_patterns)}")

print("\n  Top 10 REAL patterns:")
for i, (pattern, support) in enumerate(list(real_patterns.items())[:10], 1):
    print(f"    {i}. '{pattern}' (support: {support:.4f})")

print("\n  Top 10 FAKE patterns:")
for i, (pattern, support) in enumerate(list(fake_patterns.items())[:10], 1):
    print(f"    {i}. '{pattern}' (support: {support:.4f})")

# STEP 4: Prepare Data for CNN
print("\n[STEP 4/7] Preparing data for CNN...")

def tokenize(text):
    return text.lower().split()

all_words = []
for text in df['text']:
    all_words.extend(tokenize(text))

word_counts = Counter(all_words)
vocab = {word: idx + 1 for idx, (word, _) in enumerate(word_counts.most_common(5000))}
vocab['<PAD>'] = 0
vocab_size = len(vocab)

print(f"  ✓ Vocabulary size: {vocab_size}")

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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"  ✓ Train: {len(X_train)} samples")
print(f"  ✓ Test:  {len(X_test)} samples")

X_train_t = torch.LongTensor(X_train)
y_train_t = torch.FloatTensor(y_train)
X_test_t = torch.LongTensor(X_test)
y_test_t = torch.FloatTensor(y_test)

# STEP 5: Train CNN
print("\n[STEP 5/7] Training CNN with MC Dropout...")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"  → Using device: {device}")

model = SimpleCNN(vocab_size=vocab_size, embed_dim=64, num_filters=100, dropout_p=0.5)
model = model.to(device)

criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

batch_size = 32
epochs = 20

print(f"  → Epochs: {epochs}, Batch size: {batch_size}")

best_loss = float('inf')
for epoch in range(epochs):
    model.train()
    total_loss = 0
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
    
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_t.to(device))
        test_loss = criterion(test_outputs, y_test_t.to(device))
        test_preds = (test_outputs.cpu().numpy() > 0.5).astype(int)
        test_acc = accuracy_score(y_test, test_preds)
    
    print(f"  Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f} - Test Loss: {test_loss:.4f} - Test Acc: {test_acc:.4f}")
    
    if avg_loss < best_loss:
        best_loss = avg_loss
        torch.save(model.state_dict(), 'english_easy_10k_best_model.pth')

print(f"\n  ✓ Best loss: {best_loss:.4f}")

# STEP 6: MC Dropout Predictions
print("\n[STEP 6/7] Generating MC Dropout predictions...")

model.eval()
for module in model.modules():
    if isinstance(module, nn.Dropout):
        module.train()

all_predictions = []
for _ in range(50):
    with torch.no_grad():
        preds = model(X_test_t.to(device)).cpu().numpy()
        all_predictions.append(preds)

all_predictions = np.array(all_predictions)
mean_predictions = all_predictions.mean(axis=0)
std_predictions = all_predictions.std(axis=0)

np.save('fnn_en_easy_10k_cnn_prob.npy', mean_predictions)
print(f"  ✓ Saved predictions")

# STEP 7: Evaluate
print("\n[STEP 7/7] Evaluating performance...")

final_preds = (mean_predictions > 0.5).astype(int)
accuracy = accuracy_score(y_test, final_preds)
precision, recall, f1, _ = precision_recall_fscore_support(y_test, final_preds, average='binary')
cm = confusion_matrix(y_test, final_preds)

print(f"\n{'='*80}")
print("FINAL RESULTS - ENGLISH EASY 10K")
print(f"{'='*80}")
print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"\nConfusion Matrix:")
print(f"  TN: {cm[0,0]}  FP: {cm[0,1]}")
print(f"  FN: {cm[1,0]}  TP: {cm[1,1]}")
print(f"\nFinal Loss: {best_loss:.4f}")
print(f"Uncertainty: {std_predictions.mean():.4f}")
print(f"{'='*80}\n")

report = f"""# ENGLISH EASY 10K TRAINING REPORT
{'='*80}

## Dataset
- Total: {len(df)}
- Real: {sum(df['label'] == 1)}
- Fake: {sum(df['label'] == 0)}
- Difficulty: EASY

## Results
- **Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)**
- Precision: {precision:.4f}
- Recall: {recall:.4f}
- F1-Score: {f1:.4f}
- Loss: {best_loss:.4f}

## Confusion Matrix
```
TN: {cm[0,0]}  FP: {cm[0,1]}
FN: {cm[1,0]}  TP: {cm[1,1]}
```

## Knowledge Base
- Real patterns: {len(real_patterns)}
- Fake patterns: {len(fake_patterns)}
- Vocabulary: {vocab_size}

{'='*80}
"""

with open('ENGLISH_EASY_10K_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ Report saved: ENGLISH_EASY_10K_REPORT.md")
print(f"\n🎉 English Easy 10K training completed!\n")