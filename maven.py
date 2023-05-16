import os
import sys

def find_parent_pom_directory_for_all_changed_files(changed_files): 
    parent_dirs = {}
    for changed_file in changed_files:
        current_dir = os.path.abspath(os.path.dirname(changed_file))
        while current_dir != os.path.dirname(current_dir):
            pom_file = os.path.join(current_dir, "pom.xml")
            if os.path.isfile(pom_file):
                parent_dirs[changed_file] = current_dir
                break
            current_dir = os.path.dirname(current_dir)
        if changed_file not in parent_dirs: 
            parent_dirs[changed_file] = None
    return parent_dirs

path = sys.argv[1]
changed_files = [path]
print(f" Changed file is - {changed_files} ")
parent_dirs = find_parent_pom_directory_for_all_changed_files(changed_files)
for changed_file, parent_dir in parent_dirs.items():
    if parent_dir:
        print(f"The parent directory containing the pom.xml file for {changed_file} is: {parent_dir}")
    else:
        print(f"No pom.xml file was found in any parent directory for {changed_file}.")
