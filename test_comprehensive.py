#!/usr/bin/env python3
"""Comprehensive test of the fixed system"""
import requests

API_URL = "http://localhost:8000"

test_cases = [
    {
        "text": "Scientists reveal 200% effective miracle cure that doctors hate!",
        "expected": "FAKE",
        "reason": "Impossible %, miracle cure, doctors hate pattern"
    },
    {
        "text": "Government announces new environmental protection research program.",
        "expected": "REAL",
        "reason": "Normal government announcement, no red flags"
    },
    {
        "text": "COVID-19 pandemic started in 2015 according to experts.",
        "expected": "FAKE",
        "reason": "Historical inaccuracy (COVID-19 = 2019)"
    },
    {
        "text": "This miracle cure works 100% of the time with 0% side effects!",
        "expected": "FAKE",
        "reason": "Impossible claims, miracle cure"
    },
    {
        "text": "University researchers conduct study on climate change impacts.",
        "expected": "REAL",
        "reason": "Legitimate research announcement"
    }
]

print("="*70)
print("  🧪 COMPREHENSIVE TESTING AFTER FIX")
print("="*70)
print()

passed = 0
failed = 0

for i, case in enumerate(test_cases, 1):
    print(f"\n{'─'*70}")
    print(f"Test {i}: {case['text'][:60]}...")
    print(f"Expected: {case['expected']}")
    print(f"Reason: {case['reason']}")
    
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": case['text'], "use_double_power": True}
        )
        
        if response.ok:
            data = response.json()
            result = data['prediction']
            
            if result == case['expected']:
                print(f"✅ PASS: Got {result} (confidence: {data['confidence']*100:.1f}%)")
                passed += 1
            else:
                print(f"❌ FAIL: Got {result}, expected {case['expected']}")
                print(f"   Fake prob: {data['fake_probability']*100:.1f}%")
                print(f"   Verification: {data['verification']['verification_score']}")
                failed += 1
        else:
            print(f"❌ API Error: {response.status_code}")
            failed += 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        failed += 1

print()
print("="*70)
print(f"  📊 FINAL RESULTS: {passed}/{len(test_cases)} PASSED")
print("="*70)

if failed == 0:
    print()
    print("🎉 ALL TESTS PASSED! The system is working correctly!")
    print()
    print("✅ Bug Fix Verified:")
    print("   • Negative verification scores now correctly identify fake news")
    print("   • Real news is still correctly identified")
    print("   • Historical inaccuracies are caught")
    print("   • Impossible claims are detected")
else:
    print()
    print(f"⚠️  {failed} test(s) failed - review needed")
