.. _flash_documentation-recommended_hardware:

Recommended Hardware
====================

- Up to four Hamamatsu Fusion cameras (C14440-20UP). For optimal results, these should have sequential serial numbers and the same firmware version.
  `https://www.hamamatsu.com/eu/en/product/cameras/cmos-cameras/C14440-20UP.html <https://www.hamamatsu.com/eu/en/product/cameras/cmos-cameras/C14440-20UP.html>`_

- Each camera is dedicated to a specific fluorophore’s spectra band using an optical splitter such as Cairn MultiCam with appropriate dichroics and band-pass filters. The system should be adjusted so the camera fields of view are closely aligned and parfocal. 
  `https://www.cairn-research.co.uk/product/multicam/ <https://www.cairn-research.co.uk/product/multicam/>`_

- Nikon Eclipse Ti2-E microscope stand configured with standard motorized filter turret, motorized encoder stage, and motorized Z-drive objective mount.

- Four Uniblitz LS6 shutters (for 473, 532, 640, 721 nm laser lines) with VCM-D4 driver:
  `https://www.uniblitz.com/products/ls6/ <https://www.uniblitz.com/products/ls6/>`_
  `https://www.uniblitz.com/products/vmm-d4-shutter-driver/ <https://www.uniblitz.com/products/vmm-d4-shutter-driver/>`_

- Optional: Thorlabs PRM1Z8 for rapid laser power attenuation with a rotating polarizer.
  `https://www.thorlabs.com/thorproduct.cfm?partnumber=PRM1Z8 <https://www.thorlabs.com/thorproduct.cfm?partnumber=PRM1Z8>`_

- Arduino Due (see below) for triggering shutters, cameras, and fluidics.

- Dell Precision 7920 or similar Xeon processor (8 or more physical cores), 128 GB RAM, and Intel Optane 905P PCIe SSD (1.5 TB). If another SSD is used, make sure it has a measured sustained write speed of at least 2 gigabytes/s.

- Windows 10 and 11.
