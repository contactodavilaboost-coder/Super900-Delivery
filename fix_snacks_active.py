import os
from bs4 import BeautifulSoup

files = ['carnes.html', 'verduras.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove active state from "Snacks"
    for a in soup.find_all('a'):
        text = a.get_text().strip()
        classes = a.get('class', [])
        
        if 'Snacks' in text:
            # We must remove the active classes and add inactive ones
            if 'bg-primary-container' in classes: classes.remove('bg-primary-container')
            if 'text-on-primary-container' in classes: classes.remove('text-on-primary-container')
            if 'font-bold' in classes: classes.remove('font-bold')
            if 'translate-x-1' in classes: classes.remove('translate-x-1')
            
            # Add inactive classes if not present
            for c in ['text-on-surface-variant', 'hover:bg-surface-variant', 'transition-all', 'hover:bg-surface-variant/50']:
                if c not in classes:
                    classes.append(c)
                    
            a['class'] = classes
            
            # Unfill icon
            span = a.find('span', class_='material-symbols-outlined')
            if span:
                # remove inline style fill 1
                if span.has_attr('style') and "'FILL' 1" in span['style']:
                    span['style'] = span['style'].replace("'FILL' 1", "'FILL' 0")

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Snacks active state fixed.")
