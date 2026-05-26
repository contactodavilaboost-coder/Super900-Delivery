import os
from bs4 import BeautifulSoup

files = ['carnes.html', 'verduras.html', 'despensa.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Look for buttons that contain "Cereales Premium"
    for button in soup.find_all('button'):
        if button.string and 'Cereales Premium' in button.string:
            # The parent of this button is the div we want to remove
            parent_div = button.find_parent('div')
            if parent_div and 'overflow-x-auto' in parent_div.get('class', []):
                parent_div.decompose()
                print(f"Removed filters from {file}")
            break

    # Also remove the <!-- Category Filters (Glassmorphic Pills) --> comment if possible
    # We will just write it back, beautifulsoup might leave the comment but it doesn't hurt

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
