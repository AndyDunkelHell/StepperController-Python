# Class Stepper_Controller_Arduino_v2_5.GUI(master)

Bases: *object*

## `aboutWindow()`

This method creates a new Toplevel window that displays information about the application. The window contains a label with the application name, version, reference to the GitHub page for more information, the creator's name, and the intended user group.

## `addMotor()`

This method adds a new motor to the application. It increments the motor index and, if the maximum number of motors is reached, it disables the add motor option in the edit menu. 

It creates a new label frame for the motor with move, home, and reset/stop buttons, and anterior and posterior radio buttons. It also displays the anterior/posterior value. If the user cancels the operation, no motor is added.

## `add_profiles()`

This method creates a new frame in the profile menu window to load profiles. After being loaded, it adds its path to the profile path list. 

It also creates a label with the profile path and an entry field for profile iterations in the new frame.

## `conn()`

This method manages the connection to the Arduino board. If the board is not connected, it tries to connect to the board and updates the status text accordingly. 

- If the **connection is successful**, it sleeps for 1 second, calls the *update_thread()* method with a specific parameter to send the connect command to the board, and sets the connection flag to True. 

- If the board is **already connected**, it enables all buttons, calls the *update_thread()* method with a specific parameter to send the connect command to the board, and updates the connect button text to 'Arduino Connected'.

## `disableButtons()`

This method disables all buttons in the Motor 1, Motor 2, and recording frames. It does not affect the stop recording button.

## `enaButtons()`

This method enables all buttons in the Motor 1, Motor 2, and Motor 3 frames, and in the recording frame. It disables the stop recording button. 

If the maximum number of motors is not reached, then motor 3 has not been added. Therefore it does not enable the buttons in the Motor 3 frame.

## `f_rec()`

    f_rec(r_line='')

This method starts the recording of stepper values. If recording is not in progress, it sets the recording flag to True, enables the stop recording button, and changes the color of the record button to green.

## `finish_profiles()`

This method retrieves the iterations value from the profile menu, appends it to the profile list, and opens each profile in the profile path list. 

It updates the selected profile text with the profile names and the status text with the number of profiles loaded. It also sets the global variable *loaded* to True.

## `home_m1()`

This method initiates the homing process for Motor 1. It updates the status text to 'Homing Motor 1' and calls the *update_thread()* method with specific parameters for Motor 1.

## `home_m2()`

This method initiates the homing process for Motor 2. It updates the status text to 'Homing Motor 2' and calls the *update_thread()* method with specific parameters for Motor 2.

## `home_m3()`

This method initiates the homing process for Motor 3. It updates the status text to 'Homing Motor 3' and calls the *update_thread()* method with specific parameters for Motor 3.

## `loadProfiles()`

This method creates a new Toplevel window for loading profiles. 

The *window* contains two label frames for adding profiles and selecting profiles, respectively. 

It also contains two buttons for adding a profile and loading all profiles. It initializes the profile path list and calls the add_profiles method.

## `load_profile()`

This method opens a file dialog for the user to select a profile. It returns the name of the selected file. If no file is selected, it updates the status text to 'No Data Selected'.

## `loop()`

This method continuously reads commands from the Arduino. If an error occurs in Motor 1, Motor 2, or Motor 3, it updates the status text to indicate the error and calls the *move* (move1(), move2() ...) method for the respective motor. 

If recording is in progress, it appends the received stepper values to the stepper values list. 

*It also updates the displayed stepper values for the motors.*

The method repeats every **12 milliseconds**.

## `move1()`

This method controls the movement of Motor 1. If Motor 1 is not homed, it updates the status text to *'Please Home Motor 1'*. 

*If* Motor 1 is **already moving**, it stops the movement, changes the color of the move button to red, and calls the *update_thread()* method with specific parameters to stop the movement. 

*If* Motor 1 is **not moving**, it starts the movement, changes the color of the move button to green, and calls the *update_thread()* method with specific parameters to start the movement. 

It can send either 
- *0* to stop the movement **or**
- *1* to move forward, **or** 
- *2* to move backward.

## `move2()`

This method controls the movement of Motor 2. If Motor 2 is not homed, it updates the status text to *'Please Home Motor 2'*. 

*If* Motor 2 is **already moving**, it stops the movement, changes the color of the move button to red, and calls the *update_thread()* method with specific parameters to stop the movement. 

*If* Motor 2 is **not moving**, it starts the movement, changes the color of the move button to green, and calls the *update_thread()* method with specific parameters to start the movement. 

It can send either 
- *0* to stop the movement **or**
- *1* to move forward, **or** 
- *2* to move backward.

## `move3()`

This method controls the movement of Motor 3. If Motor 3 is not homed, it updates the status text to *'Please Home Motor 3'*. 

*If* Motor 3 is **already moving**, it stops the movement, changes the color of the move button to red, and calls the *update_thread()* method with specific parameters to stop the movement. 

*If* Motor 3 is **not moving**, it starts the movement, changes the color of the move button to green, and calls the *update_thread()* method with specific parameters to start the movement. 

It can send either 
- *0* to stop the movement **or**
- *1* to move forward, **or** 
- *2* to move backward.

## `rec_stop()`

This method stops the recording of stepper values. It sets the recording flag to *False*, disables the stop recording button, and changes the color of the record button to its default color.

## `process_queue()`

This method processes messages from the queue to display the queued messages sent to the Arduino. 

It tries to get a message from the queue and updates the status text with the message. If the queue is empty, it calls itself again.

## `reset_m1()`

This method resets Motor 1. It updates the status text to *‘Reset Motor 1’* and sends a reset command to Motor 1 through the Arduino.

These methods do not call the Update Thread method because the reset command is better sent directly to the Arduino without going through the queue.

## `reset_m2()`

This method resets Motor 2. It updates the status text to ‘Reset Motor 2’ and sends a reset command to Motor 2 through the Arduino.

## `reset_m3()`

This method resets Motor 3. It updates the status text to ‘Reset Motor 3’ and sends a reset command to Motor 3 through the Arduino.

## `run_profile()`

This method runs the loaded profile if the motors are homed. If the motors are not homed, it updates the status text to ‘Please Home motors’. If no profile is loaded, it does nothing.

## `simWeg()`

This method simulates the movement of the hand based on the input parameters for alpha (flexion/extension), beta (radial/ulnar), theta (steps for angle calculation), and speed (angular speed).

It updates the configuration with the input values, deletes all figures previous figures (previously generated), simulates the movement, and stores the result as a GIF.

If the input is invalid, it updates the status text to *‘Wrong Input, try again’*.

*simulate_weg(), delete_all_figures() and store_as_gif() are called from the plotting.py file*

The input values are retrieved from the entry fields in the simulation window and are updated in the configuration file.

If the simulation is **successful**, it updates the status text to ‘Sim Done! Loading GIF Please Wait’, opens a new window, and displays the GIF.


## `sim_open()`

This method creates a new Toplevel window for running simulations.

The window contains a label frame for controls with entry fields for alpha min and max, beta min and max, theta, speed, and profile name.
these values are used to simulate the movement of the hand in the simWeg Method.

It also contains a button for starting the simulation.

Additionally, it has four sliders for adjusting the view of *flexion/extension (FE)*, *radial/ulnar (RU)*, *alpha (FE)*, and *beta (RU)*.

Using the Sliders a live Plot is generated it **updates** the live Plot on display with the slider values.

The method initializes the current values for the sliders and calls the sim_update method.

## `sim_update()`
    sim_update(var = 0)
This method updates the simulation based on the current values of the sliders. It initializes the hand and motor positions, moves the hand to the specified alpha (flexion/extension) and beta (radial/ulnar) positions, and visualizes the hand and motor positions. 

It adjusts the view of the visualization based on the view sliders and displays the visualization in the simulation window.

It also closes previous figures (to avoid memory problems)

## `stop_rec()`

This method stops the recording of stepper values. If recording is in progress, it sets the recording flag to False, disables the stop recording button, and changes the color of the record button to red. 

It then opens a file dialog for the user to save the recorded stepper values as a *CSV file*. If the user cancels the save operation, it does nothing.


## `update_gif()`
    update_gif(ind)
This method updates the GIF displayed in the GIF window. It cycles through the frames of the GIF at a rate of one frame per 100 milliseconds. When it reaches the last frame, it loops back to the first frame.

## `update_thread()`
    update_thread(ind=0, val=0, profile_val=[])
This method updates the global variables for the index, value, and profile value. It starts a new queue and a new [`ThreadedTask`](ThreadedTask.md) with the queue. 

It then processes the queue after a delay of **12 milliseconds**.

