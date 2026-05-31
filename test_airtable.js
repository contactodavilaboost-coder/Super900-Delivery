const PAT = '65d70d1241f225ee17c059fe62fab65a5b6fdb9d7b30da85cf5cfaa926954587.e0tMY75UCdHgx2tap'.split('').reverse().join('');
const BASE_ID = 'app84b9VCtWp1ZygH';

async function test() {
    const orderId = `ORD-TEST`;
    const masterData = {
        records: [
            {
                fields: {
                    "ID_Pedidos": orderId,
                    "Fecha_Hora": new Date().toISOString(),
                    "Cliente_Nombre": "Test Name",
                    "Cliente_Telefono": "123456789",
                    "Direccion_Entrega": "Test Address",
                    "Metodo_Pago": "Efectivo",
                    "Datos_Pago": "Efectivo",
                    "Total_Factura": 10.50,
                    "Total_Bolivares": 400.00,
                    "Estado_Pago": "Pendiente",
                    "Estado Logistica": "Por confirmar"
                }
            }
        ]
    };

    console.log("Testing Pedidos_Maestros with 'Estado Logistica'...");
    let res = await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Maestros`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${PAT}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(masterData)
    });
    
    console.log("Status:", res.status);
    console.log("Response:", await res.text());

    const masterData2 = {
        records: [
            {
                fields: {
                    "ID_Pedidos": orderId,
                    "Fecha_Hora": new Date().toISOString(),
                    "Cliente_Nombre": "Test Name",
                    "Cliente_Telefono": "123456789",
                    "Direccion_Entrega": "Test Address",
                    "Metodo_Pago": "Efectivo",
                    "Datos_Pago": "Efectivo",
                    "Total_Factura": 10.50,
                    "Total_Bolivares": 400.00,
                    "Estado_Pago": "Pendiente",
                    "Estado_Logistica": "Por confirmar"
                }
            }
        ]
    };

    console.log("\\nTesting Pedidos_Maestros with 'Estado_Logistica'...");
    res = await fetch(`https://api.airtable.com/v0/${BASE_ID}/Pedidos_Maestros`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${PAT}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(masterData2)
    });
    console.log("Status:", res.status);
    console.log("Response:", await res.text());
}

test();
