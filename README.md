# toniq
Python3 based codes to automize lab instruments.

- (WINDOWS) install pywin32
- Recquiered python modules: vxi11, pyvisa, pyvisa-py, pyusb

Notes:
- Some of the codes are very basic and/or in test phase => please report problems/suggestions
- Be sure to have all the necessary python libraries
    notably: appropriate GPIB libraries for your OS (linux-gpib for linux), matplotlib, numpy, scipy, time, math, ...
- Have a look on Prog_Manual folder if you want to implement your own functions and help improve the repository

=== Guidelines for the organization of this repository and drivers structure ===
- The main folder has to be named "<manufacturer>_<model>"
- Inside the main folder, the driver script has to be named exactly as the folder : "<manufacturer>_<model>.py"
- Inside the driver script, a class "Device" has to be present, which establishes a connection with the device once instantiated (connection process in the in the __init__ function).
- The class "Device" should have a function "close" to close properly the connection to the device.
    
