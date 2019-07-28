# toniq
Python3 based codes to automize lab instruments.

- (WINDOWS) install pywin32
- Recquiered python modules: vxi11, pyvisa, pyvisa-py, pyusb

Notes:
- Some of the codes are very basic and/or in test phase => please report problems/suggestions
- Be sure to have all the necessary python libraries
    notably: appropriate GPIB libraries for your OS (linux-gpib for linux), matplotlib, numpy, scipy, time, math, ...
- Have a look on Prog_Manual folder if you want to implement your own functions and help improve the repository


__=== Guidelines for the organization of this repository and drivers structure ===__
- The main folder has to be named "\<manufacturer\>_\<model\>". It contains at least the driver script, and the programming documentation of the device.
- Inside the main folder, the driver script has to be named exactly as the folder : "\<manufacturer\>_\<model\>.py"
- A class "Device" has to be present in the driver script, which establishes directly a connection with the device once instantiated (connection process in the \_\_init\_\_ function of Device's class).
- The class "Device" should have a function "close" to close properly the connection to the device. After calling this function, the instance then become unusable, and a new instance of the class Device has to be created to re-establish a connection with the device.
    
