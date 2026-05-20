.. _flash_development_guide-troubleshooting:

Troubleshooting
===============

This section provides tips for troubleshooting errors and program crashes.

Error Codes
-----------

.. warning::

   Below is a list of standard error codes for FLASH.

   .. list-table::
      :header-rows: 1
   
      * - Code
        - Actor
        - Error description
      * - 5981
        - Stage
        - Soft limit exceeded
      * - 5982
        - Stage
        - Invalid axis
      * - 5989
        - Stage
        - Other error
      * - 
        - 
        - 
      * - 5972
        - Microscope
        - Ti2 stand not detected
      * - 5979
        - Microscope
        - Other error
      * - 
        - 
        - 
      * - 5961
        - Sync
        - Arduino configuration error
      * - 5962
        - Sync
        - Arduino acquisition period too short
      * - 5969
        - Sync
        - Other error
      * - 
        - 
        - 
      * - 5951
        - Power Meter
        - Initialization failed (device not detected)
      * - 
        - 
        - 
      * - 5941
        - Camera
        - Initialization error
      * - 5942
        - Camera
        - Invalid acquisition settings
      * - 5943
        - Camera
        - Disk streaming failed
      * - 5944
        - Camera
        - Not enough disk space
      * - 5949
        - Camera
        - Other error
      * - 
        - 
        - 
      * - 5931
        - Autosampler
        - Initialization error
      * - 5932
        - Autosampler
        - Invalid response
      * - 5933
        - Autosampler
        - Protocols error
      * - 5938
        - Autosampler
        - Wait for Idle Timeout
      * - 5939
        - Autosampler
        - Other error
      * - 
        - 
        - 
      * - 5921
        - Tiff Writer
        - Operation cancelled
      * - 5921
        - Tiff Writer
        - Invalid input file(s)
      * - 5922
        - Tiff Writer
        - Invalid output file(s)
      * - 5923
        - Tiff Writer
        - Potentially dropped frame (timestamp jump)
      * - 5929
        - Tiff Writer
        - Other error
      * - 
        - 
        - 
      * - 5910
        - Any
        - Not implemented
      * - 5911
        - Any
        - Operation timed out
      * - 5912
        - Any
        - Operation failed

Log Files
---------

.. warning::

   FLASH logs the execution of Application actor-level functions, along with a timestamp. This
   information can be retrieved using *Resources/Log Message.vi*, which is a functional global variable
   containing the log information. The log data is also displayed in the Main Window’s “log” tab as
   well as saved to disk in real time at “C:\\temp\\FLASH.log”, which is particularly useful in the
   case of program crashes.
   
    - 17:20:53.96 -- Set filter=1, path=2
   
   DCAM, if used, logs commands, return values, and any error codes in C:\\temp\\tmlog.txt.
   
    - 1.944 TMCC_GETAREA_40 -> i=0
   
    - 1.953 TMCC_GETAREA_40 OK hov=0 vov=0 hwv=2048 vwv=2048
   
   dcimg2tiff logs any errors in C:\\temp\\dcimg2tiff.log.

Keyboard Shortcuts for LabVIEW
------------------------------
- **Ctrl-U**: 
- **Ctrl-E**: 
- **Ctrl-W**: 
- **Ctrl-B**: 
- **Ctrl-Space**: 

Note about using the *'Pre Launch Init'* method: actors CANNOT be launched there (it will cause the program to hang without any error message). The best place for most initialization code is the actor core itself. 'Pre Launch Init' should only be used to check if pre-requisites for running the core are met (e.g. parameters initialized?) and abort launching the actor if necessary. 

Don’t use *“show FP”* when launching actor, as this will not work for built application. Use VI properties of Actor Core instead.
