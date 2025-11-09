#!/usr/bin/env python3
"""Fix the verification score bug in logical_consistency.py"""

# Read the file
with open('verification/logical_consistency.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Bug #1: Reverse the verification score logic
old_line = "            adjusted_prediction = 0.5 + (verification_score * 0.08)"
new_line = "            adjusted_prediction = 0.5 - (verification_score * 0.08)  # Fixed: negative score = higher fake prob"

content = content.replace(old_line, new_line)

# Write the fixed file
with open('verification/logical_consistency.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Bug fixed!")
print("   Old: adjusted_prediction = 0.5 + (verification_score * 0.08)")
print("   New: adjusted_prediction = 0.5 - (verification_score * 0.08)")
print("\nNow: Negative score → Higher fake probability → Correct verdict")
