import markdown
import yaml
from jinja2 import Environment, FileSystemLoader
import os

# Directory to store rendered markdown files
RENDERED_DIR = "rendered_markdown"

# Ensure the directory exists
if not os.path.exists(RENDERED_DIR):
    os.makedirs(RENDERED_DIR)

# Load data from YAML
with open("data.yaml", "r") as file:
    data = yaml.safe_load(file)

# Convert markdown to HTML for entries with markdown content
for entry in data:
    if 'markdown' in entry:
        with open(entry['markdown'], 'r') as md_file:
            md_content = md_file.read()
            html_content = markdown.markdown(md_content)
            
            # Save the HTML content to a separate file
            rendered_filename = os.path.join(RENDERED_DIR, os.path.basename(entry['markdown']).replace('.markdown', '.html'))
            with open(rendered_filename, 'w') as html_file:
                html_file.write(html_content)
            
            # Update the markdown entry to link to the rendered HTML file
            entry['markdown_link'] = rendered_filename

# Set up the Jinja2 environment and load the template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('index.j2')

# Render the template with the YAML data
rendered_html = template.render(items=data)

# Save the rendered HTML to a file
with open("index.html", "w") as file:
    file.write(rendered_html)

print("HTML file generated successfully.")
