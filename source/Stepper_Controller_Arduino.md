# Stepper_Controller_Arduino module

This is the documentation for the Stepper_Controller_Arduino_v2_5 module in the FreeMove Python 2.5 project.

- The first important factor to mention is that the python program (Stepper control) has two main classes, namely the threaded task and the GUI. The threaded task class runs on a different thread as the GUI since it must execute complicated computations (home the motor, run the profile, move the motor) if these processes were to be ran on the GUI class the GUI would lag until the process is finished. 
- Both of these classes communicate with the updateThread() function which receives a set_ind variable that represents either, a function (zB. 72 for the homing function) or the index of the motor we want to move manually. This function also takes set_val variable that represents either the value of the motor for the manual control (plus or minus) or in the case of the functions the different options, zB. if we are homing motor one or two. 

## Variables

- `set_ind` and `set_val`: Variables for motor index and value to be set.
- `stepperVals`: A list to store motor values.
- `SelecStepperVals`: A list to store selected stepper values.
- `myports`: A list of available ports.
- `arduino_port`: List for the selected Arduino port.
- `conn_bool`: Boolean for the connection status.
- `act`: An integer for the number of activated motors.
- `k`: An integer for mode selection.
- `loaded`: Boolean for profile mode status.
- `stepp_vals`: List for storing motor step values.
- `_looping`: Boolean for looping.
- `_func`: Boolean for function.
- `send1`, `send2`, and `send3`: Booleans for enabling motors.
- `home_mot1`, `home_mot2`, and `home_mot3`: Booleans for home iteration.
- `rec_bool`: Boolean for recording.
- `stepMode` and `mmPerStep`: Variables related to motor step mode and millimeters per step.


## [`class GUI()`](GUI.md)

Initializes the main GUI for the application. 
Creates frames for motor positions, motor controls, record controls, and connection controls. 

Defines buttons for various operations such as moving motors, recording, starting simulation, resetting, and stopping. 

Also sets up a menu bar with options for loading profiles, adding motors, and viewing help information.
    
- Global Variables:
    + **arduinoData:** The serial connection to the Arduino board.
    + **conn_bool:** Boolean value indicating the status of the connection.
    + **glob_status:** The global status of the application.
- Methods:
    +  [aboutWindow()](GUI.md#aboutwindow)
    +  [addMotor()](GUI.md#addmotor)
    +  [add_profiles()](GUI.md#add_profiles)
    +  [conn()](GUI.md#conn)
    +  [disableButtons()](GUI.md#disablebuttons)
    +  [enaButtons()](GUI.md#enabuttons) 
    +  [f_rec()](GUI.md#f_rec)
    +  [finish_profiles()](GUI.md#finish_profiles)
    +  [home_m1()](GUI.md#home_m1)
    +  [home_m2()](GUI.md#home_m2)
    +  [home_m3()](GUI.md#home_m3)
    +  [loadProfiles()](GUI.md#loadprofiles)
    +  [loop()](GUI.md#loop)
    +  [move1()](GUI.md#move1)
    +  [move2()](GUI.md#move2)
    +  [move3()](GUI.md#move3)
    +  [process_queue()](GUI.md#process_queue)
    +  [reset_m1()](GUI.md#reset_m1)
    +  [reset_m2()](GUI.md#reset_m2)
    +  [reset_m3()](GUI.md#reset_m3)
    +  [run_profile()](GUI.md#run_profile)
    +  [simWeg()](GUI.md#simweg)
    +  [sim_open()](GUI.md#sim_open)
    +  [sim_update()](GUI.md#sim_update)
    +  [stop_rec()](GUI.md#stop_rec)
    +  [update_gif()](GUI.md#update_gif)
    +  [update_thread()](GUI.md#update_thread)


## `MainGUI()`

This method creates the main GUI for the application. The GUI includes entry fields for the COM port and baud rate, a button for starting the program, and a status bar. 

The method also sets the protocol for closing the window and the window icon. It starts the main event loop for the GUI.

## [`class ThreadedTask()`](ThreadedTask.md)

Initializes the instance of the class. 
It takes a queue as an argument and sets it as an instance variable. 

It also sets several global variables, including 
- 'arduinoData'
- 'set_val', and 
- 'set_profile', 

It initializes several instance variables, including 
- 'val', 
- 'home_mot1', 
- 'home_mot2', 
- 'home', and 
- 'profile'. 

The *'val'* instance variable is set to the value of *'set_val'*, and the *'home_mot1', 'home_mot2', 'home', and 'profile'* instance variables are all initially set to *False*.

Methods: 
- [run()](ThreadedTask.md#run)
    
## `check_presence()`

    check_presence(correct_port, interval=0.1)    

Continuously checks the presence of the Arduino board at the specified interval. If the Arduino board is disconnected, it updates the global connection status and breaks the loop. 

Also checks for errors in Motor 1 and Motor 2 and updates the global status accordingly.

Args:
- **correct_port (str)**: The port to which the Arduino board is connected.
- **interval (float, optional)**: The time interval at which to check the presence of the board. Defaults to 0.1.

Global Variables:
-  **conn_bool**: Boolean value indicating the status of the connection. 
- **glob_status**: The global status of the application. 
- **_looping**: Boolean value indicating whether the application is looping. 
- **_func**: Boolean value indicating whether a function is being executed.

## `connectBoard()`

    connectBoard(uport='COM3', ubaudrate=250000)

Establishes a serial connection with an Arduino board using the specified port and baudrate. If the connection is successful, it starts a new thread to continuously check the presence of the board. If the connection fails, it raises a ValueError and destroys the main GUI.

Args:
- **uport (str, optional)**: The port to connect to. Defaults to “COM3”.
- **ubaudrate (int, optional)**: The baudrate for the connection. Defaults to 250000.

Raises:
- **ValueError**: If the connection to the Arduino board fails.

Global Variables:
- **arduinoData**: Stores the serial connection to the Arduino board
- **conn_bool**: Boolean value indicating the status of the connection.
- **myports**: List of available ports.
- **arduino_port**: The port to which the Arduino board is connected.

## `on_closing()`

Handles the event of closing the application. Prompts the user for confirmation before quitting. If the user confirms, it sends a *'!DC' * command to the Arduino board and quits the application.

Global Variables:
- **arduinoData***: The serial connection to the Arduino board. MainGUI.
- **root**: The root window of the main GUI.

## `on_closingStart()`

This function is triggered when the start button is clicked on the main GUI. It retrieves the COM port and baud rate from the GUI, and then attempts to connect to the Arduino board using these parameters.

If the **COM port** is set to *“NAM1”*, the function will ask the user if they want to enter “No Arduino Mode”, in which some functions may be disabled or not work. If the user confirms, the main GUI is launched.

If any other **COM port** is entered, the function will attempt to connect to the Arduino board.

If the connection is unsuccessful, an error message is displayed on the GUI. If the connection is successful, the main GUI is launched.