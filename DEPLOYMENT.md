# BANED - Production Deployment Guide

Complete guide for deploying BANED fake news detection as a REST API with web interface.

## 📋 Prerequisites

```bash
Python 3.8+
pip
```

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Model and Knowledge Base
```bash
# Use existing trained model (10K dataset)
python prepare_deployment.py
```

This will create:
- `models/model.pth` - CNN weights
- `models/vocab.txt` - Vocabulary
- `kb/real_patterns.csv` - Real news patterns
- `kb/fake_patterns.csv` - Fake news patterns

### 3. Start API Server
```bash
python api.py
```

API will be available at: `http://localhost:8000`

### 4. Open Web Interface
Open `static/index.html` in your browser or visit `http://localhost:8000/docs` for API documentation.

---

## 📁 Directory Structure

```
baned-test/
├── api.py                    # FastAPI REST API
├── static/
│   └── index.html            # Web interface
├── models/                   # Model artifacts (created by deployment)
│   ├── model.pth            # CNN weights
│   └── vocab.txt            # Vocabulary
├── kb/                       # Knowledge base (created by deployment)
│   ├── real_patterns.csv    # Real news patterns
│   └── fake_patterns.csv    # Fake news patterns
└── prepare_deployment.py     # Deployment preparation script
```

---

## 🔧 API Endpoints

### Health Check
```bash
GET /
```

Response:
```json
{
  "status": "online",
  "model_loaded": true,
  "kb_loaded": true,
  "version": "3.0.0"
}
```

### Single Prediction
```bash
POST /predict
Content-Type: application/json

{
  "text": "Department announces new policy",
  "use_fusion": true
}
```

Response:
```json
{
  "text": "Department announces new policy",
  "prediction": "REAL",
  "confidence": 0.8523,
  "cnn_probability": 0.9261,
  "kb_match": {
    "real": ["department", "announces"],
    "fake": []
  },
  "method": "fusion"
}
```

### Batch Prediction
```bash
POST /predict/batch
Content-Type: application/json

{
  "texts": ["Text 1", "Text 2", "Text 3"],
  "use_fusion": true
}
```

### Statistics
```bash
GET /stats
```

Response:
```json
{
  "model": {
    "loaded": true,
    "vocabulary_size": 360,
    "device": "cpu"
  },
  "knowledge_base": {
    "loaded": true,
    "real_patterns": 4,
    "fake_patterns": 0,
    "total_patterns": 4
  }
}
```

---

## 🌐 API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 💻 Usage Examples

### Python
```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "text": "Scientists discover new planet",
        "use_fusion": True
    }
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news alert", "use_fusion": true}'
```

### JavaScript (Web)
```javascript
async function analyzNews(text) {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      text: text,
      use_fusion: true
    })
  });
  
  const result = await response.json();
  console.log(result);
}
```

---

## 🔒 Production Deployment

### Option 1: Local Server
```bash
# Start with custom host/port
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Option 2: Docker (Recommended)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t baned-api .
docker run -p 8000:8000 baned-api
```

### Option 3: Cloud Platforms

#### Heroku
```bash
# Procfile
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

#### AWS Lambda (with Mangum)
```python
from mangum import Mangum
handler = Mangum(app)
```

#### Google Cloud Run
```bash
gcloud run deploy baned-api \
  --source . \
  --platform managed \
  --region us-central1
```

---

## ⚙️ Configuration

### Environment Variables
```bash
# API Configuration
export API_HOST="0.0.0.0"
export API_PORT=8000

# Model Configuration
export MODEL_DIR="models"
export KB_DIR="kb"

# MC Dropout samples for prediction
export MC_SAMPLES=10
```

### Custom Model
To use a different trained model:

1. Train model with your data
2. Save model: `torch.save(model.state_dict(), 'models/custom_model.pth')`
3. Save vocabulary: Create `models/vocab.txt` with one word per line
4. Update patterns: Place CSVs in `kb/` directory
5. Restart API

---

## 📊 Performance Optimization

### 1. GPU Acceleration
```python
# In api.py, change:
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

### 2. Batch Processing
Use `/predict/batch` endpoint for multiple texts

### 3. Caching
Add Redis for frequent queries:
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="baned-cache")
```

### 4. Load Balancing
Use Nginx or load balancer for multiple instances:
```nginx
upstream baned_api {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}
```

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host http://localhost:8000
```

### API Testing
```bash
# Test health
curl http://localhost:8000/

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Test news", "use_fusion": true}'
```

---

## 🔍 Monitoring

### Logging
API logs to console by default. Configure logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Metrics
Add Prometheus metrics:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### Health Checks
```bash
# Kubernetes liveness probe
livenessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
```

---

## ❓ Troubleshooting

### Model Not Loading
```
Error: Model not loaded

Solution:
1. Check models/model.pth exists
2. Check models/vocab.txt exists
3. Verify file permissions
4. Check console logs for errors
```

### KB Not Loading
```
Warning: Failed to load KB

Solution:
1. Check kb/real_patterns.csv exists
2. Check kb/fake_patterns.csv exists
3. Verify CSV format (pattern,support)
4. KB is optional, API works without it
```

### CORS Errors
```
Error: CORS policy blocked

Solution: Already configured in api.py
If using reverse proxy, add:
add_header Access-Control-Allow-Origin *;
```

### Port Already in Use
```
Error: Address already in use

Solution:
uvicorn api:app --port 8001
```

---

## 📈 Scaling

### Horizontal Scaling
```bash
# Start multiple instances
uvicorn api:app --port 8000 &
uvicorn api:app --port 8001 &
uvicorn api:app --port 8002 &
```

### Load Balancer
```python
# Use Gunicorn with multiple workers
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔐 Security

### API Keys
```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/predict")
async def predict(request: PredictionRequest, api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ... prediction logic
```

### Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(request: Request, prediction: PredictionRequest):
    # ... prediction logic
```

---

## 📚 Additional Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com
- **PyTorch Deployment:** https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html
- **Uvicorn:** https://www.uvicorn.org
- **BANED Research:** https://github.com/PiotrStyla/BANED

---

## 🆘 Support

Issues or questions?
- **GitHub Issues:** https://github.com/PiotrStyla/BANED/issues
- **Documentation:** See README.md
- **API Docs:** http://localhost:8000/docs (when running)

---

**Version:** 3.0.0  
**Last Updated:** November 2025  
**Status:** ✅ Production Ready
