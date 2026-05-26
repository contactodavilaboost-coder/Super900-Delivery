/**
 * Super900 - Checkout & Cart Rendering Logic
 */

document.addEventListener('DOMContentLoaded', async () => {
    // Only run if we are on the checkout page
    const cartWrapper = document.getElementById('cart-drawer-copy');
    if (!cartWrapper) return;

    if (!window.Cart || !window.AirtableConfig) {
        console.error("Cart or AirtableConfig missing");
        return;
    }

    // Ensure BCV Rate is loaded
    const bcvRate = await AirtableConfig.getExchangeRate();

    const renderCheckoutCart = () => {
        const cartItems = Cart.getCart();
        const itemsContainer = cartWrapper.querySelector('.overflow-y-auto');
        const countBadge = cartWrapper.querySelector('h2').nextElementSibling;
        const totalContainer = cartWrapper.querySelector('.space-y-3.pt-4'); // Container for totals

        if (!itemsContainer || !totalContainer) return;

        // Update counts
        const totalItems = Cart.getTotalItems();
        countBadge.innerText = `${totalItems} items`;

        // Calculate Totals
        let subtotalUSD = 0;
        
        // Render items
        if (cartItems.length === 0) {
            itemsContainer.innerHTML = `
                <div class="py-12 flex flex-col items-center justify-center text-on-surface-variant text-center opacity-70">
                    <span class="material-symbols-outlined text-6xl mb-4">shopping_cart_checkout</span>
                    <p class="font-body-lg">Tu carrito está vacío</p>
                    <a href="index.html" class="mt-4 text-primary hover:underline">Volver a la tienda</a>
                </div>
            `;
            subtotalUSD = 0;
        } else {
            itemsContainer.innerHTML = ''; // Clear hardcoded
            cartItems.forEach(item => {
                const itemTotal = item.price * item.qty;
                subtotalUSD += itemTotal;
                
                const itemTotalBs = (itemTotal * bcvRate).toFixed(2);
                
                const div = document.createElement('div');
                div.className = 'flex gap-4 p-4 rounded-xl bg-surface-container-low border border-glass-border hover:bg-surface-container transition-colors group relative';
                div.innerHTML = `
                    <div class="w-20 h-20 rounded-lg bg-white overflow-hidden relative flex-shrink-0 p-1">
                        <img src="${item.img}" alt="${item.name}" class="w-full h-full object-contain">
                    </div>
                    <div class="flex flex-col flex-1 justify-between">
                        <div class="flex justify-between items-start">
                            <div class="pr-6">
                                <h3 class="font-label-md text-label-md text-on-surface line-clamp-1">${item.name}</h3>
                                <p class="text-on-surface-variant text-sm mt-0.5">${item.unit}</p>
                            </div>
                            <button onclick="Cart.removeItem('${item.id}'); renderCheckoutCart();" class="text-outline-variant hover:text-error absolute top-4 right-4 transition-colors">
                                <span class="material-symbols-outlined" style="font-size: 18px;">delete</span>
                            </button>
                        </div>
                        <div class="flex justify-between items-end mt-2">
                            <div>
                                <div class="font-headline-md text-headline-md text-secondary-fixed text-lg">$${itemTotal.toFixed(2)}</div>
                                <div class="text-xs text-on-surface-variant">Bs. ${itemTotalBs}</div>
                            </div>
                            <div class="flex items-center gap-3 bg-surface-container-high rounded-lg px-2 py-1 border border-glass-border">
                                <button onclick="Cart.updateQty('${item.id}', -1); renderCheckoutCart();" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
                                    <span class="material-symbols-outlined" style="font-size: 16px;">remove</span>
                                </button>
                                <span class="text-on-surface font-label-md w-4 text-center">${item.qty}</span>
                                <button onclick="Cart.updateQty('${item.id}', 1); renderCheckoutCart();" class="text-on-surface hover:text-primary transition-colors flex items-center justify-center">
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
        const deliveryFee = subtotalUSD > 0 ? 5.00 : 0;
        const totalUSD = subtotalUSD + deliveryFee;
        const totalBs = (totalUSD * bcvRate).toFixed(2);
        
        totalContainer.innerHTML = `
            <div class="flex justify-between text-on-surface-variant">
                <span class="text-body-md">Subtotal</span>
                <span class="text-body-md">$${subtotalUSD.toFixed(2)}</span>
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

    // Make renderCheckoutCart globally accessible so inline onclick handlers work
    window.renderCheckoutCart = renderCheckoutCart;

    // Initial render
    renderCheckoutCart();
});
