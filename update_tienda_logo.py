import os
from bs4 import BeautifulSoup

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'checkout.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove "Tienda"
    for a in soup.find_all('a'):
        text = a.get_text().strip()
        if 'Tienda' in text:
            a.decompose()

    # Link logo to index.html
    for img in soup.find_all('img'):
        if img.get('alt') == 'Super900 Logo':
            # Check if parent is already an 'a' tag
            if img.parent.name == 'a':
                img.parent['href'] = 'index.html'
            else:
                # Wrap the image in an a tag
                a_tag = soup.new_tag('a', href='index.html')
                img.wrap(a_tag)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Tienda removed and logo linked successfully.")
