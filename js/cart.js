
function showToast(message) {
    let toast = document.getElementById('cart-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'cart-toast';
        toast.className = 'fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-success-green text-white px-4 py-2 rounded-lg shadow-lg z-50 transition-opacity duration-300 opacity-0';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.remove('opacity-0');
    toast.classList.add('opacity-100');
    setTimeout(() => {
        toast.classList.remove('opacity-100');
        toast.classList.add('opacity-0');
    }, 2500);
}
/**
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
