import os
from bs4 import BeautifulSoup

# 1. Fix cart buttons in all pages
files = ['index.html', 'carnes.html', 'verduras.html', 'despensa.html', 'bebidas.html', 'checkout.html']

for file in files:
    if not os.path.exists(file):
        continue
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Fix Top Navbar cart button (mobile)
    for btn in soup.find_all('button'):
        if btn.find('span', string='shopping_cart'):
            btn['onclick'] = "window.location.href='checkout.html'"

    # Fix Bottom Navbar cart button (mobile)
    for a in soup.find_all('a'):
        if a.find('span', string='shopping_basket'):
            a['href'] = 'checkout.html'

    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))


# 2. Translate and fix checkout.html
if os.path.exists('checkout.html'):
    with open('checkout.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Ensure airtable-config is included before cart.js!
    body = soup.body
    if body:
        if not soup.find('script', src='js/airtable-config.js'):
            script = soup.new_tag('script', src='js/airtable-config.js')
            cart_script = soup.find('script', src='js/cart.js')
            if cart_script:
                cart_script.insert_before(script)
            else:
                body.append(script)

    # Translate texts
    title = soup.find('title')
    if title: title.string = "Super900 - Carrito de Compras"
    
    for h1 in soup.find_all('h1'):
        if 'Checkout' in h1.text: h1.string = "Finalizar Pedido"
    for p in soup.find_all('p'):
        if 'Complete your order' in p.text: p.string = "Completa tu pedido proporcionando tus datos a continuación."
        if 'Efectivo (Cash)' in p.text: p.string = "Para Efectivo, por favor asegúrate de tener el monto exacto al momento de la entrega."
        
    for h2 in soup.find_all('h2'):
        if '1. Customer Information' in h2.text: h2.string = " 1. Información del Cliente"
        if '2. Delivery Address' in h2.text: h2.string = " 2. Dirección de Entrega"
        if '3. Payment Method' in h2.text: h2.string = " 3. Método de Pago"
        if 'Your Cart' in h2.text: h2.string = "Tu Carrito"

    for h3 in soup.find_all('h3'):
        if 'Pago Móvil Details' in h3.text: h3.string = "Datos de Pago Móvil"

    for label in soup.find_all('label'):
        if 'Full Name' in label.text: label.string = "Nombre Completo"
        if 'Email Address' in label.text: label.string = "Correo Electrónico"
        if 'Phone Number' in label.text: label.string = "Número de Teléfono"
        if 'Street Address' in label.text: label.string = "Dirección (Calle/Av, Casa/Apto)"
        if 'City' in label.text: label.string = "Ciudad"
        if 'Landmarks' in label.text: label.string = "Punto de Referencia / Instrucciones"

    for input_tag in soup.find_all('input'):
        if input_tag.get('placeholder') == 'Bank Name': input_tag['placeholder'] = 'Nombre del Banco'
        if input_tag.get('placeholder') == 'ID (Cédula)': input_tag['placeholder'] = 'Cédula de Identidad'
        if input_tag.get('placeholder') == 'Phone': input_tag['placeholder'] = 'Teléfono'
        if input_tag.get('placeholder') == 'Account Email': input_tag['placeholder'] = 'Correo Zelle'
        if input_tag.get('placeholder') == 'Reference Number': input_tag['placeholder'] = 'Número de Referencia'
        if input_tag.get('placeholder') == 'Near the shopping mall': input_tag['placeholder'] = 'Cerca de...'

    for btn in soup.find_all('button'):
        if 'Confirm Order' in btn.text:
            for content in btn.contents:
                if content.name is None and 'Confirm Order' in content:
                    content.replace_with("Confirmar Pedido y Pagar ")

    with open('checkout.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
print("Links and translations applied correctly!")
