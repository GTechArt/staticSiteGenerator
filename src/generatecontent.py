import os, shutil
from log import log 
from markdown_block import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()

    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path, basepath, verbose):
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

    html_content = html_content.replace('href="/', f'href="{basepath}')
    html_content = html_content.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath, verbose):

    os.makedirs(dest_dir_path, exist_ok=True)
    log(f"create dir content: '{dest_dir_path}'", verbose)

    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        if not item.endswith(".md"):
            dst_path = os.path.join(dest_dir_path, item)
        else:
            html_file = item[:-3] + ".html"
            dst_path = os.path.join(dest_dir_path, html_file)
            

        if os.path.isdir(src_path):
            log(f"[DIR]: {src_path}", verbose)
            generate_pages_recursive(src_path, template_path, dst_path, basepath, verbose)
        else:
            log(f"[FILE]: convert {src_path} in html", verbose)
            generate_page(src_path, template_path, dst_path, basepath, verbose)
            #shutil.copy(src_path, dst_path)