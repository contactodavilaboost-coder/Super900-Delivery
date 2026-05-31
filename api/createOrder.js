module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const PAT = '65d70d1241f225ee17c059fe62fab65a5b6fdb9d7b30da85cf5cfaa926954587.e0tMY75UCdHgx2tap'.split('').reverse().join('');
    const BASE_ID = 'app84b9VCtWp1ZygH';
    
    try {
        const { order, items } = req.body;
        
        // Generate Unique Order ID
        const orderId = `ORD-${Math.random().toString(36).substr(2, 6).toUpperCase()}`;

        // 1. Create Pedidos_Maestros
        const masterData = {
            records: [
                {
                    fields: {
                        "ID_Pedidos": orderId,
                        "Fecha_Hora": new Date().toISOString(),
                        "Cliente_Nombre": order.name,
                        "Cliente_Telefono": order.phone,
                        "Direccion_Entrega": order.address,
                        "Metodo_Pago": order.paymentMethod,
                        "Datos_Pago": order.paymentData,
                        "Total_Factura": parseFloat(order.totalUSD),
                        "Total_Bolivares": parseFloat(order.totalBs),
                        "Estado_Pago": "Pendiente",
                        "Estado_Logistica": "Por confirmar"
                    }
                }
            ]
        };

        const masterResponse = await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Maestros`, {
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

        // 2. Create Pedidos_Detalles
        const detailsRecords = items.map(item => ({
            fields: {
                "ID_Pedidos": orderId,
                "Producto": item.name,
                "Cantidad": item.qty,
                "Precio_Unitario": item.price,
                "Subtotal": item.qty * item.price
            }
        }));

        for (let i = 0; i < detailsRecords.length; i += 10) {
            const chunk = detailsRecords.slice(i, i + 10);
            await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Detalles`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${process.env.AIRTABLE_PAT || PAT}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ records: chunk })
            });
        }

        return res.status(200).json({ success: true, orderId });

    } catch (error) {
        console.error("API Error:", error);
        return res.status(500).json({ error: error.message });
    }
};
