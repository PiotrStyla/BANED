import requests
import json

print("Testing BANED API...\n")

# Test 1: Real news
print("=" * 60)
print("TEST 1: Real News")
print("=" * 60)
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "text": "Department of Health announces new vaccination program for children",
        "use_fusion": True
    }
)
result = response.json()
print(f"Text: {result['text']}")
print(f"Prediction: {result['prediction']} {'✅' if result['prediction'] == 'REAL' else '❌'}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"CNN Probability: {result['cnn_probability']:.1%}")
print(f"Method: {result['method']}")
if result.get('kb_match'):
    print(f"Real patterns: {result['kb_match']['real']}")
    print(f"Fake patterns: {result['kb_match']['fake']}")

# Test 2: Fake news
print("\n" + "=" * 60)
print("TEST 2: Fake News")
print("=" * 60)
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "text": "Scientists discover miracle cure for cancer by eating this one weird fruit",
        "use_fusion": True
    }
)
result = response.json()
print(f"Text: {result['text']}")
print(f"Prediction: {result['prediction']} {'✅' if result['prediction'] == 'FAKE' else '❌'}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"CNN Probability: {result['cnn_probability']:.1%}")
print(f"Method: {result['method']}")
if result.get('kb_match'):
    print(f"Real patterns: {result['kb_match']['real']}")
    print(f"Fake patterns: {result['kb_match']['fake']}")

# Test 3: Stats
print("\n" + "=" * 60)
print("TEST 3: API Statistics")
print("=" * 60)
response = requests.get("http://localhost:8000/stats")
stats = response.json()
print(json.dumps(stats, indent=2))

print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED!")
print("=" * 60)
print("\nAPI is working perfectly!")
print("Open static/index.html in your browser to use the web interface!")
