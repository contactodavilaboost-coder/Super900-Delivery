import os
import re
from bs4 import BeautifulSoup

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Fix badges
    for span in soup.find_all('span'):
        if span.string and span.string.strip() == '0' and 'bg-error' in span.get('class', []):
            if 'cart-badge-counter' not in span['class']:
                span['class'] = span.get('class', []) + ['cart-badge-counter']
        elif span.string and span.string.strip() == '0' and 'bg-secondary' in span.get('class', []):
            if 'cart-badge-counter' not in span['class']:
                span['class'] = span.get('class', []) + ['cart-badge-counter']

    # Add Carrito to Side Navbar (Desktop)
    # The side nav has "Mis Pedidos"
    navs = soup.find_all('nav', class_=lambda c: c and 'flex-col' in c and 'fixed' in c)
    for nav in navs:
        # Check if Carrito already exists
        if not nav.find('span', string='shopping_cart') or not nav.find('span', string='Carrito'):
            # Find Mis Pedidos
            mis_pedidos = nav.find('a', href=re.compile(r'checkout\.html'))
            if mis_pedidos and mis_pedidos.parent:
                cart_btn = soup.new_tag('a', href='checkout.html', **{'class': 'flex items-center space-x-3 px-4 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-colors relative'})
                
                icon = soup.new_tag('span', **{'class': 'material-symbols-outlined'})
                icon.string = 'shopping_cart'
                cart_btn.append(icon)
                
                text = soup.new_tag('span', **{'class': 'font-label-md text-label-md'})
                text.string = 'Carrito'
                cart_btn.append(text)
                
                badge = soup.new_tag('span', **{'class': 'cart-badge-counter absolute top-1 left-7 bg-error text-white text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center', 'style': 'display: none;'})
                badge.string = '0'
                cart_btn.append(badge)
                
                mis_pedidos.insert_before(cart_btn)

    # Ensure all shopping cart buttons redirect to checkout
    for btn in soup.find_all('button'):
        if btn.find('span', string='shopping_cart'):
            btn['onclick'] = "window.location.href='checkout.html'"
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))


# Fix Checkout JS resilience
if os.path.exists('js/checkout.js'):
    with open('js/checkout.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    # Change getElementById('cart-drawer-copy') to a more generic selector in case ID was lost
    js = js.replace("document.getElementById('cart-drawer-copy')", "document.getElementById('cart-drawer-copy') || document.querySelector('.lg\\\\:w-\\\\[480px\\\\]') || document.querySelector('.h-full.bg-charcoal-surface.flex.flex-col')")
    
    with open('js/checkout.js', 'w', encoding='utf-8') as f:
        f.write(js)

print("UI fixes applied successfully.")
