import os

new_cart_js = """
/**
 * Super900 - Advanced Global Cart Drawer & State Manager
 */
class ShoppingCart {
    constructor() {
        this.STORAGE_KEY = 'super900_cart';
        this.items = this.loadCart();
        this.bcvRate = 535; // Fallback
        
        // Setup DOM when ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    async init() {
        try {
            if (window.AirtableConfig && typeof window.AirtableConfig.getExchangeRate === 'function') {
                this.bcvRate = await window.AirtableConfig.getExchangeRate();
            }
        } catch(e) {
            console.error("Error fetching BCV:", e);
        }
        
        this.injectDrawerHTML();
        this.initListeners();
        this.notify();
    }

    loadCart() {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY)) || [];
        } catch (e) {
            return [];
        }
    }

    saveCart() {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.items));
        this.notify();
    }

    notify() {
        window.dispatchEvent(new CustomEvent('cartUpdated', { detail: { items: this.items } }));
        this.renderDrawer();
    }

    addItem(product) {
        const existing = this.items.find(p => p.id === product.id);
        if (existing) {
            existing.qty += 1;
        } else {
            this.items.push({ ...product, qty: 1 });
        }
        this.saveCart();
        this.showToast(`¡Agregado al carrito!`);
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

    // -- UI METHODS --

    injectDrawerHTML() {
        if (document.getElementById('super900-cart-drawer-overlay')) return;

        const overlay = document.createElement('div');
        overlay.id = 'super900-cart-drawer-overlay';
        overlay.className = 'fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] opacity-0 pointer-events-none transition-opacity duration-300';
        overlay.onclick = () => this.closeDrawer();

        const drawer = document.createElement('div');
        drawer.id = 'super900-cart-drawer';
        drawer.className = 'fixed top-0 right-0 h-full w-full sm:w-[400px] bg-surface-container-lowest shadow-2xl z-[101] transform translate-x-full transition-transform duration-300 flex flex-col';
        
        drawer.innerHTML = `
            <div class="flex items-center justify-between px-6 py-4 border-b border-glass-border bg-charcoal-surface">
                <div class="flex items-center gap-3">
                    <span class="material-symbols-outlined text-primary text-2xl">shopping_cart</span>
                    <h2 class="font-headline-md text-headline-md text-on-surface m-0">Tu Carrito</h2>
                    <span id="drawer-item-count" class="bg-surface-container-highest text-on-surface-variant font-label-sm text-label-sm px-2 py-0.5 rounded-full">0</span>
                </div>
                <button id="close-drawer-btn" class="text-on-surface-variant hover:text-error transition-colors p-1">
                    <span class="material-symbols-outlined">close</span>
                </button>
            </div>
            
            <div id="drawer-items-container" class="flex-1 overflow-y-auto p-4 space-y-4 bg-charcoal-surface">
                <!-- Items injected here -->
            </div>
            
            <div class="p-6 bg-charcoal-surface border-t border-glass-border">
                <div class="space-y-2 mb-4">
                    <div class="flex justify-between text-on-surface-variant">
                        <span class="text-body-md">Subtotal</span>
                        <span id="drawer-subtotal" class="text-body-md font-bold">$0.00</span>
                    </div>
                    <div class="flex justify-between items-end pt-2 border-t border-glass-border">
                        <span class="font-headline-md text-headline-md text-on-surface">Total</span>
                        <div class="text-right">
                            <div id="drawer-total-usd" class="font-headline-md text-headline-md text-secondary text-xl leading-none">$0.00</div>
                            <div id="drawer-total-bs" class="text-sm text-on-surface-variant mt-1">Bs. 0.00</div>
                        </div>
                    </div>
                </div>
                <a href="checkout.html" class="bypass-drawer w-full block text-center bg-primary text-on-primary font-headline-md text-headline-md py-3 rounded-xl hover:bg-primary-fixed transition-colors shadow-lg">
                    Ir a Pagar
                </a>
            </div>
        `;

        document.body.appendChild(overlay);
        document.body.appendChild(drawer);
        
        document.getElementById('close-drawer-btn').onclick = () => this.closeDrawer();
    }

    openDrawer() {
        const overlay = document.getElementById('super900-cart-drawer-overlay');
        const drawer = document.getElementById('super900-cart-drawer');
        if (overlay && drawer) {
            overlay.classList.remove('opacity-0', 'pointer-events-none');
            overlay.classList.add('opacity-100', 'pointer-events-auto');
            drawer.classList.remove('translate-x-full');
            drawer.classList.add('translate-x-0');
            this.renderDrawer();
        }
    }

    closeDrawer() {
        const overlay = document.getElementById('super900-cart-drawer-overlay');
        const drawer = document.getElementById('super900-cart-drawer');
        if (overlay && drawer) {
            overlay.classList.remove('opacity-100', 'pointer-events-auto');
            overlay.classList.add('opacity-0', 'pointer-events-none');
            drawer.classList.remove('translate-x-0');
            drawer.classList.add('translate-x-full');
        }
    }

    renderDrawer() {
        const container = document.getElementById('drawer-items-container');
        if (!container) return;

        document.getElementById('drawer-item-count').textContent = this.getTotalItems();

        if (this.items.length === 0) {
            container.innerHTML = `
                <div class="h-full flex flex-col items-center justify-center text-on-surface-variant opacity-70">
                    <span class="material-symbols-outlined text-6xl mb-4">shopping_cart_checkout</span>
                    <p class="font-body-lg">Tu carrito está vacío</p>
                    <button onclick="window.Cart.closeDrawer()" class="mt-4 text-primary hover:underline">Continuar comprando</button>
                </div>
            `;
            document.getElementById('drawer-subtotal').textContent = "$0.00";
            document.getElementById('drawer-total-usd').textContent = "$0.00";
            document.getElementById('drawer-total-bs').textContent = "Bs. 0.00";
            return;
        }

        container.innerHTML = '';
        this.items.forEach(item => {
            const itemTotal = item.price * item.qty;
            
            const div = document.createElement('div');
            div.className = 'flex gap-3 p-3 rounded-xl bg-surface-container-low border border-glass-border hover:bg-surface-container transition-colors group relative';
            div.innerHTML = `
                <div class="w-16 h-16 rounded-lg bg-white overflow-hidden relative flex-shrink-0 p-1">
                    <img src="${item.img}" alt="${item.name.replace(/"/g, '&quot;')}" class="w-full h-full object-contain">
                </div>
                <div class="flex flex-col flex-1 justify-between py-0.5">
                    <div class="flex justify-between items-start">
                        <div class="pr-5">
                            <h3 class="font-label-md text-label-md text-on-surface line-clamp-1 leading-tight">${item.name}</h3>
                            <p class="text-on-surface-variant text-xs mt-0.5">${item.unit}</p>
                        </div>
                        <button onclick="window.Cart.removeItem('${item.id}')" class="text-outline-variant hover:text-error absolute top-2 right-2 transition-colors">
                            <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
                        </button>
                    </div>
                    <div class="flex justify-between items-end mt-2">
                        <div class="font-headline-md text-headline-md text-secondary-fixed text-base">$${itemTotal.toFixed(2)}</div>
                        
                        <div class="flex items-center gap-2 bg-surface-container-high rounded-lg px-2 py-1 border border-glass-border">
                            <button onclick="window.Cart.updateQty('${item.id}', -1)" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                <span class="material-symbols-outlined" style="font-size: 14px;">remove</span>
                            </button>
                            <span class="text-on-surface font-label-md w-3 text-center text-xs">${item.qty}</span>
                            <button onclick="window.Cart.updateQty('${item.id}', 1)" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                <span class="material-symbols-outlined" style="font-size: 14px;">add</span>
                            </button>
                        </div>
                    </div>
                </div>
            `;
            container.appendChild(div);
        });

        const subtotal = this.getSubtotal();
        const totalBs = (subtotal * this.bcvRate).toFixed(2);
        
        document.getElementById('drawer-subtotal').textContent = `$${subtotal.toFixed(2)}`;
        document.getElementById('drawer-total-usd').textContent = `$${subtotal.toFixed(2)}`;
        document.getElementById('drawer-total-bs').textContent = `Bs. ${totalBs}`;
    }

    initListeners() {
        window.addEventListener('cartUpdated', () => {
            const count = this.getTotalItems();
            document.querySelectorAll('.cart-badge-counter').forEach(badge => {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'flex' : 'none';
            });
        });

        // Intercept global clicks
        document.addEventListener('click', (e) => {
            // Add To Cart
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
                // Optionally open drawer when item is added:
                this.openDrawer();
                return;
            }

            // Cart triggers
            const cartTrigger = e.target.closest('a[href="checkout.html"], button[onclick*="checkout.html"]');
            if (cartTrigger) {
                // If we are already on checkout page, let it navigate/stay.
                // Or if it's the specific bypass button inside the drawer, let it pass.
                if (!cartTrigger.classList.contains('bypass-drawer') && !window.location.pathname.includes('checkout.html')) {
                    e.preventDefault();
                    this.openDrawer();
                }
            }
        });
    }

    showToast(message) {
        let toast = document.getElementById('cart-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'cart-toast';
            toast.className = 'fixed bottom-20 left-1/2 -translate-x-1/2 bg-success-green text-white px-6 py-3 rounded-full shadow-lg z-[150] transition-all duration-300 transform translate-y-4 opacity-0 pointer-events-none font-label-md border border-glass-border';
            document.body.appendChild(toast);
        }
        toast.innerText = message;
        
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
    f.write(new_cart_js)

print("cart.js refactored successfully.")
