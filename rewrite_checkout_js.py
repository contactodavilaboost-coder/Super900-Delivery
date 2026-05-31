new_js = """
/**
 * Super900 - Checkout Reactive Renderer & Form Submitter
 */
document.addEventListener('DOMContentLoaded', async () => {
    const cartWrapper = document.getElementById('cart-drawer-copy') || document.querySelector('.lg\\\\:w-\\\\[480px\\\\]');
    if (!cartWrapper) return;

    if (!window.AirtableConfig || !window.Cart) return;

    let bcvRate = 535; // Default fallback
    try {
        bcvRate = await AirtableConfig.getExchangeRate();
    } catch(e) {
        console.error("Error fetching BCV rate, using fallback.");
    }

    const renderCheckout = () => {
        const items = Cart.items;
        const itemsContainer = cartWrapper.querySelector('.overflow-y-auto') || cartWrapper.querySelector('div.flex-1');
        const countBadge = cartWrapper.querySelector('h2')?.nextElementSibling;
        const totalContainer = cartWrapper.querySelector('.space-y-3.pt-4');

        if (!itemsContainer || !totalContainer) return;

        if (countBadge) countBadge.innerText = `${Cart.getTotalItems()} items`;

        if (items.length === 0) {
            itemsContainer.innerHTML = `
                <div class="py-12 flex flex-col items-center justify-center text-on-surface-variant text-center opacity-70">
                    <span class="material-symbols-outlined text-6xl mb-4">shopping_cart_checkout</span>
                    <p class="font-body-lg">Tu carrito está vacío</p>
                    <a href="index.html" class="mt-4 text-primary hover:underline">Volver a la tienda</a>
                </div>
            `;
        } else {
            itemsContainer.innerHTML = ''; 
            items.forEach(item => {
                const itemTotal = item.price * item.qty;
                const itemTotalBs = (itemTotal * bcvRate).toFixed(2);
                
                const div = document.createElement('div');
                div.className = 'flex gap-4 p-4 rounded-xl bg-surface-container-low border border-glass-border hover:bg-surface-container transition-colors group relative';
                div.innerHTML = `
                    <div class="w-20 h-20 rounded-lg bg-white overflow-hidden relative flex-shrink-0 p-1">
                        <img src="${item.img}" alt="${item.name.replace(/"/g, '&quot;')}" class="w-full h-full object-contain">
                    </div>
                    <div class="flex flex-col flex-1 justify-between">
                        <div class="flex justify-between items-start">
                            <div class="pr-6">
                                <h3 class="font-label-md text-label-md text-on-surface line-clamp-1">${item.name}</h3>
                                <p class="text-on-surface-variant text-sm mt-0.5">${item.unit}</p>
                            </div>
                            <button type="button" onclick="window.Cart.removeItem('${item.id}')" class="text-outline-variant hover:text-error absolute top-4 right-4 transition-colors">
                                <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
                            </button>
                        </div>
                        <div class="flex justify-between items-end mt-2">
                            <div>
                                <div class="font-headline-md text-headline-md text-secondary-fixed text-lg">$${itemTotal.toFixed(2)}</div>
                                <div class="text-xs text-on-surface-variant">Bs. ${itemTotalBs}</div>
                            </div>
                            <div class="flex items-center gap-3 bg-surface-container-high rounded-lg px-2 py-1 border border-glass-border">
                                <button type="button" onclick="window.Cart.updateQty('${item.id}', -1)" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                    <span class="material-symbols-outlined" style="font-size: 16px;">remove</span>
                                </button>
                                <span class="text-on-surface font-label-md w-4 text-center">${item.qty}</span>
                                <button type="button" onclick="window.Cart.updateQty('${item.id}', 1)" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                    <span class="material-symbols-outlined" style="font-size: 16px;">add</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                itemsContainer.appendChild(div);
            });
        }

        const subtotal = Cart.getSubtotal();
        const deliveryFee = subtotal > 0 ? 5.00 : 0;
        const totalUSD = subtotal + deliveryFee;
        const totalBs = (totalUSD * bcvRate).toFixed(2);
        
        totalContainer.innerHTML = `
            <div class="flex justify-between text-on-surface-variant">
                <span class="text-body-md">Subtotal</span>
                <span class="text-body-md">$${subtotal.toFixed(2)}</span>
            </div>
            <div class="flex justify-between text-on-surface-variant">
                <span class="text-body-md">Delivery</span>
                <span class="text-body-md">$${deliveryFee.toFixed(2)}</span>
            </div>
            <div class="flex justify-between items-end pt-3 border-t border-glass-border mt-3">
                <span class="font-headline-md text-headline-md text-on-surface">Total</span>
                <div class="text-right">
                    <div class="font-headline-md text-headline-md text-secondary text-2xl leading-none">$${totalUSD.toFixed(2)}</div>
                    <div class="text-sm text-on-surface-variant mt-1">Bs. ${totalBs}</div>
                </div>
            </div>
        `;
    };

    window.addEventListener('cartUpdated', renderCheckout);
    renderCheckout();

    // Toggle Payment Panels
    const radios = document.querySelectorAll('input[name="metodo_pago"]');
    const pmPanel = document.getElementById('panel-pagomovil');
    const zellePanel = document.getElementById('panel-zelle');

    radios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            pmPanel.classList.add('hidden');
            zellePanel.classList.add('hidden');
            if(e.target.value === 'Pago Movil') pmPanel.classList.remove('hidden');
            if(e.target.value === 'Zelle') zellePanel.classList.remove('hidden');
        });
    });

    // Handle Form Submission
    const submitBtn = cartWrapper.querySelector('button');
    if (submitBtn) {
        submitBtn.type = "button"; // prevent accidental form submit
        submitBtn.addEventListener('click', async () => {
            if (Cart.items.length === 0) {
                alert("El carrito está vacío.");
                return;
            }

            const nombre = document.getElementById('cliente_nombre').value.trim();
            const tlf = document.getElementById('cliente_telefono').value.trim();
            const calle = document.getElementById('dir_calle').value.trim();
            
            if(!nombre || !tlf || !calle) {
                alert("Por favor completa tu Nombre, Teléfono y Dirección.");
                return;
            }
            
            const city = document.getElementById('dir_ciudad').value;
            const ref = document.getElementById('dir_ref').value;
            const address = `${calle}, ${city} (${ref})`;

            const method = document.querySelector('input[name="metodo_pago"]:checked').value;
            let paymentData = "";
            if (method === 'Pago Movil') {
                const b = document.getElementById('pm_banco').value;
                const r = document.getElementById('pm_ref').value;
                const t = document.getElementById('pm_tlf').value;
                if(!r) { alert("Ingresa el Nro de Referencia de Pago Móvil."); return; }
                paymentData = `Banco: ${b}, Ref: ${r}, Tlf: ${t}`;
            } else if (method === 'Zelle') {
                const c = document.getElementById('zelle_correo').value;
                const r = document.getElementById('zelle_ref').value;
                if(!r) { alert("Ingresa el Número de Confirmación Zelle."); return; }
                paymentData = `Correo: ${c}, Ref: ${r}`;
            } else {
                paymentData = "Efectivo al recibir";
            }

            const subtotal = Cart.getSubtotal();
            const deliveryFee = 5.00;
            const totalUSD = subtotal + deliveryFee;
            const totalBs = (totalUSD * bcvRate).toFixed(2);

            const payload = {
                order: {
                    name: nombre,
                    phone: tlf,
                    address: address,
                    paymentMethod: method,
                    paymentData: paymentData,
                    totalUSD: totalUSD,
                    totalBs: totalBs
                },
                items: Cart.items
            };

            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="material-symbols-outlined animate-spin">autorenew</span> Procesando...';
            submitBtn.disabled = true;

            try {
                const res = await fetch('/api/createOrder', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await res.json();
                if(data.success) {
                    Cart.clear();
                    document.body.innerHTML = `
                        <div class="min-h-screen bg-background flex flex-col items-center justify-center text-center p-6">
                            <div class="w-24 h-24 bg-success-green rounded-full flex items-center justify-center mb-6 shadow-[0_0_40px_rgba(40,199,111,0.4)]">
                                <span class="material-symbols-outlined text-white text-5xl">check_circle</span>
                            </div>
                            <h1 class="font-headline-lg text-4xl text-on-surface mb-2">¡Pedido Confirmado!</h1>
                            <p class="text-on-surface-variant text-lg mb-8 max-w-md">Tu número de orden es <b class="text-primary">${data.orderId}</b>. Estaremos preparando tu pedido y te contactaremos en breve.</p>
                            <a href="index.html" class="bg-primary text-on-primary px-8 py-3 rounded-lg font-label-md hover:bg-primary-fixed transition-colors">Volver a la tienda</a>
                        </div>
                    `;
                } else {
                    alert("Hubo un error al procesar tu pedido. Intenta nuevamente.");
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            } catch(e) {
                alert("Error de conexión. Intenta nuevamente.");
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
});
"""

with open('js/checkout.js', 'w', encoding='utf-8') as f:
    f.write(new_js)
print("Updated js/checkout.js")
