.. _flash_development_guide-software_architecture:

Software Architecture
=====================

Subsystems
----------

FLASH is divided into five subsystems with distinct roles:

- **User Interface (UI) layer**. These actors handle all user interactions, communicating this information as messages to the *Application* actor. There is never direct interaction between UI and hardware actors. The UI does not maintain state – it simply mirrors the state of the Application, as indicated by status messages. The UI checks the validity of input parameters only for user convenience; the *Application* actor performs any critical parameter checks.

- *Main Window*: primary user interface for FLASH and provides most program control.

- *Viewer*: displays frame data, streaming status, and live analysis (e.g., particle counts).

- **Application layer**. This layer includes only one actor: *Application*. It is the core system that loads the instrument configuration, controls the lifecycle of all the other Actors, and translates high-level commands from the UI into a specific sequence of device commands (HAL methods), after verifying input parameters. The Application maintains the state of the program.

- *AutomationContext* is a class within the application layer that provides methods for translating a *P**rotocol* (parameters from the UI that describe a movie series) into a run plan (array of actions and associated parameters to be sent to the *Application* actor in sequence). This class keeps track of the current step in the run, freeing up the *Application* actor to only consider the immediate step being executed.

- **Hardware abstraction layer** (HAL). Classes in this layer provides abstract interfaces for mapping general device actions (like “start streaming”) into device-specific commands. Each class in this layer encapsulates the functionality of a device type (*Camera*, *Laser*, etc.). The public methods of the class are called by the Application actor via a message, describing a high-level command. The public method then calls protected methods in the same class that abstract device-specific commands (such as “prepare camera”). These protected methods (“hooks”) are overridden by device-specific classes so that dynamic dispatch can be used to call the correct device-specific class. HAL classes do not maintain state.

- **Device layer**. Actors in this layer all inherit from a specific HAL class, overriding methods to translate a high-level device action into device-specific code (such as DLL calls). These actors independently monitor the state of device and report this information, including errors, as messages back to the Application actor. When several physical devices are represented by a single driver/API (such as cameras), these should be supported by a single underlying actor to avoid race conditions.

- **Services**. These classes asynchronously execute computationally intensive tasks, such as saving frame data to disk and live image analysis, the results of which are not immediately needed by the application.


Class Hierarchy
---------------

The main classes within FLASH are Actors, which are derived from the *Actor *class of the Actor
Framework built into LabView. The core *Application *actor implements the Application subsystem. *UI
Window *and *Device *are abstract classes that provide generic functionality for the UI and Hardware
subsystems; specific windows and devices are implemented by subclassing. Messages between actors are
derived from a separate *Message* class, which is also part of the framework.

Actor (LabVIEW built in type)

- Application

- TIFF Writer (Service)

- Particle Counter (Service)

- Timer (Service)

- UI Window

- Main Window

- Viewer

- Splash Screen

- Device

- Autosampler

- Altesta Autosampler (SIELC)

- Simulated Autosampler

- Camera

- Hamamatsu

- Andor (SDK2)

- Photometrics

- Laser

- LaserQuantum

- Coherent (Obis and HOPS families)

- Thorlabs (polarizer motion control)

- Cobolt

- Microscope Stand

- Nikon Ti2

- Power Meter

- NewPort

- Thorlabs

- Stage Controller

- Nikon Ti2

- ESP30x

- Ludl

- ASI

- Simulated Stage

- Sync Device

- NI DAQ

- Arduino DAQ (`Mega2560 <https://github.com/stjude-smc/sync_device_8bit_legacy>`_; legacy support)

- Microsync

AutomationContext

Protocol

TIFF


File Structure
--------------

Below is the virtual file structure of the project, which may not perfectly match the file structure
on disk, but is very similar:

- **Application**: Application actor, AutomationContext, Protocol classes

- **BinaryTIFF**: TIFF class, Tiff Writer actor, and dcimg2tiff (C++ project)

- **Hardware**

- **Hardware Abstraction Layer:** abstract classes defining interfaces for each device type

- **Hardware Devices:** concrete child classes implementing support for specific devices

- **Protocols**: .json files describing the sequence of steps for executing parameters sweeps and other automated workflows.

- **Resources**

- **Config:** JSON files defining instrument configurations.

- **Dependencies**: external libraries used by FLASH.

- **dll**: binary dependencies

- **GLOBAL**: global variables (to be removed in a future version)

- *GLOBAL Experiment Metadata.vi:* used for collecting device settings in real time to be used when saving the metadata for output TIFF files.

- *GLOBAL Time-Critical.vi*: used for data sharing of a small number of variables such as frame data to reduce message-passing overhead.

- **Helper VIs**: stand-alone functions that are used throughout the codebase. Any VI’s that have a functional scope within one module should be moved into that lvlib instead.

- **Images**: artwork and icons used for compiling the application.

- **Testing**: VI’s used to isolate specific actors or modules for testing.

- **docs**: documentation, user guide, dev guide, release notes, etc.

- **Services** (Particle Counter, Timer actors)

- **User Interface** (Main Window, Viewer, Splash Screen actors)

- **Dialogs:** modal dialog VI’s used by the Main Window actor.


Configuration Files
-------------------

FLASH stores instrument configuration settings as JSON files in the “Config” folder. The JSON format
is compact, human-readable text that is robust to changes in the type definitions between versions.
For example, when data is not available in the config file, the default value is used. Extraneous
values/fields are silently ignored. This allows old configuration files to be used by new versions
of FLASH even when the *Hardware Configuration* typedef has changed significantly.

The format of the file is just a serialized version of the *Hardware Configuration**.vi* typedef
cluster, which includes a cluster for each device type. The *Create Hardware Configuration UI.vi*
dialog provides a visual representation of this typedef cluster. Enums are matched by their text
value, so they are robust to expansions and reordering of enum values, but not to changes in the
text names.

The *Init.json* file in the main project directory contains general settings, including a map of
computer host names and default configuration files to use for each. This mechanism aids in
deploying the software to facilities with a large number of microscopes. This file can be edited
with a text editor or you can use the *Create Initialization File.vi* dialog.


Automation
----------

FLASH is designed for workflow automation. The *Application* actor focuses only on executing one
step at a time, keeping its state management simple. The AutomationContext object, which is stored
in *Application* private data, executes a sequence of commands that make up the desired workflow.

Below is a list of the relevant objects and typedefs that coordinate this process:

- **Protocol**: encapsulates the high-level parameters describing a movie sequence and includes a method to check the validity of these the settings against the current hardware configuration.

- **AutomationContext**: encapsulates methods to build (compile) and execute the Run Plan.

- **Run Plan**: array of Parallel Blocks describing the full sequence of planned events.

- **Parallel Block**: array of Tasks that will be executed simultaneously.

- **Task**: cluster of Action, Parameters (variant), and correlation ID (integer).

- **Action**: enum that can be directly mapped to *Application*’s public methods, such as next field, autofocus, set laser power, start streaming, etc.

- **Correlation ID**: unique value used to match notifications of a completed device task against those pending in the Run Plan. The values are sequential for the lifetime of the program.

The normal program flow has *Main Window* creating a Protocol object that is translated into a Run
Plan for execution, but these classes could be extended to provide more complex utilities for
creating a Run Plan or loading one from file.
