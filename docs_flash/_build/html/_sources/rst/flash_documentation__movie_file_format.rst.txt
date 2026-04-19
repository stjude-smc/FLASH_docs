.. _flash_documentation-movie_file_format:

Movie File Format
=================

Image stacks (movies) are saved as monochrome, uncompressed .tif files with the 16-bit pixel data.
For each frame, the image data is flipped vertically and/or horizontally according to the
configuration and the images from all active cameras are then assembled into a montage. The montage
is designed to simulate the layout of an optical splitter. For 4-channel acquisitions, the panel
order by wavelength is bottom-left, top-left, top-right, bottom-right (Cy2, Cy3, Cy5, Cy7,
respectively). For 3-channel acquisitions, the field corresponding to the inactive camera is filled
with zeros. For 2-channel acquisitions, the fields are tiled horizontally left-to-right by
wavelength.

Movie files use the BigTIFF standard, which uses 64-bit offsets to enable file sizes larger than 4
GB: `https://www.awaresystems.be/imaging/tiff/bigtiff.html
<https://www.awaresystems.be/imaging/tiff/bigtiff.html>`_ . This is required for instruments with
sCMOS cameras, which often produce movies that are 30 GB or larger. The movies have one Image File
Directory (IFDs) for each frame, all of which are stored at the beginning of the file. The pixel
data is saved in one contiguous block at the end of the file (offset=16384 bytes), with each frame
being a single stripe without any intervening bytes. This allows the pixel data to be efficiently
read from disk for data analysis.

The movies include many metadata tags, but these two are of particular importance. The pixel size
parameter is set for the Flash cameras and a 60x objective and may not be correct for any other
setup.

- ExposureTime (33434): interval between camera frames.

- ImageDescription (270): plain-text description of the experiment and instrument parameters, which can be used to automate the analysis process.
