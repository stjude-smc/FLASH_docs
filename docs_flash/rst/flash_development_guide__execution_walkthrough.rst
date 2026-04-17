.. _flash_development_guide-execution_walkthrough:

Execution Walkthrough
=====================

This section provides an overview of the program flow, focusing on the key methods.

Application Startup
-------------------

Below are the steps executed on successful startup:

- **FLASH.vi** launches the *Application* as root actor.

- **Application/Startup.vi** launches the* Splash Screen* Actor.

- **Application/Load Configuration.vi** dialog allows user to select the hardware configuration, saving this information in the *Application* private data. The “Create Hardware Configuration UI.vi” dialog is used for modifying an existing configuration or creating a new one.

- **Application/Init HW.vi** initialize configured hardware:

- **Application/Initialize Lasers.vi:** launches *Laser* actors (up to 4).

- **Application/Initialize Virtual Microscope.vi:** launches *Microscope* actor.

- **Application/Initialize Stage Controller.vi:** launches *Stage Controller* actor.

- **Application/Init Power Meter.vi:** launches *Power Meter* actor.

- **Application/Initialize Shutters.vi:** launches *Sync Device* actor.

- **Application/Initialize Virtual Camera.vi**: launches *Camera* actor.

- **Application/Initialize UI.vi**: launches service actors and initializes *AutomationContext*.

- **Application/Init Telemetry.vi**: sends telemetry data to server for usage statistics.

- **Application/Startup.vi*** launches the *Main Window* actor and closes the splash screen.

“Initialize <device>.vi” methods launch child actors by class path so that dependencies are only
loaded as needed, which may not all be present in production systems. The device’s *Initialize.vi*
method is called directly using the object’s data wire, rather than by message, to ensure the
startup process is sequential and deterministic to avoid race conditions.

The device initialization order is most arbitrary, except that (1) *Sync Device* provides a jitter
parameter to *Camera* for timing calculations and (2) *Lasers* are initialized first to ensure the
laser power is set to zero before *Sync Device* for extra safety.

Application Shutdown
--------------------

Below is the execution flow for normal (user-initiated) shutdown:

- *Main Window* sends *Shutdown Msg* to *Application*.

- **Application/Cancel Current Operation.vi** terminates running operations (such as streaming).

- **Application/Shut Down.vi** sends *Stop Msg* to all running actors and reopens the splash screen.

- **<Device>/Shut Down.vi** puts each physical device in a safe state (such as escaping the objective and closing shutters) and frees allocated resources like file handles.

- **Application/Handle Last Ack Core.vi** decrements a counter when each child actor is terminated and, when the counter reaches zero, sends **Stop** Msg to *Application*.

- **Application/Stop Core.vi** closes the log file and the splash screen.

This shut down procedure ensures that the log file is properly closed only after all actors have
terminated, which helps with troubleshooting actors that freeze on shutdown. It also ensures the
splash screen only closes when the application has actually terminated.

Error Handling
--------------

Below is a description of how error handling should be done in FLASH; in practice some legacy code
does not follow this pattern.

- **Minor errors** are handled entirely within the device method. “Minor” means that the current acquisition process can continue without interruption. An example would be a bad power meter reading, where the result isn't important to the acquisition. Another example is a blocking command that can be repeated quickly and safely.

- **Serious but non-fatal errors** are caught in device methods, logged in detail, converted to a relevant program-level error code, and passed to Application using the "cancel current operation" method, including the error code. An example would be an invalid or unsafe command sent to an autosampler -- the device is in unstable state and we need to reset before continuing. The Application will convert the error code into a plain-language warning dialog (using an int->string map/registry) with suggested next steps to recover.

- **Fatal or unknown errors** propagate to the output terminal of an actor method, where they are handled in Actor/Handle Error.vi. The device actor will be terminated and the Application will receive a Last Ack message with the final error cluster, which will be displayed and the user offered a choice whether to continue. If the user says yes, the next command sent to the device will still crash the application (because the reference is now invalid).

- **"Handle Error.vi" overrides** can provide an additional safety net to clean up and put the device in a safe state after a fatal error but should still propagate that error to the application and terminate the actor. Don't use this override for normal error handling.

- Initialization methods are a special case because they are called directly by the Application. But in practice, they are handled the same way, except that errors propagating through the method end up directly on the Application's error wire and prevent the Application from starting.

Show Live / Stop Live
---------------------

This section describes events after user clicks the “Show Live” button in *Main Window*:

- *Main Window* sends *Start Live Msg* to *Application* with current acquisition parameters.

- **Application/Start Live.vi** validates settings, sends *Start Live Mode Msg* to *Camera*, *Start Streaming Msg *to *Sync Device*, *Application Mode Change Msg* to *Main Window*, and *Set Visibility Msg *to *Live Viewer*.

- **<Camera>/Start Live Mode.vi** configures camera(s) for frame acquisition.

- **<Sync Device>/Start Streaming.vi** starts TTL pulse sequence to other devices.

- **<Camera>/Get Most Recent Frame.vi** saves the most recently acquired frame and index to the “Live Frame” and “Current Frame” global variables, respectively, and sends *New Frame Notify Msg* to *Application*.

- **Application/New Frame Notify.vi** sends *New Frame Msg* to the *Particle Counter* service actor.

- **Viewer/Actor Core.vi** renders the most recent frame from “Live Frame” global variable.

- Steps 7-9 repeat until the user closes the *Viewer* window or clicks “Stop Live” in *Main Window*, both of which send “Stop Live Msg” to *Application*.

- **Application/Stop Live Mode.vi** sends *Stop Live Msg* to *Camera*, *Stop Streaming* to *Sync Device*, *Application Mode Change Msg* to *Main Window*, and *Set Visibility Msg* to *Viewer*.

Stream Acquisition
------------------

This program sequence occurs when the user clicks “Start Streaming” in the *Main Window* front
panel. See the section above with a more complete description of AutomationContext and Protocol
objects.

- A *Start Recording Msg* with a newly created Protocol object is sent to *Application*.

- **Application/Start Recording.vi** checks Protocol validity against the hardware configuration.

- **AutomationContext/Compile Protocol.vi** and builds a Run Plan, which will include the full sequence of steps for the acquisition, including stage movement, setting laser power, Z stack acquisition for autofocus, and streaming, along with parameter values for each. For brevity, we consider the simplest case below.

- **AutomationContext/Next Step.vi** pulls all Tasks in the next Parallel Block in the Run Plan and sends them as messages to *Application* with their associated correlation ID. In the simplest case, this is always *Start Stream Msg*.

- **Application/Start Stream.vi** sends *Start Stream Msg* to *Camera*, runs the timer dialog (if applicable), sends *Start Streaming Msg* to *Sync Device*, and opens the *Viewer* window.

- **<Camera>/Start Stream.vi** configures camera for frame acquisition and streaming to disk.

- **<Sync Device>/Start Streaming.vi** starts TTL pulse sequence to other devices.

- **<Camera>/Get Most Recent Frame.vi** saves the most recently acquired frame to the “Live Frame” global variables and sends *New Frame Notify Msg* to *Application*.

- **Application/New Frame Notify.vi** sends *New Frame Msg* to the *Particle Counter* service actor. When the last frame is received, *Finish Stream.vi* is called.

- **Application/Finish Stream.vi** sends *Stop Streaming Msg* to *Sync Device* and *Finish Stream Msg* to *Camera* to end the current acquisition.

- **<Sync Device>/Stop Streaming.vi** ends pulse sequence and resets to idle state.

- **Camera/Finish Stream.vi** stops the acquisition, compiles metadata for final movie file, and sends *Save Tiff Msg* to *TiffWriter*, and sends* **Automation_TaskCompleted** Msg *to* Application*.

- **Tiff Writer/Save Tiff.vi** prepares a TIFF file with header, dcimg2tiff.dll transfers the raw frame data on disk into the TIFF file, and polls communicates the progress to the *Main Window* via the “Saving Frame” global variable. This process runs in the background.

- **Application/Automation_TaskCompleted.vi** executes the next step in the Run Plan, or if all steps are complete, sends *Finish Recording Msg* to *Application* to return to the idle state.
