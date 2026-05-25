import os
import shutil
from bs4 import BeautifulSoup

source_dir = 'stitch_super900_delivery_express'

# File mappings (source_subfolder: target_file)
mappings = {
    'super900_inicio_actualizado': 'index.html',
    'super900_carnes_actualizado': 'carnes.html',
    'super900_verduras_y_frutas_actualizado': 'verduras.html',
    'super900_despensa_actualizado': 'despensa.html',
    'super900_finalizar_compra': 'checkout.html'
}

# 1. Copy files
for subfolder, target_file in mappings.items():
    src_path = os.path.join(source_dir, subfolder, 'code.html')
    if os.path.exists(src_path):
        shutil.copy2(src_path, target_file)
        print(f"Copied {src_path} -> {target_file}")
    else:
        print(f"Missing {src_path}")

# 2. Fix links
target_files = list(mappings.values())

for file_name in target_files:
    if not os.path.exists(file_name):
        continue
    
    with open(file_name, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Update links by finding text or icons
    for a in soup.find_all('a'):
        text = a.get_text().strip().lower()
        
        if 'tienda' in text or 'inicio' in text or 'shop' in text:
            a['href'] = 'index.html'
        elif 'carnes' in text:
            a['href'] = 'carnes.html'
        elif 'verduras' in text:
            a['href'] = 'verduras.html'
        elif 'snacks' in text or 'despensa' in text:
            a['href'] = 'despensa.html'
        elif 'pedidos' in text or 'carrito' in text or 'cart' in text or 'checkout' in text or 'ver carrito' in text:
            a['href'] = 'checkout.html'
        
        # Super900 logo link (it doesn't have text, but it contains an img with alt="Super900 Logo")
        img = a.find('img')
        if img and img.get('alt') == 'Super900 Logo':
            a['href'] = 'index.html'

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Restoration and linking complete.")
