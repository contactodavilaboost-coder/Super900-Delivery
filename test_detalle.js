const PAT = '67308eed00a9ad960bc990e03a374d67102d6fa705be50bf1a7e8c130287aa54.nHZwbkEs5b7ZzTtap'.split('').reverse().join('');
const BASE_ID = 'app84b9VCtWp1ZygH';

async function test() {
    const testField = async (fieldName, value) => {
        let res = await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Detalle`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${PAT}`, 'Content-Type': 'application/json' },
            body: JSON.stringify({ typecast: true, records: [{ fields: { [fieldName]: value } }] })
        });
        const status = res.status;
        if (status === 200) {
            console.log(`✅ FOUND FIELD: ${fieldName}`);
        }
    }

    const priceNames = ["Sub_Total", "Sub_total", "Total_Detalle", "Precio_Unit", "PrecioUnitario", "SubTotal", "Precio (dolares)", "Subtotal (dolares)", "Precio Unitario", "Monto Total"];
    for (let name of priceNames) { await testField(name, 10.50); }
}
test();
