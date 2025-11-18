#!/usr/bin/env python3
"""
fact_checker.py - Stage 2: Fact Verification Module for BANED
Checks claims against knowledge base with transparent source attribution
"""
import json
import re
import os
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class FactChecker:
    """
    Stage 2: Fact Verification
    Checks specific claims against a knowledge base (Wikipedia-sourced facts)
    with transparent source attribution.
    """
    
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """Initialize fact checker with knowledge base"""
        if knowledge_base_path is None:
            # Default path relative to this file
            base_dir = Path(__file__).parent.parent
            knowledge_base_path = base_dir / "knowledge_base.json"
        
        self.knowledge_base_path = knowledge_base_path
        self.facts = []
        self.kb_info = {}
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load knowledge base from JSON file"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.facts = data.get('facts', [])
                self.kb_info = {
                    'version': data.get('knowledge_base_version', 'unknown'),
                    'reference_date': data.get('reference_date', 'unknown'),
                    'philosophy': data.get('interpretation_philosophy', '')
                }
                print(f"✓ Loaded {len(self.facts)} facts from knowledge base")
        except FileNotFoundError:
            print(f"⚠ Knowledge base not found at {self.knowledge_base_path}")
            self.facts = []
        except json.JSONDecodeError as e:
            print(f"⚠ Error parsing knowledge base: {e}")
            self.facts = []
    
    def extract_years(self, text: str) -> List[int]:
        """Extract year mentions from text"""
        # Match 4-digit years (1000-2999)
        years = re.findall(r'\b([12]\d{3})\b', text)
        return [int(y) for y in years]
    
    def extract_numbers(self, text: str) -> List[float]:
        """Extract numerical values from text"""
        # Match integers and decimals
        numbers = re.findall(r'\b(\d+\.?\d*)\b', text)
        return [float(n) for n in numbers if len(n) <= 10]  # Avoid matching years as numbers
    
    def check_fact(self, text: str) -> Tuple[List[Dict], float]:
        """
        Check text against knowledge base facts.
        Returns: (list of checks, verification score)
        """
        text_lower = text.lower()
        checks = []
        score = 0.0
        
        # Extract potential claims
        mentioned_years = self.extract_years(text)
        mentioned_numbers = self.extract_numbers(text)
        
        # Check each fact in knowledge base
        for fact in self.facts:
            keywords = fact.get('keywords', [])
            
            # Check if any keyword is mentioned
            keyword_matches = [kw for kw in keywords if kw.lower() in text_lower]
            
            if not keyword_matches:
                continue  # Fact not relevant to this text
            
            # Fact is potentially relevant
            check_result = {
                'fact_id': fact['id'],
                'topic': fact['topic'],
                'statement': fact['statement'],
                'source': fact['source'],
                'controversy_level': fact['controversy_level'],
                'interpretation_note': fact.get('interpretation_note', ''),
                'matched_keywords': keyword_matches,
                'status': 'mentioned',  # mentioned, verified, contradicted, unclear
                'detail': ''
            }
            
            # Perform specific checks based on claim type
            claim_type = fact.get('claim_type')
            
            if claim_type == 'date_range' or claim_type == 'date':
                # Check if years match
                fact_years = []
                if 'start_year' in fact['value']:
                    fact_years.append(fact['value']['start_year'])
                if 'end_year' in fact['value']:
                    fact_years.append(fact['value']['end_year'])
                if 'emergence_year' in fact['value']:
                    fact_years.append(fact['value']['emergence_year'])
                
                if mentioned_years:
                    matching_years = [y for y in mentioned_years if y in fact_years]
                    wrong_years = [y for y in mentioned_years if y not in fact_years and abs(y - max(fact_years)) <= 50]
                    
                    if matching_years:
                        check_result['status'] = 'verified'
                        check_result['detail'] = f"Correct year(s): {matching_years}"
                        score += 2.0
                    elif wrong_years:
                        check_result['status'] = 'contradicted'
                        check_result['detail'] = f"Incorrect year(s): {wrong_years}. Expected: {fact_years}"
                        score -= 3.0
                    else:
                        check_result['status'] = 'mentioned'
                        check_result['detail'] = "Topic mentioned without specific date"
            
            elif claim_type == 'measurement':
                # Check if numbers are close to expected values
                expected_value = None
                tolerance = 0.0
                
                if 'meters_per_second' in fact['value']:
                    expected_value = fact['value']['meters_per_second'] / 1000000  # Convert to comparable
                    tolerance = expected_value * 0.05  # 5% tolerance
                elif 'celsius' in fact['value']:
                    expected_value = fact['value']['celsius']
                    tolerance = 2.0  # 2 degree tolerance
                elif 'meters_per_second_squared' in fact['value']:
                    expected_value = fact['value']['meters_per_second_squared']
                    tolerance = 0.2
                
                if expected_value and mentioned_numbers:
                    close_numbers = [n for n in mentioned_numbers if abs(n - expected_value) <= tolerance]
                    if close_numbers:
                        check_result['status'] = 'verified'
                        check_result['detail'] = f"Correct value mentioned: {close_numbers}"
                        score += 1.5
                    else:
                        check_result['status'] = 'mentioned'
                        check_result['detail'] = "Topic mentioned without specific measurement"
            
            elif claim_type == 'count':
                # Check specific counts
                expected_count = fact['value'].get('count')
                if expected_count and mentioned_numbers:
                    if expected_count in mentioned_numbers:
                        check_result['status'] = 'verified'
                        check_result['detail'] = f"Correct count: {expected_count}"
                        score += 1.5
                    else:
                        nearby_counts = [n for n in mentioned_numbers if abs(n - expected_count) <= 3]
                        if nearby_counts:
                            check_result['status'] = 'contradicted'
                            check_result['detail'] = f"Incorrect count: {nearby_counts}. Expected: {expected_count}"
                            score -= 2.0
            
            elif claim_type == 'definition':
                # For definitions, just note that topic was mentioned
                # More sophisticated NLP would be needed for full verification
                check_result['status'] = 'mentioned'
                check_result['detail'] = f"Topic mentioned. This is a {fact['controversy_level']} controversy topic."
                if fact['controversy_level'] == 'high':
                    check_result['detail'] += " See interpretation note."
            
            checks.append(check_result)
        
        return checks, score
    
    def verify(self, text: str) -> Dict:
        """
        Main verification method.
        Returns comprehensive fact check results.
        """
        checks, score = self.check_fact(text)
        
        # Categorize results
        verified = [c for c in checks if c['status'] == 'verified']
        contradicted = [c for c in checks if c['status'] == 'contradicted']
        mentioned = [c for c in checks if c['status'] == 'mentioned']
        
        # Determine overall status
        if contradicted:
            status = "CONTRADICTIONS_FOUND"
        elif verified:
            status = "FACTS_VERIFIED"
        elif mentioned:
            status = "RELEVANT_TOPICS"
        else:
            status = "NO_CHECKABLE_CLAIMS"
        
        return {
            'status': status,
            'fact_check_score': round(score, 2),
            'total_checks': len(checks),
            'verified_count': len(verified),
            'contradicted_count': len(contradicted),
            'mentioned_count': len(mentioned),
            'checks': checks,
            'knowledge_base_info': self.kb_info
        }


if __name__ == "__main__":
    # Test the fact checker
    checker = FactChecker()
    
    test_texts = [
        "World War II started in 1939 and ended in 1945.",
        "COVID-19 pandemic began in 2015 according to reports.",
        "There are 9 planets in the solar system including Pluto.",
        "Human body temperature is normally around 37 degrees Celsius.",
        "The speed of light is approximately 300,000 kilometers per second.",
        "This is just a random text without any checkable claims."
    ]
    
    for text in test_texts:
        print(f"\n{'='*70}")
        print(f"Text: {text}")
        result = checker.verify(text)
        print(f"Status: {result['status']}")
        print(f"Score: {result['fact_check_score']}")
        print(f"Checks: {result['total_checks']} (verified: {result['verified_count']}, contradicted: {result['contradicted_count']})")
        
        if result['checks']:
            for check in result['checks']:
                print(f"\n  📌 {check['topic']}: {check['status'].upper()}")
                print(f"     {check['detail']}")
                if check['status'] in ['verified', 'contradicted']:
                    print(f"     Source: {check['source']['url']}")
