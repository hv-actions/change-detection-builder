import os
import sys

#funtion to find parent dir name having pom.xml for all changed files
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

#Reading all changed files path from argumennts
path = sys.argv[1]

# Converting path variables value from string to array by split function
changed_files = path.split()
print(f" All changed files - {changed_files} ")

#Here we are excluding all workflow path which got changed while triggering the workflow
changed_files_exclude_yaml = [[f for f in changed_files if not f.endswith(".yaml") and not f.endswith(".yml") or not f.startswith(".github/workflows/")]]
print(f" Changed file after excluding workflow yaml files - {changed_files_exclude_yaml} ")

#Initialize empty dict
res={}

#Calling "find_parent_pom_directory_for_all_changed_files" function
parent_dirs = find_parent_pom_directory_for_all_changed_files(*changed_files_exclude_yaml)

#Traversing the parent_dirs dict with changed_file path as key and parent_dir as value
for changed_file, parent_dir in parent_dirs.items():
    if parent_dir:
        print(f"The parent directory containing the pom.xml file for {changed_file} is: {parent_dir}")
        # Adding all unique dirs_name inside the "res" dict 
        res.setdefault(parent_dir, changed_file)
    else:
        print(f"No pom.xml file was found in any parent directory for {changed_file}.")
#converting all dict keys into list
moduleList = list(res.keys())

delimiter = ', '

# join the list with the delimiter and converting it from list to string
my_modules = delimiter.join(moduleList)
print(my_modules)

#Creating an env file to pass modules names into the github env context
env_file = os.getenv('GITHUB_ENV')
with open(env_file, "a") as myfile:
    #Writing all module name into githun env "MY_MODULES"
    myfile.write("MY_MODULES="+ my_modules)
