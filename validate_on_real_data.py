#!/usr/bin/env python3
"""
Validate BANED Models on Real-World Fact-Checked Data
Tests API predictions against verified examples
"""

import requests
import csv
import json
import time
from collections import defaultdict

# API Configuration
API_URL = "https://baned-xi.vercel.app/api/predict"  # Vercel deployment
# API_URL = "https://fake-checker.eu/api/predict"  # Custom domain (if configured)
# API_URL = "http://localhost:3000/api/predict"  # Local testing

def test_api_prediction(text):
    """Test single text against API."""
    try:
        response = requests.post(
            API_URL,
            json={"text": text},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ⚠️  API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"  ❌ Request failed: {e}")
        return None

def validate_all_examples():
    """Run validation on all real-world examples."""
    
    print("="*80)
    print("REAL-WORLD VALIDATION")
    print("="*80)
    print(f"\nTesting API: {API_URL}\n")
    
    # Load validation dataset
    examples = []
    with open('real_world_validation.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        examples = list(reader)
    
    print(f"📊 Loaded {len(examples)} fact-checked examples\n")
    
    # Test each example
    results = []
    stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'false_positives': 0, 'false_negatives': 0})
    
    for i, example in enumerate(examples, 1):
        text = example['text']
        true_label = example['label']
        language = example['language']
        difficulty = example['difficulty']
        
        print(f"[{i}/{len(examples)}] Testing {language.upper()} {difficulty}...")
        print(f"  True label: {true_label}")
        print(f"  Text: {text[:80]}...")
        
        # Get API prediction
        prediction = test_api_prediction(text)
        
        if prediction:
            pred_label = prediction.get('prediction', 'UNKNOWN')
            confidence = prediction.get('confidence', 0)
            detected_lang = prediction.get('language', 'unknown')
            
            # Check if correct
            is_correct = (pred_label == true_label)
            
            # Update stats
            stats['overall']['total'] += 1
            stats[language]['total'] += 1
            stats[difficulty]['total'] += 1
            stats[f"{language}_{true_label}"]['total'] += 1
            
            if is_correct:
                stats['overall']['correct'] += 1
                stats[language]['correct'] += 1
                stats[difficulty]['correct'] += 1
                stats[f"{language}_{true_label}"]['correct'] += 1
                print(f"  ✅ CORRECT: {pred_label} (confidence: {confidence:.2f})")
            else:
                print(f"  ❌ WRONG: {pred_label} (confidence: {confidence:.2f})")
                
                # Track false positives/negatives
                if pred_label == 'FAKE' and true_label == 'REAL':
                    stats['overall']['false_positives'] += 1
                    stats[language]['false_positives'] += 1
                elif pred_label == 'REAL' and true_label == 'FAKE':
                    stats['overall']['false_negatives'] += 1
                    stats[language]['false_negatives'] += 1
            
            # Store result
            results.append({
                'text': text,
                'true_label': true_label,
                'predicted_label': pred_label,
                'confidence': confidence,
                'correct': is_correct,
                'language': language,
                'detected_language': detected_lang,
                'difficulty': difficulty,
                'source': example['source']
            })
            
        else:
            print(f"  ⚠️  No prediction received")
            stats['overall']['total'] += 1
            stats[language]['total'] += 1
        
        print()
        time.sleep(0.5)  # Rate limiting
    
    return results, stats

def generate_report(results, stats):
    """Generate detailed validation report."""
    
    print("\n" + "="*80)
    print("VALIDATION RESULTS")
    print("="*80)
    
    # Overall stats
    overall = stats['overall']
    if overall['total'] > 0:
        accuracy = (overall['correct'] / overall['total']) * 100
        print(f"\n📊 OVERALL PERFORMANCE:")
        print(f"  Accuracy: {accuracy:.2f}% ({overall['correct']}/{overall['total']})")
        print(f"  False Positives (Real → Fake): {overall['false_positives']}")
        print(f"  False Negatives (Fake → Real): {overall['false_negatives']}")
    
    # Language breakdown
    print(f"\n🌍 BY LANGUAGE:")
    for lang in ['pl', 'en']:
        if stats[lang]['total'] > 0:
            acc = (stats[lang]['correct'] / stats[lang]['total']) * 100
            lang_name = "Polish" if lang == 'pl' else "English"
            print(f"  {lang_name}: {acc:.2f}% ({stats[lang]['correct']}/{stats[lang]['total']})")
            print(f"    False Positives: {stats[lang]['false_positives']}")
            print(f"    False Negatives: {stats[lang]['false_negatives']}")
    
    # Difficulty breakdown
    print(f"\n🎯 BY DIFFICULTY:")
    for diff in ['standard', 'extreme']:
        if stats[diff]['total'] > 0:
            acc = (stats[diff]['correct'] / stats[diff]['total']) * 100
            print(f"  {diff.upper()}: {acc:.2f}% ({stats[diff]['correct']}/{stats[diff]['total']})")
    
    # Label breakdown
    print(f"\n🏷️  BY TRUE LABEL:")
    for lang in ['pl', 'en']:
        for label in ['REAL', 'FAKE']:
            key = f"{lang}_{label}"
            if stats[key]['total'] > 0:
                acc = (stats[key]['correct'] / stats[key]['total']) * 100
                lang_name = "Polish" if lang == 'pl' else "English"
                print(f"  {lang_name} {label}: {acc:.2f}% ({stats[key]['correct']}/{stats[key]['total']})")
    
    # Failure analysis
    print(f"\n❌ FAILURE ANALYSIS:")
    failures = [r for r in results if not r['correct']]
    
    if failures:
        print(f"\nTotal failures: {len(failures)}\n")
        for i, failure in enumerate(failures, 1):
            print(f"{i}. [{failure['language'].upper()}] {failure['true_label']} → {failure['predicted_label']}")
            print(f"   Confidence: {failure['confidence']:.2f}")
            print(f"   Text: {failure['text'][:100]}...")
            print(f"   Source: {failure['source']}")
            print()
    else:
        print("🎉 NO FAILURES! Perfect 100% accuracy!\n")
    
    # Save detailed results
    with open('validation_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'summary': dict(stats),
            'results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: validation_results.json")
    
    # Generate markdown report
    markdown_report = f"""# REAL-WORLD VALIDATION REPORT
{'='*80}

## Overall Performance
- **Accuracy: {accuracy:.2f}%** ({overall['correct']}/{overall['total']})
- False Positives (Real → Fake): {overall['false_positives']}
- False Negatives (Fake → Real): {overall['false_negatives']}

## By Language

### Polish
- Accuracy: {(stats['pl']['correct'] / stats['pl']['total'] * 100) if stats['pl']['total'] > 0 else 0:.2f}%
- Correct: {stats['pl']['correct']}/{stats['pl']['total']}
- False Positives: {stats['pl']['false_positives']}
- False Negatives: {stats['pl']['false_negatives']}

### English
- Accuracy: {(stats['en']['correct'] / stats['en']['total'] * 100) if stats['en']['total'] > 0 else 0:.2f}%
- Correct: {stats['en']['correct']}/{stats['en']['total']}
- False Positives: {stats['en']['false_positives']}
- False Negatives: {stats['en']['false_negatives']}

## By Difficulty
- Standard: {(stats['standard']['correct'] / stats['standard']['total'] * 100) if stats['standard']['total'] > 0 else 0:.2f}%
- Extreme: {(stats['extreme']['correct'] / stats['extreme']['total'] * 100) if stats['extreme']['total'] > 0 else 0:.2f}%

## Failures

{'### Perfect! No failures! 🎉' if not failures else '### ' + str(len(failures)) + ' failures detected:'}

"""
    
    if failures:
        for i, failure in enumerate(failures, 1):
            markdown_report += f"""
**{i}. {failure['language'].upper()} - {failure['true_label']} → {failure['predicted_label']}**
- Confidence: {failure['confidence']:.2f}
- Text: {failure['text'][:200]}...
- Source: {failure['source']}

"""
    
    markdown_report += f"""
## Insights

{"🎉 **EXCELLENT!** The model performs perfectly on real fact-checked data!" if accuracy == 100 else "⚠️ **NEEDS IMPROVEMENT** - Model struggles with real-world examples."}

{f"🔴 **Main issue:** {'Too many false positives (marking real news as fake)' if overall['false_positives'] > overall['false_negatives'] else 'Too many false negatives (missing fake news)'}" if accuracy < 100 else ""}

{'='*80}
"""
    
    with open('VALIDATION_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"📄 Markdown report saved to: VALIDATION_REPORT.md")
    
    print("\n" + "="*80)
    print("✅ VALIDATION COMPLETE!")
    print("="*80)
    
    # Final verdict
    if accuracy >= 90:
        print("\n🎉 EXCELLENT! Model performs well on real data!")
    elif accuracy >= 75:
        print("\n✅ GOOD! Model is usable but has room for improvement.")
    elif accuracy >= 60:
        print("\n⚠️  MODERATE. Model needs significant improvement.")
    else:
        print("\n❌ POOR. Model needs major rework.")
    
    return accuracy

if __name__ == '__main__':
    # Run validation
    results, stats = validate_all_examples()
    
    # Generate report
    accuracy = generate_report(results, stats)
    
    print(f"\n🎯 Final accuracy: {accuracy:.2f}%\n")