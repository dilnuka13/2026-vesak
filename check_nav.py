import re
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's see the aside and mobile navigation implementations
aside_match = re.search(r'<aside.*?</aside>', content, re.DOTALL)
if aside_match:
    print("ASIDE:", aside_match.group(0)[:500])

# Print what handles mobile navigation
mobile_nav = re.search(r'<select.*?className="[^"]*?lg:hidden[^"]*?".*?</select>', content, re.DOTALL)
if mobile_nav:
    print("MOBILE NAV:", mobile_nav.group(0)[:500])

bottom_nav = re.search(r'<nav.*?bottom.*?.*?</nav>', content, re.DOTALL)
if bottom_nav:
    print("BOTTOM NAV:", bottom_nav.group(0)[:500])
