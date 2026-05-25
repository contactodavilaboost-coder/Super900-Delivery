import shutil
from bs4 import BeautifulSoup

# Data for replacement
pages_data = {
    'carnes.html': {
        'active_text': 'Carnes',
        'title': 'Carnes Premium',
        'desc': 'Cortes selectos, frescura garantizada para tus mejores platillos.',
        'img': 'https://lh3.googleusercontent.com/aida-public/AB6AXuByXjPPGmiLzUIlNbRqHt_q9YRanv5ydPyr_qEvwAmxBzzSWqGR3PRIdQWEuRU2lMT1bdZFLcVPlkMYIVUB-XC4XYC-2i4mAQhbD_NpHIh3wQZF5astKz9XcoPmKy0kLj2pw8UU7pm-lUIpzsn_quxY2AcQYWcFiYFmLOYUcqJ9FIo6ZGCo2iQ4I8DM_GcrmrWZ62XKfA38VKFwcxgsno3yXpW4PjcpQ5Gm6yQIK_7ixSYvu4Lk47u7pt3R-6o_XUdPdlr3qBD64QE'
    },
    'verduras.html': {
        'active_text': 'Verduras',
        'title': 'Verduras Frescas',
        'desc': 'Selección premium directa de la cosecha. Frescura garantizada cada día.',
        'img': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBm4fA-A2JyEiN38Y-4LjF51UB1yW62jlHmIId71RZlu-riqiXNIYbm8hnjrAR-qYaEkzzdcwFzGWgd88qWYGod8UhAceH03Idc18kA8pabIr3XXyir1g8WIIpHl48HNOtHsK7FiNmnWxISGu8ElLUED50VybucR_EGbDW6Ru54l6rVB6Vtk0gIZ4YgEaH0Ta67fDH9AfHMDhI4_rqma5lA2lvAYVz9GTpqsIzvp6HcodZaVrm_bu2z4S12V9Cs0l_TZksx-PUfiTU'
    }
}

for target_file, data in pages_data.items():
    # 1. Start from despensa.html
    shutil.copy2('despensa.html', target_file)
    
    with open(target_file, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 2. Update Hero Section
    h2 = soup.find('h2', string="Despensa Selecta")
    if h2:
        h2.string = data['title']
        
    p = soup.find('p', string=lambda s: s and "esenciales para tu alacena" in s)
    if p:
        p.string = data['desc']
        
    # Update Hero Image
    hero_section = soup.find('section', class_=lambda c: c and 'rounded-2xl' in c)
    if hero_section:
        img = hero_section.find('img')
        if img:
            img['src'] = data['img']
            
    # Update HTML title
    if soup.title:
        soup.title.string = f"Super900 - {data['title']}"

    # 3. Update active sidebar item
    for a in soup.find_all('a'):
        classes = a.get('class', [])
        if not classes:
            continue
        text = a.get_text().strip()
        
        # Remove active state from Despensa
        if 'Despensa' in text:
            if 'bg-primary-container' in classes: classes.remove('bg-primary-container')
            if 'text-on-primary-container' in classes: classes.remove('text-on-primary-container')
            if 'font-bold' in classes: classes.remove('font-bold')
            classes.extend(['text-on-surface-variant', 'hover:bg-surface-variant', 'transition-all', 'hover:bg-surface-variant/50'])
            a['class'] = classes
            
            span = a.find('span', class_='fill')
            if span:
                span_classes = span.get('class', [])
                if 'fill' in span_classes: span_classes.remove('fill')
                span['class'] = span_classes
                
        # Add active state to target category
        if data['active_text'] in text:
            # Clean old hover classes
            classes = [c for c in classes if c not in ['text-on-surface-variant', 'hover:bg-surface-variant', 'transition-all', 'hover:bg-surface-variant/50']]
            classes.extend(['bg-primary-container', 'text-on-primary-container', 'font-bold'])
            a['class'] = classes
            
            span = a.find('span', class_='material-symbols-outlined')
            if span:
                span_classes = span.get('class', [])
                if 'fill' not in span_classes: span_classes.append('fill')
                span['class'] = span_classes

    # Ensure JS points to right category if Airtable is injected (it's injected via restored scripts usually, but just in case we update the placeholder text)
    input_search = soup.find('input', placeholder="Buscar en despensa...")
    if input_search:
        input_search['placeholder'] = f"Buscar en {data['active_text'].lower()}..."

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Pages standardized successfully.")
