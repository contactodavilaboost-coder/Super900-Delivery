import os
import re

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'bebidas.html']

cart_nav_item = """<a class="flex items-center space-x-3 px-4 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-colors relative" href="checkout.html">
    <span class="material-symbols-outlined">shopping_cart</span>
    <span class="font-label-md text-label-md">Carrito</span>
    <span class="cart-badge-counter absolute top-1 left-7 bg-error text-white text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center" style="display: none;">0</span>
</a>"""

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Insert cart button before Mis Pedidos in desktop nav
    if 'shopping_cart' not in html or 'Carrito' not in html:
        # Looking for the hr before Mis Pedidos
        pattern = r'(<hr class="border-glass-border my-4"\s*/>\s*)<a[^>]*href="checkout\.html"[^>]*>.*?Mis Pedidos.*?</a>'
        match = re.search(pattern, html, re.DOTALL)
        if match:
            # We want to replace it by putting the cart BEFORE Mis Pedidos
            # Actually, Mis Pedidos is checkout.html right now. Wait, Cart IS checkout.html!
            # The user wants a "Carrito" button. "Mis Pedidos" is technically the same page right now.
            # We can put "Carrito" and "Mis Pedidos" (maybe we should point Mis Pedidos to a real past orders page later, but for now both point to checkout).
            
            replacement = match.group(1) + cart_nav_item + match.group(0).replace(match.group(1), '')
            html = html.replace(match.group(0), replacement)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

# Fix checkout.html scripts
if os.path.exists('checkout.html'):
    with open('checkout.html', 'r', encoding='utf-8') as f:
        checkout_html = f.read()

    # Remove all scripts at the bottom first to avoid duplicates
    checkout_html = re.sub(r'<script src="js/airtable-config\.js"></script>', '', checkout_html)
    checkout_html = re.sub(r'<script src="js/cart\.js"></script>', '', checkout_html)
    checkout_html = re.sub(r'<script src="js/checkout\.js"></script>', '', checkout_html)

    # Insert them right before </body>
    scripts_to_insert = """
    <script src="js/airtable-config.js"></script>
    <script src="js/cart.js"></script>
    <script src="js/checkout.js"></script>
    </body>
    """
    checkout_html = checkout_html.replace('</body>', scripts_to_insert)

    with open('checkout.html', 'w', encoding='utf-8') as f:
        f.write(checkout_html)

print("Nav bar cart added and checkout.html scripts fixed.")
