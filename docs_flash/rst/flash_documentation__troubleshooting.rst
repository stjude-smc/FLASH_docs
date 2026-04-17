.. _flash_documentation-troubleshooting:

Troubleshooting
===============

**Synchronization**

Be sure to verify synchronization of cameras before using an instrument for routine experiments.
Connect the “trigger/expose out” port of each camera to an oscilloscope and verify that the rising
edges are synchronized within ~1 ms. Check this at varying exposure times between 200 ms and 2 ms.
With the NI DAQ and exposure times faster than 2 ms, the cameras are internally triggered and may
lose synchronization over time.

**How do I determine the virtual addresses of the ports on the **NI DAQ?**

Check the documentation for your DAQ and use the NI MAX utility. NI DAQs often include helpful
stickers. If in doubt, use the NI Test Panels utility (accessible from NI Device Manager) to set the
line voltages and test with an oscilloscope or volt meter.

**Missing DLLs**

FLASH works with a set of drivers for common microscope hardware. For licensing reasons, not all of
these can be packaged together with the software and must be installed by the user. Check the
installation instructions to verify all required software is installed. If the problem persists:

- Ti2_Mic_Driver.dll: install Nikon Ti2 SDK. Then copy this file from “C:\\Program Files\\Nikon\\Ti2-SDK\\bin\\” into FLASH’s dll folder.

- tmcamcon.dll: install the Hamamatsu Video Capture library.

- dcampapi.dll or dcimgapi.dll: install DCAM (camera drivers).

- Thorlabs….dll: install the Thorlabs Kinesis library.

- nilvaiu.dll: install the National Instruments DAQmx software.

**Error -1073807202: A Code Library Required by NI-VISA Could Not Be Located**

Although it should have come with DAQmx, you may need to install the NI-VISA driver.

`https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#306119
<https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html>`_

**Failed load to configuration**

Your configuration file is invalid. We recommend against manually editing these files as this is
highly error prone. Use the configuration dialog in FLASH to edit these files instead.

**Microscope is**** not detected** (Nikon Ti2)

You must install the Nikon Ti2 SDK in order for the microscope to be detected. Verify the USB
connection and the device shows up in Windows Device Manager.

**“No cameras detected!” error on startup.** *(Hamamatsu cameras)

Verify the cameras are turned on and have completed their startup procedure (status lights not
flashing) before starting FLASH. If no lights come on at all, check the power connection. With the
Fusion camera, the red lights near the coaxial data ports never stop flashing, it suggests the
camera could not establish a connection to the computer; check your USB or coaxial data connection.
Finally, double check the configuration file to make sure the serial numbers exactly match. The DCAM
Configurator tool can be helpful for this task.

In some cases, the cameras take a long time to initialize and FLASH times out. It’s worth trying a
few times before giving up.

If you are using the compiled version but also have LabVIEW and the Hamamatsu Video Capture (HVC)
library installed, there may be a conflict with the copy of tmcamcon.dll included with FLASH and the
version installed in C:\\Windows\\System32. To resolve this problem, remove the copy of tmcamcon.dll
from the FLASH directory.

If all else fails, use software provided with the camera manufacturer such as HCImage and work with
the camera vendor to troubleshoot the issue.

**“Invalid camera model”** (Hamamatsu cameras)

Only a limited number of Hamamatsu camera models are currently supported. Please check the
“Supported Hardware” section above. For the source code version, a new model number can be added to
the case structure in the file “Hardware\\Hamamatsu Camera\\Max Lines Auto.vi”. For the stand-alone
version, please contact us with the camera model number.

**One of my cameras has an inverted **or rotated image**** relative to the others**

You may need to change the Configuration settings for this camera to set one of the “flip” settings
to “true”. If it is rotated, this must be fixed by physically rotating the camera so that it is
aligned with the others.

**I get errors about the lasers**

FLASH will not start if any hardware in the configuration file is not found or connecting to it
failed. Either change the device type to “Disabled” or delete the Laser Configuration entry
corresponding to the device.

**Lasers are on and shutters are **open but I see nothing in the cameras/eyepieces**

First, manually select filter and output port to eyepieces on the microscope body or remote control
pad and verify you get the expected signal. If this does not work, the problem may be with the
instrument or sample. Otherwise, check your configuration file under Microscope Configuration –
Detection Settings. Microscope Type should be “Ti2”. The integer values correspond to the filter
turret position (same as written on the filter cubes themselves) and light path (output port). For
the Nikon Ti2 microscope stand, the light path has the following values:

- Eyepieces

- Right port

- Bottom (U) port

- Left port

If you see all black in the camera Live Viewer, first adjust the scale bars (or use the Auto Scale
mode). This should be showing a rapidly changing static signal – zoom in to verify if this isn’t
clear. If the image is completely black or completely static, there may be a problem either with the
cameras or with the triggering. The cameras will not acquire frame data unless they receive
triggering pulses on their “Trigger Input” line from the DAQ. Check the physical connections and
verify the output port specified in the configuration file under Virtual Camera – Sync Line is
connected to the “external trigger” port of the camera.

**When I move to a new field, some of the molecules near the border are already bleached****.**

Adjust the stage parameters in the configuration file to take a larger step in that direction. These
values will depend on the size of the illuminated area.

**I get errors about dropped frames.**

Frame data may not get saved to disk if the disk is not fast enough for the large volume of data
produced by sCMOS camera arrays. The simplest solution is to get an SSD drive dedicated to saving
movies with a sustained write speed > 2GB/s. Second, limit the use of other disk or CPU-intensive
applications (such as Python or MATLAB for data analysis) while recording a movie. Finally, before
acquiring a movie, wait until the previous one has completely saved to disk.

**FLASH** is in a strange state where buttons do not work or behave unexpectedly.**

Stand-alone version: close FLASH. Verify the icon in the taskbar shows that it successfully exited.
If it does not, use Task Manager to kill the process. Turn off the cameras, wait 10 seconds, and
turn them on again. Wait for the cameras to complete their startup procedure and start FLASH. If
this does not solve the problem, restart your computer.

**S**till need help****?**

Please email `scott.blanchard@stjude.org <mailto:scott.blanchard@stjude.org>`_ with the following
information:

- Name, institution, principal investigator.

- Version of FLASH and type of installation (stand-alone or source code).

- Describe the problem in detail. Take a screenshot of any error dialogs.

- If applicable, attach the relevant log file (C:\\temp\\FLASH.log).

- Is the problem reproducible? If so, what are the steps to reproduce it?

- If using the source code, have there been any modifications? If so, have you tried using the original version?

- Describe your instrument in detail:

- Camera make, model, and connection interface (e.g., USB). Are you using dedicated PCIe cards for each camera?

- Microscope stand and stage model and connection interface.

- DAQ make and model. If possible, use an oscilloscope to investigate whether FLASH is sending the correct signals to devices as expected.

- Please also include a copy of your configuration file.

- Describe your computer and installed software:

- Windows version and computer hardware: In Windows Control Panel, select “About your PC”. Take a screenshot to include with your report.

- What version of the Hamamatsu DCAM software is installed?
You can find this information in Windows Control Panel under “Add/Remove Programs” in Windows Control Panel or by running DCAM Configurator utility. If there are multiple versions installed, please include this information.

- Source code version: what version of LabVIEW and HVC are you using?

- Versions of all other relevant software: NI DAQmx, Nikon Ti2 SDK, etc.
