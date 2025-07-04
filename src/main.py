import os, shutil, sys
from markdown_page import generate_page_recursive

def main():
    basepath = "/"
    if(len(sys.argv) > 1):
        basepath = sys.argv[1]
    print(basepath)
    copy_static()
    generate_page_recursive("content", "template.html", "docs", basepath)

def copy_static():
    try:
        if os.path.exists("docs"):
            shutil.rmtree("docs")
        os.mkdir("docs")
        copy_dir("", "static", "docs")
    except Exception as e:
        print(e)

def copy_dir(name, parent_source, parent_target):
    source_path, target_path = os.path.join(parent_source, name), os.path.join(parent_target, name)
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"source directory {source_path} missing")
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    for file in os.listdir(source_path):
        if os.path.isdir(os.path.join(source_path, file)):
            copy_dir(file, source_path, target_path)
        elif os.path.isfile(os.path.join(source_path, file)):
            shutil.copy(os.path.join(source_path, file), os.path.join(target_path, file))

if __name__ == "__main__":
    main()