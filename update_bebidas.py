import os
import shutil
from bs4 import BeautifulSoup

# 1. Copy file
shutil.copy2('despensa.html', 'bebidas.html')

files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'checkout.html', 'bebidas.html']

for file in files:
    if not os.path.exists(file):
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Remove "Café" from desktop and mobile navs
    for a in soup.find_all('a'):
        text = a.get_text().strip()
        if 'Café' in text:
            a.decompose()
        elif 'Bebidas' in text:
            a['href'] = 'bebidas.html'

    # If it's bebidas.html, update the hero section and active states
    if file == 'bebidas.html':
        # Update Title
        if soup.title:
            soup.title.string = "Super900 - Bebidas y Licores"
            
        # Update Hero Section text
        h1 = soup.find('h1')
        if h1 and "Despensa" in h1.text:
            h1.string = "Bebidas y Licores"
            
        p = soup.find('p', class_=lambda c: c and 'max-w-xl' in c)
        if p and "esenciales" in p.text.lower():
            p.string = "La mejor selección de refrescos, cervezas artesanales y licores premium."

        # Fix Active Classes in Desktop Nav
        # In the original design, active item has bg-primary-container
        # Find all nav items
        for a in soup.find_all('a'):
            classes = a.get('class', [])
            text = a.get_text().strip()
            
            # Remove active state from despensa
            if 'Despensa' in text:
                if 'bg-primary-container' in classes: classes.remove('bg-primary-container')
                if 'text-on-primary-container' in classes: classes.remove('text-on-primary-container')
                if 'font-bold' in classes: classes.remove('font-bold')
                
                classes.extend(['text-on-surface-variant', 'hover:bg-surface-variant', 'transition-all', 'hover:bg-surface-variant/50'])
                a['class'] = classes
                
                # Unfill icon
                span = a.find('span', class_='fill')
                if span:
                    span_classes = span.get('class', [])
                    if 'fill' in span_classes: span_classes.remove('fill')
                    span['class'] = span_classes
                    
            # Add active state to bebidas
            if 'Bebidas' in text:
                # Remove inactive classes
                classes = [c for c in classes if c not in ['text-on-surface-variant', 'hover:bg-surface-variant', 'transition-all', 'hover:bg-surface-variant/50']]
                # Add active classes
                classes.extend(['bg-primary-container', 'text-on-primary-container', 'font-bold'])
                a['class'] = classes
                
                # Fill icon
                span = a.find('span', class_='material-symbols-outlined')
                if span:
                    span_classes = span.get('class', [])
                    if 'fill' not in span_classes: span_classes.append('fill')
                    span['class'] = span_classes

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Updated categories successfully.")
