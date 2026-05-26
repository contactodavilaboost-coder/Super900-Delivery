import os
from bs4 import BeautifulSoup

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'checkout.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements that might contain "Snacks" in the navigation
    for a in soup.find_all('a'):
        # Check span inside a
        for span in a.find_all('span', class_='font-label-md'):
            if span.string and span.string.strip() == 'Snacks':
                span.string = 'Despensa'

    # Additionally, check the category filter pills if any still say "Snacks"
    for button in soup.find_all('button'):
        if button.string and button.string.strip() == 'Snacks':
            # Only change if it makes sense, maybe in despensa.html
            pass # The user specifically asked to change the page name/sidebar "Snacks" to "Despensa". Let's stick to the nav spans.

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Renamed Snacks to Despensa successfully.")
