import os, shutil
from log import log

def copy_content(src, dst, verbose):
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
            copy_content(src_path, dst_path, verbose)
        else:
            log(f"[FILE]: {src_path}", verbose)
            shutil.copy(src_path, dst_path)