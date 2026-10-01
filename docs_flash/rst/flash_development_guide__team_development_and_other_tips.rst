.. _flash_development_guide-team_development_and_other_tips:

Team Development and Other Tips
===============================

Due to LabVIEW’s graphical nature and binary source code, version control has some unique challenges
but is doable. Below are some tips to make the process as painless as possible:

- All developers on the project must use the exact same version of LabView.

- When moving files, always do so in LabView using the “Move on disk” option in the Files view – do not move files outside of LabView! The source files (and possibly others) will be modified in this process because LabView maintains file paths for all references.

- It is best to use a single shared computer for producing compiled versions. This ensures the build number is always correct and avoids linking issues where the absolute path to some resources is slightly different.

- Only commit files that were intentionally changed or cascaded from a known dependency (such as an updated typedef). LabVIEW tends to alter files that the user did not touch for obscure reasons. In particular, take care when committing the main project file (“.lvproj”) to avoid conflicts with other branches/developers.

- Never commit the “.aliases” and “.lvlps” files, which are workstation specific. Use .gitignore if possible to exclude them explicitly.

- Although possible, merging multiple commits to a single file isn’t recommended. If multiple contributors are working on the code base at the same time, take extra effort to minimize the scope of changes to avoid possible conflicts. If larger scale changes are needed (such as widely-used typedefs), communication is essential to coordinate commits without conflicts.


- It is possible to diff or merge commits using LVDIFF and LVMERGE utilities, but this requires some work to set up and is finicky. `https://labviewwiki.org/wiki/Set_up_differencing_capabilities <https://labviewwiki.org/wiki/Set_up_differencing_capabilities>`_


- Changes to typedefs (including enums) will cascade through every file that references it, which increases the likelihood of merge conflicts. Avoid changes to typedefs when possible. Typedefs are only needed when it is desirable for every piece of code using that typedef to need review if the data structure is modified. When used, keep the scope of any typedefs confined only to where it is needed. In some cases, it is appropriate to pass such data as a Variant type to avoid dependencies, such as when the handling class/method doesn’t inspect the message contents.


- Review this article about separating source and compiled code. If this option is not selected, source files are more likely to be altered indirectly and cause issues for version control.
  `https://www.ni.com/docs/en-US/bundle/labview/page/facilitating-source-control-by-separating-compiled-code-from-vis-and-other-file-types.html <https://www.ni.com/docs/en-US/bundle/labview/page/facilitating-source-control-by-separating-compiled-code-from-vis-and-other-file-types.html>`_
