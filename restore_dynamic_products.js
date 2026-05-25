const fs = require('fs');
const path = require('path');

const dir = 'd:/monke/antigravityqlq/SUPER900';
const filesMap = {
    'index.html': { filter: "r.fields.Destacado || r.fields.Oferta" },
    'carnes.html': { filter: "r.fields.Categoria === 'Carnes'" },
    'despensa.html': { filter: "r.fields.Categoria === 'Despensa'" },
    'verduras.html': { filter: "r.fields.Categoria === 'Verduras'" }
};

for (const [file, config] of Object.entries(filesMap)) {
    const filePath = path.join(dir, file);
    if (!fs.existsSync(filePath)) continue;

    let content = fs.readFileSync(filePath, 'utf8');

    // Add ID to the main grid. We assume it's the one with grid-cols-2 md:grid-cols-3 or similar.
    // In index.html: <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
    content = content.replace(/<div class="grid grid-cols-2 (.*?) gap-4 md:gap-6(?!.*id=)">/, '<div id="dynamic-products-grid" class="grid grid-cols-2 $1 gap-4 md:gap-6">');
    // If it didn't match because of spacing or exact classes, try a more generic replace
    if (!content.includes('id="dynamic-products-grid"')) {
        content = content.replace(/<div class="grid grid-cols-2(.*?)">/, '<div id="dynamic-products-grid" class="grid grid-cols-2$1">');
    }

    // Inject Javascript before </body>
    const script = `
<script>
document.addEventListener('DOMContentLoaded', async () => {
    if (!AirtableConfig || !AirtableConfig.isConfigured()) return;

    const grid = document.getElementById('dynamic-products-grid');
    if (!grid) return;

    const loadingEl = document.createElement('div');
    loadingEl.className = 'col-span-full py-12 flex flex-col items-center justify-center text-on-surface-variant gap-3';
    loadingEl.innerHTML = \`
        <span class="material-symbols-outlined animate-spin text-4xl text-primary">sync</span>
        <p class="text-sm font-label-md">Cargando productos...</p>
    \`;
    grid.innerHTML = '';
    grid.appendChild(loadingEl);

    const records = await AirtableConfig.getRecords('Inventario');
    if (!records || records.length === 0) {
        console.warn('Airtable no retornó registros.');
        return;
    }

    grid.innerHTML = '';
    const filtered = records.filter(r => ${config.filter});
    const displayList = filtered.length > 0 ? filtered : records;

    displayList.forEach(rec => {
        const f = rec.fields;
        const name = AirtableConfig.getFieldValue(f, ['Nombre', 'Name']) || 'Producto';
        const priceVal = AirtableConfig.getFieldValue(f, ['Precio_Regular', 'Precio', 'Price']);
        const price = priceVal !== undefined ? parseFloat(priceVal) : 0.00;
        const unit = AirtableConfig.getFieldValue(f, ['Unidad_Medida', 'Unidad', 'Unit']) || 'ud';
        const isOffer = AirtableConfig.getFieldValue(f, ['Oferta', 'Offer']) || false;
        const offerPriceVal = AirtableConfig.getFieldValue(f, ['Precio_Oferta', 'OfferPrice']);
        const offerPrice = offerPriceVal !== undefined ? parseFloat(offerPriceVal) : 0.00;
        const img = AirtableConfig.getImageUrl(f) || 'https://via.placeholder.com/400';

        const card = document.createElement('div');
        card.className = 'bg-charcoal-surface rounded-xl border border-glass-border overflow-hidden flex flex-col group hover:border-primary/50 transition-all duration-500 hover:shadow-glow hover:-translate-y-1 relative';
        
        card.innerHTML = \`
            <div class="relative h-40 md:h-48 bg-surface-container-high overflow-hidden">
                <img src="\${img}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90" alt="\${name}">
                \${isOffer ? '<span class="absolute top-2 left-2 bg-error text-on-error font-label-sm px-2 py-1 rounded-full text-xs font-bold shadow-soft">OFERTA</span>' : ''}
                <button class="absolute top-3 right-3 w-8 h-8 rounded-full bg-surface/50 backdrop-blur-md flex items-center justify-center border border-glass-border text-on-surface hover:text-error transition-all duration-300">
                    <span class="material-symbols-outlined" style="font-size: 18px;">favorite</span>
                </button>
            </div>
            <div class="p-4 flex-1 flex flex-col">
                <h4 class="font-label-md text-label-md text-on-surface mb-1 line-clamp-2">\${name}</h4>
                <p class="font-label-sm text-label-sm text-on-surface-variant mb-4">\${unit}</p>
                <div class="mt-auto flex items-center justify-between">
                    <div class="flex flex-col">
                        \${isOffer ? \`<span class="text-xs text-on-surface-variant line-through">$\${price.toFixed(2)}</span>
                                     <span class="font-headline-md text-headline-md text-error shadow-glow-secondary">$\${offerPrice.toFixed(2)}</span>\`
                                  : \`<span class="font-headline-md text-headline-md text-on-surface">$\${price.toFixed(2)}</span>\` }
                    </div>
                    <button class="w-10 h-10 rounded-lg bg-secondary text-on-secondary-fixed flex items-center justify-center hover:bg-secondary-fixed-dim transition-all duration-300 hover:shadow-glow-secondary hover:-translate-y-0.5 shadow-soft add-to-cart-btn">
                        <span class="material-symbols-outlined">add</span>
                    </button>
                </div>
            </div>
        \`;
        grid.appendChild(card);
    });
});
</script>
</body>`;
    
    // Remove old inline scripts if they exist so we don't duplicate
    content = content.replace(/<script>\s*document\.addEventListener\('DOMContentLoaded', async \(\) => {[\s\S]*?<\/script>\s*<\/body>/, '</body>');

    content = content.replace('</body>', script);
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Restored dynamic products for ' + file);
}
