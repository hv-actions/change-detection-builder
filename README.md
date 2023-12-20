# change-detection-builder

Aims to focus maven builds for certain submodules. When executing a Maven build, it builds all the modules defined in the project. However, in certain scenarios, it may be desirable to build only a subset of the modules, such as when working on a specific feature or fixing a bug that affects only a particular submodule. This composite action helps achieve this selective build by providing a mechanism to specify the desired changed submodule paths, thereby reducing build times and improving efficiency.

## Usage examples
```
# Calling Change detection composite action in workflow
- name: Change detection Composite action
  id: change_detection
  uses: hv-actions/change-detection-builder@stable  #The stable tag always points to the latest changes
```

```
#Build The Project for changed modules
- name: Build
  id: Build
  uses: lumada-common-services/gh-composite-actions@stable
  with:
    command: mvn clean install -pl "${{ steps.change_detection.outputs.changed_modules }}"  -DskipTests -amd -s ${{env.MAVEN_SETTINGS}}
```

## change-detection-builder flow
This composite system performs two main tasks: detecting files that have changed and locating the parent folder with a pom.xml file in its root directory for each of those changed files.
- The first step is file detection. It scans a given directory to identify files that have been modified. Once the changed files are identified, the system moves on to the second step: locating the parent folder with a pom.xml file. It traverses the directory structure of each changed file to find the nearest parent folder that contains a pom.xml file in its root directory. This search is performed recursively, moving up the directory tree until a suitable parent folder is found. The paths of the changed modules are then stored in the GITHUB_OUTPUT variable. We can access these module paths using the expression ```${{ steps.change_detection.outputs.changed_modules }}```.
- Afterwards, the Maven build command is executed with the -pl flag followed by                                                                                                           
   ${{ steps.change_detection.outputs.changed_modules }} and -amd flag.
  - -pl "./module1_path, ./module2_path": The -pl option, followed by a comma-separated list of module paths, allows you to specify specific modules to build. In this case, it indicates that only the modules named "module1" and "module2" should be built. Other modules in the project will be skipped.
  - -amd: The -amd option, short for "also make dependencies," is a non-standard option typically used with the Maven reactor. When this option is enabled, Maven will build not only the specified modules (module1 and module2) but also their dependent modules if they have changed since the last build. It ensures that the dependencies are up to date.
- If no files have been changed, the value of ${{ steps.change_detection.outputs.changed_modules }} is set to the current directory, represented by ".". Running the Maven build command with -pl "${{ steps.change_detection.outputs.changed_modules }}" will then build all submodules in the project.
- As a default, it will exclude these paths ```'.yaml, .yml, .github/'``` while running the change detection. However, if we want to exclude specific paths or files ending with a particular extension, we can define that value as follows
```
- name: Change detection Composite action
  id: change_detection
  uses: hv-actions/change-detection-builder@stable
  with:
    exclude_paths: '.github/, .frogbot/, .json, .py'
```
In summary, this script optimizes the build process by selectively building only the necessary submodules when changes are detected, improving overall build efficiency.
