# POLISH EXTREME 10K TRAINING REPORT
================================================================================

## Dataset
- Total samples: 10000
- Real: 5000
- Fake: 5000
- Train/Test split: 80/20

## Knowledge Base
- Real patterns: 18
- Fake patterns: 11
- Min support: 0.1 (10%)

## Model Architecture
- Type: SimpleCNN with MC Dropout
- Vocabulary: 288 words
- Embedding dim: 64
- Filters: 100
- Dropout: 0.5

## Training
- Epochs: 20
- Batch size: 32
- Optimizer: Adam (lr=0.001)
- Best loss: 0.0000

## Results
- **Accuracy: 1.0000 (100.00%)**
- Precision: 1.0000
- Recall: 1.0000
- F1-Score: 1.0000

## Confusion Matrix
```
TN: 1000  FP: 0
FN: 0  TP: 1000
```

## MC Dropout (50 samples)
- Mean uncertainty: 0.0000
- Max uncertainty: 0.0004

================================================================================
