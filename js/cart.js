/**
 * Super900 - Cart Logic
 */

const Cart = {
    STORAGE_KEY: 'super900_cart',

    getCart() {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY)) || [];
        } catch (e) {
            return [];
        }
    },

    saveCart(cartArray) {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cartArray));
        this.updateBadge();
    },

    addItem(product) {
        const cart = this.getCart();
        const existing = cart.find(p => p.id === product.id);
        
        if (existing) {
            existing.qty += 1;
        } else {
            cart.push({ ...product, qty: 1 });
        }
        
        this.saveCart(cart);
        this.showToast(`Agregado: ${product.name}`);
    },

    removeItem(id) {
        let cart = this.getCart();
        cart = cart.filter(p => p.id !== id);
        this.saveCart(cart);
    },

    updateQty(id, delta) {
        let cart = this.getCart();
        const existing = cart.find(p => p.id === id);
        if (existing) {
            existing.qty += delta;
            if (existing.qty <= 0) {
                this.removeItem(id);
                return;
            }
        }
        this.saveCart(cart);
    },

    clearCart() {
        localStorage.removeItem(this.STORAGE_KEY);
        this.updateBadge();
    },

    getTotalItems() {
        return this.getCart().reduce((sum, item) => sum + item.qty, 0);
    },

    updateBadge() {
        const count = this.getTotalItems();
        // Update any element with class 'cart-badge-counter'
        const badges = document.querySelectorAll('.cart-badge-counter');
        badges.forEach(b => {
            b.innerText = count;
            if (count > 0) {
                b.style.display = 'flex';
            } else {
                b.style.display = 'none';
            }
        });
    },

    showToast(message) {
        let toast = document.getElementById('cart-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'cart-toast';
            toast.className = 'fixed bottom-20 left-1/2 -translate-x-1/2 bg-surface-container-high text-on-surface px-6 py-3 rounded-full shadow-lg z-[100] transition-opacity duration-300 opacity-0 pointer-events-none font-label-md border border-glass-border';
            document.body.appendChild(toast);
        }
        toast.innerText = message;
        toast.classList.remove('opacity-0');
        toast.classList.add('opacity-100');
        
        // Hide after 2 seconds
        if (this.toastTimeout) clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
            toast.classList.remove('opacity-100');
            toast.classList.add('opacity-0');
        }, 2000);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Cart.updateBadge();
});

window.Cart = Cart;