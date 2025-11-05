#!/usr/bin/env python3
"""
generate_dataset.py - Generate large-scale fake news datasets with variations
"""
import random
import csv
import argparse


# ============================================================================
# EASY EXAMPLES - Clear distinction
# ============================================================================

EASY_REAL_TEMPLATES = [
    # Government/Politics
    "{department} announces new {policy} for {topic}",
    "Governor signs legislation regarding {topic}",
    "City council approves {policy} plan",
    "State legislature debates {topic} bill",
    "Federal agency releases report on {topic}",
    "Mayor announces initiative to improve {topic}",
    "Senate committee holds hearing on {topic}",
    "Presidential administration proposes {policy} changes",
    
    # Healthcare/Science
    "FDA approves {treatment} for {condition}",
    "CDC issues guidelines for {topic}",
    "Study published in {journal} shows {finding}",
    "Researchers at {university} discover {finding}",
    "Clinical trial demonstrates efficacy of {treatment}",
    "Medical center reports success with {treatment}",
    "Scientists identify new approach to {topic}",
    
    # Education
    "School district implements {policy} program",
    "University announces expansion of {topic} department",
    "Education board approves new {topic} curriculum",
    "College receives grant for {topic} research",
    
    # Business/Economy
    "Company reports quarterly earnings for {topic}",
    "Stock market closes with gains in {sector} sector",
    "Federal Reserve maintains interest rate policy",
    "Trade agreement signed between {country} and partners",
    "Corporation announces expansion in {sector} industry",
    
    # Local News
    "Police department releases crime statistics",
    "Fire department responds to {topic} incident",
    "Library opens new branch in {location}",
    "Park department announces {topic} improvements",
    "Transportation authority updates {topic} schedule",
    "Museum opens exhibit featuring {topic}",
]

EASY_FAKE_TEMPLATES = [
    # Conspiracy/Pseudoscience
    "Secret {organization} hiding truth about {topic}",
    "Doctors hate this one weird trick for {condition}",
    "Government covering up evidence of {topic}",
    "Big pharma suppressing natural cure for {condition}",
    "Illuminati controls {topic} through {method}",
    "Aliens responsible for {topic} says expert",
    "Crystals can cure {condition} naturally",
    
    # Absurd Health Claims
    "Eating {food} cures {condition} instantly",
    "Drinking {beverage} reverses aging process",
    "Sleeping under {object} enhances {ability}",
    "Wearing {item} protects against {threat}",
    "Looking at {object} improves {ability}",
    "{food} contains secret ingredient that {effect}",
    
    # Ridiculous Claims
    "Scientists baffled by {absurd_event}",
    "Man discovers {impossible_thing} in backyard",
    "Woman lives without {basic_need} for {duration}",
    "Child invents {impossible_device} in garage",
    "Local {profession} solves {major_problem} accidentally",
    
    # Conspiracy Economics
    "Banks planning to {evil_plan} your money",
    "Government wants to ban {common_thing}",
    "New world order controlling {topic}",
    "Billionaires plotting to {evil_plan}",
]

# Substitution dictionaries
DEPARTMENTS = ["Department of Transportation", "Health Department", "Department of Education", 
               "Justice Department", "Environmental Protection Agency", "Department of Agriculture"]

POLICIES = ["regulation", "funding", "oversight", "reform", "modernization", "expansion"]

TOPICS = ["infrastructure", "healthcare", "education", "environment", "public safety", 
          "transportation", "housing", "employment", "technology", "energy"]

TREATMENTS = ["medication", "therapy", "procedure", "vaccine", "diagnostic tool", "treatment protocol"]

CONDITIONS = ["heart disease", "diabetes", "cancer", "arthritis", "respiratory illness", 
              "mental health conditions", "chronic pain", "infectious disease"]

JOURNALS = ["New England Journal of Medicine", "The Lancet", "Nature", "Science", "JAMA"]

UNIVERSITIES = ["Stanford University", "MIT", "Harvard University", "Johns Hopkins", "Yale University"]

FINDINGS = ["correlation between lifestyle and health", "new biomarker for disease",
            "improved treatment outcomes", "risk factors for condition"]

SECTORS = ["technology", "healthcare", "finance", "energy", "manufacturing", "retail"]

COUNTRIES = ["United States", "European Union", "China", "Japan", "Canada"]

LOCATIONS = ["downtown", "suburbs", "city center", "residential area", "business district"]

ORGANIZATIONS = ["committee", "council", "agency", "corporation", "foundation"]

METHODS = ["mind control", "satellites", "fluoride", "vaccines", "chemtrails"]

FOODS = ["kale", "coconut oil", "apple cider vinegar", "turmeric", "green tea", "garlic"]

BEVERAGES = ["coffee", "alkaline water", "kombucha", "lemon water", "herbal tea"]

OBJECTS = ["pyramid", "crystal", "magnet", "copper wire", "orgonite"]

ABILITIES = ["brain power", "psychic abilities", "memory", "vision", "intuition"]

THREATS = ["5G radiation", "EMF", "toxins", "negative energy", "bad vibrations"]

ITEMS = ["bracelet", "necklace", "pendant", "amulet", "ring", "hat"]

EFFECTS = ["eliminates toxins", "boosts immunity", "increases energy", "prevents disease"]

IMPOSSIBLE_DEVICES = ["perpetual motion machine", "free energy device", "anti-gravity machine", "teleporter"]

ABSURD_EVENTS = ["man reading terms and conditions", "person enjoying Monday", 
                 "teenager putting phone down", "cat listening to owner"]

IMPOSSIBLE_THINGS = ["perpetual motion machine", "free energy device", "time machine", 
                     "anti-gravity device", "teleportation portal"]

BASIC_NEEDS = ["food", "water", "sleep", "oxygen", "sunlight"]

DURATIONS = ["20 years", "decade", "entire life", "five years", "several months"]

PROFESSIONS = ["plumber", "accountant", "librarian", "baker", "mechanic"]

MAJOR_PROBLEMS = ["climate change", "world hunger", "disease", "poverty", "pollution"]

EVIL_PLANS = ["steal", "control", "monitor", "confiscate", "track"]

COMMON_THINGS = ["coffee", "meat", "cars", "cash", "privacy"]


# ============================================================================
# HARD EXAMPLES - Ambiguous/Clickbait
# ============================================================================

HARD_REAL_TEMPLATES = [
    "You won't believe what {authority} discovered about {topic}",
    "Scientists shocked by unexpected {finding} in {field} research",
    "Study reveals surprising truth about {topic}",
    "Experts warn about alarming trend in {topic}",
    "Revolutionary {technology} promises to change {field}",
    "Breakthrough research challenges conventional wisdom about {topic}",
    "Investigation uncovers disturbing patterns in {topic}",
    "Research reveals counterintuitive findings about {topic}",
    "Analysis shows surprising connection between {topic1} and {topic2}",
    "Researchers observe unusual phenomenon in {field}",
    "Study documents concerning rise in {problem}",
    "Amazing discovery in {field} stuns {experts}",
    "Incredible new study reveals {finding}",
    "This {method} could revolutionize {field}",
]

HARD_FAKE_TEMPLATES = [
    "Study shows {technology} may affect {health_effect}",
    "Experts increasingly concerned about {common_thing}",
    "New research suggests link between {topic1} and {negative_effect}",
    "Scientists debate controversial findings about {topic}",
    "Alternative {profession} report success with {pseudoscience}",
    "Researchers question mainstream narrative about {topic}",
    "Study finds correlation between {common_thing} and {health_effect}",
    "Investigation reveals {authority} may be hiding {secret}",
    "Research suggests mainstream {field} suppresses {alternative}",
    "Experts warn about {common_thing} affecting {health_effect}",
    "Study shows possible connection between {topic1} and {problem}",
    "Investigation uncovers conflicts of interest in {field}",
    "Research team finds evidence of manipulation in {field}",
    "Alternative researchers propose controversial new {theory}",
]

AUTHORITIES = ["researchers", "scientists", "doctors", "experts", "investigators", "specialists"]

FIELDS = ["climate science", "medicine", "physics", "biology", "psychology", "neuroscience"]

TECHNOLOGIES = ["AI system", "medical device", "diagnostic tool", "treatment method", "technology"]

HEALTH_EFFECTS = ["brain activity", "hormone levels", "immune response", "sleep patterns", "cognition"]

NEGATIVE_EFFECTS = ["increased risk", "adverse outcomes", "unexpected complications", "side effects"]

PSEUDOSCIENCES = ["energy healing", "detox protocols", "natural remedies", "ancient practices"]

SECRETS = ["natural cures", "important information", "real data", "actual findings", "truth"]

ALTERNATIVES = ["alternative treatments", "holistic approaches", "natural methods", "traditional wisdom"]

THEORIES = ["hypothesis", "explanation", "model", "framework", "paradigm"]

PROBLEMS = ["chronic disease", "mental health issues", "autoimmune conditions", "disorders"]

EXPERTS_PLURAL = ["researchers", "scientists", "medical professionals", "specialists", "experts"]


# ============================================================================
# EXTREME EXAMPLES - Satire, Propaganda, Context Manipulation
# ============================================================================

EXTREME_REAL_TEMPLATES = [
    # Satire (clearly marked)
    "Satire: {absurd_headline} parody mocks {topic}",
    "Comedy show presents satirical take on {topic}",
    "Humor website publishes obviously fake {story} for entertainment",
    "Parody account tweets absurd {claim} to highlight {issue}",
    
    # Disclosed conflicts
    "{industry} funded study with disclosed conflicts shows {finding}",
    "Research paper clearly states limitations and {disclosure}",
    "Clinical trial results published with transparent {disclosure}",
    "Study acknowledges potential bias from {funding} in discussion",
    
    # Proper context
    "Expert quoted in context explains both {aspect1} and {aspect2}",
    "Doctor statement includes full explanation of {statistical_term}",
    "Researcher clarifies {fallacy} in interview",
    "Scientist emphasizes uncertainty and need for further research",
    
    # Nuanced findings
    "Health data shows mixed outcomes with {nuance}",
    "Study finds nuanced relationship between variables with {condition}",
    "Research demonstrates moderate effect size within {limitation}",
    "Analysis shows modest improvement in some measures but not others",
]

EXTREME_FAKE_TEMPLATES = [
    # Absurd satire (unmarked/misrepresented)
    "Local {profession} {absurd_achievement} shocking revelation",
    "Area {person} still hasn't {mundane_task} breaking news",
    "Nation divided over {trivial_thing} controversy continues",
    
    # Hidden conflicts
    "Study paid for by {industry} finds {convenient_finding}",
    "{industry} sponsored trial shows {product} outperforms alternatives",
    "Corporate backed investigation finds no concerns with {product}",
    "{industry} financed study concludes regulations unnecessary",
    
    # Misleading context
    "Doctor recommends {unnecessary_treatment} for {minor_condition}",
    "One patient had {reaction} so treatment must be dangerous",
    "Anecdotal evidence suggests {unproven_remedy} works",
    "Single study with small sample proves {definitive_claim}",
    
    # Conspiracy framing
    "New study reveals shocking truth {authority} don't want you to know",
    "Research uncovers what big {industry} has been hiding",
    "Investigation exposes mainstream {field} covering up findings",
    "Insider leaks information establishment desperately trying to suppress",
    
    # False equivalence
    "Experts call into question everything we thought we knew about {topic}",
    "Revolutionary approach challenges all conventional {field}",
    "Natural remedy cures {condition} better than any pharmaceutical",
    "Ancient {practice} proves superior to modern {field}",
]

ABSURD_HEADLINES = ["Local man solves world hunger", "Area woman time travels", 
                    "Cat becomes mayor", "Dog learns quantum physics"]

STORIES = ["story about aliens", "tale of miracle", "account of impossibility", "article about absurdity"]

CLAIMS = ["scenario", "statement", "prediction", "observation"]

ISSUES = ["policy contradiction", "logical fallacy", "double standard", "inconsistency"]

INDUSTRIES = ["pharmaceutical", "tobacco", "oil", "chemical", "food"]

DISCLOSURES = ["funding sources", "conflicts of interest", "study limitations", "potential biases"]

ASPECTS = ["benefits", "risks", "uncertainties", "limitations"]

STATISTICAL_TERMS = ["statistical significance", "confidence intervals", "effect size", "correlation"]

FALLACIES = ["correlation does not imply causation", "selection bias", "confounding variables"]

NUANCES = ["context dependent effects", "population specific results", "conditional benefits"]

CONDITIONS_LIMITING = ["specific conditions", "certain populations", "particular contexts"]

LIMITATIONS = ["specific conditions", "controlled environments", "particular populations"]

ACHIEVEMENTS = ["solves poverty", "discovers time travel", "invents perpetual motion"]

PERSONS = ["woman", "man", "teenager", "senior citizen"]

MUNDANE_TASKS = ["replied to email", "finished diet", "organized closet", "read manual"]

TRIVIAL_THINGS = ["gif pronunciation", "pineapple on pizza", "toilet paper orientation"]

CONVENIENT_FINDINGS = ["product is safe", "no health risks", "better than competitors"]

PRODUCTS = ["product", "chemical", "device", "substance"]

UNNECESSARY_TREATMENTS = ["expensive new treatment", "experimental therapy", "premium medication"]

MINOR_CONDITIONS = ["minor symptoms", "common ailment", "slight discomfort"]

REACTIONS = ["adverse reaction", "side effect", "complication"]

UNPROVEN_REMEDIES = ["miracle cure", "ancient remedy", "natural solution"]

DEFINITIVE_CLAIMS = ["definitive conclusion", "absolute truth", "final answer"]

PRACTICES = ["healing method", "traditional practice", "folk remedy", "ancient technique"]


def substitute_template(template, **kwargs):
    """Substitute placeholders in template with random values."""
    # Combine all substitution dictionaries
    all_subs = {
        'department': random.choice(DEPARTMENTS),
        'policy': random.choice(POLICIES),
        'topic': random.choice(TOPICS),
        'treatment': random.choice(TREATMENTS),
        'condition': random.choice(CONDITIONS),
        'journal': random.choice(JOURNALS),
        'university': random.choice(UNIVERSITIES),
        'finding': random.choice(FINDINGS),
        'sector': random.choice(SECTORS),
        'country': random.choice(COUNTRIES),
        'location': random.choice(LOCATIONS),
        'organization': random.choice(ORGANIZATIONS),
        'method': random.choice(METHODS),
        'food': random.choice(FOODS),
        'beverage': random.choice(BEVERAGES),
        'object': random.choice(OBJECTS),
        'item': random.choice(ITEMS),
        'ability': random.choice(ABILITIES),
        'threat': random.choice(THREATS),
        'effect': random.choice(EFFECTS),
        'impossible_device': random.choice(IMPOSSIBLE_DEVICES),
        'absurd_event': random.choice(ABSURD_EVENTS),
        'impossible_thing': random.choice(IMPOSSIBLE_THINGS),
        'basic_need': random.choice(BASIC_NEEDS),
        'duration': random.choice(DURATIONS),
        'profession': random.choice(PROFESSIONS),
        'major_problem': random.choice(MAJOR_PROBLEMS),
        'evil_plan': random.choice(EVIL_PLANS),
        'common_thing': random.choice(COMMON_THINGS),
        'authority': random.choice(AUTHORITIES),
        'field': random.choice(FIELDS),
        'technology': random.choice(TECHNOLOGIES),
        'health_effect': random.choice(HEALTH_EFFECTS),
        'negative_effect': random.choice(NEGATIVE_EFFECTS),
        'pseudoscience': random.choice(PSEUDOSCIENCES),
        'secret': random.choice(SECRETS),
        'alternative': random.choice(ALTERNATIVES),
        'theory': random.choice(THEORIES),
        'problem': random.choice(PROBLEMS),
        'experts': random.choice(EXPERTS_PLURAL),
        'absurd_headline': random.choice(ABSURD_HEADLINES),
        'story': random.choice(STORIES),
        'claim': random.choice(CLAIMS),
        'issue': random.choice(ISSUES),
        'industry': random.choice(INDUSTRIES),
        'disclosure': random.choice(DISCLOSURES),
        'aspect1': ASPECTS[0] if len(ASPECTS) > 0 else "benefits",
        'aspect2': ASPECTS[1] if len(ASPECTS) > 1 else "risks",
        'statistical_term': random.choice(STATISTICAL_TERMS),
        'fallacy': random.choice(FALLACIES),
        'nuance': random.choice(NUANCES),
        'condition': random.choice(CONDITIONS_LIMITING),
        'limitation': random.choice(LIMITATIONS),
        'achievement': random.choice(ACHIEVEMENTS),
        'person': random.choice(PERSONS),
        'mundane_task': random.choice(MUNDANE_TASKS),
        'trivial_thing': random.choice(TRIVIAL_THINGS),
        'convenient_finding': random.choice(CONVENIENT_FINDINGS),
        'product': random.choice(PRODUCTS),
        'unnecessary_treatment': random.choice(UNNECESSARY_TREATMENTS),
        'minor_condition': random.choice(MINOR_CONDITIONS),
        'reaction': random.choice(REACTIONS),
        'unproven_remedy': random.choice(UNPROVEN_REMEDIES),
        'definitive_claim': random.choice(DEFINITIVE_CLAIMS),
        'practice': random.choice(PRACTICES),
        'topic1': random.choice(TOPICS),
        'topic2': random.choice([t for t in TOPICS if len(TOPICS) > 1][:2])[-1] if len(TOPICS) > 1 else random.choice(TOPICS),
        'funding': random.choice(['corporate sponsorship', 'industry funding', 'private donors']),
    }
    
    # Update with any provided kwargs
    all_subs.update(kwargs)
    
    try:
        return template.format(**all_subs)
    except KeyError as e:
        print(f"Warning: Missing key {e} in template: {template}")
        return template


def generate_examples(templates, count):
    """Generate examples from templates."""
    examples = []
    templates_cycle = templates * (count // len(templates) + 1)
    
    for i in range(count):
        template = templates_cycle[i]
        example = substitute_template(template)
        examples.append(example)
    
    return examples


def main():
    parser = argparse.ArgumentParser(description='Generate large-scale fake news dataset')
    parser.add_argument('--easy_real', type=int, default=200, help='Number of easy real examples')
    parser.add_argument('--easy_fake', type=int, default=200, help='Number of easy fake examples')
    parser.add_argument('--hard_real', type=int, default=150, help='Number of hard real examples')
    parser.add_argument('--hard_fake', type=int, default=150, help='Number of hard fake examples')
    parser.add_argument('--extreme_real', type=int, default=150, help='Number of extreme real examples')
    parser.add_argument('--extreme_fake', type=int, default=150, help='Number of extreme fake examples')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    print(f"\n{'='*80}")
    print("GENERATING LARGE-SCALE DATASET")
    print(f"{'='*80}\n")
    
    # Generate EASY examples
    print(f"[1/6] Generating {args.easy_real} EASY REAL examples...")
    easy_real = generate_examples(EASY_REAL_TEMPLATES, args.easy_real)
    
    print(f"[2/6] Generating {args.easy_fake} EASY FAKE examples...")
    easy_fake = generate_examples(EASY_FAKE_TEMPLATES, args.easy_fake)
    
    # Generate HARD examples
    print(f"[3/6] Generating {args.hard_real} HARD REAL examples...")
    hard_real = generate_examples(HARD_REAL_TEMPLATES, args.hard_real)
    
    print(f"[4/6] Generating {args.hard_fake} HARD FAKE examples...")
    hard_fake = generate_examples(HARD_FAKE_TEMPLATES, args.hard_fake)
    
    # Generate EXTREME examples
    print(f"[5/6] Generating {args.extreme_real} EXTREME REAL examples...")
    extreme_real = generate_examples(EXTREME_REAL_TEMPLATES, args.extreme_real)
    
    print(f"[6/6] Generating {args.extreme_fake} EXTREME FAKE examples...")
    extreme_fake = generate_examples(EXTREME_FAKE_TEMPLATES, args.extreme_fake)
    
    # Write to CSV files
    datasets = [
        ('fnn_real_1k.csv', easy_real),
        ('fnn_fake_1k.csv', easy_fake),
        ('fnn_real_hard_1k.csv', hard_real),
        ('fnn_fake_hard_1k.csv', hard_fake),
        ('fnn_extreme_real_1k.csv', extreme_real),
        ('fnn_extreme_fake_1k.csv', extreme_fake),
    ]
    
    for filename, examples in datasets:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['text'])
            for example in examples:
                writer.writerow([example])
        print(f"  ✓ Saved {len(examples)} examples to {filename}")
    
    # Summary
    total = args.easy_real + args.easy_fake + args.hard_real + args.hard_fake + args.extreme_real + args.extreme_fake
    
    print(f"\n{'='*80}")
    print("GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nTotal examples generated: {total}")
    print(f"  • Easy:    {args.easy_real + args.easy_fake} ({args.easy_real} real + {args.easy_fake} fake)")
    print(f"  • Hard:    {args.hard_real + args.hard_fake} ({args.hard_real} real + {args.hard_fake} fake)")
    print(f"  • Extreme: {args.extreme_real + args.extreme_fake} ({args.extreme_real} real + {args.extreme_fake} fake)")
    print(f"\n{'='*80}\n")


if __name__ == '__main__':
    main()
