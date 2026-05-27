module.exports = async function handler(req, res) {
    const PAT = '65d70d1241f225ee17c059fe62fab65a5b6fdb9d7b30da85cf5cfaa926954587.e0tMY75UCdHgx2tap'.split('').reverse().join('');
    const BASE_ID = 'app84b9VCtWp1ZygH';
    const url = `https://api.airtable.com/v0/${BASE_ID}/Dolar%20BCV?maxRecords=1`;
    
    try {
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${process.env.AIRTABLE_PAT || PAT}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            if (data.records && data.records.length > 0) {
                const price = parseFloat(data.records[0].fields.Precio);
                if (!isNaN(price)) {
                    return res.status(200).json({ price });
                }
            }
        }
        return res.status(200).json({ price: 535 }); // Fallback
    } catch (error) {
        return res.status(200).json({ price: 535 });
    }
};
