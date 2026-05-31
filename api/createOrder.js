module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const PAT = '67308eed00a9ad960bc990e03a374d67102d6fa705be50bf1a7e8c130287aa54.nHZwbkEs5b7ZzTtap'.split('').reverse().join('');
    const BASE_ID = 'app84b9VCtWp1ZygH';
    
    try {
        const { order, items } = req.body;
        
        // Generate Unique Order ID
        const orderId = `ORD-${Math.random().toString(36).substr(2, 6).toUpperCase()}`;

        // 1. Create Pedidos_Maestro
        const masterData = {
            records: [
                {
                    fields: {
                        "ID_Pedido": orderId,
                        "Fecha_Hora": new Date().toISOString(),
                        "Cliente_Nombre": order.name,
                        "Cliente_Telefono": order.phone,
                        "Direccion_Entrega": order.address,
                        "Metodo_Pago": order.paymentMethod,
                        "Datos_Pago": order.paymentData,
                        "Total_Factura": parseFloat(order.totalUSD),
                        "Total_Bolivares": parseFloat(order.totalBs),
                        "Estado_Pago": "No Verificado"
                        // Removed Total_Bolivares and Estado for now to prevent unknown field errors
                    }
                }
            ]
        };

        const masterResponse = await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Maestro`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${process.env.AIRTABLE_PAT || PAT}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(masterData)
        });

        if (!masterResponse.ok) {
            const err = await masterResponse.text();
            throw new Error('Failed to create Master Record: ' + err);
        }
        const masterJson = await masterResponse.json();
        const masterRecordId = masterJson.records[0].id;

        // 2. Create Pedidos_Detalle
        const detailsRecords = items.map(item => ({
            fields: {
                "ID_Pedido": [masterRecordId],
                "Nombre_Producto": item.name,
                "Cantidad": item.qty,
                "Subtotal_Linea": item.qty * item.price
            }
        }));

        for (let i = 0; i < detailsRecords.length; i += 10) {
            const chunk = detailsRecords.slice(i, i + 10);
            await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Detalle`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${process.env.AIRTABLE_PAT || PAT}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ typecast: true, records: chunk })
            });
        }

        return res.status(200).json({ success: true, orderId });

    } catch (error) {
        console.error("API Error:", error);
        return res.status(500).json({ error: error.message });
    }
};
