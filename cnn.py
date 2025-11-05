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
    
    # Build vocabulary
    print("[INFO] Building vocabulary...")
    vocab = build_vocab(all_texts)
    print(f"[INFO] Vocabulary size: {len(vocab)}")
    
    # Create dataset
    dataset = TextDataset(all_texts, all_labels, vocab)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
    
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
        
        for inputs, labels in dataloader:
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
        
        accuracy = correct / total
        print(f"  Epoch {epoch+1}/{args.epochs} - Loss: {total_loss:.4f}, Accuracy: {accuracy:.4f}")
    
    # MC Dropout inference
    print(f"[INFO] Running MC Dropout inference ({args.mc_samples} samples)...")
    test_dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)
    predictions = mc_dropout_predict(model, test_dataloader, args.mc_samples, device)
    
    # Save predictions
    np.save(args.out_probs, predictions)
    print(f"[INFO] Saved predictions to: {args.out_probs}")
    print(f"[INFO] Predictions shape: {predictions.shape}")
    print(f"[INFO] Sample predictions (first 5): {predictions[:5]}")


if __name__ == '__main__':
    main()
