document.addEventListener('DOMContentLoaded', async () => {
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
