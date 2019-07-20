This package is dedicated to control the GUI Winspec.

2 configurations : LOCAL or REMOTE

Description of the files :
- princeton_winspec.py is the main script. It contains the main class Device. (front-end)
- connector.py contains a class WinspecConnector from which the class Device of the main script is inherited. There are two versions of connector.py, whether you use LOCAL or REMOTE configuration.
- winspec_gui_driver.py controls directly the GUI Winspec, so it is located in the computer running it.

First of all, you have to move these files in a correct way, depending on the configuration you are using (LOCAL or REMOTE).

=== LOCAL mode ===
Winspec is running on the same computer as the one used by the user to automatize the measures.
- Move the file connector.py of the LOCAL folder in the folder containing the main driver script princeton_winspec.py
- Let the file winspec_gui_driver.py in the folder containing the main driver script princeton_winspec.py
- Instantiate the class Device in princeton_winspec.py

=== REMOTE mode ===
Winspec is running on a HOST computer while the user controls it from a REMOTE computer.
The communication between the two use a TCPIP server on the HOST computer, which controls Winspec through the file winspec_gui_driver.py
- Move the file connector.py of the REMOTE folder in the folder containing the main driver script princeton_winspec.py
- Move the file winspec_gui_driver.py in the folder "winspec_server" and then move it to the HOST computer.
- Start the server in the HOST computer by following the instructions in the server README file.
- Instantiate the class Device in princeton_winspec.py on the REMOTE computer.