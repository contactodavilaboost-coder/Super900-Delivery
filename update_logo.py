import os
from bs4 import BeautifulSoup

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'checkout.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Update logo
    for img in soup.find_all('img'):
        if img.get('alt') == 'Super900 Logo':
            img['src'] = 'image.png'
            
    # Remove "Premium Selection" text
    for p in soup.find_all('p'):
        if p.get_text() and 'Premium Selection' in p.get_text():
            p.decompose()

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Logo and text updated successfully.")
