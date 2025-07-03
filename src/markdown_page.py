import os
from markdown_blocks import markdown_to_html_node, extract_title

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        if os.path.isdir(os.path.join(dir_path_content, file)):
            generate_page_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
        elif file.endswith(".md"):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file[:-3] + ".html"))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f_from:
        with open(template_path) as f_template:
            markdown = f_from.read()
            html = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)
            page = f_template.read().replace("{{ Title }}", title).replace("{{ Content }}", html)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as f_dest:
                f_dest.write(page)