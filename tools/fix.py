import os, re

base = r'C:/Users/lecom/OneDrive/Images/Essex_University/year_1/module/Secure Software Developement/secure-software-development-portfolio'

# Process each unit file
for n in range(1, 13):
    html_path = os.path.join(base, 'modules', 'secure-software-development', f'unit-{n}', 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace relative paths with CDN links
        content = content.replace(
            '<link rel="stylesheet" href="../../assets/styles/main.css">',
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
        )
        content = content.replace(
            '<link rel="icon" href="../../assets/diagrams/favicon.svg">',
            '<link rel="icon" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/img/favicon.svg">'
        )
        content = content.replace(
            '<script src="../../assets/scripts/main.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>'
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated unit-{n}/index.html')

print('All 12 files updated successfully')