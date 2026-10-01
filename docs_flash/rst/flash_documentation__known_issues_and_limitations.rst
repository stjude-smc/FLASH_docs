.. _flash_documentation-known_issues_and_limitations:

Known Issues and Limitations
============================
.. important::  
    **Live Viewer:**
    Depending on window size, the bottom or right part of image may not visible.

.. important::  
    **Main Window:**
    - “Shutter” and other buttons may appear highlighted even when the button is not active. This is known bug in LabView.
    
    - File paths are limited to 120 characters (limitation in the Hamamatsu driver). Most special characters are also not permitted (limitation in Photometrics driver).
    
    - “Photobleach” button causes stage to move and laser power to increase at the same time, so initial fields may not experience the same laser power as the other fields.
    
    - Changing the enabled shutters during a recording may alter the camera triggering pattern and result in a failed acquisition, particularly with ALEX. Such changes are also ignored in series acquisitions.
    
    - A minimum shutter open time of 2ms is enforced and cannot be changed, even when a faster-responding device is used (AOM, EOM, AOTF, etc.).

.. important::  
    **Lasers**
    - Only one Coherent HOPS laser may be connected.
    
    - Only one Thorlabs PRM1-Z8 motorized polarizer may be connected.
    
    - Coherent HOPS driver may show warning “more than one device detected; arbitrarily choosing the first”. This warning is safe to ignore.

.. important::  
    **Stage:**
    - Only the Nikon Ti2 can be used for image-based autofocusing and Z stack recordings.
    
    - Only the Nikon Ti2 can be used for stage map indicator (because it is the only supported stage with absolute positioning on startup).

.. important::  
    **Synchronization devices:**
    - If cameras miss any frame trigger pulses, acquisition will never complete. Workaround: data can be recovered by cancelling the acquisition and choosing to save the partial movie.
    
    - NI-DAQ: Movie series (automation) should not be used with, especially with high frame rates. The high CPU utilization can sometimes cause dropped frames.
    
    - NI DAQ has a maximum trigger rate of 500 s-1 (2 ms frame intervals). For faster imaging rates, only the first frame is triggered by the external device and all cameras run on their own internal clocks. This approach may result in a loss of synchronization over long time periods (seconds to minutes, depending on how well matched are the camera internal clocks), but that his is not generally a problem given the fast photobleaching of commonly used fluorophores under the intense illumination required for such short exposure times. Especially with short exposure times, we advise utilizing an oscilloscope to monitor device synchronization.

.. important::  
    **Cameras:**

    - Timing calculations (including ROI size) assume the cameras have optimal connection (data transfer interface is assumed to never be limiting). This assumption may not be true when using a USB connection. For example, with Hamamatsu cameras, exposure times below 40 ms will fail when using 1x1 binning and USB connection.
    
    - Rapid movie series acquisitions may cause the hard disk recorder to fail, even though the disk is fast enough for data transfer. If this happens, turn on the countdown timer to slow acquisition rate or acquire movies one at a time
    
    - All cameras in use at the same time must have the same model number.
    
    - Hamamatsu FLASH does not always shut down completely, leaving an icon in the taskbar. This appears to be a bug in the DCAM driver. Workaround is to use task manager to kill the process or logging out of Windows.
    
    - Photometrics: pixel correction filters cannot be disabled (UI settings have no effect).
.. caution::
    **Other:**

    - Saved .tif files may have incorrect pixel size in metadata – magnification is assumed to be 60x and camera physical pixel size is assumed to be 6.5 µm.
