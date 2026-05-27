import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    # Skip checkout.html because in checkout we might want the cart buttons to just stay there or not be modified
    # Actually, in checkout.html, it's fine if the cart button opens the drawer too, or we leave it.
    if file == 'checkout.html':
        continue
        
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix the top right button with onclick
    html = html.replace(
        '''onclick="window.location.href='checkout.html'"''',
        '''onclick="window.Cart.openDrawer()"'''
    )

    # 2. Fix the SideNav cart link
    # The SideNav has: <a class="..." href="checkout.html"><span class="material-symbols-outlined">shopping_cart</span>...
    # We replace href="checkout.html" with href="javascript:void(0)" onclick="window.Cart.openDrawer()" IF it contains shopping_cart
    
    # We can use a regex to find all <a ... href="checkout.html" ... shopping_cart ...> 
    # But it's easier to just replace all checkout.html links that have the cart badge or shopping_cart icon
    # Since we only want checkout to be reached from the drawer's "Ir a Pagar" button, we can just replace ALL `href="checkout.html"` in the navigation.
    # The only link that SHOULD go to checkout.html is inside the drawer (which is injected via JS, so it's not in the HTML files!).
    # Wait, the "Mis Pedidos" link goes to checkout.html too in the original code? 
    # "<a class="... href="checkout.html"><span ...>receipt_long</span>" -> no, it shouldn't. But let's only fix the cart ones.

    html = html.replace(
        '''href="checkout.html"''',
        '''href="javascript:void(0)" onclick="window.Cart.openDrawer()"'''
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
        
print("Cart buttons fixed in all HTML files.")
