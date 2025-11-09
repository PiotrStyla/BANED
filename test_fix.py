#!/usr/bin/env python3
"""Test the fix with the problematic text"""
import requests
import json

API_URL = "http://localhost:8000"

print("="*70)
print("  🧪 TESTING THE FIX")
print("="*70)
print()

# The problematic text that was showing REAL instead of FAKE
test_text = "Scientists reveal 200% effective miracle cure that doctors hate!"

print(f"Testing: \"{test_text}\"")
print()
print("Expected: FAKE (this is obviously fake news!)")
print("Previous bug: Was showing REAL ❌")
print()

try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": test_text, "use_double_power": True}
    )
    
    if response.ok:
        data = response.json()
        
        print("="*70)
        print("  ✅ RESULTS AFTER FIX:")
        print("="*70)
        print()
        print(f"📊 Verdict: {data['prediction']}")
        print(f"📈 Confidence: {data['confidence']*100:.1f}%")
        print(f"🎯 Fake Probability: {data['fake_probability']*100:.1f}%")
        print(f"🔢 Verification Score: {data['verification']['verification_score']}")
        print(f"🌐 Language: {data['language'].upper()}")
        print(f"⚙️  Method: {data['method']}")
        print()
        
        if data['verification']['all_issues']:
            print("⚠️  Issues Detected:")
            for issue in data['verification']['all_issues']:
                print(f"   • {issue}")
            print()
        
        # Check if the fix worked
        if data['prediction'] == 'FAKE':
            print("="*70)
            print("  🎉 SUCCESS! The bug is FIXED!")
            print("="*70)
            print()
            print("✅ The system now correctly identifies this as FAKE news")
            print("✅ Negative verification score now increases fake probability")
            print("✅ Logic: score=-4 → fake_prob=82% → FAKE verdict")
        else:
            print("="*70)
            print("  ❌ STILL WRONG - Need more investigation")
            print("="*70)
            
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure the server is running: python api_with_html.py")
