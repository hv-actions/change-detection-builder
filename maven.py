#!/usr/bin/env python3
import argparse
import os
def find_module(modified_file):
    file_folder = os.path.dirname(modified_file)
    while True:
        file_path = os.path.join(file_folder, "pom.xml")
        if os.path.isfile(file_path):
            module = file_folder.split("/")[-1]
            print(f"{file_folder}, {module}")
            break
        parent_dir = os.path.dirname(file_folder)
        if file_folder == parent_dir:
            break
        file_folder = parent_dir
    return None
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modified_file", default="", help="modified file to find its respective module name")
    args = parser.parse_args()
    find_module(args.modified_file)
