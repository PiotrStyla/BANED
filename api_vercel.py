#!/usr/bin/env python3
"""
Vercel-compatible API for BANED Double Power
Serverless deployment without PyTorch (verification-only mode)
"""
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add verification module to path
sys.path.insert(0, os.path.dirname(__file__))

# Import only the verification components (no PyTorch needed)
from verification.logical_consistency import DoublePowerVerifier

# Initialize verifier
verifier = DoublePowerVerifier()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "name": "BANED Double Power API",
                "version": "4.0.0-vercel",
                "status": "online",
                "mode": "verification-only",
                "features": [
                    "Logical Consistency Checking",
                    "Fact Database Verification",
                    "Double Power Verification",
                    "Bilingual (PL/EN)"
                ],
                "note": "Running in serverless mode (verification-only, no CNN models)"
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "verification_active": True,
                "double_power_enabled": True,
                "mode": "serverless"
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/predict' or self.path == '/api/predict':
            try:
                # Read request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Get text from request
                text = data.get('text', '')
                
                if not text or len(text) < 10:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "error": "Text too short (min 10 characters)"
                    }).encode())
                    return
                
                # Detect language
                lang = self._detect_language(text)
                
                # Run verification (no CNN in serverless mode)
                result = verifier.verify(text, cnn_prediction=None)
                
                # Build response
                response = {
                    "text": text[:200],
                    "prediction": result['verdict'],
                    "confidence": result['confidence'],
                    "fake_probability": result['fake_probability'],
                    "language": lang,
                    "method": "VERIFICATION_ONLY",
                    "cnn_score": None,
                    "verification": result,
                    "explanation": [
                        f"Verification: {result['verdict']} (score: {result['verification_score']})",
                        f"Consistency: {result['power_1_consistency']['consistency_level']}",
                        f"Fact Check: {result['power_2_fact_check']['verification_level']}"
                    ]
                }
                
                if result['all_issues']:
                    response['explanation'].append(f"Issues found: {len(result['all_issues'])}")
                    for issue in result['all_issues'][:3]:
                        response['explanation'].append(f"  • {issue}")
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": str(e)
                }).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _detect_language(self, text):
        """Simple language detection"""
        import re
        
        polish_chars = set('ąćęłńóśźż')
        polish_words = {
            'jest', 'się', 'nie', 'że', 'jak', 'ale', 'dla', 'jego', 'przez',
            'na', 'do', 'po', 'przed', 'bardzo', 'może', 'tylko'
        }
        
        text_lower = text.lower()
        
        # Check for Polish diacritics
        if any(char in polish_chars for char in text_lower):
            return 'pl'
        
        # Check for common Polish words
        words = set(re.findall(r'\b\w+\b', text_lower))
        polish_word_count = len(words & polish_words)
        
        if polish_word_count >= 2 or (polish_word_count > 0 and len(words) < 10):
            return 'pl'
        
        return 'en'
