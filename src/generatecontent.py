import os
from log import log 
from markdown_block import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path, verbose):
    log(f"Generating page from {from_path} to {dest_path} using {template_path}.", verbose)

    file = open(from_path)
    mk_content = file.read()
    file.close()

    file = open(template_path)
    html_content = file.read()
    file.close()

    title = extract_title(mk_content)
    mk_html = markdown_to_html_node(mk_content).to_html()
    

    html_content = html_content.replace("{{ Title }}", title)
    html_content = html_content.replace("{{ Content }}", mk_html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(html_content)