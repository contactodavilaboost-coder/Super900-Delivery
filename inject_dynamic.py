import os
from bs4 import BeautifulSoup

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Add scripts to body
    body = soup.body
    if body:
        # Check if already injected
        if not soup.find('script', src='js/airtable-config.js'):
            script1 = soup.new_tag('script', src='js/airtable-config.js')
            body.append(script1)
            
        if not soup.find('script', src='js/dynamic_products.js'):
            script2 = soup.new_tag('script', src='js/dynamic_products.js')
            body.append(script2)

    # Find the product grid and add ID
    # Usually it's the grid inside a section that has products.
    # We can look for the div that contains 'article' tags or 'bg-charcoal-surface' tags
    grids = soup.find_all('div', class_=lambda x: x and 'grid' in x and 'gap-' in x)
    
    for g in grids:
        # If it contains product articles or product cards
        if g.find('article') or g.find('div', class_=lambda c: c and 'bg-charcoal-surface' in c):
            g['id'] = 'dynamic-products-grid'
            break

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Dynamic scripts injected successfully.")
