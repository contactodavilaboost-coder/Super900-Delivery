with open('js/cart.js', 'r', encoding='utf-8') as f:
    content = f.read()

btn_html = """<button class="text-on-surface-variant hover:text-error transition-colors p-1 mr-2" title="Vaciar carrito" onclick="if(confirm('¿Seguro que deseas vaciar el carrito?')) window.Cart.clear()"><span class="material-symbols-outlined">delete_sweep</span></button><button id="close-drawer-btn\""""

content = content.replace('<button id="close-drawer-btn"', btn_html)

with open('js/cart.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('Added clear button')
