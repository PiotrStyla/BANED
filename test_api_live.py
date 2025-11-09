#!/usr/bin/env python3
"""Quick test to verify the API is working"""
import requests
import json

API_URL = "http://localhost:8000"

print("🔍 Testing BANED Double Power API...")
print("="*50)

# Test 1: Check API status
print("\n1. Checking API status...")
try:
    response = requests.get(f"{API_URL}/")
    if response.ok:
        data = response.json()
        print(f"✅ API Status: {data['status']}")
        print(f"   Version: {data['version']}")
        print(f"   Models loaded: {data['models_loaded']}")
    else:
        print(f"❌ API returned status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Test prediction
print("\n2. Testing prediction...")
test_text = "Government announces new environmental protection research program."
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": test_text, "use_double_power": True},
        headers={"Content-Type": "application/json"}
    )
    if response.ok:
        data = response.json()
        print(f"✅ Prediction successful!")
        print(f"   Text: {test_text[:50]}...")
        print(f"   Verdict: {data['prediction']}")
        print(f"   Confidence: {data['confidence']*100:.1f}%")
        print(f"   Method: {data['method']}")
        print(f"   Language: {data['language']}")
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Test with fake news
print("\n3. Testing with obvious fake news...")
test_fake = "Scientists reveal 200% effective miracle cure!"
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": test_fake, "use_double_power": True}
    )
    if response.ok:
        data = response.json()
        print(f"✅ Prediction successful!")
        print(f"   Text: {test_fake}")
        print(f"   Verdict: {data['prediction']}")
        print(f"   Confidence: {data['confidence']*100:.1f}%")
        if data.get('verification') and data['verification'].get('all_issues'):
            print(f"   Issues found: {len(data['verification']['all_issues'])}")
            for issue in data['verification']['all_issues'][:3]:
                print(f"     • {issue}")
    else:
        print(f"❌ Prediction failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*50)
print("✅ All tests completed!")
print("\n💡 If all tests passed, the API is working correctly.")
print("   Refresh your browser page (F5) to use the web interface.")
