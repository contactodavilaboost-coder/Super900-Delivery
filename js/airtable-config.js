const AirtableConfig = {
    async getRecords(tableName = 'Inventario') {
        try {
            const response = await fetch(`/api/getProducts?tableName=${tableName}`);
            if (response.ok) {
                const data = await response.json();
                return data.records || [];
            }
            return [];
        } catch (error) {
            console.error("Fetch error:", error);
            return [];
        }
    },
    
    async getExchangeRate() {
        const cached = sessionStorage.getItem('super900_dolar_bcv');
        if (cached) return parseFloat(cached);

        try {
            const response = await fetch(`/api/getExchangeRate`);
            if (response.ok) {
                const data = await response.json();
                if (data.price) {
                    sessionStorage.setItem('super900_dolar_bcv', data.price);
                    return data.price;
                }
            }
            return 535;
        } catch (error) {
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
