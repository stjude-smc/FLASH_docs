.. _flash_documentation-installation_stand_alone_executable_version:

Installation (stand-alone executable version)
=============================================

The stand-alone executable version is recommended for all users unless you plan to customize the
code to add new devices. Before installing, please install the following pre-requisites, according
to the specific hardware actually installed. No license should be required to download any of the
software.

- 64-bit LabVIEW run-time engine 2023-SP3. **Required for all hardware configurations.**
  `https://www.ni.com/en/support/downloads/software-products/download.labview-runtime.html#484336 <https://www.ni.com/en/support/downloads/software-products/download.labview-runtime.html>`_

- MATLAB is required for live particle counting.

- DAQ-mx version 21.8 (for the USB-6501 device only):
  `https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html#445931 <https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html>`_

- Latest version of DCAM (for Hamamatsu cameras). We have tested most extensively with versions 22.2.6391 and 22.8.6486. `https://dcam-api.com/ <https://dcam-api.com/>`_

- Latest version of PVCAM (for Photometrics cameras). We have tested most extensively with version 3.10.1. `https://www.photometrics.com/support/download/pvcam <https://www.photometrics.com/support/download/pvcam>`_

- Nikon Ti2 SDK 64-bit, which includes the device driver for the Ti2 microscope.
  `https://nisdk.recollective.com/microscopes <https://nisdk.recollective.com/microscopes>`_

- Thorlabs Kinesis (for Thorlabs PRM1Z8).
  `https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control>`_

- Coherent Genesis driver. Your laser should have included a CD that will install an application called “OPSL” and the driver. If you need to install the driver directly, it can be found in a directory similar to “CDM v2.12.28 WHQL Certified” on the CD.
  `https://www.coherent.com/support <https://www.coherent.com/support>`_

Once these packages are installed, unzip FLASH.zip to “C:\\FLASH” and create a desktop shortcut to
FLASH.exe. Ensure all devices are initialized and connected. Run FLASH.exe to start the program.
