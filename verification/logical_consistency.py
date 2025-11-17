#!/usr/bin/env python3
"""
logical_consistency.py - Logical Consistency Checker for BANED Double Power
Inspired by LIMM's LLM-based reasoning approach
Implements neural verification concepts for sound fake news detection
"""
import re
from typing import Dict, List, Tuple
from datetime import datetime


class LogicalConsistencyChecker:
    """
    Checks logical consistency of news text using multiple verification methods.
    Inspired by LIMM's logical reasoning and neural proof verification.
    """
    
    def __init__(self):
        # Contradiction patterns
        self.contradiction_pairs = [
            (['always', 'constantly', 'invariably'], ['never', 'rarely', 'seldom'], -3.0),
            (['all', 'every', 'everyone'], ['none', 'nobody', 'no one'], -3.0),
            (['increase', 'rise', 'grow'], ['decrease', 'fall', 'decline'], -2.5),
            (['confirm', 'prove', 'verify'], ['deny', 'disprove', 'refute'], -2.5),
            (['zawsze', 'stale'], ['nigdy', 'rzadko'], -3.0),  # Polish
            (['wszyscy', 'każdy'], ['nikt', 'żaden'], -3.0),  # Polish
        ]
        
        # Temporal impossibilities
        self.current_year = datetime.now().year
        
        # Numerical impossibility patterns
        self.numerical_patterns = [
            (r'\b([2-9][0-9]{2}|1[1-9][0-9])%\b', -4.0, "percentage_over_100"),  # >100%
            (r'\b0\.0*%\b', -1.5, "exactly_zero_percent"),
            (r'\b(150|200|250|300) (lat|years old|roku)\b', -5.0, "impossible_age"),
            (r'\b([5-9][0-9]{2}|[1-9][0-9]{3}) (procent|percent)\b', -4.0, "huge_percentage"),
        ]
        
        # Statistical red flags
        self.statistical_flags = [
            (r'\b100% (accurate|effective|success|skuteczny|pewny)\b', -2.0),
            (r'\b0% (risk|failure|ryzyko)\b', -2.0),
            (r'\b(infinity|nieskończony|unlimited|nieograniczony)\b', -1.5),
        ]
        
        # Temporal logic patterns
        self.temporal_patterns = [
            r'\b(yesterday|wczoraj) in (\d{4})\b',
            r'\b(tomorrow|jutro) in (\d{4})\b',
            r'\b(next year|przyszły rok) in (\d{4})\b',
        ]
    
    def check_contradictions(self, text: str) -> Tuple[float, List[str]]:
        """Detect self-contradictions in text"""
        score = 0.0
        issues = []
        text_lower = text.lower()
        
        for positive_words, negative_words, weight in self.contradiction_pairs:
            has_positive = any(word in text_lower for word in positive_words)
            has_negative = any(word in text_lower for word in negative_words)
            
            if has_positive and has_negative:
                score += weight
                issues.append(f"Contradiction detected: {positive_words[0]} vs {negative_words[0]}")
        
        return score, issues
    
    def check_numerical_consistency(self, text: str) -> Tuple[float, List[str]]:
        """Check for impossible numerical claims"""
        score = 0.0
        issues = []
        
        # Check impossible percentages and numbers
        for pattern, weight, issue_type in self.numerical_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                score += weight
                issues.append(f"{issue_type}: {match.group()}")
        
        # Check statistical red flags
        for pattern, weight in self.statistical_flags:
            if re.search(pattern, text, re.IGNORECASE):
                score += weight
                issues.append(f"Statistical red flag: {pattern}")
        
        return score, issues
    
    def check_temporal_logic(self, text: str) -> Tuple[float, List[str]]:
        """Check for temporal inconsistencies"""
        score = 0.0
        issues = []
        
        # Check for temporal contradictions
        for pattern in self.temporal_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                referenced_year = int(match.group(2))
                if abs(referenced_year - self.current_year) > 1:
                    score -= 3.0
                    issues.append(f"Temporal inconsistency: {match.group()}")
        
        # Check for impossible future dates
        future_pattern = r'\b(20\d{2})\b'
        for match in re.finditer(future_pattern, text):
            year = int(match.group(1))
            if year > self.current_year + 1:
                score -= 1.0
                issues.append(f"Suspicious future date: {year}")
        
        return score, issues
    
    def analyze(self, text: str) -> Dict:
        """
        Comprehensive logical consistency analysis.
        Returns detailed verification results.
        """
        contradiction_score, contradiction_issues = self.check_contradictions(text)
        numerical_score, numerical_issues = self.check_numerical_consistency(text)
        temporal_score, temporal_issues = self.check_temporal_logic(text)
        
        total_score = contradiction_score + numerical_score + temporal_score
        all_issues = contradiction_issues + numerical_issues + temporal_issues
        
        # Determine consistency level
        if total_score >= -1.0:
            consistency = "EXCELLENT"
            confidence_impact = 1.0
        elif total_score >= -3.0:
            consistency = "GOOD"
            confidence_impact = 0.95
        elif total_score >= -5.0:
            consistency = "MODERATE"
            confidence_impact = 0.85
        elif total_score >= -8.0:
            consistency = "POOR"
            confidence_impact = 0.70
        else:
            consistency = "VERY_POOR"
            confidence_impact = 0.50
        
        return {
            'total_score': round(total_score, 2),
            'consistency_level': consistency,
            'confidence_impact': confidence_impact,
            'issues': all_issues,
            'breakdown': {
                'contradiction_score': contradiction_score,
                'numerical_score': numerical_score,
                'temporal_score': temporal_score
            }
        }


class EmotionalLanguageDetector:
    """
    Detects emotionally charged language commonly used in fake news.
    """
    
    def __init__(self):
        # Emotional/sensational words
        self.emotional_words = {
            'en': [
                'shocking', 'outrageous', 'devastating', 'horrifying', 'terrifying',
                'unbelievable', 'incredible', 'amazing', 'stunning', 'explosive',
                'bombshell', 'urgent', 'breaking', 'exclusive', 'revealed',
                'exposed', 'secrets', 'hidden truth', 'conspiracy', 'cover-up'
            ],
            'pl': [
                'szokujące', 'oburzające', 'druzgocące', 'przerażające', 'niewiarygodne',
                'niesamowite', 'zdumiewające', 'pilne', 'najnowsze', 'ekskluzywne',
                'ujawnione', 'sekrety', 'ukryta prawda', 'spisek', 'ukrywane'
            ]
        }
        
        # Fear-mongering words
        self.fear_words = {
            'en': ['danger', 'threat', 'risk', 'warning', 'alert', 'crisis', 'disaster'],
            'pl': ['niebezpieczeństwo', 'zagrożenie', 'ryzyko', 'ostrzeżenie', 'alarm', 'kryzys', 'katastrofa']
        }
    
    def analyze(self, text: str) -> Tuple[float, List[str]]:
        """Detect emotional language"""
        score = 0.0
        issues = []
        text_lower = text.lower()
        
        # Count emotional words
        emotional_count = 0
        for lang_words in self.emotional_words.values():
            for word in lang_words:
                if word in text_lower:
                    emotional_count += 1
        
        # Count fear words
        fear_count = 0
        for lang_words in self.fear_words.values():
            for word in lang_words:
                if word in text_lower:
                    fear_count += 1
        
        # Scoring
        if emotional_count >= 3:
            score -= 2.0
            issues.append(f"High emotional language ({emotional_count} emotional words)")
        elif emotional_count >= 2:
            score -= 1.0
            issues.append(f"Moderate emotional language ({emotional_count} emotional words)")
        
        if fear_count >= 2:
            score -= 1.5
            issues.append(f"Fear-mongering language ({fear_count} fear words)")
        
        return score, issues


class StyleDetector:
    """
    Detects style markers typical of fake news (CAPS, excessive punctuation, etc.)
    """
    
    def analyze(self, text: str) -> Tuple[float, List[str]]:
        """Detect suspicious style markers"""
        score = 0.0
        issues = []
        
        # ALL CAPS words detection
        words = text.split()
        caps_words = [w for w in words if w.isupper() and len(w) > 2]
        if len(caps_words) >= 3:
            score -= 2.0
            issues.append(f"Excessive ALL CAPS usage ({len(caps_words)} words)")
        elif len(caps_words) >= 2:
            score -= 1.0
            issues.append(f"Multiple ALL CAPS words ({len(caps_words)} words)")
        
        # Excessive exclamation marks
        exclamation_count = text.count('!')
        if exclamation_count >= 5:
            score -= 2.0
            issues.append(f"Excessive exclamation marks ({exclamation_count})")
        elif exclamation_count >= 3:
            score -= 1.0
            issues.append(f"Multiple exclamation marks ({exclamation_count})")
        
        # Multiple exclamation/question marks in sequence
        if re.search(r'[!?]{3,}', text):
            score -= 1.5
            issues.append("Multiple punctuation marks in sequence (!!!, ???)")
        
        # Excessive emojis
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
        emoji_count = len(re.findall(emoji_pattern, text))
        if emoji_count >= 5:
            score -= 1.0
            issues.append(f"Excessive emoji usage ({emoji_count} emojis)")
        
        return score, issues


class FactDatabase:
    """
    Knowledge base of known facts and impossible claims.
    Neural proof-inspired verification against ground truth.
    """
    
    def __init__(self):
        # Known historical events
        self.historical_facts = {
            'covid-19': {'year': 2019, 'keywords': ['covid', 'coronavirus', 'sars-cov-2']},
            'world war ii': {'year_range': (1939, 1945), 'keywords': ['wwii', 'world war 2']},
            'world war i': {'year_range': (1914, 1918), 'keywords': ['wwi', 'world war 1']},
            '2020 olympics': {'year': 2021, 'keywords': ['olympics 2020'], 'note': 'delayed'},
        }
        
        # Impossible/highly suspicious claims
        self.impossible_claims = [
            # English
            'cures all diseases',
            'works 100% of the time',
            'doctors hate this one trick',
            '200% success rate',
            'never fails',
            'absolute guarantee',
            'miracle cure',
            'secret that they don\'t want you to know',
            'big pharma doesn\'t want you to see this',
            
            # Polish
            'leczy wszystkie choroby',
            'działa w 100% przypadków',
            'lekarze tego nienawidzą',
            'cudowne lekarstwo',
            'tajemnica której nie chcą byś poznał',
            'koncerny farmaceutyczne ukrywają',
        ]
        
        # Scientific impossibilities
        self.scientific_impossibilities = [
            'perpetual motion',
            'free energy',
            'anti-gravity',
            'teleportation',
            'time travel',
            'ruch wieczny',  # Polish
            'darmowa energia',
            'antygrawitacja',
        ]
        
        # Common fake news patterns (expanded)
        self.fake_patterns = [
            # English
            'what they don\'t tell you',
            'what they don\'t want you to know',
            'mainstream media won\'t report',
            'mainstream media is hiding',
            'shocking truth revealed',
            'the truth they hide',
            'you won\'t believe',
            'this will blow your mind',
            'doctors/scientists don\'t want you to know',
            'they are lying to you',
            'wake up people',
            'open your eyes',
            'do your own research',
            'question everything',
            'follow the money',
            'the elite don\'t want',
            'big pharma/tech/media doesn\'t want',
            'censored by',
            'banned by',
            'they deleted this',
            
            # Polish
            'czego ci nie mówią',
            'czego nie chcą żebyś wiedział',
            'media głównego nurtu ukrywają',
            'media ukrywają prawdę',
            'szokująca prawda',
            'prawda której ukrywają',
            'nie uwierzysz',
            'obudź się',
            'otwórz oczy',
            'zbadaj sam',
            'podążaj za pieniędzmi',
            'elity nie chcą',
            'wielkie koncerny nie chcą',
            'cenzurowane przez',
            'usunięte przez',
        ]
    
    def check_impossible_claims(self, text: str) -> Tuple[float, List[str]]:
        """Check for known impossible claims"""
        score = 0.0
        detected = []
        text_lower = text.lower()
        
        for claim in self.impossible_claims:
            if claim in text_lower:
                score -= 4.0
                detected.append(f"Impossible claim: {claim}")
        
        for impossibility in self.scientific_impossibilities:
            if impossibility in text_lower:
                score -= 3.0
                detected.append(f"Scientific impossibility: {impossibility}")
        
        for pattern in self.fake_patterns:
            if pattern in text_lower:
                score -= 2.5
                detected.append(f"Fake pattern: {pattern}")
        
        return score, detected
    
    def check_historical_accuracy(self, text: str) -> Tuple[float, List[str]]:
        """Verify historical facts mentioned in text"""
        score = 0.0
        issues = []
        text_lower = text.lower()
        
        # Extract years from text
        years = [int(y) for y in re.findall(r'\b(19\d{2}|20\d{2})\b', text)]
        
        for event_name, facts in self.historical_facts.items():
            # Check if event is mentioned
            if any(kw in text_lower for kw in facts['keywords']):
                if 'year' in facts:
                    # Check if correct year is mentioned
                    if facts['year'] in years:
                        score += 2.0
                    elif years:  # Wrong year mentioned - stronger penalty
                        score -= 4.0  # Increased from -2.0
                        issues.append(f"Historical inaccuracy: Wrong year for {event_name}")
                
                elif 'year_range' in facts:
                    # Check if any year in range is mentioned
                    start, end = facts['year_range']
                    if any(start <= y <= end for y in years):
                        score += 2.0
                    elif years:
                        score -= 4.0  # Increased from -2.0
                        issues.append(f"Historical inaccuracy: Wrong date range for {event_name}")
        
        return score, issues
    
    def verify(self, text: str) -> Dict:
        """
        Comprehensive fact verification.
        Returns verification results with confidence impact.
        """
        impossible_score, impossible_claims = self.check_impossible_claims(text)
        historical_score, historical_issues = self.check_historical_accuracy(text)
        
        total_score = impossible_score + historical_score
        all_issues = impossible_claims + historical_issues
        
        # Determine verification level
        if total_score >= 0:
            verification = "VERIFIED"
            confidence_impact = 1.0
        elif total_score >= -3.0:
            verification = "MOSTLY_VERIFIED"
            confidence_impact = 0.90
        elif total_score >= -6.0:
            verification = "SUSPICIOUS"
            confidence_impact = 0.75
        else:
            verification = "HIGHLY_SUSPICIOUS"
            confidence_impact = 0.50
        
        return {
            'total_score': round(total_score, 2),
            'verification_level': verification,
            'confidence_impact': confidence_impact,
            'issues': all_issues,
            'breakdown': {
                'impossible_claims_score': impossible_score,
                'historical_accuracy_score': historical_score
            }
        }


class DoublePowerVerifier:
    """
    Double Power Verification System combining:
    1. Neural Network (CNN) - Pattern recognition
    2. Logical Verification - Consistency & fact checking
    
    Inspired by neural proof systems for sound verification.
    """
    
    def __init__(self):
        self.consistency_checker = LogicalConsistencyChecker()
        self.fact_database = FactDatabase()
        self.emotional_detector = EmotionalLanguageDetector()
        self.style_detector = StyleDetector()
    
    def verify(self, text: str, cnn_prediction: float = None) -> Dict:
        """
        Perform double power verification.
        Combines neural network output with logical verification.
        
        Args:
            text: News text to verify
            cnn_prediction: CNN probability (0-1, where 1 = fake)
            
        Returns:
            Comprehensive verification report with final confidence
        """
        # Power 1: Logical Consistency Check
        consistency_results = self.consistency_checker.analyze(text)
        
        # Power 2: Fact Database Verification
        fact_results = self.fact_database.verify(text)
        
        # Additional heuristics: Emotional Language
        emotional_score, emotional_issues = self.emotional_detector.analyze(text)
        
        # Additional heuristics: Style Detection
        style_score, style_issues = self.style_detector.analyze(text)
        
        # Combine all verification powers
        verification_score = (
            consistency_results['total_score'] + 
            fact_results['total_score'] +
            emotional_score +
            style_score
        )
        
        # Calculate combined confidence impact
        combined_confidence_impact = (
            consistency_results['confidence_impact'] * 
            fact_results['confidence_impact']
        )
        
        # Collect all issues
        all_issues = (
            consistency_results['issues'] + 
            fact_results['issues'] +
            emotional_issues +
            style_issues
        )
        
        # If we have CNN prediction, combine it with verification
        if cnn_prediction is not None:
            # Adjust CNN prediction based on verification results
            adjusted_prediction = cnn_prediction * combined_confidence_impact
            
            # If verification found major issues, increase fake probability more aggressively
            if verification_score < -5.0:
                adjusted_prediction = min(1.0, adjusted_prediction + abs(verification_score) * 0.08)
            elif verification_score < -3.0:
                adjusted_prediction = min(1.0, adjusted_prediction + abs(verification_score) * 0.06)
            
            # If verification found positive signals, decrease fake probability
            if verification_score > 2.0:
                adjusted_prediction = max(0.0, adjusted_prediction - abs(verification_score) * 0.05)
            
            final_confidence = abs(adjusted_prediction - 0.5) * 2.0
        else:
            # Verification-only mode: more aggressive scoring
            adjusted_prediction = 0.5 - (verification_score * 0.08)  # Fixed: negative score = higher fake prob
            adjusted_prediction = max(0.0, min(1.0, adjusted_prediction))
            
            # If no issues detected in verification-only mode, bias toward REAL
            if verification_score >= 0 and len(all_issues) == 0:
                adjusted_prediction = 0.35  # Bias toward REAL when no issues
                final_confidence = 0.30
            else:
                final_confidence = abs(adjusted_prediction - 0.5) * 2.0
        
        # Determine final verdict with more decisive thresholds
        if adjusted_prediction > 0.55:  # More decisive (was 0.7)
            verdict = "FAKE"
        elif adjusted_prediction < 0.45:  # More decisive (was 0.3)
            verdict = "REAL"
        else:
            verdict = "UNCERTAIN"
        
        return {
            'verdict': verdict,
            'fake_probability': round(adjusted_prediction, 4),
            'confidence': round(final_confidence, 4),
            'verification_score': round(verification_score, 2),
            'combined_confidence_impact': round(combined_confidence_impact, 4),
            'power_1_consistency': consistency_results,
            'power_2_fact_check': fact_results,
            'emotional_analysis': {
                'score': emotional_score,
                'issues': emotional_issues
            },
            'style_analysis': {
                'score': style_score,
                'issues': style_issues
            },
            'all_issues': all_issues
        }


if __name__ == "__main__":
    # Test the double power verifier
    verifier = DoublePowerVerifier()
    
    # Test cases
    test_texts = [
        "Scientists reveal 200% effective miracle cure that doctors hate!",
        "Government announces new environmental protection research program.",
        "COVID-19 started in 2015 according to mainstream media.",
        "Naukowcy z uniwersytetu ujawniają badania dotyczące ochrony środowiska."
    ]
    
    for text in test_texts:
        print(f"\n{'='*60}")
        print(f"Text: {text}")
        result = verifier.verify(text)
        print(f"Verdict: {result['verdict']}")
        print(f"Fake Probability: {result['fake_probability']:.2%}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Verification Score: {result['verification_score']}")
        if result['all_issues']:
            print("Issues detected:")
            for issue in result['all_issues']:
                print(f"  - {issue}")
