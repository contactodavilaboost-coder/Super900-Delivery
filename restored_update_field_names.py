import os

workspace_dir = r"d:\monke\antigravityqlq\SUPER900"
files = ["index.html", "verduras.html", "carnes.html", "despensa.html"]

for fname in files:
    fpath = os.path.join(workspace_dir, fname)
    if not os.path.exists(fpath):
        continue
        
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace field list lookups for Price and Unit
    content = content.replace(
        "AirtableConfig.getFieldValue(f, ['Precio', 'Price'])",
        "AirtableConfig.getFieldValue(f, ['Precio_Regular', 'Precio', 'Price'])"
    )
    content = content.replace(
        "AirtableConfig.getFieldValue(f, ['Unidad', 'Unit'])",
        "AirtableConfig.getFieldValue(f, ['Unidad_Medida', 'Unidad', 'Unit'])"
    )

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Updated lookup fields in {fname} to search for Precio_Regular and Unidad_Medida!")
