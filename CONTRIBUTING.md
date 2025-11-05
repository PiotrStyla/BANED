# Contributing to BANED

Thank you for your interest in contributing to the BANED Minimal Standalone Implementation!

## 🎯 Project Goals

This project aims to provide:
1. **Easy-to-use** fake news detection pipeline
2. **Reproducible** research results
3. **Educational** resource for ML/NLP students
4. **Extensible** codebase for future research

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.8
torch >= 2.0
numpy >= 1.20
```

### Setup Development Environment
```bash
# Clone repository
git clone https://github.com/PiotrStyla/BANED.git
cd BANED
git checkout minimal-standalone

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/  # (if tests exist)
```

## 📝 How to Contribute

### 1. Report Bugs
- Use GitHub Issues
- Include:
  - Python version
  - OS (Windows/Linux/Mac)
  - Full error message
  - Steps to reproduce
  - Expected vs actual behavior

### 2. Suggest Features
- Open an Issue with label `enhancement`
- Describe:
  - Use case
  - Proposed solution
  - Alternative approaches
  - Impact on existing features

### 3. Submit Pull Requests

#### Branch Naming
```
feature/your-feature-name
bugfix/issue-number-description
docs/documentation-improvement
refactor/code-cleanup
```

#### Commit Messages
```
feat: Add GPT-based adversarial example generator
fix: Resolve train/test split index error
docs: Update README with 10K dataset results
refactor: Simplify fusion algorithm
test: Add unit tests for preprocessing
```

#### PR Checklist
- [ ] Code follows project style
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts

## 🏗️ Code Structure

### Adding New Features

#### Example: New Dataset Generator Template
```python
# In generate_dataset.py

# 1. Add template list
NEW_CATEGORY_TEMPLATES = [
    "{subject} {verb} {object}",
    # ... more templates
]

# 2. Add substitution lists
SUBJECTS = ["researcher", "scientist", ...]
VERBS = ["discovers", "announces", ...]
OBJECTS = ["breakthrough", "innovation", ...]

# 3. Update main() to use new templates
def main():
    # ... existing code
    new_examples = generate_examples(NEW_CATEGORY_TEMPLATES, count)
```

#### Example: New Analysis Tool
```python
# Create new file: analyze_my_feature.py

#!/usr/bin/env python3
"""
analyze_my_feature.py - Description of what it does
"""
import argparse
import csv
import numpy as np

def analyze_feature(data):
    """Analyze specific feature."""
    # Implementation
    pass

def main():
    parser = argparse.ArgumentParser(description='Analyze my feature')
    # ... add arguments
    
    args = parser.parse_args()
    # ... implementation

if __name__ == '__main__':
    main()
```

## 🧪 Testing Guidelines

### Unit Tests
```python
# tests/test_preprocessing.py
import pytest
from prep_data import clean_text

def test_clean_text_lowercase():
    assert clean_text("HELLO") == "hello"

def test_clean_text_urls():
    text = "Check http://example.com for info"
    assert "http" not in clean_text(text)
```

### Integration Tests
```python
# tests/test_pipeline.py
def test_full_pipeline():
    # 1. Generate data
    # 2. Preprocess
    # 3. Train CNN
    # 4. Evaluate
    # Assert results
```

## 📊 Benchmarking

When adding new features that affect performance:

```python
import time

start = time.time()
# Your code
end = time.time()

print(f"Execution time: {end - start:.2f}s")
```

Include benchmark results in PR description:
```
Benchmark Results:
- Old method: 5.2s
- New method: 2.1s (2.5x faster)
- Accuracy: No change (100%)
```

## 📖 Documentation Standards

### Code Comments
```python
def complex_function(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
    
    Returns:
        type: Description of return value
    
    Example:
        >>> result = complex_function(1, 2)
        >>> print(result)
        3
    """
    # Implementation
```

### README Updates
When adding features, update:
- Quick Start section
- Features list
- Usage Examples
- Configuration options

### CHANGELOG Updates
Follow format:
```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description

### Results
- Performance impact
```

## 🎨 Code Style

### Python (PEP 8)
```python
# Good
def calculate_accuracy(predictions, labels):
    correct = sum(p == l for p, l in zip(predictions, labels))
    return correct / len(labels)

# Bad
def calc_acc(p,l):
    return sum([p[i]==l[i] for i in range(len(p))])/len(p)
```

### Variable Naming
```python
# Good
train_accuracy = 0.95
num_samples = 1000
real_patterns = load_patterns("real.csv")

# Bad
acc = 0.95
n = 1000
patterns = load_patterns("real.csv")
```

### Line Length
- Max 100 characters per line
- Break long strings:
```python
message = (
    "This is a very long message that exceeds "
    "the maximum line length and needs to be broken"
)
```

## 🔍 Code Review Process

1. **Automated Checks**
   - Linting (flake8, pylint)
   - Type checking (mypy)
   - Tests (pytest)

2. **Manual Review**
   - Code correctness
   - Performance implications
   - Documentation quality
   - Test coverage

3. **Approval**
   - At least 1 maintainer approval
   - All checks passing
   - No conflicts

## 📦 Release Process

### Version Numbering (Semantic Versioning)
```
MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes
```

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Tagged in git
- [ ] GitHub release created

## 🤔 Questions?

- **General questions:** Open a GitHub Discussion
- **Bug reports:** Open a GitHub Issue
- **Security issues:** Email (see SECURITY.md)
- **Feature requests:** Open a GitHub Issue with `enhancement` label

## 📜 Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors.

### Standards
- Be respectful and constructive
- Accept feedback gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing private information

## 🙏 Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- GitHub contributors list
- Release notes (for significant contributions)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

**Thank you for contributing to BANED!** 🎉

Your efforts help make fake news detection more accessible and effective for everyone.
