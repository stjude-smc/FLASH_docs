.. _flash_development_guide-introduction:

Introduction
============

FLASH is a microscope instrument control and data acquisition software tool specialized for
widefield single-molecule fluorescence imaging, especially single-molecule FRET, written to be
highly modular and parallelized to support new devices, workflows, and user interfaces relatively
easily. Read “FLASH Documentation.pdf” to review the normal functioning of the program.

The purpose of this document is to provide an overview of the software architecture, implementation
strategies, team development tips, and style guidelines. Because FLASH is written primarily in
LabView, it does not have the extensive inline documentation of text-based languages, making this
document especially important for understanding how FLASH works, how to add features, and how to fix
bugs. If you are new to LabView, we suggest first reviewing the `LabVIEW programming paradigms
<https://learn.ni.com/learn/article/labview-tutorial>`_ and the various guides for the `Actor
Framework <https://labviewwiki.org/wiki/Actor_Framework>`_.

The image below provides a high-level overview of the modules in FLASH and how they are connected.
Files are orange, software modules in green, and physical hardware devices in blue.

After installing all prerequisites listed in the next section, deploy the FLASH source code to
“C:\\FLASH\\Development”. To run FLASH, open the project file, double click on “FLASH.vi” from
within the LabVIEW project, and click the “play” button to start the program. Always open the
project file (.lvproj) in the FLASH directory to examine the code or make any changes. Avoid running
or modifying files outside the project, which will cause link errors.
