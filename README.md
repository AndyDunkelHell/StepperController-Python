# Welcome to FreeMove Python's documentation

This program is meant to be used with the FreeMove Arduino project. It is a GUI that allows the user to control the stepper motors connected to the Arduino board. The GUI is written in Python and uses the Tkinter library. The GUI communicates with the Arduino board via serial communication. Check the [`requiremnts.txt`](.github/requirements.txt) file for the required libraries.

At the bottom of this page you can find the [`Index`](genindex.md) and the [`Module Index`](py-modindex.md). These pages serve as a reference for ALL the different functions and classes used in the program. Refer to these pages for more information on the function of the different functions and classes.

To find out more about the inner works of the Arduino Sketch, refer to the README inside the [`src folder`](/src/). In order to use the GUI with the Arduino board, you need to upload the sketch to the board first. This project was setup with the PlatformIO IDE, so you can use that to upload the sketch to the board. This way you can ensure that the correct libraries are uploaded to the arduino board.

The following Diagram shows the general structure of the program:

![Imgur Image](https://imgur.com/LzSM1lU.jpg)

## FreeMove Arduino Project GUI User Guide

This user guide explains how to use the FreeMove Arduino Project GUI, which allows you to control stepper motors connected to an Arduino board using a graphical interface. The GUI is written in Python and utilizes the Tkinter library for its interface.

The GUI has different frames (sections) that are shown divided into different classes of the diagram with their own attributes and the functions they execute when interacted with. The name of the frames depicted on the top left of the following figures is the same as in the diagram.

## Dryve D1 Settings: 
The Motorcontroller Dryve D1 (Igus) has different setting. 
If you want to use the Arduino for Controllong the "Takt Richtung Setting" must be selected.

**Takt/Richtung:** 
  Um den Motor in der Betriebsart „Takt/Richtung“ zu steuern gehen Sie wie folgt vor:
  1. Setzen Sie auf der „Achse“ Seite die „Bewegungslimits“: 
      Max. Geschwindigkeit“ = 100.000 
      Tippgeschwindigkeit“ = 100.000
      Max. Beschleunigung“ = 1.000.000
  2. Erteilen Sie der dryve durch Schalten von DI 7 die „Freigabe“.
  3. Setzen Sie die Bewegungsrichtung durch Schalten von DI 2 „Richtung“

## GUI preview:

Once you start the program you will be greeted with the following window:

![Imgur](https://imgur.com/yyyg3bg.jpg)

Please insert the correct COM port and Baudrate for your specific Arduino board. The program will then initialize the connection, if it succeeds you will be greeted with the main GUI window, where you can control the motors and use the different functions.

![Screenshot 2023-10-24 223115](https://github.com/AndyDunkelHell/FreeMove-Python/assets/58504780/746a9d3e-33da-4a42-b307-6c769878705d)

In the following section we will go over the different Parts of the GUI and their functions.

## Table of Contents
1. [Connecting to the Arduino Board](#1-connecting-to-the-arduino-board)
2. [Menu Bar](#2-menu-bar)
3. [Motor Control](#2-motor-control)
   - [Motor 1 Control](#motor-1-control)
   - [Motor 2 Control](#motor-2-control)
   - [Motor 3 Control](#motor-3-control)
   - [Motor Positions](#motor-positions)
4. [Simulation](#4-simulation)
5. [Recording](#5-recording)
6. [Home Functions](#6-home-functions)
7. [Reset Motors](#7-reset-motors)
8. [Profile Functions](#8-profile-functions)

## 1. Connecting to the Arduino Board
Before you can control the stepper motors, you need to confirm a connection with the Arduino board. Here's how:

- Click the "Connect" button to confirm a connection with the Arduino board.
- Once connected, the button will change to "Arduino Connected" in green, indicating a successful connection.

**Note:** If the connection is lost or you want to reconnect, you can click the "Connect" button again. 

**IMPORTANT**: This function also **initiates** the motors on the Arduino

## 2. Menu Bar

The menu bar offers additional options:

- **File**:
  - **Load Profiles**: Open a window to load profiles. For more information on profiles check the [Profile Functions](#8-profile-functions) section.

- **Edit**:
  - **Add Motor**: Add a motor.

- **Help**:
  - **About**: Display information about the application.


## 3. Motor Control

The GUI allows you to control up to three stepper motors, labeled as Motor 1, Motor 2, and Motor 3. The directions are specified with medical nomenclature, but they are defined as **PLUS/MINUS** directions. Below are the common controls for each motor:

For more information refer to the [Move methods](source/GUI.md#move1) in the GUI class.

### Motor 1 Control
- **Move:** Click the "Move" button to start the movement of Motor 1. Click again to stop the movement.
- **Anterior/Posterior:** Use the radio buttons to select the direction of movement.
- **Home:** Click the "Home" button to initiate the homing process for Motor 1.
- **Reset/Stop:** Click the "Reset/Stop" button to stop Motor 1 or reset its position if needed.

### Motor 2 Control
- **Move:** Similar to Motor 1, the "Move" button controls the movement of Motor 2.
- **Anterior/Posterior:** Use the radio buttons to specify the direction.
- **Home:** Click the "Home" button to initiate the homing process for Motor 2.
- **Reset/Stop:** Use the "Reset/Stop" button to stop Motor 2 or reset its position.

### Motor 3 Control (if available)

This motor is not usually available, but you can add it using the [`addMotor()`](source/GUI.md#addMotor) function. This is accesable through the [Add Motor Menu option](#2-menu-bar). 

- **Move:** If Motor 3 is available, you can control it similarly to Motor 1 and Motor 2.
- **Anterior/Posterior:** Choose the direction with the radio buttons.
- **Home:** Initiate the homing process for Motor 3 by clicking "Home."
- **Reset/Stop:** Use the "Reset/Stop" button to stop Motor 3 or reset its position.

## Motor Positions

- **Motor 1**: Displays the position for Flexion/Extension.
- **Motor 2**: Displays the position for Medial/Lateral.
- **Motor 3 (if available)**: Displays the position for Anterior/Posterior.

## 4. Simulation
The simulation feature allows you to visualize the movement of the hand based on specific parameters. Follow these steps:

- Full Simulation: using this function you can simulate the movement of the hand based on the parameters you provide. 
    - Enter values for *min and max* Alpha (Flexion/Extension) and Beta (Radial/Ulnar). You can also provide the Theta (Steps for angle calculation), and Speed (Angular speed).
    - Click "Simulate Weg" to run the simulation.
    - The simulation will run for the full range of motion of the hand. A GIF will be generated and displayed in a new Window. 
    - The specific motor positions and the required speed to move to the next position will be saved in a CSV file named as the profile name you provided.

The profiles are formatted as follows 
    
    Position motor 1 (in mm), Speed Motor 1, Position motor 2 (in mm), Speed Motor 2
    
    Example:
    124,1000,4,1000

- Preview, Live plot:
    - You can adjust the *Live view plot* using the sliders provided for Flexion/Extension (FE), Radial/Ulnar (RU), Alpha (FE), and Beta (RU). Please note that this will not affect the full simulation and it just serves as a preview.

## 5. Recording
The recording feature allows you to capture stepper motor values. Here's how it works:

- Click the "Record" button to start recording values.
- To stop recording, click the "Stop Recording" button. You'll be prompted to save the recorded values as a CSV file.

## 6. Home Functions
The "Home" buttons for each motor (e.g., "Home Motor 1") initiate the homing process. This process helps the system identify the motor's home position.

## 7. Reset Motors
The "Reset" buttons for each motor (e.g., "Reset Motor 1") allow you to reset the motor. This can be helpful if a motor is stuck or not functioning correctly.


## 8. Profile Functions

- **Add Profiles**: Add profile paths and define the number of iterations.
- **Load All Profiles**: Load all added profiles for execution. Take into consideration that the iteration number must be defined for each profile.
- **Run Profile**: Run the loaded profiles.



## Please note
 That the functionality of some buttons may depend on the status of motors, connections, and loaded profiles. Ensure that the motors are homed before running profiles. Refer to the status messages for guidance.

## Indices and tables

- [Index](genindex.md)
- [Module Index](py-modindex.md)

---

©2023, \@AndyDunkeHell (Github).
