import os

base = r'C:/Users/lecom/OneDrive/Images/Essex_University/year_1/module/Secure Software Developement/secure-software-development-portfolio'

# Find all unit directories
units = [d for d in os.listdir(os.path.join(base, 'modules', 'secure-software-development')) 
         if d.startswith('unit-') and os.path.isdir(os.path.join(base, 'modules', 'secure-software-development', d))]

print(f'Found {len(units)} unit directories')

for unit in units:
    html_path = os.path.join(base, 'modules', 'secure-software-development', unit, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Replace the CSS link
        new_content = content.replace(
            '<link rel="stylesheet" href="../../assets/styles/main.css">',
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">'
        )
        # Also replace the favicon link
        new_content = new_content.replace(
            '<link rel="icon" href="../../assets/diagrams/favicon.svg">',
            '<link rel="icon" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/img/favicon.svg">'
        )
        if new_content != content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {unit}/index.html')
        else:
            print(f'No change needed for {unit}/index.html')

print('Done!')