import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the specific text
# To be safe, let's find the exact block.
old_block = '<h3 class="font-label-md text-label-md text-on-surface">Snacks</h3>'
new_block = '<h3 class="font-label-md text-label-md text-on-surface">Despensa</h3>'

if old_block in html:
    html = html.replace(old_block, new_block)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Renamed Snacks to Despensa.")
else:
    print("Could not find the Snacks block.")
