import argparse, os
from copy_content import copy_content
from generatecontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
file_path_template = "./template.html"

def parse_args():
    parser = argparse.ArgumentParser(description="StaticWebSite generator for bootdev exercice")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true", # if it does not appear: set it to False
        help="Enable verbose output"
    )

    return parser.parse_args()

def main(args):
    copy_content(dir_path_static, dir_path_public, args.verbose)
    generate_page(
        os.path.join(dir_path_content, "index.md"),
        file_path_template,
        os.path.join(dir_path_public, "index.html"),
        args.verbose
    )


if __name__ == "__main__":
    args = parse_args()
    main(args)