.. _ui_window_actor-preamble:

Creating a New UI Window Actor
==============================

Introduction
------------

.. note::

   User interface windows that need to run continuously and asynchronously from other actors should be
   instances of the *UI Window* class. For many modal dialog type use cases, it is best to use a simple
   VI wired directly into the calling VI with the front panel visible, which will block execution until
   the task is complete (see *Countdown Timer.vi* for example).

Here are the basic steps for creating a new *UI Window* class:

- Create a new class inheriting from *UI Window*

- Create an override of the “Create Front Panel Events” that calls “Create User Event.vi” for each type of message that may need to be passed to Actor Core. Bundle these into the class data and update the class .ctl file to include them.

- Create an override for “Destroy Front Panel Events” that calls “Destroy User Event.vi” to clean up all of the User Event instances.

- Create an override method for Actor Core.vi. This will generally include all user interface elements on the front panel and a helper loop with an Event Structure in the wire diagram. User interactions with front panel controls trigger cases in the Event Structure and perform the desired actions. Be sure to wire the various User Event properties from the class data into the Event Structure so Actor Core can receive these events.

- Alternatively, references to front panel controls can be added to the class members that are updated via properties nodes in message handler methods. This approach is useful for handling device status updates where no action is needed other than updating a front panel control (such as the progress bar in the *Viewer* window).

.. important::

   Don’t wire TRUE to “Show Front Panel” option when launching the actor, as this will not
   work for built applications. Use VI properties of Actor Core.vi file instead.

Creating a new method
---------------------

First decide whether the method should be public (often used for message handling) or private
(internal methods with no associated messages). To override the behavior of a parent class, right
click on the virtual folder associated with this scope and select “Add->VI for Override”. To add a
method that is specific to the class, right-click on the fold and select “Add->VI from dynamic
dispatch template”.

Utility methods that do not use class data should be created as an ordinary VI and added to the
.lvlib outside of the class hierarchy.

Adding and accessing class properties
-------------------------------------

Class properties are defined in a .ctl file in each class, to which new properties can be directly
added. These are easily accessed by class methods using the cluster “bundle/unbundle by name” Vis
wired form the class instance wire. To access properties inherited from the base class (such as
*Device* or *Camera*), either use property nodes or create a new method in the parent class
specifically designed for this task.

Creating a message
------------------

.. note::

   Actors generally communicate by asynchronous message passing. This approach minimizes coupling
   between actors and allows them to run simultaneously and independently with minimal chances of race
   conditions.

.. important::

   Messages are processed by the actor in a first-in-first-out order (not in parallel). As such, any
   method used to respond to a *Message* should generally execute in minimal time; tasks that may block
   while waiting for a resource to become available or are computationally intensive should not be
   executed directly in message handling methods. These are best processed within Actor Core.vi (or
   passed along to some other actor specialized for this task).

To create a new *Message* for an existing method, first make sure the target vi is in the “Public”
scope and its connector pane has been finalized, including which inputs are required, as this will
be harder to change later. Next, right click on the desired method vi and select “Actor
Framework->Create Message”. This will execute a script to create a new message class, which should
reside in the “Messages for this actor” virtual folder. The class properties include all elements
for each of the VI inputs. The methods include a Do.vi that calls the target method and a “Send
<method name>.vi” that is used to send a message to the target actor. None of these files should be
edited directly by the developer.

.. caution::

   It is possible to send messages synchronously by inheriting from the “Send Message And Wait For
   Response” VI, but this is not recommended as it can create race conditions and was intentionally
   made by NI to be difficult to implement.

Editing a message
-----------------

Changes to class methods do not generally require any changes to the associated message class.
However, if you have changed the connector pane of a method VI, including which terminals are
required, you need to update the associated message class. This is accomplished by right-clicking on
the message class and choosing “Actor Framework->Rescript message”.

Actor Core.vi
-------------

Actor Core.vi runs continuously throughout the lifetime of the actor. This VI typically splits the
actor instance wire to the parent Actore Core, which implements a “message handler” loop, and a
`“helper loop” <https://www.mooregoodideas.com/actor-framework/basics/AF-basics-part-4/>`_ (in the
override method). The helper loop runs in its own thread separate from message handling, which
creates several issues that the developer should keep in mind:

- The ‘stale’ actor object wire is not updated when message handling methods modify the class data over time. This wire is still useful, for example for referencing the device configuration, which cannot be changed in FLASH after initialization.

- Class methods should not be called directly from Actor Core using the stale actor object wire. Instead, use “Read Caller Enqueuer.vi” to self-enqueue messages, which will call class methods using the active reference to the class data.

- Class methods can communicate with the Actor Core helper loop in a few ways:

  - **User Events:** “Create User Event” VI creates a reference to a queue that is saved in class properties. Class methods call the “Generate User Event” VI to add an event to the queue. Actor Core wires a reference to the queue to its Event Structure and add cases to react each user event type. The class destructor should call “Destroy User Event” to clean up these references. This approach is ideal for reactive actors such as *UI Window* instances.

  - **Data Value Reference (DVR):** a DVR can be referenced by both class methods and Actor Core to refer to the same memory location. This approach is most valuable for time-critical applications such as in *Synchronization Device*. The flow of information should be unidirectional and extra care must be taken to avoid race conditions.

  - **Global variables:**

    .. warning::

       this approach should be avoided if possible. It is currently used in FLASH for broadcasting some information across the whole application, such as the current frame number. This behavior will be changed in a future version.

  - Notifiers, queues, and some other objects are passed by reference and therefore can be used for communication between Actor Core and other class methods, but this isn’t standard in FLASH. This can include references to front panel controls, which can be useful for real-time updates of the user interface elements.

Asynchronous Communication
--------------------------

.. note::

   One of the most challenging aspects of the Actor Framework for many developers is the asynchronous
   nature of the message passing architecture. Rather than executing an imperative sequence of steps in
   series, Actors send messages to other Actors that execute tasks asynchronously. This works well when
   no reply is needed as steps can be executed simultaneously.

.. danger::

   One solution to provide synchronous execution is for the sending actor to poll a variable (with a
   global variable, functional global variable, data value reference, queue etc.) that is modified by
   the receiving actor when the task is complete. This will block the actor from processing any
   messages during this time, which could lock the application. As such, this approach is only used in
   FLASH for short steps such as waiting for cameras to be ready for acquiring data. The process also
   includes a timeout to prevent the application from locking completely.

.. tip::

   Another solution is for the sending actor to be configured as a state machine with member variable
   being checked by every message handler vi to determine how to react to various messages it receives.
   The next step in a process can then be executed when the actor receives a reply that the requested
   task has been completed by the other actor. This is generally the preferred method, and is used by
   the Application actor, but is more complex to implement.
