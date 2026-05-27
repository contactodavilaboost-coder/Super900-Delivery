import os

# 1. Refactor cart.js (State Manager with Custom Events)
cart_js = """/**
 * Super900 - Advanced Cart State Manager
 */
class ShoppingCart {
    constructor() {
        this.STORAGE_KEY = 'super900_cart';
        this.items = this.loadCart();
        this.initListeners();
    }

    loadCart() {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY)) || [];
        } catch (e) {
            console.error("Cart parse error:", e);
            return [];
        }
    }

    saveCart() {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.items));
        this.notify();
    }

    notify() {
        window.dispatchEvent(new CustomEvent('cartUpdated', { detail: { items: this.items } }));
    }

    addItem(product) {
        const existing = this.items.find(p => p.id === product.id);
        if (existing) {
            existing.qty += 1;
        } else {
            this.items.push({ ...product, qty: 1 });
        }
        this.saveCart();
        this.showToast(`Agregado: ${product.name}`);
    }

    removeItem(id) {
        this.items = this.items.filter(p => p.id !== id);
        this.saveCart();
    }

    updateQty(id, delta) {
        const existing = this.items.find(p => p.id === id);
        if (existing) {
            existing.qty += delta;
            if (existing.qty <= 0) {
                this.removeItem(id);
                return;
            }
        }
        this.saveCart();
    }

    clear() {
        this.items = [];
        this.saveCart();
    }

    getTotalItems() {
        return this.items.reduce((sum, item) => sum + item.qty, 0);
    }

    getSubtotal() {
        return this.items.reduce((sum, item) => sum + (item.price * item.qty), 0);
    }

    initListeners() {
        // Listen to cart changes to update all badges globally
        window.addEventListener('cartUpdated', () => {
            const count = this.getTotalItems();
            document.querySelectorAll('.cart-badge-counter').forEach(badge => {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'flex' : 'none';
            });
        });

        // Delegate Add To Cart clicks globally
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.add-to-cart-btn');
            if (btn) {
                const product = {
                    id: btn.dataset.id,
                    name: btn.dataset.name,
                    price: parseFloat(btn.dataset.price),
                    img: btn.dataset.img,
                    unit: btn.dataset.unit
                };
                this.addItem(product);
            }
        });

        // Trigger initial render
        document.addEventListener('DOMContentLoaded', () => {
            this.notify();
        });
    }

    showToast(message) {
        let toast = document.getElementById('cart-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'cart-toast';
            toast.className = 'fixed bottom-20 left-1/2 -translate-x-1/2 bg-surface-container-high text-on-surface px-6 py-3 rounded-full shadow-lg z-[100] transition-all duration-300 transform translate-y-4 opacity-0 pointer-events-none font-label-md border border-glass-border';
            document.body.appendChild(toast);
        }
        toast.innerText = message;
        
        // Show
        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-4', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');
        });
        
        if (this.toastTimeout) clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
            toast.classList.remove('translate-y-0', 'opacity-100');
            toast.classList.add('translate-y-4', 'opacity-0');
        }, 2000);
    }
}

// Initialize Singleton
window.Cart = new ShoppingCart();
"""

with open('js/cart.js', 'w', encoding='utf-8') as f:
    f.write(cart_js)

# 2. Refactor dynamic_products.js (Use data-attributes instead of inline onclick)
dynamic_js = """document.addEventListener('DOMContentLoaded', async () => {
    if (!window.AirtableConfig) return;

    const grid = document.getElementById('dynamic-products-grid');
    if (!grid) return;

    const path = window.location.pathname;
    let filterFn = () => true;
    
    if (path.includes('carnes')) filterFn = r => r.fields.Categoria === 'Carnes';
    else if (path.includes('verduras')) filterFn = r => r.fields.Categoria === 'Verduras';
    else if (path.includes('bebidas')) filterFn = r => r.fields.Categoria === 'Bebidas';
    else if (path.includes('despensa')) filterFn = r => r.fields.Categoria === 'Despensa' || r.fields.Categoria === 'Snacks';

    grid.innerHTML = `
        <div class="col-span-full py-16 flex flex-col items-center justify-center text-on-surface-variant">
            <span class="material-symbols-outlined animate-spin text-5xl text-primary mb-4">sync</span>
            <p class="font-headline-md">Cargando catálogo...</p>
        </div>
    `;

    const [records, bcvRate] = await Promise.all([
        AirtableConfig.getRecords('Inventario'),
        AirtableConfig.getExchangeRate()
    ]);
    
    const validRecords = records.filter(r => AirtableConfig.getFieldValue(r.fields, ['Nombre', 'Name']));
    const displayList = validRecords.filter(filterFn);
    
    if (displayList.length === 0) {
        grid.innerHTML = `<div class="col-span-full py-12 text-center text-on-surface-variant"><p>No se encontraron productos.</p></div>`;
        return;
    }

    grid.innerHTML = '';

    displayList.forEach(rec => {
        const f = rec.fields;
        const name = AirtableConfig.getFieldValue(f, ['Nombre', 'Name']) || 'Producto';
        const price = parseFloat(AirtableConfig.getFieldValue(f, ['Precio_Regular', 'Precio', 'Price']) || 0);
        const unit = AirtableConfig.getFieldValue(f, ['Unidad_Medida', 'Unidad', 'Unit']) || 'ud';
        const isOffer = AirtableConfig.getFieldValue(f, ['Oferta', 'Offer']) || false;
        const offerPriceVal = AirtableConfig.getFieldValue(f, ['Precio_Oferta', 'OfferPrice']);
        const offerPrice = offerPriceVal !== undefined ? parseFloat(offerPriceVal) : price;
        const img = AirtableConfig.getImageUrl(f);

        const currentPrice = (isOffer || (offerPrice < price && offerPrice > 0)) ? offerPrice : price;
        const currentPriceBs = (currentPrice * bcvRate).toFixed(2);
        
        const priceHtml = (isOffer || (offerPrice < price && offerPrice > 0))
            ? `<div class="flex flex-col">
                 <span class="font-label-sm text-label-sm text-outline-variant line-through">$${price.toFixed(2)}</span>
                 <div class="flex items-end gap-1">
                     <span class="font-headline-md text-headline-md text-error">$${offerPrice.toFixed(2)}</span>
                     <span class="text-xs text-on-surface-variant mb-1">Bs. ${currentPriceBs}</span>
                 </div>
               </div>`
            : `<div class="flex flex-col">
                 <div class="flex items-end gap-1">
                     <span class="font-headline-md text-headline-md text-on-surface">$${price.toFixed(2)}</span>
                     <span class="text-xs text-on-surface-variant mb-1">Bs. ${currentPriceBs}</span>
                 </div>
               </div>`;

        const offerBadge = (isOffer || (offerPrice < price && offerPrice > 0))
            ? `<div class="absolute top-3 left-3 bg-error-red text-white text-[10px] font-bold px-2 py-1 rounded uppercase tracking-wider z-20">OFERTA</div>`
            : '';

        const card = document.createElement('article');
        card.className = "group relative bg-surface-container rounded-xl overflow-hidden border border-glass-border hover:border-primary/50 transition-all duration-300 flex flex-col h-full";
        
        card.innerHTML = `
            <div class="relative h-48 w-full bg-white p-4 flex items-center justify-center overflow-hidden">
                ${offerBadge}
                <img src="${img}" alt="${name.replace(/"/g, '&quot;')}" class="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-500 z-10" />
            </div>
            <div class="p-4 flex flex-col flex-1">
                <h3 class="font-body-lg text-body-lg text-on-surface font-semibold mb-1 line-clamp-2">${name}</h3>
                <p class="font-label-md text-label-md text-on-surface-variant mb-4">${unit}</p>
                <div class="mt-auto flex items-center justify-between">
                    ${priceHtml}
                    <button class="add-to-cart-btn bg-surface-variant text-on-surface hover:bg-primary hover:text-on-primary rounded-full w-10 h-10 flex items-center justify-center transition-colors relative z-20 shadow-lg"
                            data-id="${rec.id}" 
                            data-name="${name.replace(/"/g, '&quot;')}" 
                            data-price="${currentPrice}" 
                            data-img="${img}" 
                            data-unit="${unit.replace(/"/g, '&quot;')}">
                        <span class="material-symbols-outlined pointer-events-none">add</span>
                    </button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
});
"""

with open('js/dynamic_products.js', 'w', encoding='utf-8') as f:
    f.write(dynamic_js)


# 3. Refactor checkout.js (Reactive rendering based on cartUpdated event)
checkout_js = """/**
 * Super900 - Checkout Reactive Renderer
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

        // Count
        if (countBadge) countBadge.innerText = `${Cart.getTotalItems()} items`;

        // Render List
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
                            <button onclick="window.Cart.removeItem('${item.id}')" class="text-outline-variant hover:text-error absolute top-4 right-4 transition-colors">
                                <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
                            </button>
                        </div>
                        <div class="flex justify-between items-end mt-2">
                            <div>
                                <div class="font-headline-md text-headline-md text-secondary-fixed text-lg">$${itemTotal.toFixed(2)}</div>
                                <div class="text-xs text-on-surface-variant">Bs. ${itemTotalBs}</div>
                            </div>
                            <div class="flex items-center gap-3 bg-surface-container-high rounded-lg px-2 py-1 border border-glass-border">
                                <button onclick="window.Cart.updateQty('${item.id}', -1)" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                    <span class="material-symbols-outlined" style="font-size: 16px;">remove</span>
                                </button>
                                <span class="text-on-surface font-label-md w-4 text-center">${item.qty}</span>
                                <button onclick="window.Cart.updateQty('${item.id}', 1)" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                    <span class="material-symbols-outlined" style="font-size: 16px;">add</span>
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                itemsContainer.appendChild(div);
            });
        }

        // Render Totals
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

    // React to any cart change globally
    window.addEventListener('cartUpdated', renderCheckout);
    
    // Initial Render
    renderCheckout();
});
"""

with open('js/checkout.js', 'w', encoding='utf-8') as f:
    f.write(checkout_js)

print("Senior Frontend Refactoring completed!")
