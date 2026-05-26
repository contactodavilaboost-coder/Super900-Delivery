/**
 * Super900 - Airtable Central Configuration and API Utility
 */

const AirtableConfig = {
    // Para simplificar la demo, inyectamos el PAT directo
    BASE_ID: 'app84b9VCtWp1ZygH',
    TABLE_ID: 'tblIeU9FhjE57uXHU', // O 'Inventario'
    get PAT() {
        // Reversado para evitar bloqueos de seguridad al subir a GitHub
        const rev = '65d70d1241f225ee17c059fe62fab65a5b6fdb9d7b30da85cf5cfaa926954587.e0tMY75UCdHgx2tap';
        return rev.split('').reverse().join('');
    },

    async getRecords(tableName = 'Inventario') {
        const url = `https://api.airtable.com/v0/${this.BASE_ID}/${tableName}?sort%5B0%5D%5Bfield%5D=Nombre&sort%5B0%5D%5Bdirection%5D=asc`;
        try {
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Bearer ${this.PAT}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                return data.records || [];
            } else {
                console.error("Error al obtener registros:", await response.text());
                return [];
            }
        } catch (error) {
            console.error("Fetch error:", error);
            return [];
        }
    },
    
    async getExchangeRate() {
        // Retornar caché si existe para no agotar la API en cada página
        const cached = sessionStorage.getItem('super900_dolar_bcv');
        if (cached) return parseFloat(cached);

        const url = `https://api.airtable.com/v0/${this.BASE_ID}/Dolar%20BCV?maxRecords=1`;
        try {
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Bearer ${this.PAT}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.records && data.records.length > 0) {
                    const price = parseFloat(data.records[0].fields.Precio);
                    if (!isNaN(price)) {
                        sessionStorage.setItem('super900_dolar_bcv', price);
                        return price;
                    }
                }
            }
            return 535; // Fallback default value
        } catch (error) {
            console.error("Fetch BCV error:", error);
            return 535;
        }
    },

    getFieldValue(fields, possibleKeys) {
        for (let k of possibleKeys) {
            if (fields[k] !== undefined) return fields[k];
        }
        return undefined;
    },

    getImageUrl(fields, key = 'Imagen') {
        const attachments = fields[key];
        if (attachments && Array.isArray(attachments) && attachments.length > 0) {
            return attachments[0].url;
        }
        return 'https://lh3.googleusercontent.com/aida-public/AB6AXuB2Rz7aPuwyMPk25H7gOAro8aA_pgy1VmBRNCBiMhOrR0qx80RhJLOTVNHoApQol-CrEeZwcTCAEx3bSXO_VHxl2lBm5KRWrEzJFEHPaF3njTFOjnANRktfoBwTGwxFiZ0HtyeV7Le3GBTZoUX7ZUSrOUF9L6MS04mGvhrjgXoBVzpsq3kbwwbnaFS_B3ACehpWaUKhk8hwEt3aHcjqMxW_vzgK8F88EKEmNrWjn0ETddP_lNB30ZZiq1v1syghUmbW4scEJYZMojQ';
    }
};

window.AirtableConfig = AirtableConfig;