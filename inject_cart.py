import os
from bs4 import BeautifulSoup

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'bebidas.html', 'checkout.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Add cart.js script before body closes
    body = soup.body
    if body:
        if not soup.find('script', src='js/cart.js'):
            script = soup.new_tag('script', src='js/cart.js')
            body.append(script)

    # Find the hardcoded "2" badge and add 'cart-badge-counter' class
    # <span class="absolute -top-1 -right-1 bg-secondary text-on-secondary text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center">2</span>
    for span in soup.find_all('span'):
        if span.string and span.string.strip() == '2':
            classes = span.get('class', [])
            if 'bg-secondary' in classes and 'absolute' in classes:
                if 'cart-badge-counter' not in classes:
                    classes.append('cart-badge-counter')
                span['class'] = classes
                span.string = '0' # default
                span['style'] = 'display: none;'

    # Find bottom nav "Carrito" and add a badge to it!
    # <span class="material-symbols-outlined">shopping_basket</span>
    for nav in soup.find_all('nav'):
        if 'bottom-0' in nav.get('class', []):
            for a in nav.find_all('a'):
                if a.find('span', text='shopping_basket') or a.find('span', string=lambda s: s and 'shopping_basket' in s):
                    # add absolute position to the anchor
                    if 'relative' not in a.get('class', []):
                        a['class'] = a.get('class', []) + ['relative']
                    
                    # check if it already has a badge
                    if not a.find('span', class_='cart-badge-counter'):
                        badge = soup.new_tag('span')
                        badge['class'] = 'cart-badge-counter absolute top-0 right-2 bg-error text-white text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center'
                        badge['style'] = 'display: none;'
                        badge.string = '0'
                        a.append(badge)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("cart.js injected and badges configured.")
