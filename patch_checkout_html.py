import re

with open('checkout.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace inputs with ID versions
html = html.replace('placeholder="John Doe" type="text"', 'id="cliente_nombre" placeholder="John Doe" type="text" required')
html = html.replace('placeholder="john@example.com" type="email"', 'id="cliente_email" placeholder="john@example.com" type="email"')
html = html.replace('placeholder="+58 412 000 0000" type="tel"', 'id="cliente_telefono" placeholder="+58 412 000 0000" type="tel" required')

html = html.replace('placeholder="Av. Principal, Urb. Puerta Maraven" type="text"', 'id="dir_calle" placeholder="Av. Principal, Urb. Puerta Maraven" type="text" required')
html = html.replace('type="text" value="Punto Fijo"', 'id="dir_ciudad" type="text" value="Punto Fijo" required')
html = html.replace('placeholder="Cerca de..." type="text"', 'id="dir_ref" placeholder="Cerca de..." type="text"')

# Add radios for Payment Method selection
payment_html = """
<div class="space-y-6">
    <div class="flex gap-4 mb-4">
        <label class="flex items-center gap-2 text-on-surface cursor-pointer">
            <input type="radio" name="metodo_pago" value="Pago Movil" checked class="text-primary focus:ring-primary"> Pago Móvil
        </label>
        <label class="flex items-center gap-2 text-on-surface cursor-pointer">
            <input type="radio" name="metodo_pago" value="Zelle" class="text-primary focus:ring-primary"> Zelle
        </label>
        <label class="flex items-center gap-2 text-on-surface cursor-pointer">
            <input type="radio" name="metodo_pago" value="Efectivo" class="text-primary focus:ring-primary"> Efectivo
        </label>
    </div>
    
    <div id="panel-pagomovil" class="p-6 bg-surface-container-low border border-glass-border rounded-xl">
        <div class="flex items-center gap-3 mb-4">
            <span class="material-symbols-outlined text-secondary">smartphone</span>
            <h3 class="font-label-md text-on-surface">Datos de Pago Móvil</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <input id="pm_banco" class="bg-charcoal-surface border-glass-border rounded-lg p-2.5 text-sm" placeholder="Banco Origen" type="text"/>
            <input id="pm_ref" class="bg-charcoal-surface border-glass-border rounded-lg p-2.5 text-sm" placeholder="Nro de Referencia" type="text"/>
            <input id="pm_tlf" class="bg-charcoal-surface border-glass-border rounded-lg p-2.5 text-sm" placeholder="Teléfono Emisor" type="text"/>
        </div>
    </div>
    
    <div id="panel-zelle" class="p-6 bg-surface-container border border-primary/20 rounded-xl hidden">
        <div class="flex items-center gap-3 mb-4">
            <span class="material-symbols-outlined text-secondary">payments</span>
            <h3 class="font-label-md text-on-surface">Zelle</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input id="zelle_correo" class="bg-charcoal-surface border-glass-border rounded-lg p-2.5 text-sm" placeholder="Correo Titular" type="email"/>
            <input id="zelle_ref" class="bg-charcoal-surface border-glass-border rounded-lg p-2.5 text-sm" placeholder="Número de Confirmación" type="text"/>
        </div>
    </div>
    
    <div class="p-4 bg-surface-container-highest/30 rounded-lg flex items-start gap-3">
        <span class="material-symbols-outlined text-on-surface-variant">info</span>
        <p class="text-xs text-on-surface-variant">Para Efectivo, por favor asegúrate de tener el monto exacto al momento de la entrega.</p>
    </div>
</div>
"""

# Replace the entire payment section content
html = re.sub(r'<div class="space-y-6">.*?</div>\s*</section>', payment_html + '\n</section>', html, flags=re.DOTALL)

with open('checkout.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated checkout.html forms")
