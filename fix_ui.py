import os
import re

html_files = ['bebidas.html', 'carnes.html', 'despensa.html', 'verduras.html']

for file in html_files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove floating button
    # The floating button looks like: <div class="hidden lg:flex fixed bottom-8 right-8 z-50">...</div>
    floating_btn_regex = r'<div class="hidden lg:flex fixed bottom-8 right-8 z-50">.*?</div>'
    html = re.sub(floating_btn_regex, '', html, flags=re.DOTALL)

    # 2. Fix the stuck badge in category pages
    # The stuck badge is: <span class="absolute -top-1 -right-1 bg-secondary text-on-secondary text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center">3</span>
    # Or in mobile nav: <span class="absolute -top-1 right-0 bg-secondary text-on-secondary text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center">3</span>
    html = re.sub(
        r'<span class="absolute -top-1 -right-1 bg-secondary text-on-secondary text-\[10px\] font-bold h-4 w-4 rounded-full flex items-center justify-center">3</span>',
        r'<span class="cart-badge-counter absolute -top-1 -right-1 bg-secondary text-on-secondary text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center" style="display: none;">0</span>',
        html
    )
    
    html = re.sub(
        r'<span class="absolute -top-1 right-0 bg-secondary text-on-secondary text-\[10px\] font-bold h-4 w-4 rounded-full flex items-center justify-center">3</span>',
        r'<span class="cart-badge-counter absolute -top-1 right-0 bg-secondary text-on-secondary text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center" style="display: none;">0</span>',
        html
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed UI in {file}")

# 3. Add back button to checkout.html
checkout_file = 'checkout.html'
if os.path.exists(checkout_file):
    with open(checkout_file, 'r', encoding='utf-8') as f:
        checkout_html = f.read()

    header_target = '<h1 class="font-headline-lg text-headline-lg text-on-surface mb-2">Finalizar Pedido</h1>'
    new_header = '''
<div class="mb-4">
    <a href="index.html" class="inline-flex items-center gap-2 text-on-surface-variant hover:text-primary transition-colors text-sm font-label-md">
        <span class="material-symbols-outlined" style="font-size: 18px;">arrow_back</span>
        Volver a la tienda
    </a>
</div>
''' + header_target

    if 'arrow_back' not in checkout_html:
        checkout_html = checkout_html.replace(header_target, new_header)
        with open(checkout_file, 'w', encoding='utf-8') as f:
            f.write(checkout_html)
        print("Added back button to checkout.html")

print("UI fixes applied.")
