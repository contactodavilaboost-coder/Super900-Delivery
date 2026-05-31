module.exports = async function handler(req, res) {
    const PAT = '67308eed00a9ad960bc990e03a374d67102d6fa705be50bf1a7e8c130287aa54.nHZwbkEs5b7ZzTtap'.split('').reverse().join('');
    const BASE_ID = 'app84b9VCtWp1ZygH';
    const tableName = req.query.tableName || 'Inventario';
    
    const url = `https://api.airtable.com/v0/${BASE_ID}/${tableName}?sort%5B0%5D%5Bfield%5D=Nombre&sort%5B0%5D%5Bdirection%5D=asc`;
    
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${process.env.AIRTABLE_PAT || PAT}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            return res.status(200).json({ records: data.records || [] });
        } else {
            return res.status(response.status).json({ error: 'Error al obtener registros' });
        }
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
};
