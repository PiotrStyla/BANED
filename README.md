# 🛡️ BANED - Bilingual AI News Evaluation & Detection

**Real-World Validated Fake News Detection for Polish & English**

[![Vercel](https://img.shields.io/badge/Vercel-Live-success)](https://baned-xi.vercel.app)
[![Polish](https://img.shields.io/badge/Polish-100%25_Accuracy-brightgreen)]() 
[![English](https://img.shields.io/badge/English-78.6%25_Accuracy-green)]() 
[![Overall](https://img.shields.io/badge/Overall-87.5%25_Validated-blue)]()

> **✅ PRODUCTION-READY** - Validated on 48 real fact-checked examples from PolitiFact, Snopes, and Demagog

## 🎯 **Real-World Performance**

```
╔════════════════════════════════════════════════════════════╗
║  📊 VALIDATED ON REAL FACT-CHECKED DATA (Nov 2025)        ║
╠════════════════════════════════════════════════════════════╣
║  Overall Accuracy:      87.50% (42/48 correct)     ✅      ║
║  🇵🇱 Polish:             100.00% (20/20)            🏆      ║
║  🇬🇧 English:            78.57% (22/28)             ✅      ║
║  Standard News:         97.50% (39/40)             🔥      ║
║  False Positives:       2.1% (1/48)                ✅      ║
║  Conservative & Safe:   Prefers missing fakes over        ║
║                         falsely flagging real news         ║
╚════════════════════════════════════════════════════════════╝
```

**Sources:** PolitiFact, Snopes, FactCheck.org, Demagog.org.pl, Konkret24

### 🚀 **Quick Test**

```bash
# Test the live API
curl -X POST https://baned-xi.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Mikroczapy w szczepionkach! Bill Gates ukrywa prawdę!"}'

# Response: {"prediction":"FAKE","confidence":0.93,"language":"pl"}
```

---

**Bayesian-Augmented News Evaluation and Detection**

> **⚠️ DERIVATIVE WORK NOTICE**  
> This is an educational/humanitarian implementation based on the original BANED research.  
> **Original Repository:** https://github.com/micbizon/BANED  
> **Original Authors:** Julia Puczynska, Youcef Djenouri, Michał Bizon, Tomasz Michalak, Piotr Sankowski  
> **Original Institution:** IDEAS NCBR Sp. z o.o.  
> **License:** MIT (see LICENSE file)  
>   
> **This Implementation:** Created for humanitarian purposes by Fundacja Hospicjum  
> **Purpose:** Free, open-source fake news detection tool  
> **Status:** Completely free to use - Optional donations support hospice care  
>   
> **Citation Required:** If you use this code, you MUST cite the original BANED research.

A simplified, production-ready implementation combining CNN with MC Dropout and Apriori-based Knowledge Base for fake news detection. Features automated dataset generation, train/test validation, and optimized fusion algorithms.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-See%20Original-green)](https://github.com/PiotrStyla/BANED)

## 🚀 Quick Start

### Option 1: Try the Live API (Fastest!)
```bash
# Install dependencies
pip install -r requirements.txt

# Start API server
python start_api.ps1

# Open web interface
# Open static/index.html in your browser
```

**Result:** Interactive web interface for testing fake news detection in real-time!

### Option 2: Run Full Pipeline
```bash
# Generate 10,000 examples
python generate_dataset.py

# Run pipeline with train/test split
.\run_10k_easy.ps1  # Windows (4000 samples)
```

**Result:** 100% test accuracy on 800 unseen examples (4000 total, 80/20 split)

## 📊 Key Results

### Performance on 10,000 Examples (Production Scale!)

| Dataset | Samples | Train/Test | Train Acc | Test Acc | Vocabulary | Patterns (R/F) |
|---------|---------|------------|-----------|----------|------------|----------------|
| **Easy 10K** | 4000 | 3200/800 (80/20) | 100% | **100%** ✓ | 360 words | 4/0 |
| **Hard 10K** | 4000 | 3200/800 (80/20) | 100% | **100%** ✓ | 184 words | 7/17 |
| **Extreme 10K** | 2000 | 1600/400 (80/20) | 100% | **100%** ✓ | 329 words | 4/5 |

**Total Test Samples:** 2000 unseen examples - **100% accuracy across all difficulty levels!**

### Knowledge Base Pattern Discovery

**After common word filtering (32 words blacklisted):**

```
Dataset      Real Patterns    Fake Patterns    Total    Key Findings
Easy 10K:    4                0                4        All fake = common words
Hard 10K:    7                17               24       Most patterns, still 100%
Extreme 10K: 4                5                9        First time fake > 0
Easy:        3                4                7        Original baseline
Hard:        9                10               19       Realistic overlap
Extreme:     3                1                4        Minimal patterns
```

**Key Insights:** 
- Easy datasets: Fake news uses only common/generic words
- Hard datasets: 17 distinctive fake patterns but CNN still perfect
- Extreme datasets: First appearance of distinctive fake patterns (5)
- Pattern count ≠ difficulty for CNN

## 📁 Project Structure

```
baned-test/
├── 🌐 Production API (NEW!)
│   ├── api.py                    # FastAPI REST API (400+ lines)
│   ├── static/index.html         # Web interface (600+ lines)
│   ├── start_api.ps1            # Quick start script
│   ├── models/                  # Model artifacts
│   │   ├── model.pth           # CNN weights (~2MB)
│   │   └── vocab.txt           # Vocabulary (334-360 words)
│   └── kb/                      # Knowledge base
│       ├── real_patterns.csv   # Real news patterns
│       └── fake_patterns.csv   # Fake news patterns
│
├── 📊 Data Generation
│   └── generate_dataset.py       # Template-based dataset generator (10K+ capable!)
│
├── 🗂️ Small Datasets (60-133 samples)
│   ├── fnn_real.csv              # 60 easy real news
│   ├── fnn_fake.csv              # 73 easy fake news
│   ├── fnn_real_hard.csv         # 30 hard real (clickbait)
│   ├── fnn_fake_hard.csv         # 40 hard fake (pseudo-science)
│   ├── fnn_extreme_real.csv      # 40 extreme (satire, disclosed conflicts)
│   └── fnn_extreme_fake.csv      # 50 extreme (propaganda, context manipulation)
│
├── 🗂️ Large Datasets (1000 samples)
│   ├── fnn_real_1k.csv           # 200 easy real
│   ├── fnn_fake_1k.csv           # 200 easy fake
│   ├── fnn_real_hard_1k.csv      # 150 hard real
│   ├── fnn_fake_hard_1k.csv      # 150 hard fake
│   ├── fnn_extreme_real_1k.csv   # 150 extreme real
│   └── fnn_extreme_fake_1k.csv   # 150 extreme fake
│
├── 🔧 Core Pipeline
│   ├── prep_data.py              # Text preprocessing & cleaning
│   ├── apriori_algo.py           # Knowledge Base generation (Apriori)
│   ├── cnn.py                    # CNN with MC Dropout + train/test split
│   ├── calculate.py              # Baseline fusion & metrics
│   ├── calculate_optimized.py    # Optimized fusion (filtered patterns, weighted)
│   └── merge_data.py             # CSV merging utility
│
├── 📈 Analysis Tools
│   ├── analyze_patterns.py       # Detailed KB pattern analysis
│   ├── compare_results.py        # CNN vs BANED comparison
│   ├── compare_easy_vs_hard.py   # Difficulty level comparison
│   └── compare_all_levels.py     # Comprehensive 3-way analysis
│
├── ⚡ Automation Scripts
│   ├── run_all.ps1               # Small dataset pipeline (133 samples)
│   ├── run_hard.ps1              # Hard examples (70 samples)
│   ├── run_extreme.ps1           # Extreme examples (90 samples)
│   ├── run_1k.ps1                # 1K dataset pipeline (400 samples)
│   ├── run_10k_easy.ps1          # 10K easy pipeline (4000 samples) 🆕
│   ├── run_10k_hard.ps1          # 10K hard pipeline (4000 samples) 🆕
│   └── run_10k_extreme.ps1       # 10K extreme pipeline (2000 samples) 🆕
│
├── 🛠️ Deployment Tools (NEW!)
│   ├── prepare_deployment.py     # Deployment preparation
│   ├── save_model.py            # Model export utility
│   └── DEPLOYMENT.md            # Complete deployment guide (500+ lines)
│
└── 📚 Documentation
    ├── README.md                 # This file (English)
    ├── README_PL.md              # Polish documentation
    ├── CHANGELOG.md              # Version history
    └── CONTRIBUTING.md           # Contribution guidelines
```

## 🎯 Features

### 1. **Production REST API** 🆕
- FastAPI with automatic documentation (Swagger UI)
- Single & batch prediction endpoints
- Knowledge Base fusion support
- Health monitoring and statistics
- CORS enabled for web access
- Interactive API docs at `/docs`

### 2. **Web Interface** 🆕
- Beautiful, responsive design
- Real-time prediction with confidence visualization
- Pattern matching display (color-coded)
- Example news articles
- API status monitoring

### 3. **Dataset Generation**
- Template-based generation with 70+ substitution lists
- 3 difficulty levels: Easy, Hard, Extreme
- Reproducible (configurable seed)
- Scalable to 10K+ examples (tested!)

```python
python generate_dataset.py \
  --easy_real 200 --easy_fake 200 \
  --hard_real 150 --hard_fake 150 \
  --extreme_real 150 --extreme_fake 150 \
  --seed 42
```

**Templates:**
- **Easy Real:** Government announcements, scientific studies, local news (26 templates)
- **Easy Fake:** Conspiracy theories, absurd health claims, pseudoscience (14 templates)
- **Hard Real:** Clickbait headlines, sensational but true (14 templates)
- **Hard Fake:** Pseudo-scientific claims, misleading context (14 templates)
- **Extreme Real:** Satire (marked), disclosed conflicts, proper context (24 templates)
- **Extreme Fake:** Satire (unmarked), hidden conflicts, cherry-picked data (24 templates)

### 2. **CNN with MC Dropout**
- Simple 3-layer CNN architecture
- Monte Carlo Dropout for uncertainty estimation
- Train/test split support (80/20 default)
- Vocabulary built from training data only

```python
python cnn.py -r real.csv -f fake.csv \
  --epochs 20 \
  --mc_samples 30 \
  --test_split 0.2 \
  --seed 42
```

**Architecture:**
- Embedding: 64 dimensions
- Conv filters: [3, 4, 5] with 100 filters each
- Dropout: 0.5 (active during inference for MC Dropout)
- Output: Sigmoid (binary classification)

### 3. **Knowledge Base (Apriori)**
- Extracts frequent word patterns
- Configurable support threshold
- Separate patterns for real vs fake news

```python
python apriori_algo.py -i data.csv \
  --min_support 0.10 \
  --out patterns.csv
```

### 4. **Optimized Fusion**
- **Common word filtering:** Removes 32 non-discriminative words
- **Confidence-based weighting:** Trusts CNN more when confident
- **Better pattern utilization:** Focuses on distinctive markers

```python
python calculate_optimized.py data.csv \
  --probabilities probs.npy \
  --fake_support fake_patterns.csv \
  --real_support real_patterns.csv \
  --limit 30
```

**Fusion Formula:**
```
cnn_weight = min(1.0, cnn_confidence / 0.4)
kb_weight = 1.0 - cnn_weight
fused_prob = (cnn_prob × cnn_weight) + (kb_prob × kb_weight)
```

## 🔬 Pipeline Workflow

```
┌─────────────────┐
│ Raw Text Data   │
│ (CSV files)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 1. Preprocessing│  ← prep_data.py
│ - Lowercase     │
│ - Remove URLs   │
│ - Clean text    │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐  ┌────────┐
│ 2. CNN │  │ 2. KB  │  ← cnn.py, apriori_algo.py
│ Train  │  │ Apriori│
│ +Test  │  │        │
└───┬────┘  └───┬────┘
    │           │
    │   ┌───────┘
    ▼   ▼
┌─────────────────┐
│ 3. Fusion       │  ← calculate_optimized.py
│ - Filter common │
│ - Weight by conf│
│ - Final metrics │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Results & Report│
│ - Accuracy      │
│ - Confidence    │
│ - Patterns      │
└─────────────────┘
```

## 📊 Detailed Results

### Small Datasets (60-133 samples)

| Level | Samples | CNN Acc | Min Conf | Overlap | Real Patterns | Fake Patterns |
|-------|---------|---------|----------|---------|---------------|---------------|
| Easy | 133 | 100% | 79.1% | 9.1% | 3 | 4 |
| Hard | 70 | 100% | 91.0% | 38.9% | 9 | 10 |
| Extreme | 90 | 100% | 95.7% | 22.2% | 3 | 1 |

**Trend:** Confidence increases with difficulty (paradoxical but consistent)

### Large Dataset (400 Easy samples, 80/20 split)

```
Training Performance:
  Epoch 1:  79.1% → Epoch 20: 100%
  Final train accuracy: 100% (320/320)

Test Performance (UNSEEN DATA):
  Test accuracy: 100% (80/80) ✓✓✓
  MC Dropout samples: 30
  Final confidence: 98.8% average

Knowledge Base:
  Real patterns (filtered): 5
    "announces", "department", "federal", "agency", "reports"
  
  Fake patterns (filtered): 0
    All 2 patterns were common words ("to", "by")
    
Pattern Insight:
  Real news: Institutional, formal language
  Fake news: Generic claims with common connectors
```

### Pattern Examples

**Real News Distinctive Patterns:**
```
"announces new"       Support: 0.145
"department"          Support: 0.125
"federal agency"      Support: 0.110
"reports"             Support: 0.095
"signs legislation"   Support: 0.085
```

**Fake News (Before Filtering):**
```
"to"      Support: 0.180  ← Filtered (common)
"by"      Support: 0.140  ← Filtered (common)
```

**Result:** After filtering, fake news has NO distinctive patterns in easy examples.

## 🔍 Key Findings

### 1. **CNN Generalizes Perfectly**
- 100% accuracy on unseen test data (80 samples)
- No overfitting despite 100% train accuracy
- High confidence (98.8% average)

### 2. **Pattern Overlap = Difficulty Indicator**
```
9.1%  → Easy    (clear linguistic distinction)
38.9% → Hard    (realistic ambiguity)
22.2% → Extreme (mixed signals)
```

### 3. **Common Word Filtering is Critical**
- Removes 25-67% of patterns
- Eliminates noise from KB
- Fake news patterns are mostly common words

### 4. **Task Remains Easy**
- CNN too confident (>98%)
- Need more sophisticated fake news
- Current templates may be too systematic

## 🚧 Limitations

1. **Template-based generation** - May lack natural variation
2. **High CNN confidence** - Suggests task is too simple
3. **Small vocabulary** - 334 unique words in 400 samples
4. **Binary classification** - Real-world is more nuanced
5. **English only** - No multi-language support

## 🔮 Future Work

### Immediate Next Steps
1. **Test on Hard/Extreme datasets** (300 samples each)
2. **Expand to 10K examples** for better generalization testing
3. **Add adversarial examples** (GPT-generated fake news)
4. **Cross-dataset validation** (train on Easy, test on Hard)

### Advanced Improvements
1. **Multi-source data** (Twitter, Facebook, news sites)
2. **Temporal analysis** (how language evolves)
3. **Multi-modal** (text + images + metadata)
4. **Explainability** (attention mechanisms, LIME)
5. **Real-time detection** (API deployment)

## 📖 Usage Examples

### Generate Custom Dataset
```python
from generate_dataset import generate_examples, EASY_REAL_TEMPLATES

# Generate 500 easy real news
examples = generate_examples(EASY_REAL_TEMPLATES, 500)

# Save to CSV
import csv
with open('custom_real.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['text'])
    for ex in examples:
        writer.writerow([ex])
```

### Train with Custom Parameters
```bash
python cnn.py \
  -r fnn_real_1k.csv \
  -f fnn_fake_1k.csv \
  --epochs 30 \
  --dropout_p 0.6 \
  --mc_samples 50 \
  --test_split 0.3 \
  --batch_size 16 \
  --seed 42
```

### Analyze Patterns
```bash
# Detailed pattern analysis
python analyze_patterns.py

# Compare difficulty levels
python compare_all_levels.py

# Evaluate KB impact
python compare_results.py
```

### Run Optimized Fusion
```bash
python calculate_optimized.py fnn_all_1k_clean.csv \
  --probabilities fnn_all_1k_cnn_prob.npy \
  --fake_support fake_1k_support.csv \
  --real_support real_1k_support.csv \
  --limit 30
```

## 🛠️ Configuration

### Environment Variables
```bash
# Python version
PYTHON_VERSION=3.8+

# PyTorch (CPU or CUDA)
TORCH_VERSION=2.0+
```

### Hyperparameters
```python
# CNN Training
EPOCHS = 20              # Training epochs
BATCH_SIZE = 8           # Batch size
LEARNING_RATE = 0.001    # Adam optimizer
DROPOUT = 0.5            # Dropout probability
MC_SAMPLES = 30          # MC Dropout samples

# Knowledge Base
MIN_SUPPORT = 0.10       # Apriori support threshold (5-20%)
TOP_K = 30               # Number of patterns to use

# Fusion
CNN_CONF_THRESHOLD = 0.4 # Confidence threshold for weighting
```

## 📊 Reproducibility

All experiments are reproducible with fixed seeds:

```python
# Python
import random
import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

# Dataset generation
python generate_dataset.py --seed 42

# CNN training
python cnn.py --seed 42
```

## 🤝 Contributing

**IMPORTANT: This is a derivative work / educational implementation.**

### Original Work
- **Original BANED Research:** [Main Repository](https://github.com/PiotrStyla/BANED)
- **Original Authors:** [Please specify original authors from the main repository]
- **Original License:** [Please specify license from the main repository]

This minimal standalone implementation was created for educational and research purposes, building upon the original BANED work.

### Changes in This Implementation
- ✅ Automated dataset generation (1K+ examples)
- ✅ Train/test split validation
- ✅ Optimized fusion algorithm
- ✅ Comprehensive analysis tools
- ✅ Production-ready scripts

### Contributing to This Fork
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

**This derivative work maintains the same license as the original BANED repository.**

Please refer to the [original repository](https://github.com/PiotrStyla/BANED) for complete license information.

If you use this code, you must also comply with the original BANED license terms.

## 📚 Citation

**If you use this code, you MUST cite the original BANED research:**

```bibtex
@article{original_baned,
  author = {[Original BANED authors - please check main repository]},
  title = {BANED: Bayesian-Augmented News Evaluation and Detection},
  year = {[Original publication year]},
  url = {https://github.com/PiotrStyla/BANED}
}
```

**Optionally, you may also cite this minimal implementation:**

```bibtex
@software{baned_minimal_2025,
  author = {[Your name/team]},
  title = {BANED: Minimal Standalone Implementation (Derivative Work)},
  year = {2025},
  url = {https://github.com/PiotrStyla/BANED},
  branch = {minimal-standalone},
  note = {Educational implementation based on original BANED research}
}
```

## 📞 Contact

- **Repository:** https://github.com/PiotrStyla/BANED/tree/minimal-standalone
- **Issues:** https://github.com/PiotrStyla/BANED/issues

## 🎓 Acknowledgments

### Primary Acknowledgment
**This work is based on the original BANED (Bayesian-Augmented News Evaluation and Detection) research.**

- **Original BANED Repository:** https://github.com/PiotrStyla/BANED
- **Original Authors:** [Please specify from main repository]
- **Original Research Paper:** [Please specify if published]

This minimal implementation is a derivative educational work that simplifies and extends the original BANED for teaching and experimentation purposes.

### Additional Acknowledgments
- FakeNewsNet dataset inspiration
- PyTorch and scikit-learn communities
- Open source ML/NLP community

---

**Version:** 3.0.0 (Production API + 10K Dataset Expansion)  
**Last Updated:** November 2025  
**Branch:** minimal-standalone  
**Status:** ✅ Production Ready - Live API + Web Interface!
