.. _flash_documentation-hardware_setup_guide:

Hardware Setup Guide
====================

For a general overview of the experimental setup, please see the following paper:
`https://www.nature.com/articles/nmeth.3769 <https://www.nature.com/articles/nmeth.3769>`_


**Cameras:**

    - All cameras being used together should have the same camera model and firmware version.

    - Cameras should be oriented so that the image matches the field of view of the eyepieces, with only horizontal flipping required. On many sCMOS camera modes, vertical flipping may interfere with line-by-line synchronization.

    - USB-connected cameras generally should each have a dedicated interface card.

    - Follow all manufacturer recommendations for camera hardware installation, such as appropriate device drivers, software configuration, and BIOS settings.


**Triggering:**

    - Configure the shutter driver(s) so that the shutters are closed with 0V input and open with +5V input. With Uniblitz drivers, connect the appropriate DAQ outputs to the “pulse input” port.

    - The camera trigger DAQ line should be connected in parallel to the “external trigger” input of all cameras.

    - For `Arduino MEGA <https://github.com/stjude-smc/sync_device_8bit_legacy>`_ (legacy) DAQ, pins A0-A3 control the four shutter lines (e.g., 473, 532, 640, 721 nm), pin 13 is used for camera triggering, and pin 2 is used for fluidics triggering.

    - For `Microsync <https://github.com/stjude-smc/microsync>`_ device (Arduino Due), pins D8-11 control the four shutter lines (e.g., 473, 532, 640, 721 nm), pin D7 is used for camera triggering, and pin D6 is used for fluidics triggering. Optionally, pins D12 (input) and D13 (output) are used for an interlock loop. We recommend using the `custom shield <https://github.com/stjude-smc/PCB-microsync>`_ for this device to convert internal 3.3V to TTL (5V) expected by most devices.


**Other:**

    - Recommended: disable power management in Device Manager for all USB devices (and any hubs they depend on). Otherwise, devices may randomly fail when put to sleep. This is a known problem for Hamamatsu cameras connected via USB PCIe cards.

    - Control software associated with each device, such as the RemoteApp program for LaserQuantum lasers or Coherent Connection can be useful both to verify the device is properly connected and determine the COM port and other connection parameters for it.
