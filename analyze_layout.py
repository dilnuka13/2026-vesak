import re

def analyze(filename):
    print(f"--- Analyzing {filename} ---")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if '<aside' in line or '<nav' in line or '<main' in line or 'bottom-0' in line or 'lg:hidden' in line:
            print(f"Line {i+1}: {line.strip()[:100]}")

analyze('index.html')
