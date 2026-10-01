.. _flash_development_guide-compiling_an_executable:

Compiling an executable
=======================

Except for testing and development, FLASH should always be run as a compiled binary. To compile the
executable, follow these steps. Version numbers are specified as MAJOR.MINOR.BUGFIX.BUILD. Major
versions break significant functionality users may depend on (such as migrating the new file
formats). Minor versions implement significant new features. Bugfixes are slight changes to the code
that only correct a specific bug and add no new features. The build number is used internally for
development purposes and roughly corresponds to each commit in the source code repository.

- In the project, double-click on “Build Specifications->FLASH”.

- Click on the “Version Information” tab and update the version number. Build number should be set to be automatically incremented with each build.

- If new files are required that LabVIEW may not find by traversing the VI dependencies (such as image and dll files or classes referenced only by file path), these can be added in the “Source Files” page.

- Click “Build” to compile the project. This will often modify the .lvproj file.

- The destination for the compiled project should be “C:\\FLASH\\testing” for unstable versions to be tested and “C:\\FLASH\\master” for stable releases deployed to production workstations.

- Use “Resources\\Post-Build Action.vi” to run any actions after the executable is built to prepare for deployment, such as removing temporary files. This script also moves .dll files to the appropriate place where the executable will search for them, which is often in the root folder with FLASH.exe for easy linking at run time.
