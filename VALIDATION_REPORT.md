# REAL-WORLD VALIDATION REPORT
================================================================================

## Overall Performance
- **Accuracy: 87.50%** (42/48)
- False Positives (Real → Fake): 1
- False Negatives (Fake → Real): 5

## By Language

### Polish
- Accuracy: 100.00%
- Correct: 20/20
- False Positives: 0
- False Negatives: 0

### English
- Accuracy: 78.57%
- Correct: 22/28
- False Positives: 1
- False Negatives: 5

## By Difficulty
- Standard: 97.50%
- Extreme: 37.50%

## Failures

### 6 failures detected:


**1. EN - FAKE → REAL**
- Confidence: 0.55
- Text: This ancient remedy melts belly fat overnight! Doctors can't explain it. Pharmaceutical companies panicking!...
- Source: Fact-checked FALSE


**2. EN - REAL → FAKE**
- Confidence: 0.58
- Text: Corporate-sponsored research suggests benefits, but independent scientists question methodology and funding transparency....
- Source: Edge case


**3. EN - FAKE → REAL**
- Confidence: 0.55
- Text: Breaking: Scientists discover that thinking about exercise burns same calories as actual exercise. Gyms closing worldwide....
- Source: Edge case


**4. EN - FAKE → REAL**
- Confidence: 0.56
- Text: Study shows cigarettes are safe. Researchers claim no health risks found in decades of smoking....
- Source: Edge case


**5. EN - FAKE → REAL**
- Confidence: 0.55
- Text: Crime rate explodes by 300%! (Note: went from 1 incident to 4 in small town of 500 people)...
- Source: Edge case


**6. EN - FAKE → REAL**
- Confidence: 0.55
- Text: Both sides are equally bad: Professional scientists and random bloggers disagree on climate change....
- Source: Edge case


## Insights

⚠️ **NEEDS IMPROVEMENT** - Model struggles with real-world examples.

🔴 **Main issue:** Too many false negatives (missing fake news)

================================================================================
