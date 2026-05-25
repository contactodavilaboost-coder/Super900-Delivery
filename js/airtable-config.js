/**
 * Super900 - Airtable Central Configuration and API Utility
 */

const AirtableConfig = {
    DEFAULT_BASE_ID: 'app84b9VCtWp1ZygH',
    STORAGE_KEY_PAT: 'super900_airtable_pat',
    STORAGE_KEY_BASE: 'super900_airtable_base',

    getBaseId() {
        return localStorage.getItem(this.STORAGE_KEY_BASE) || this.DEFAULT_BASE_ID;
    },

    getPAT() {
        return localStorage.getItem(this.STORAGE_KEY_PAT) || '';
    },

    saveConfig(pat, baseId) {
        localStorage.setItem(this.STORAGE_KEY_PAT, pat.trim());
        localStorage.setItem(this.STORAGE_KEY_BASE, baseId.trim());
    },

    clearConfig() {
        localStorage.removeItem(this.STORAGE_KEY_PAT);
        localStorage.removeItem(this.STORAGE_KEY_BASE);
    },

    isConfigured() {
        return this.getPAT().length > 0;
    },

    async testConnection() {
        const pat = this.getPAT();
        const baseId = this.getBaseId();
        if (!pat) return { success: false, message: 'No se ha configurado un Token de Acceso (PAT).' };

        try {
            const response = await fetch(`https://api.airtable.com/v0/${baseId}/Inventario?maxRecords=1`, {
                headers: {
                    'Authorization': `Bearer ${pat}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                return { success: true, message: '¡Conexión establecida con éxito!' };
            } else {
                const errData = await response.json().catch(() => ({}));
                return { 
                    success: false, 
                    message: errData.error?.message || `Error de servidor: ${response.status}` 
                };
            }
        } catch (error) {
            return { success: false, message: 'Error de red o CORS al contactar Airtable.' };
        }
    },

    async getRecords(tableName, filterByFormula = '') {
        if (!this.isConfigured()) return null;
        
        const pat = this.getPAT();
        const baseId = this.getBaseId();
        
        let url = `https://api.airtable.com/v0/${baseId}/${encodeURIComponent(tableName)}`;
        if (filterByFormula) {
            url += `?filterByFormula=${encodeURIComponent(filterByFormula)}`;
        }

        try {
            const response = await fetch(url, {
                headers: {
                    'Authorization': `Bearer ${pat}`,
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            return data.records;
        } catch (e) {
            console.error(`Error fetching records from ${tableName}:`, e);
            return null;
        }
    },

    getFieldValue(fields, possibleNames) {
        for (const name of possibleNames) {
            if (fields[name] !== undefined) return fields[name];
        }
        return undefined;
    },

    getImageUrl(fields) {
        // Try to find the image URL from an attachment field
        for (const key of Object.keys(fields)) {
            const val = fields[key];
            if (Array.isArray(val) && val.length > 0 && val[0].url) {
                return val[0].url;
            }
        }
        return null;
    }
};

window.AirtableConfig = AirtableConfig;