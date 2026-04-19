.. _flash_development_guide-adding_support_for_new_devices:

Adding support for new devices
==============================

This section provides tips for how to modify FLASH to add support for new devices.

Modifying an Existing Device Actor
----------------------------------

If FLASH already supports devices from the vendor of the new device, it may be possible to add
support for the new device relatively easily. For example, all Hamamatsu cameras use the same DCAM
driver and should require relatively small changes to add support. For such cases, below is a brief
guide of how each *Device* class would be updated to support a new device type.

**Cameras:**

- **Hamamatsu**: modify the file *Max Lines Auto.vi*, specifically adding a new case to the “Camera Model” case structure. This is mainly to give plain-text names to the readout modes and specify a triggering overhead term that is not otherwise considered by the driver. You may need to modify *Prepare Acquisition.vi* if the triggering modes have changed.

- **Photometrics**: this may work for new sCMOS cameras without modification because the code is not model-specific. If there are issues with triggering, first check the timing calculations in *PmSetRegion.vi*. The default readout mode (“Auto”) is set in *PmSetReadoutMode.vi*. Prepare Acquisition.vi may also need to be modified, particularly if the triggering modes are different than the Kinetix.

- **Andor**: the current code, which is unstable, only support SDK2 for EMCCD cameras. If you want to use a modern sCMOS camera, you will need to create a new *Camera* class for it.

**Power meter:**

- **Thorlabs:** any power meter using the TLPM library should be supported without modification.

**Lasers:**

- **Coherent:** all lasers in the OBIS series and those using the HOPS driver (Genesis MX) should be supported without modification. Other series using a different driver will require a new case to each case structure in the main class methods.

- **Laser Quantum**: all lasers in this series currently support a common RS232 protocol, so new lasers from this company should be supported without modification.

- **Thorlabs:** any “KCubeDCServo” type device is probably supported without modification. For other rotation stage devices, *Initialize.vi* and *Set Power.vi* may need to be modified.

**Sync Device****:**

- Many National Instruments DAQ devices are likely supported by simply modifying the NI-DAQmx physical channel addresses in the configuration file. However, we do not recommend this path because the jitter of triggering from software is not very good.

- Other Arduino-type devices can be supported if they can be programmed to accept the same communication protocol as those already supported by FLASH.


Creating a New Device Actor
---------------------------

Below is the general process for creating a new *Device* actor, inheriting from an existing HAL
interface class, such as *Camera*, *Laser*, *Sync Device*, etc.

- Before you begin, create a stand-alone test VI to implement all planning functions of the target device driver. It is easier to troubleshoot errors and explore device quirks outside of the complexity of FLASH and the Actor Framework. If implemented as a series of helper VIs, these can be re-used in the new actor’s methods. Be sure to fully test all planned workflows this way.

- Create a new .lvlib in the “Hardware Devices” project virtual folder and save it in a new folder of the same name under the “Hardware” folder on disk.

- Create a new class inheriting from the desired HAL class and save in the same folder as the lvlib.

- Add the new lvclass to the to the “always included” list under the “source files” tab of the project build specification.

- Add any device-specific data to the properties in the .ctl file associated with the class. Most often this matches the relevant part of the *Hardware Configuration* typedef.

- Right-click on the lvclass and select “New->VI for Override…” and select a method to override from the HAL parent class. The list includes all parent classes, many of which are irrelevant. Some classes require the child to call the parent method, so it is best to look at other concrete classes of this device type to determine the expected pattern.

- Override *Initialize.vi* (sometimes *Create Instance Impl.vi*) to connect to the device and perform any startup actions such as calibration.

- Override *Shut Down Device.vi* (from *Device* class) with code to leave the device in a safe state, free up any resources, and disconnect.

- Override *Handle Error.vi* (from Actor Framework) to deal with any errors that propagate to the output terminal of class methods. Unhandled errors will kill the actor.

- Other override methods will be determined by the specific HAL class.

- Append a new enum entry in the hardware configuration cluster for that device type. Generally located under “Resources/Type Defs”. This will likely cascade further changes in the codebase. Check the Error List to see if any references need to be updated manually.

- Update the relevant *Application/Init **<HW>**.vi* to include a case to include the file path for the new class. In some cases, such as the *Stage* class, it is the parent’s *Initialize.vi* method that needs to be modified.

- Run FLASH, selecting the new device in the hardware configuration, to test the new actor.
