# Changelog

All notable changes to the BANED Minimal Standalone Implementation.

## [2.0.0] - 2025-11-05

### Added - 1000+ Examples Expansion
- **Dataset Generator** (`generate_dataset.py`)
  - Template-based generation with 70+ substitution lists
  - 3 difficulty levels: Easy (400), Hard (300), Extreme (300)
  - Reproducible with configurable seed
  - Total: 1000 generated examples

- **Train/Test Split in CNN**
  - `--test_split` parameter for validation on unseen data
  - `--seed` parameter for reproducibility
  - Separate train/test evaluation during training
  - Final test set performance report with MC Dropout

- **Large Dataset Files**
  - `fnn_real_1k.csv` - 200 easy real examples
  - `fnn_fake_1k.csv` - 200 easy fake examples
  - `fnn_real_hard_1k.csv` - 150 hard real examples
  - `fnn_fake_hard_1k.csv` - 150 hard fake examples
  - `fnn_extreme_real_1k.csv` - 150 extreme real examples
  - `fnn_extreme_fake_1k.csv` - 150 extreme fake examples

- **Automation**
  - `run_1k.ps1` - Pipeline for 400 easy examples with 80/20 split

### Results
- **100% test accuracy** on 80 unseen examples (400 total)
- **Perfect generalization** - no overfitting detected
- **Pattern discovery:** All fake patterns were common words (filtered out)
- **High confidence:** 98.8% average CNN confidence

### Changed
- Updated `cnn.py` with train/test split functionality
- Vocabulary now built only from training data
- Enhanced logging with train vs test accuracy reporting

## [1.1.0] - 2025-11-05

### Added - Hard & Extreme Datasets
- **Hard Examples** (70 total)
  - 30 real: Clickbait headlines, sensational but true
  - 40 fake: Pseudo-scientific language, misleading context
  
- **Extreme Examples** (90 total)
  - 40 real: Satire (marked), disclosed conflicts, proper context
  - 50 fake: Propaganda, context manipulation, hidden conflicts

- **Analysis Tools**
  - `compare_easy_vs_hard.py` - 2-way difficulty comparison
  - `compare_all_levels.py` - 3-way comprehensive analysis

- **Optimized Fusion** (`calculate_optimized.py`)
  - Common word filtering (32 word blacklist)
  - Confidence-based weighted fusion
  - Better pattern utilization

- **Automation Scripts**
  - `run_hard.ps1` - Hard examples pipeline
  - `run_extreme.ps1` - Extreme examples pipeline

### Results
- **Pattern overlap increases with difficulty:**
  - Easy: 9.1% overlap
  - Hard: 38.9% overlap (most realistic!)
  - Extreme: 22.2% overlap
  
- **CNN maintains 100% accuracy** across all levels
- **Confidence paradox:** Higher confidence on harder examples
  - Easy: 79.1% min confidence
  - Hard: 91.0% min confidence
  - Extreme: 95.7% min confidence

### Key Insights
- Hard examples show realistic linguistic overlap
- Optimized fusion maintains accuracy with better calibration
- Pattern filtering removes 25-67% of noise

## [1.0.0] - 2025-11-05

### Added - Initial Release
- **Core Pipeline**
  - `prep_data.py` - Text preprocessing
  - `apriori_algo.py` - Knowledge Base generation
  - `cnn.py` - CNN with MC Dropout
  - `calculate.py` - Baseline fusion
  - `merge_data.py` - CSV utility

- **Easy Dataset** (133 samples)
  - 60 real news examples
  - 73 fake news examples

- **Analysis Tools**
  - `analyze_patterns.py` - Pattern analysis
  - `compare_results.py` - CNN vs BANED comparison

- **Automation**
  - `run_all.ps1` - Full pipeline automation

- **Documentation**
  - `README.md` - English documentation
  - `README_PL.md` - Polish documentation

### Results
- **100% accuracy** on easy examples
- **4 real patterns** found (institutional language)
- **8 fake patterns** found (conspiracy terms)
- **9.1% pattern overlap**

---

## Version History Summary

| Version | Date | Samples | Features | Test Accuracy |
|---------|------|---------|----------|---------------|
| **2.0.0** | 2025-11-05 | 1000 | Generator, Train/Test | 100% (80 unseen) |
| **1.1.0** | 2025-11-05 | 293 | Hard/Extreme, Optimized Fusion | 100% |
| **1.0.0** | 2025-11-05 | 133 | Core Pipeline | 100% |

## Roadmap

### v2.1.0 (Planned)
- [ ] Run pipeline on Hard 1K (300 samples)
- [ ] Run pipeline on Extreme 1K (300 samples)
- [ ] Cross-dataset validation (train Easy, test Hard)
- [ ] Confidence calibration analysis

### v3.0.0 (Future)
- [ ] Expand to 10K examples
- [ ] GPT-generated adversarial examples
- [ ] Multi-source data integration
- [ ] Visualization dashboard
- [ ] REST API deployment

### v4.0.0 (Research)
- [ ] Multi-modal detection (text + images)
- [ ] Temporal evolution analysis
- [ ] Multi-language support
- [ ] Explainability features (attention, LIME)

---

**Maintained by:** PiotrStyla  
**Repository:** https://github.com/PiotrStyla/BANED  
**Branch:** minimal-standalone
