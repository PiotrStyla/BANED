#!/usr/bin/env python3
"""
cnn.py - Simple CNN with MC Dropout for text classification
Trains a model and outputs probability predictions
"""
import argparse
import csv
import numpy as np
import sys

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
except ImportError:
    print("[ERROR] PyTorch not installed. Run: pip install torch")
    sys.exit(1)


class TextDataset(Dataset):
    """Simple text dataset."""
    def __init__(self, texts, labels, vocab, max_len=50):
        self.texts = texts
        self.labels = labels
        self.vocab = vocab
        self.max_len = max_len
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # Convert text to indices
        tokens = text.split()[:self.max_len]
        indices = [self.vocab.get(token, 0) for token in tokens]
        
        # Pad
        if len(indices) < self.max_len:
            indices += [0] * (self.max_len - len(indices))
        
        return torch.tensor(indices, dtype=torch.long), torch.tensor(label, dtype=torch.float32)


class SimpleCNN(nn.Module):
    """Simple CNN with dropout for text classification."""
    def __init__(self, vocab_size, embed_dim=64, num_filters=100, dropout_p=0.5):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.conv1 = nn.Conv1d(embed_dim, num_filters, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(embed_dim, num_filters, kernel_size=4, padding=2)
        self.conv3 = nn.Conv1d(embed_dim, num_filters, kernel_size=5, padding=2)
        self.dropout = nn.Dropout(dropout_p)
        self.fc = nn.Linear(num_filters * 3, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        # x: [batch, seq_len]
        x = self.embedding(x)  # [batch, seq_len, embed_dim]
        x = x.permute(0, 2, 1)  # [batch, embed_dim, seq_len]
        
        # Apply convolutions
        c1 = torch.relu(self.conv1(x))
        c2 = torch.relu(self.conv2(x))
        c3 = torch.relu(self.conv3(x))
        
        # Max pooling
        c1 = torch.max(c1, dim=2)[0]
        c2 = torch.max(c2, dim=2)[0]
        c3 = torch.max(c3, dim=2)[0]
        
        # Concatenate
        out = torch.cat([c1, c2, c3], dim=1)
        out = self.dropout(out)
        out = self.fc(out)
        out = self.sigmoid(out)
        
        return out.squeeze()


def build_vocab(texts, min_freq=1):
    """Build vocabulary from texts."""
    word_counts = {}
    for text in texts:
        for word in text.split():
            word_counts[word] = word_counts.get(word, 0) + 1
    
    vocab = {'<PAD>': 0, '<UNK>': 1}
    for word, count in word_counts.items():
        if count >= min_freq:
            vocab[word] = len(vocab)
    
    return vocab


def mc_dropout_predict(model, dataloader, mc_samples=20, device='cpu'):
    """Perform MC Dropout inference."""
    model.train()  # Keep dropout active
    all_predictions = []
    
    with torch.no_grad():
        for _ in range(mc_samples):
            batch_preds = []
            for inputs, _ in dataloader:
                inputs = inputs.to(device)
                outputs = model(inputs)
                batch_preds.append(outputs.cpu().numpy())
            all_predictions.append(np.concatenate(batch_preds))
    
    # Average predictions
    predictions = np.mean(all_predictions, axis=0)
    return predictions


def main():
    parser = argparse.ArgumentParser(description='Train CNN with MC Dropout')
    parser.add_argument('-r', '--real', required=True, help='Real news CSV')
    parser.add_argument('-f', '--fake', required=True, help='Fake news CSV')
    parser.add_argument('--dropout_p', type=float, default=0.5, help='Dropout probability')
    parser.add_argument('--mc_samples', type=int, default=20, help='MC samples for inference')
    parser.add_argument('--out_probs', default='fnn_all_clean_cnn_prob.npy', help='Output probabilities file')
    parser.add_argument('--epochs', type=int, default=5, help='Training epochs')
    parser.add_argument('--batch_size', type=int, default=8, help='Batch size')
    parser.add_argument('--test_split', type=float, default=0.0, help='Test set ratio (0.0-0.5)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    print("[INFO] Loading data...")
    
    # Load real news (label=1)
    real_texts = []
    with open(args.real, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('text'):
                real_texts.append(row['text'])
    
    # Load fake news (label=0)
    fake_texts = []
    with open(args.fake, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('text'):
                fake_texts.append(row['text'])
    
    # Combine
    all_texts = real_texts + fake_texts
    all_labels = [1.0] * len(real_texts) + [0.0] * len(fake_texts)
    
    print(f"[INFO] Total samples: {len(all_texts)} (Real: {len(real_texts)}, Fake: {len(fake_texts)})")
    
    # Train/Test split if requested
    if args.test_split > 0:
        np.random.seed(args.seed)
        indices = np.random.permutation(len(all_texts))
        test_size = int(len(all_texts) * args.test_split)
        test_indices = indices[:test_size]
        train_indices = indices[test_size:]
        
        train_texts = [all_texts[i] for i in train_indices]
        train_labels = [all_labels[i] for i in train_indices]
        test_texts = [all_texts[i] for i in test_indices]
        test_labels = [all_labels[i] for i in test_indices]
        
        print(f"[INFO] Train/Test split: {len(train_texts)}/{len(test_texts)} ({(1-args.test_split)*100:.0f}%/{args.test_split*100:.0f}%)")
    else:
        train_texts = all_texts
        train_labels = all_labels
        test_texts = all_texts
        test_labels = all_labels
        print(f"[INFO] No train/test split - using all data for both")
    
    # Build vocabulary from training data only
    print("[INFO] Building vocabulary...")
    vocab = build_vocab(train_texts)
    print(f"[INFO] Vocabulary size: {len(vocab)}")
    
    # Create datasets
    train_dataset = TextDataset(train_texts, train_labels, vocab)
    train_dataloader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    
    # Full dataset for final predictions (in original order)
    full_dataset = TextDataset(all_texts, all_labels, vocab)
    full_dataloader = DataLoader(full_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Test dataset
    if args.test_split > 0:
        test_dataset = TextDataset(test_texts, test_labels, vocab)
        test_dataloader_eval = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"[INFO] Using device: {device}")
    
    model = SimpleCNN(len(vocab), dropout_p=args.dropout_p).to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Train
    print(f"[INFO] Training for {args.epochs} epochs...")
    for epoch in range(args.epochs):
        model.train()
        total_loss = 0
        correct = 0
        total = 0
        
        for inputs, labels in train_dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            predictions = (outputs > 0.5).float()
            correct += (predictions == labels).sum().item()
            total += labels.size(0)
        
        train_accuracy = correct / total
        
        # Evaluate on test set if available
        if args.test_split > 0:
            model.eval()
            test_correct = 0
            test_total = 0
            with torch.no_grad():
                for inputs, labels in test_dataloader_eval:
                    inputs, labels = inputs.to(device), labels.to(device)
                    outputs = model(inputs)
                    predictions = (outputs > 0.5).float()
                    test_correct += (predictions == labels).sum().item()
                    test_total += labels.size(0)
            test_accuracy = test_correct / test_total
            print(f"  Epoch {epoch+1}/{args.epochs} - Loss: {total_loss:.4f}, Train Acc: {train_accuracy:.4f}, Test Acc: {test_accuracy:.4f}")
        else:
            print(f"  Epoch {epoch+1}/{args.epochs} - Loss: {total_loss:.4f}, Accuracy: {train_accuracy:.4f}")
    
    # MC Dropout inference on full dataset (in original order)
    print(f"[INFO] Running MC Dropout inference ({args.mc_samples} samples)...")
    predictions = mc_dropout_predict(model, full_dataloader, args.mc_samples, device)
    
    # Save predictions
    np.save(args.out_probs, predictions)
    print(f"[INFO] Saved predictions to: {args.out_probs}")
    print(f"[INFO] Predictions shape: {predictions.shape}")
    print(f"[INFO] Sample predictions (first 5): {predictions[:5]}")
    
    # Final accuracy report
    if args.test_split > 0:
        print(f"\n[INFO] Final Test Set Performance:")
        test_preds_mc = mc_dropout_predict(model, test_dataloader_eval, args.mc_samples, device)
        test_preds_binary = (test_preds_mc > 0.5).astype(int)
        test_labels_array = np.array(test_labels)
        test_acc_final = np.mean(test_preds_binary == test_labels_array)
        print(f"  Test Accuracy (MC Dropout): {test_acc_final:.4f} ({int(test_acc_final*len(test_labels))}/{len(test_labels)})")


if __name__ == '__main__':
    main()
