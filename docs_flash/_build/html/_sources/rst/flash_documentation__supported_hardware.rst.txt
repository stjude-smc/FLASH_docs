.. _flash_documentation-supported_hardware:

Supported Hardware
==================

The devices listed here have been tested. More devices using the same drivers will likely also
function correctly, but this has not been verified.

**Cameras**:
+++++++++++++++++++++++++++++++++++++++++++++++++++++

    - Hamamatsu sCMOS: Flash 4.0 v2 (C11440-22CU), Flash 4.0 v3 (C13440-20CU), Fusion (C14440-20UP), Fusion-BT (C15440-20UP), and Quest (C15550-20UP).

    - Photometrics: Kinetix (01-KINETIX-M-C)

**Microscope stand**
+++++++++++++++++++++++++++++++++++++++++++++++++++++

    - Nikon Eclipse Ti2-E

**Stage controller**
+++++++++++++++++++++++++++++++++++++++++++++++++++++

    - Nikon Eclipse Ti2 motorized encoder stage (TI2‑S‑SE‑E)

    - Newport ESP300/301/302 (tested with LTA-HS motors). *Must be connected by USB.*

    - ASI controllers (tested with MS-2000 stage) 

    - Must be connected by serial port (RS232) with 9600 baud rate.

    - Ludl MAC5000 or MAC6000 controller (tested with BioPrecision2 stage).

    - Must be connected by serial port (RS232) with 9600 baud rate.

**DAQ** (for triggering shutters and cameras)
++++++++++++++++++++++++++++++++++++++++++++++++++++

    - Arduino Due programmed with the `Microsync <https://github.com/stjude-smc/microsync>`_ firmware.

    - Arduino MEGA 2560 programmed with the firmware provided in a `legacy project <https://github.com/stjude-smc/sync_device_8bit_legacy>`_.

    - National Instruments USB-6501. We recommend against this option because the timing jitter is significantly worse than using an external device.

**Laser power control**
++++++++++++++++++++++++++++++++++++++++++++++++++++

    - LaserQuantum: Opus, Ventus, and Gem (RS232 interface).

    - Coherent: HOPS (Genesis line) and OBIS series. Only one such laser may be connected.

    - Thorlabs: PRM1Z8 motorized rotation stage (for laser power attenuation). Only one such device may be connected.

    - Cobolt: experimental support (untested).

    - **Power meter**

    - Newport 1919-R (RS232 connection)

    - Thorlabs PM16-121 (others probably work but have not been tested)

**Autosampler**
+++++++++++++++++++++++++++++++++++++++++++++++++++++

    - SIELC Alltesta (7/6 valve, 120 uL syringe, 96-well plate)
