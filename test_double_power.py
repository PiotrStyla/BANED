#!/usr/bin/env python3
"""
test_double_power.py - Test the Double Power Verification System
Tests both the verification modules and the API
"""
import sys
import os

# Add verification module to path
sys.path.append(os.path.dirname(__file__))

from verification.logical_consistency import (
    LogicalConsistencyChecker,
    FactDatabase,
    DoublePowerVerifier
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(label, value, color=''):
    """Print a formatted result"""
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'cyan': '\033[96m',
        'reset': '\033[0m'
    }
    color_code = colors.get(color, '')
    reset = colors['reset'] if color else ''
    print(f"{label:30} {color_code}{value}{reset}")


def test_logical_consistency():
    """Test the logical consistency checker"""
    print_section("TEST 1: Logical Consistency Checker")
    
    checker = LogicalConsistencyChecker()
    
    test_cases = [
        {
            'text': "This is always true and never false at the same time.",
            'expected': 'contradiction',
            'description': "Self-contradiction (always/never)"
        },
        {
            'text': "The study shows 200% effectiveness in all cases.",
            'expected': 'numerical_error',
            'description': "Impossible percentage (>100%)"
        },
        {
            'text': "Yesterday in 2030 we discovered this fact.",
            'expected': 'temporal_error',
            'description': "Temporal inconsistency"
        },
        {
            'text': "Scientists conducted normal research study.",
            'expected': 'clean',
            'description': "Clean text (no issues)"
        },
        {
            'text': "The patient is 200 years old and completely healthy.",
            'expected': 'numerical_error',
            'description': "Impossible age"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {case['description']}")
        print(f"   Text: \"{case['text']}\"")
        
        result = checker.analyze(case['text'])
        
        print_result("Consistency Level:", result['consistency_level'], 
                    'green' if result['consistency_level'] == 'EXCELLENT' else 'yellow')
        print_result("Total Score:", f"{result['total_score']:.2f}")
        print_result("Confidence Impact:", f"{result['confidence_impact']:.2%}")
        
        if result['issues']:
            print("   Issues detected:")
            for issue in result['issues']:
                print(f"     • {issue}")
        else:
            print("   ✓ No issues detected")


def test_fact_database():
    """Test the fact database verifier"""
    print_section("TEST 2: Fact Database Verification")
    
    db = FactDatabase()
    
    test_cases = [
        {
            'text': "This miracle cure works 100% of the time!",
            'description': "Impossible claim detection"
        },
        {
            'text': "Doctors hate this one weird trick!",
            'description': "Fake news pattern detection"
        },
        {
            'text': "Scientists invented perpetual motion machine.",
            'description': "Scientific impossibility"
        },
        {
            'text': "COVID-19 pandemic started in 2019.",
            'description': "Historical accuracy (correct)"
        },
        {
            'text': "COVID-19 pandemic started in 2015.",
            'description': "Historical accuracy (wrong)"
        },
        {
            'text': "Normal government announcement about policy.",
            'description': "Clean text"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {case['description']}")
        print(f"   Text: \"{case['text']}\"")
        
        result = db.verify(case['text'])
        
        print_result("Verification Level:", result['verification_level'],
                    'green' if result['verification_level'] == 'VERIFIED' else 'yellow')
        print_result("Total Score:", f"{result['total_score']:.2f}")
        print_result("Confidence Impact:", f"{result['confidence_impact']:.2%}")
        
        if result['issues']:
            print("   Issues detected:")
            for issue in result['issues']:
                print(f"     • {issue}")
        else:
            print("   ✓ No issues detected")


def test_double_power_verifier():
    """Test the complete double power system"""
    print_section("TEST 3: Double Power Verification System")
    
    verifier = DoublePowerVerifier()
    
    test_cases = [
        {
            'text': "Scientists reveal 200% effective miracle cure that doctors hate!",
            'cnn_prob': 0.85,  # High fake probability from CNN
            'expected': 'FAKE',
            'description': "Obvious fake news (high CNN, multiple issues)"
        },
        {
            'text': "Government announces new environmental protection research program.",
            'cnn_prob': 0.15,  # Low fake probability from CNN
            'expected': 'REAL',
            'description': "Real news (low CNN, no issues)"
        },
        {
            'text': "COVID-19 started in 2015 and everyone knows this is always true!",
            'cnn_prob': 0.50,  # Uncertain CNN
            'expected': 'FAKE',
            'description': "Fake with historical error + contradiction"
        },
        {
            'text': "Nie uwierzysz! Eksperci odkryli zaskakującą prawdę o szczepionkach!",
            'cnn_prob': 0.75,
            'expected': 'FAKE',
            'description': "Polish fake news with clickbait patterns"
        },
        {
            'text': "Naukowcy przeprowadzili badania dotyczące ochrony środowiska.",
            'cnn_prob': 0.20,
            'expected': 'REAL',
            'description': "Polish real news (neutral language)"
        },
        {
            'text': "New study shows results with proper methodology.",
            'cnn_prob': None,  # No CNN available
            'expected': 'REAL',
            'description': "Verification-only mode (no CNN)"
        }
    ]
    
    total_tests = len(test_cases)
    correct = 0
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {case['description']}")
        print(f"   Text: \"{case['text'][:60]}...\"")
        if case['cnn_prob'] is not None:
            print(f"   CNN Probability: {case['cnn_prob']:.2%} (fake)")
        else:
            print("   CNN Probability: Not available")
        
        result = verifier.verify(case['text'], case['cnn_prob'])
        
        # Check if prediction matches expected
        is_correct = result['verdict'] == case['expected']
        if is_correct:
            correct += 1
        
        verdict_color = 'green' if is_correct else 'red'
        print_result("Verdict:", result['verdict'], verdict_color)
        print_result("Fake Probability:", f"{result['fake_probability']:.2%}")
        print_result("Confidence:", f"{result['confidence']:.2%}")
        print_result("Verification Score:", f"{result['verification_score']:.2f}")
        print_result("Expected:", case['expected'], 'cyan')
        print_result("Match:", "✓ CORRECT" if is_correct else "✗ WRONG", 
                    'green' if is_correct else 'red')
        
        if result['all_issues']:
            print("   Issues detected:")
            for issue in result['all_issues'][:5]:
                print(f"     • {issue}")
    
    # Summary
    print("\n" + "=" * 70)
    accuracy = (correct / total_tests) * 100
    accuracy_color = 'green' if accuracy >= 80 else 'yellow' if accuracy >= 60 else 'red'
    print_result("Total Tests:", total_tests)
    print_result("Correct:", correct)
    print_result("Accuracy:", f"{accuracy:.1f}%", accuracy_color)


def test_api_integration():
    """Test the API (if running)"""
    print_section("TEST 4: API Integration Test")
    
    try:
        import requests
        
        api_url = "http://localhost:8000"
        
        print("Checking API status...")
        try:
            response = requests.get(f"{api_url}/", timeout=5)
            if response.ok:
                data = response.json()
                print("✅ API is online!")
                print(f"   Version: {data.get('version', 'unknown')}")
                print(f"   Models loaded: {', '.join(data.get('models_loaded', []))}")
                
                # Test prediction
                print("\nTesting prediction endpoint...")
                test_text = "Scientists reveal 200% effective cure!"
                pred_response = requests.post(
                    f"{api_url}/predict",
                    json={"text": test_text, "use_double_power": True},
                    timeout=10
                )
                
                if pred_response.ok:
                    result = pred_response.json()
                    print("✅ Prediction successful!")
                    print_result("Text:", test_text[:50])
                    print_result("Prediction:", result['prediction'])
                    print_result("Confidence:", f"{result['confidence']:.2%}")
                    print_result("Method:", result['method'])
                else:
                    print(f"❌ Prediction failed: {pred_response.status_code}")
            else:
                print(f"❌ API returned status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️  API not running")
            print("   Start the API with: python api_double_power.py")
            print("   Or use: .\\start_double_power.ps1")
        except requests.exceptions.Timeout:
            print("❌ API timeout")
    
    except ImportError:
        print("⚠️  'requests' library not installed")
        print("   Install with: pip install requests")
        print("   Skipping API integration test")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🛡️  BANED DOUBLE POWER - TEST SUITE  ".center(68) + "║")
    print("║" + "  Neural Verified Fake News Detection  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        # Run all tests
        test_logical_consistency()
        test_fact_database()
        test_double_power_verifier()
        test_api_integration()
        
        # Final summary
        print("\n")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 68 + "║")
        print("║" + "  ✅ ALL TESTS COMPLETED  ".center(68) + "║")
        print("║" + " " * 68 + "║")
        print("╚" + "═" * 68 + "╝")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
