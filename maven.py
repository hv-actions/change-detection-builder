import os
import sys

def find_parent_pom_directory_for_all_changed_files(changed_files): 
    parent_dirs = {}
    for changed_file in changed_files:
        current_dir = os.path.abspath(os.path.dirname(changed_file))
        while current_dir != os.path.dirname(current_dir):
            pom_file = os.path.join(current_dir, "pom.xml")
            if os.path.isfile(pom_file):
                parent_dirs[changed_file] = os.path.basename(current_dir)
                break
            current_dir = os.path.dirname(current_dir)
        if changed_file not in parent_dirs: 
            parent_dirs[changed_file] = None
    return parent_dirs

path = sys.argv[1]
print(f"Path is - {path}")
changed_files = path.split()
changed_files_exclude_yaml = [f for f in changed_files if not f.endswith(".yaml") and not f.endswith(".yml") or not f.startswith(".github/workflows/")]
changed_files_exclude_yaml = [changed_files_exclude_yaml]
print(f" Changed file is excluding yaml - {changed_files_exclude_yaml} ")
res={}
parent_dirs = find_parent_pom_directory_for_all_changed_files(*changed_files_exclude_yaml)
for changed_file, parent_dir in parent_dirs.items():
    if parent_dir:
        print(f"The parent directory containing the pom.xml file for {changed_file} is: {parent_dir}")
        res.setdefault(parent_dir, changed_file)
    else:
        print(f"No pom.xml file was found in any parent directory for {changed_file}.")
moduleList = list(res.keys())

print(moduleList)
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    myfile.write("MY_MODULES="+moduleList)