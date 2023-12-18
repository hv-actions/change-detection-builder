import os
import sys

#funtion to find parent dir name having pom.xml for all changed files
def find_parent_pom_directory_for_all_changed_files(changed_files,github_workspace_path): 
    parent_dirs = {}
    for changed_file in changed_files:
        current_dir = os.path.abspath(os.path.dirname(changed_file))
        while current_dir != os.path.dirname(current_dir):
            pom_file = os.path.join(current_dir, "pom.xml")
            if os.path.isfile(pom_file):
                parent_dirs[changed_file] = os.path.relpath(current_dir, github_workspace_path)
                break
            current_dir = os.path.dirname(current_dir)
        if changed_file not in parent_dirs: 
            parent_dirs[changed_file] = None
    return parent_dirs

#Reading all changed files path from arguments
path = sys.argv[1]
github_workspace_path = sys.argv[2]

#Converting space separated string into array list and storing output in variable
changed_files = path.split()
print(f" All changed files - {changed_files} ")

#Here we are excluding all workflow path which got changed while triggering the workflow
changed_files_exclude_yaml = [[f for f in changed_files if not (f.endswith(".yaml") or f.endswith(".yml")) and not f.startswith(".github/workflows/") and not f.startswith(".frogbot/")]]
print(f" Changed file after excluding workflow yaml files - {changed_files_exclude_yaml} ")

#If no file got changed then we are setting root directory path
if len(changed_files_exclude_yaml[0]) == 0:
    print("No File Change for Module. Building Whole Project.")
    my_modules_path="."
else:
    #If files got changed then we are finding root POM folder for file changed
    #Initialize empty dict
    res={}

    #Calling "find_parent_pom_directory_for_all_changed_files" function
    parent_dirs = find_parent_pom_directory_for_all_changed_files(*changed_files_exclude_yaml,github_workspace_path)

    #Traversing the parent_dirs dict with changed_file path as key and parent_dir as value
    for changed_file, parent_dir in parent_dirs.items():
        if parent_dir:
            print(f"The parent directory containing the pom.xml file for {changed_file} is: {parent_dir}")
            # Adding all unique dirs_name inside the "res" dict 
            res.setdefault(parent_dir, changed_file)
        else:
            print(f"No pom.xml file was found in any parent directory for {changed_file}.")
    #Adding "./" at the start of the Submodule Path excluding root directory
    modified_dict = {key if "." in key else "./" + key: value for key, value in res.items()}

    #converting all dict keys into list
    modulepath = list(modified_dict.keys())

    delimiter = ', '

    # join the list with the delimiter and converting it from list to string
    my_modules_path = delimiter.join(modulepath)
    print(my_modules_path)

# Passing changed module paths to GITHUB_OUTPUT
name = 'changed_modules_path'
value = my_modules_path
with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)
