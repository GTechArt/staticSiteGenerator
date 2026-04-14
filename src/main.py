import argparse, os, shutil
from markdown_block import markdown_to_html_node
#from textnode import TextNode, TextType

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
file_path_template = "./template.html"


# first recursion, create "public" dir
def copies_all_contents(src, dst, verbose):
    # rm all content if "public" already exist
    if os.path.exists(dst):        
        log(f"rmtree of '{dst}' because already exists", verbose)
        shutil.rmtree(dst)

    os.makedirs(dst, exist_ok=True)
    log(f"create '{dst}'", verbose)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            log(f"[DIR]: {src_path}", verbose)
            copies_all_contents(src_path, dst_path, verbose)
        else:
            log(f"[FILE]: {src_path}", verbose)
            shutil.copy(src_path, dst_path)


#def copies_contents(verbose):


def parse_args():
    parser = argparse.ArgumentParser(description="StaticWebSite generator for bootdev exercice")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true", # if it does not appear: set it to False
        help="Enable verbose output"
    )

    return parser.parse_args()

def log(message, verbose):
    if verbose:
        print("Log: ", message)

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
        


def main(args):
    copies_all_contents(dir_path_static, dir_path_public, args.verbose)
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        file_path_template,
        os.path.join(dir_path_public, "index.html"),
        args.verbose
    )

    print(extract_title("# Hello !"))

    #text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(text_node)


if __name__ == "__main__":
    args = parse_args()
    main(args)