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
                "version": "4.1.0-vercel",
                "status": "online",
                "mode": "heuristic-analysis",
                "features": [
                    "Heuristic Pattern Detection",
                    "Logical Consistency Checking",
                    "Fake News Pattern Recognition",
                    "Bilingual (PL/EN)",
                    "Enhanced Polish Detection"
                ],
                "note": "Stage 1: Heuristic analysis (patterns, logic, language) - NOT fact verification"
            }
            
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "heuristic_analysis_active": True,
                "pattern_detection_enabled": True,
                "mode": "serverless"
            }
            
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/examples' or self.path == '/api/examples':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "polish": {
                    "real": [
                        "Ministerstwo Zdrowia ogłosiło nowy program profilaktyki zdrowotnej dla dzieci.",
                        "Uniwersytet Warszawski opublikował wyniki badań nad zmianami klimatu.",
                        "Rada Ministrów przyjęła ustawę o ochronie środowiska.",
                        "Narodowy Bank Polski przedstawił raport o inflacji.",
                        "Minister edukacji zapowiedział reformę systemu egzaminów."
                    ],
                    "fake": [
                        "Bill Gates ukrywa mikroczapy w szczepionkach! Naukowcy potwierdzają!",
                        "Rząd ukrywa prawdę o chemtrails! Tajna operacja nad Polską!",
                        "Nie do wiary! Ten jeden sposób leczy wszystkie choroby!",
                        "Bruksela ukrywa szokującą prawdę! Udostępnij zanim usuną!",
                        "Lekarze tego nienawidzą! Schudnij bez wysiłku w 3 dni!"
                    ]
                },
                "english": {
                    "real": [
                        "The Department of Health announced new healthcare guidelines today.",
                        "Scientists at MIT published groundbreaking research on renewable energy.",
                        "The Senate passed legislation to improve infrastructure funding.",
                        "University researchers discovered new species in the Amazon.",
                        "Federal Reserve announced interest rate decision."
                    ],
                    "fake": [
                        "Doctors hate this one weird trick that cures everything!",
                        "BREAKING: Government admits aliens are real! Click to learn more!",
                        "Miracle cure discovered! Big Pharma doesn't want you to know!",
                        "Share before they delete this! The truth they hide!",
                        "Lose weight without exercise! 200% guaranteed results!"
                    ]
                }
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
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
                # Build explanation
                explanation = [
                    "⚠️ Stage 1: Heuristic Analysis (patterns, logic, language)",
                    "This is NOT fact verification - it detects suspicious patterns",
                    f"Result: {result['verdict']} (score: {result['verification_score']})",
                    f"Logical Consistency: {result['power_1_consistency']['consistency_level']}",
                    f"Pattern Detection: {result['power_2_fact_check']['verification_level']}"
                ]
                
                # Add Stage 2 info if available
                if result.get('stage2_enabled') and result.get('stage2_fact_verification'):
                    stage2 = result['stage2_fact_verification']
                    explanation.append("")
                    explanation.append("🔬 Stage 2: Fact Verification (Wikipedia-based)")
                    explanation.append(f"Status: {stage2['status']}")
                    explanation.append(f"Checked {stage2['total_checks']} facts: {stage2['verified_count']} verified, {stage2['contradicted_count']} contradicted")
                    
                    # Show contradicted facts
                    if stage2['contradicted_count'] > 0:
                        for check in stage2['checks']:
                            if check['status'] == 'contradicted':
                                explanation.append(f"  ❌ {check['topic']}: {check['detail']}")
                
                response = {
                    "text": text[:200],
                    "prediction": result['verdict'],
                    "confidence": result['confidence'],
                    "fake_probability": result['fake_probability'],
                    "language": lang,
                    "method": "HEURISTIC_ANALYSIS" if not result.get('stage2_enabled') else "STAGE1+STAGE2",
                    "cnn_score": None,
                    "verification": result,
                    "explanation": explanation
                }
                
                if result['all_issues']:
                    response['explanation'].append(f"")
                    response['explanation'].append(f"⚠️ Issues found: {len(result['all_issues'])}")
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
