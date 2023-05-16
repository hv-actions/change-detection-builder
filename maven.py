import os
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

changed_files = ["/Users/agadekar/Desktop/LDOS/data-plane/data-plane/repository/common/src/main/java/com/hitachivantara/data/plane/repository/IRepositoryEndpoints.java","C:/Users/agadekar/Desktop/LDOS/data-plane/data-plane/repository/jdbc/src/test/resources/sql_lite.db"]
parent_dirs = find_parent_pom_directory_for_all_changed_files(changed_files)
for changed_file, parent_dir in parent_dirs.items():
    if parent_dir:
        print(f"The parent directory containing the pom.xml file for {changed_file} is: {parent_dir}")
    else:
        print(f"No pom.xml file was found in any parent directory for {changed_file}.")
        