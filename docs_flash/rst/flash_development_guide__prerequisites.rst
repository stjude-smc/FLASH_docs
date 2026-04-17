.. _flash_development_guide-prerequisites:

Prerequisites
=============

The following programs and libraries must be installed before loading the FLASH source code to avoid
link errors. The associated devices are not required to be installed, but at least one physical
camera must be connected to run the program (there is no simulated camera functionality). If
necessary, you can avoid some driver dependencies by removing the device .lvlib from the project
file, assume the device actor class is always launched by path string, which is almost always true.

- **64-bit LabVIEW Professional version **2023 Q3**. This requires a license to be purchased. `https://www.ni.com/en-us/shop/labview.html <https://www.ni.com/en-us/shop/labview.html>`_

- JSONtext from JDP Science (download using VI Package Manager).

- **Hamamatsu** Video Capture library for LabVIEW. This will install VIs into LabVIEW user.lib folder and install tmcamcon.dll to C:\\Windows\\System32.
  `https://dcam-api.com/hamamatsu-software/ <https://dcam-api.com/hamamatsu-software/>`_

- **Andor** SDK2 (for EMCCD cameras): tested with version 2.104.30084.0.
  `https://andor.oxinst.com/downloads/uploads/Software%20Development%20Kit.pdf <https://andor.oxinst.com/downloads/uploads/Software%20Development%20Kit.pdf>`_
  `https://andor.oxinst.com/downloads/view/andor-sdk-2.104.30084.0 <https://nam11.safelinks.protection.outlook.com/?url=https%3A%2F%2Fandor.oxinst.com%2Fdownloads%2Fview%2Fandor-sdk-2.104.30084.0&data=05%7C02%7CDaniel.Terry%40stjude.org%7C0bfa96fbb0004ec2832d08dbfda9d7c3%7C22340fa892264871b677d3b3e377af72%7C0%7C0%7C638382680032362352%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=%2BppO2aBeX7p%2B36frNFmnxvA%2B83o9z5euuzLcQRQ%2FOXk%3D&reserved=0>`_

- **Photometrics** PVCAM and LabVIEW adapter.
  `https://www.photometrics.com/products/pvcam <https://www.photometrics.com/products/pvcam>`_
  `https://www.photometrics.com/support/third-party-software/labview <https://www.photometrics.com/support/third-party-software/labview>`_

- NOTE: the LabView adapter by default installs in the “Public Documents” folder, which causes linking issues in LabView. Instead, we recommend moving this folder into user.lib. The expected path is: “C:\\Program Files\\National Instruments\\LabVIEW 2023\\user.lib\\TPM LabVIEW adapter\\”.

- **Nikon Ti2** SDK 64-bit, which includes the device driver for the Ti2 microscope. 
  `https://nisdk.recollective.com/microscopes <https://nisdk.recollective.com/microscopes>`_

- **Thorlabs Kinesis** SDK for LabVIEW.
  `https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control <https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control>`_

- **ASI stage controller** driver for LabVIEW, which installs in user.lib.
  `https://www.asiimaging.com/support/downloads/ms-2000-control-using-nis-labview-and-the-serial-port/ <https://www.asiimaging.com/support/downloads/ms-2000-control-using-nis-labview-and-the-serial-port/>`_

- **Coherent Genesis**: You can install the “OPSL GUI”, which includes both the driver and test UI, or  install the device driver and a UI for testing, or “CDM v2.12.28 WHQL Certified” if you just want the driver.
  `https://www.coherent.com/resources?query=opsl%20gui <https://www.coherent.com/resources?query=opsl%20gui>`_
  `https://www.coherent.com/resources?query=CDM%20v2.12.28%20WHQL%20Certified <https://www.coherent.com/resources?query=CDM%20v2.12.28%20WHQL%20Certified>`_

- **Visual Studio** with C/C++ tool chain (free Community Edition is sufficient) to recompile the C++ DLLs (specifically dcimg2tiff.dll) used for time-critical operations in FLASH.

- Optional: instructions for installing software for configuring the Arduino are listed on the developer’s website: `https://github.com/stjude-smc/microsync <https://github.com/stjude-smc/microsync>`_
