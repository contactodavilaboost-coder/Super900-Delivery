import os
from bs4 import BeautifulSoup
import re

html_files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'checkout.html']

desktop_nav_html = """
<nav id="desktop-sidebar" class="hidden flex-col h-screen p-base fixed left-0 z-40 w-64 bg-surface-container dark:bg-surface-container-high shadow-xl border-r border-glass-border lg:flex">
    <div class="p-4 flex items-center gap-4 mb-8">
        <a href="index.html">
            <img alt="Super900 Logo" class="h-12 object-contain mb-2 hover:scale-105 transition-transform" src="https://lh3.googleusercontent.com/aida/ADBb0ugs-Y2XpvRrVKL70RcgQeZkWDCuZUAUIe8J9PUcHUBh5GHZWaPBVnQ9we1scdtQdW2fMrhwefeORQ7w2_33a1sFksn_OG5SPtgGPbtt1jDZ-s8Y_Z7yp1TLJET2tW093e2_LfKawyr1Mh_wsO7OZHPoWqX8LSEjYNHQzln4asKGsY3-hY6O9H1T8oICeKh8ROTNAzDCtq4IP9WZJSFipryRou7CRGhK10ATYkG1KI7hv-d7Lhajk6QslxQ"/>
        </a>
        <p class="font-label-md text-label-md text-on-surface-variant">Premium Selection</p>
    </div>
    <div class="flex-1 space-y-2" id="desktop-nav-links">
        <a class="nav-item flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-variant transition-all hover:bg-surface-variant/50" href="index.html" data-page="index.html">
            <span class="material-symbols-outlined">storefront</span>
            <span class="font-label-md text-label-md">Tienda</span>
        </a>
        <a class="nav-item flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-variant transition-all hover:bg-surface-variant/50" href="carnes.html" data-page="carnes.html">
            <span class="material-symbols-outlined">restaurant</span>
            <span class="font-label-md text-label-md">Carnes</span>
        </a>
        <a class="nav-item flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-variant transition-all hover:bg-surface-variant/50" href="verduras.html" data-page="verduras.html">
            <span class="material-symbols-outlined">eco</span>
            <span class="font-label-md text-label-md">Verduras</span>
        </a>
        <a class="nav-item flex items-center gap-3 px-4 py-3 rounded-lg text-on-surface-variant hover:bg-surface-variant transition-all hover:bg-surface-variant/50" href="despensa.html" data-page="despensa.html">
            <span class="material-symbols-outlined">fastfood</span>
            <span class="font-label-md text-label-md">Despensa y Snacks</span>
        </a>
    </div>
    <div class="mt-auto space-y-2 pt-4 border-t border-glass-border">
        <a href="checkout.html" class="w-full flex justify-center py-3 px-4 bg-primary text-on-primary font-label-md text-label-md font-bold rounded-lg hover:bg-primary-fixed transition-all duration-300 hover:shadow-glow hover:-translate-y-0.5">Mis Pedidos</a>
    </div>
</nav>
"""

mobile_bottom_nav_html = """
<nav id="mobile-bottom-nav" class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-4 py-3 lg:hidden bg-surface/90 dark:bg-surface-container-highest/90 backdrop-blur-lg border-t border-glass-border shadow-[0_-4px_12px_rgba(0,0,0,0.5)] rounded-t-xl">
    <a class="nav-item-mobile flex flex-col items-center justify-center text-on-surface-variant active:bg-surface-variant/30 rounded-lg p-1 transition-colors" href="index.html" data-page="index.html">
        <span class="material-symbols-outlined mb-1">storefront</span>
        <span class="font-label-sm text-label-sm">Tienda</span>
    </a>
    <a class="nav-item-mobile flex flex-col items-center justify-center text-on-surface-variant active:bg-surface-variant/30 rounded-lg p-1 transition-colors" href="index.html" data-page="search">
        <span class="material-symbols-outlined mb-1">search</span>
        <span class="font-label-sm text-label-sm">Buscar</span>
    </a>
    <a class="nav-item-mobile flex flex-col items-center justify-center text-on-surface-variant active:bg-surface-variant/30 rounded-lg p-1 transition-colors relative" href="checkout.html" data-page="checkout.html">
        <div class="relative">
            <span class="material-symbols-outlined mb-1">shopping_basket</span>
            <span class="absolute -top-1 right-0 bg-secondary text-on-secondary text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center">3</span>
        </div>
        <span class="font-label-sm text-label-sm">Carrito</span>
    </a>
</nav>
"""

style_html = """
<style id="global-styles">
    body { background-color: #121414; color: #e2e2e2; }
    .glass-panel { background: rgba(18, 18, 18, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.12); }
    .card-surface { background-color: #121212; border: 1px solid rgba(255, 255, 255, 0.12); }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #121414; }
    ::-webkit-scrollbar-thumb { background: #333535; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #434751; }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-fade-in-up { animation: fadeInUp 0.5s ease-out forwards; }
</style>
"""

import sys

for file_name in html_files:
    if not os.path.exists(file_name):
        continue
    
    with open(file_name, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Update Styles
    # Remove existing styles
    for style in soup.find_all('style'):
        style.decompose()
    
    style_soup = BeautifulSoup(style_html, 'html.parser')
    if soup.head:
        soup.head.append(style_soup)

    # 2. Update Desktop Nav (find <nav> or <aside> that is lg:flex or w-64)
    old_nav = None
    for nav in soup.find_all(['nav', 'aside']):
        classes = nav.get('class', [])
        if 'w-64' in classes or 'lg:flex' in classes or 'h-screen' in classes:
            old_nav = nav
            break
            
    if old_nav:
        new_nav_soup = BeautifulSoup(desktop_nav_html, 'html.parser')
        
        # Highlight active page
        for a in new_nav_soup.find_all('a', {'data-page': True}):
            if a['data-page'] == file_name:
                a['class'] = "nav-item flex items-center gap-3 px-4 py-3 rounded-lg transition-all bg-primary-container text-on-primary-container font-bold translate-x-1"
                # Change icon to fill=1
                span_icon = a.find('span', class_='material-symbols-outlined')
                if span_icon:
                    span_icon['style'] = "font-variation-settings: 'FILL' 1;"
                    
        old_nav.replace_with(new_nav_soup)

    # 3. Update Mobile Nav (find <nav> with bottom-0)
    old_mobile_nav = None
    for nav in soup.find_all('nav'):
        classes = nav.get('class', [])
        if 'bottom-0' in classes:
            old_mobile_nav = nav
            break
            
    if old_mobile_nav:
        new_mobile_nav_soup = BeautifulSoup(mobile_bottom_nav_html, 'html.parser')
        for a in new_mobile_nav_soup.find_all('a', {'data-page': True}):
            if a['data-page'] == file_name:
                a['class'] = "nav-item-mobile flex flex-col items-center justify-center font-bold scale-110 transition-transform text-primary dark:text-primary-fixed"
                span_icon = a.find('span', class_='material-symbols-outlined')
                if span_icon:
                    span_icon['style'] = "font-variation-settings: 'FILL' 1;"
                    span_icon['class'] = span_icon.get('class', []) + ['filled']
                    
        old_mobile_nav.replace_with(new_mobile_nav_soup)
        
    # 4. Standardize Card alignments (for hardcoded ones in HTML)
    # Find all divs that look like product cards
    for card in soup.find_all('div', class_=re.compile(r'bg-charcoal-surface|card-surface')):
        classes = card.get('class', [])
        if 'rounded-xl' in classes or 'rounded-2xl' in classes:
            # Ensure it has flex col and h-full and animate-fade-in-up
            if 'flex' not in classes: classes.append('flex')
            if 'flex-col' not in classes: classes.append('flex-col')
            if 'h-full' not in classes: classes.append('h-full')
            if 'animate-fade-in-up' not in classes: classes.append('animate-fade-in-up')
            
            # Hover effects
            if 'transition-all' not in classes: classes.append('transition-all')
            if 'duration-500' not in classes: classes.append('duration-500')
            if 'hover:-translate-y-1' not in classes: classes.append('hover:-translate-y-1')
            if 'hover:shadow-glow' not in classes: classes.append('hover:shadow-glow')
            
            card['class'] = classes
            
            # Find the bottom container (usually has mt-auto) to align buttons
            # We look for price / button row
            for div in card.find_all('div'):
                div_classes = div.get('class', [])
                if 'mt-auto' in div_classes or 'justify-between' in div_classes:
                    if 'mt-auto' not in div_classes:
                        div['class'] = div_classes + ['mt-auto']

    # Rewrite HTML
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    # 5. Fix JS string templates
    with open(file_name, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # In the JS template, ensure flex flex-col h-full and mt-auto
    content = re.sub(r"card\.className = 'bg-charcoal-surface([^']*)';", 
                     r"card.className = 'bg-charcoal-surface rounded-xl border border-glass-border overflow-hidden flex flex-col h-full group hover:border-primary/50 transition-all duration-500 hover:shadow-glow hover:-translate-y-1 relative animate-fade-in-up';", 
                     content)
                     
    content = re.sub(r'<div class="mt-auto flex items-center justify-between">', 
                     r'<div class="mt-auto flex items-center justify-between pt-4">', 
                     content)

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("UI Unified successfully.")
