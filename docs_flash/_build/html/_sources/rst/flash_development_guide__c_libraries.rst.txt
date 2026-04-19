.. _flash_development_guide-c_libraries:

C++ libraries
=============

Conversion to TIFF (dcimage2tiff)
---------------------------------

As mentioned above, conversion from camera-specific intermediate files to TIFF is performed in a
separate C++ library called dcimg2tiff. This library loads the individual movie files associated
with distinct cameras (spectral bands), performs vertical/horizontal flips, and tiles them within
one image for each frame. This approach produces images that mimic those produced with image-
splitting optical devices such as the Cairn MultiCam.

For Hamamatsu cameras, the intermediate data is stored as .dcimg files, which are read using the
DCIMGAPI library from Hamamatsu. The DCIMG format varies significantly between versions and should
not be read directly.

For Photometrics, pixel data for each camera are saved to .raw files along with a
“ImageJ_import_Cam*N*.txt” file, where *N* is the camera index (0..4). This text file includes two
critical numbers that can’t be derived directly from the raw files and are used by dcimg2tiff to
read them. “Offset to first image” is the byte offset to the first pixel and “Gap between images” is
the number of padding bytes between images. These extra bytes primarily serve to align the images to
disk block boundaries for faster reading and writing. There is also a short header at the beginning
of the .raw file, but its contents are undocumented and seem inconsistent between versions.

The conversion process is very disk intensive, so only one conversion happens at a time. Care should
be taken in optimizing the code by introducing parallelized disk operations because these may starve
the camera driver’s hard disk recorder from writing frame data to disk, which will result in dropped
frames.

Particle Counter
----------------

By default, FLASH uses a MATLAB node to count the number of particles (PSF maxima) in the field of
view. The code is copied from SPARTAN. This creates a dependency that we ultimately want to remove.
Towards this end, FLASH also includes a C++ module using OpenCV to perform these calculations. The
algorithms are not identical but perform similarly. This module can introduce long application
freezes that seem to be associated with context switches between LabView threads, which force OpenCV
to reload static resources. Since no solution is obvious, this module is currently unused.
