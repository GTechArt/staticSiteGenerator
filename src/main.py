import argparse, os, sys
from copy_content import copy_content
from generatecontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
file_path_template = "./template.html"

def parse_args():
    parser = argparse.ArgumentParser(description="StaticWebSite generator for bootdev exercice")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true", # if it does not appear: set it to False
        help="Enable verbose output"
    )

    parser.add_argument(
        "basepath",
        nargs="?",
        default="/",
        help="Base path for the site"
    )

    return parser.parse_args()

def main(args):
    basepath = args.basepath

    copy_content(dir_path_static, dir_path_public, args.verbose)
    
    generate_pages_recursive(        
        dir_path_content,
        #os.path.join(basepath, dir_path_content),
        file_path_template,
        #os.path.join(basepath, dir_path_public),
        dir_path_public,
        basepath,
        args.verbose
    )


if __name__ == "__main__":
    args = parse_args()
    main(args)