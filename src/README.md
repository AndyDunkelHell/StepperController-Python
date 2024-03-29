
# Arduino Code Method Explanation

In this guide, we will explain the key methods and functions in the provided Arduino code that is meant to be used with the FreeMove Arduino GUI. This code communicates with the Arduino board via serial communication.

## Global Variables

- `stepper_profile`, `stepper_dir`, `k`: Arrays to store stepper profiles, directions, and mode information.
- `val_y`, `ang`, `j1`, `j2`: Placeholder variables.
- `minPulseWidth`: Minimum pulse width for motor control.
- `err`, `motorXenable`, `motorYenable`, `motorZenable`, `connBool`, `motorVal`, `m_run`: Various boolean variables to track system states.

## Arduino Mega Information

- `Hinweise ARDUINO MEGA`: This section provides general information about the Arduino Mega board and its power requirements.

        // ==================== Hinweise ARDUINO MEGA ====================
        // https://docs.arduino.cc/hardware/mega-2560
        // InputVoltage --> 7-12V
        // InputCurrent -->

## Motor Control Configuration

- This section explains key considerations for motor control. It is recommended to always use microstepping for smooth motor operation, even though higher microstepping reduces the maximum motor speed.

        // ==================== Hinweise zur MOTORCONTROL ====================
        // Die Einstellung in DryveD1 Onlinetool müssen relatische werte haben (anders als im Handbuch angegeben).

        // Immer Mirkostepping, da sonst der Motor stottert und zwischenpositionen nicht gehalten werden
        // aber die max. Motordrehzahl wird bei höherem Mikrostepping kleiner (handbuch S. 94)
        // 1/1  	-- 200 Schritte/U   -- 7500 U/min  -- 25000 Schritte/s  -- 8750 mm/s
        // 1/2    -- 400 Schritte/U   -- 3750 U/min  -- 12500 Schritte/s  -- 4375 mm/s
        // 1/4    -- 600 Schritte/U   -- 1875 U/min  -- 6250 Schritte/s   -- 2187 mm/s
        // 1/8    -- 800 Schritte/U   -- 937 U/min   -- 3125 Schritte/s   -- 1093 mm/s
        // 1/16   -- 1600 Schritte/U  -- 468 U/min   -- 1562 Schritte/s   -- 546 mm/s
        // 1/32   -- 3200 Schritte/U  -- 234 U/min   -- 781 Schritte/s    -- 273 mm/s
        // 1/64   -- 6400 Schritte/U  -- 117 U/min   -- 390 Schritte/s    -- 136 mm/s <---- Ist für uns ausreichend

- `Closed Loop`: Mentions that closed-loop control is only effective above a certain speed threshold.

        // --> CLOSED LOOP erst ab 60 U/min -- 70 mm/s (Angabe vom Igus )

- `Minimale Periodenzeit`: Specifies the minimum pulse width for motor control.

        // Minimale Periodenzeit = 40us (Handbuch S. 95)

**Note**: For detailed information please refer to the Dryve D1 and Steppmotor manual.

## Switches and Pins

## Digital Outputs and Inputs

- `DIGITALE AUSGÄNGE`: Lists the general digital output pins on the Dryve D1 system and their functions.

        // DIGITALE AUSGÄNGE
        // X3.1   Bereit
        // X3.2   Aktiv
        // X3.3   Referenziert
        // X3.4   Alert
        // X3.5   Error

- `DIGITALER EINGANG`: Lists the general digital input pins on the Dryve D1 system and their functions.


        // DIGITALER EINGANG
        // X2.1   Takt
        // X2.2   Richtung
        // X2.7   ENA
        // X2.8   Endlagenschalter positiv
        // X2.9   Endlagenschalter negativ
        // X2.10  Fehler quittiert

## Switch Definitions

- `Switches`: Defines pins for various switches, including limit switches for X and Y axes.


        // ===== Switches ======
        #define CCWSwitchX 50 // Endlagenschalter negativ
        #define CWSwitchX 52  // Endlagenschater positiv

        #define CCWSwitchY 46 // Endlagenschalter negativ
        #define CWSwitchY 48  // Endlagenschater positiv


## Motor Initialization

- `MOTOR X Motorpins`: Defines the pins for the X-axis motor.

- `MOTOR X Pins for Digital Communication with Dryve D1`: Defines the pins for digital communication with the Dryve D1 system for the X-axis motor.


        // ===== Motor init ======

        // MOTOR X Motorpins
        #define STEP_X_PIN 2
        #define DIR_X_PIN 3
        #define ENA_X_PIN 4
        #define RES_X_PIN 5

        // MOTOR X Pins for Digital Communication with Dryve D1
        #define X3_1_X_PIN 22 // Bereit
        #define X3_2_X_PIN 24 // Aktiv
        #define X3_3_X_PIN 26 // Referenziert
        #define X3_4_X_PIN 28 // Alert
        #define X3_5_X_PIN 30 // Error 

- Similar definitions are provided for the Y and Z axis motors and their respective digital communication pins.

        // MOTOR Y Motorpins
        #define STEP_Y_PIN 6
        #define DIR_Y_PIN 7
        #define ENA_Y_PIN 8
        #define RES_Y_PIN 9


        // MOTOR Y Pins for Digital Communication with Dryve D1
        #define X3_1_Y_PIN 40 // Bereit
        #define X3_2_Y_PIN 42 // Aktiv
        #define X3_3_Y_PIN 44 // Referenziert
        #define X3_4_Y_PIN 46 // Alert
        #define X3_5_Y_PIN 48 // Error

        // MOTOR Z Motorpins
        #define STEP_Z_PIN 10
        #define DIR_Z_PIN 11
        #define ENA_Z_PIN 12
        #define RES_Z_PIN 13

        // MOTOR Z Pins for Digital Communication with Dryve D1
        #define X3_1_Z_PIN 23 // Bereit
        #define X3_2_Z_PIN 25 // Aktiv
        #define X3_3_Z_PIN 27 // Referenziert
        #define X3_4_Z_PIN 29 // Alert
        #define X3_5_Z_PIN 31 // Error 


**Note**: This must be adapted to the specific motor setup and hardware configuration.

## AccelStepper Initialization

- `AccelStepper` objects are created for X, Y, and Z motors, each with specified pins and settings. These serves as the main motor control objects.

        // AccelStepper deklarieren
        AccelStepper motorX(1, STEP_X_PIN, DIR_X_PIN);
        AccelStepper motorY(1, STEP_Y_PIN, DIR_Y_PIN);
        AccelStepper motorZ(1, STEP_Z_PIN, DIR_Z_PIN);


## MultiStepper Initialization

- `MultiStepper` object named `multiStepper` is initialized. In order to be able to control multiple motors simultaneously. The `MultiStepper` object is used to control multiple `AccelStepper` objects.

        // Multistepper deklarieren
        MultiStepper multiStepper;

## Functions to Start Motors

- `startMotorX()`, `startMotorY()`, and `startMotorZ()`: Functions to set the enable pin for motors.

        void startMotorX()
        {
        motorX.setEnablePin(ENA_X_PIN);
        motorXenable = true;
        
        }

        void startMotorY()
        {
        motorY.setEnablePin(ENA_Y_PIN);
        motorYenable = true;

        }

        void startMotorZ()
        {
        motorZ.setEnablePin(ENA_Z_PIN);
        motorZenable = true;

        }

## Coroutine for Sending Feedback

- `sendPos()`: Coroutine to periodically send motor positions to the Python code via serial communication. This function is only allowed to run when the motors are being manually controlled. This is done to ensure operation integrity while the motors are running profiles or homing. 

If the positions were sent each iteration while running these modes, the Arduino may be overwhelmed and these Processes could be interrupted. This is caused by the fact that the Arduino is not able to correctly handle multiple proceses simultaniously, so moving the motors and doing serial communication processes at the same time would overwhelm the Arduino eventhough this process runs in a *coroutine*.

        // COROUTINE to send Feedback to Python code
        COROUTINE(sendPos){
        COROUTINE_LOOP(){  
        if (motorVal == true){
        char buffer[32];
        int mot1 = motorX.currentPosition();
        int mot2 = motorY.currentPosition();
        int mot3 = motorZ.currentPosition();
        sprintf(buffer, "%d;%d;%d;", mot1, mot2 , mot3);
        Serial.println(buffer);
        
        }
        COROUTINE_DELAY(100);
        }
        }

## Motor Setup

- `setUpMultistepper()`: Configures motor settings, minimum pulse width, maximum speed, and acceleration for all three motors.

        
        void setUpMultistepper(){
        // Motor x
        motorX.setMinPulseWidth(minPulseWidth);
        motorX.setAcceleration(accel);
        motorX.setMaxSpeed(stepmaxSpeed);
        multiStepper.addStepper(motorX);
        

        // Motor Y
        motorY.setMinPulseWidth(minPulseWidth);
        motorY.setMaxSpeed(stepmaxSpeed);
        motorY.setAcceleration(accel);
        multiStepper.addStepper(motorY);

        motorZ.setMinPulseWidth(minPulseWidth);
        motorZ.setMaxSpeed(stepmaxSpeed);
        motorZ.setAcceleration(accel);
        multiStepper.addStepper(motorZ);
        
        }


## Command Handler

- `CommandHandler`: Handles serial communication with the Python code. This is the main function that receives commands and calls the appropriate functions to handle them.

        CommandHandler cmdHandler;

The Arduino control works with the CommandHandler to receive commands through serial communication with the python code and here the most important thing is that the commands only update the mode (k), the profile values or the direction for each motor. Each loop the [**setAllStepper()**](#main-loop) function runs and here depending on the mode something different happens

## Connection Handling

- `conn(CommandParameter &parameters)`: Handles the connection and motor startup.
- `disconn(CommandParameter &parameters)`: Disables motors and handles disconnection.

        void conn(CommandParameter &parameters){

                Serial.print(F("Connection confirmed and Motors Started!")); // When Connected Return to Python initiating the Motors
                setUpMultistepper();
                startMotorX();
                startMotorY();
                startMotorZ();
                connBool = false;
                delay(100);
        
        
        }
## Motor Reset

- `reset_m(CommandParameter &parameters)`: Resets a specific motor and reinitializes it.

        void reset_m(CommandParameter &parameters){
                int mot_int = parameters.NextParameterAsInteger();
                if (mot_int == 1){
                        motorX.stop();
                        digitalWrite(RES_X_PIN, HIGH);
                        delay(100);
                        digitalWrite(RES_X_PIN, LOW);   
                }
                if (mot_int == 2){
                        motorY.stop();
                        digitalWrite(RES_Y_PIN, HIGH);
                        delay(100);
                        digitalWrite(RES_Y_PIN, LOW); 
                }
                if (mot_int == 3){
                        motorZ.stop();
                        digitalWrite(RES_Z_PIN, HIGH);
                        delay(100);
                        digitalWrite(RES_Z_PIN, LOW); 
                }

        }

## Update Motor Directions and Profiles

- `updateMotors(CommandParameter &parameters)`: Receives and updates motor directions while in manual Control. 

        void updateMotors (CommandParameter &parameters){
                int int1 = parameters.NextParameterAsInteger();
                stepper_dir[0] = int1;
                int int2 = parameters.NextParameterAsInteger();
                stepper_dir[1] = int2;
                int int3 = parameters.NextParameterAsInteger();
                stepper_dir[2] = int3;
                //Serial.println(int1); 
        }

- `updateProfile(CommandParameter &parameters)`: Receives and updates motor profiles.

        void updateProfile (CommandParameter &parameters){
                profileBool = true;
                int int1 = parameters.NextParameterAsInteger();
                stepper_profile[0] = int1;
                int int2 = parameters.NextParameterAsInteger();
                stepper_profile[1] = int2;
                int int3 = parameters.NextParameterAsInteger();
                stepper_profile[2] = int3;
                int int4 = parameters.NextParameterAsInteger();
                stepper_profile[3] = int4;
                //Serial.println(int1); 
        }

- `updateMode(CommandParameter &parameters)`: Receives and updates the mode. Using the Variable k, the mode is set to manual, profile, or homing.

  - Normal mode: k = 0: the directions are fetched and then the manual control works
  - Homing mode: k = 3 (mot2) or 4 (mot1): the homing is done for the respective motor
  - Profile mode: k = 2: the profile values are fetched and ran

        void updateMode (CommandParameter &parameters){
                int k1 = parameters.NextParameterAsInteger();
                Serial.print(k1); 
                delay(100);
                k[0] = k1;
        }


## Motor Control Functions

- Functions like `plus_motorX()`, `minus_motorX()`, `plus_motorY()`, `minus_motorY()`, etc., control individual motor movements based on speed and direction.

        void plus_motorX(int spd = manualSpeed){
                motorX.setSpeed(spd);
                motorX.move(1*stepMode);
                motorX.runSpeed();       
        }
        void minus_motorX(int  spd = manualSpeed){
                motorX.setSpeed(-spd);
                motorX.move(-1*stepMode);
                motorX.runSpeed();
        }

        ...... Equal for all Motors


## Error Handling

- `errorMotor()`: Handles motor errors by stopping and reporting the error. 

## Homing Functions

- `home_mX()`, `home_mY()`, `home_mZ()`: Handle homing for the X, Y, and Z motors, respectively. To better understand how the homing works, the homeZ function will be explained bellow. The function contains conditional statements and motor control commands.

- **Conditional Checks**

   - **if (homingDoneZ == true):** This checks whether homing for the Z-axis is already done. If it's done, the function returns without further action.

   - **if (digitalRead(X3_5_Z_PIN) == LOW && homingDoneZ == false):** This checks if the specified pin (X3_5_Z_PIN) is in a LOW state and if Z-axis homing (homingDoneZ) is not already completed. If these conditions are met, it calls the **minus_motorZ** function with the manualSpeed parameter, until the end switch is triggered.

         void home_mZ(){
                if(homingDoneZ == true){
                return;
         }
        
         if(digitalRead(X3_5_Y_PIN) == LOW && homingDoneZ == false){

                minus_motorY(manualSpeed);
        
         }
         ...

- **Homing Process**

  - **If the condition digitalRead(X3_5_Z_PIN) == HIGH** is met, the code within this block is executed, indicating that the motor has reached the end position and the Z-axis homing process is initiated.

        else if(digitalRead(X3_5_Z_PIN) == HIGH){
                
                Serial.println(1);
                
                homingDoneZ = true;
                delay(1000);  
                digitalWrite(RES_Z_PIN, HIGH);
                motorZ.setCurrentPosition(0);
                delay(100);   
                digitalWrite(RES_Z_PIN, LOW);

                while(motorZ.currentPosition() != middlePointZ){
                plus_motorZ(manualSpeed);
                }

                Serial.println(5);
                digitalWrite(RES_Z_PIN, HIGH);
                motorZ.setCurrentPosition(0);
                delay(100);
                digitalWrite(RES_Z_PIN, LOW);   

                k[0] = 0;

        }

        }
        

  - **Serial.println(1)**: This line simply prints "1" to the serial monitor, indicating the start of the Z-axis homing process.

  - **homingDoneZ = true:** This sets the homingDoneZ flag to true, indicating that Z-axis homing is in progress.

  - **digitalWrite(RES_Z_PIN, HIGH):** It sets a digital pin (RES_Z_PIN) to HIGH. This action resets the motor in order to be able to move in the other direction. This is needed since in this setup, when the end switch is triggered the motor hard stops and cannot move in the other direction.

  - **motorZ.setCurrentPosition(0):** This sets the current position of the Z-axis motor to zero to be able to run back to the dessired middle point.

  - The **while loop** controls the motor's movement until it reaches a certain position (middlePointZ) by calling the *plus_motorZ* function with the manualSpeed parameter.

  - After reaching the desired position, "5" is printed to the serial monitor *(Serial.println(5))*, this number is received by the Python GUI where it is interpreted as the homing for this motor is done.

  - Finally, **k[0]** is set to 0. This is done in order to return to the manual mode before the next iteration.

The specifics of the motor control and homing process depend on additional hardware configurations. This code was created to work with the Motor set-up on the FreeMove testbench using the Dryve D1 motor controller and the integrated Induction end switches. It should be possible to check any other type of proximity sensor or end switch by changing the **digitalRead()** function to the appropriate pin.

## Main Loop

- `setAllSteppers()`: Checks the motor direction and mode and controls motor movement accordingly.

There are multiple posibilities when going into this Method depending on the k variable. This function is inside the main loop and is called every time which ensures the smooth running of the motors and the proper handling of the different functions, namely homing and profile running.

 - The homing is started if the k is either 3, 4 or 5. 
 - The profile is started if the k is 2. While excecuting the profiles the current position of the motors is checked every loop. 
 
 If it is equal to the desired positon then a '1' is sent to the python GUI whcih in turn sends the next desired positon and speed. 
 
 If the current position is not equal to the desired position then the motors are moved towards the desired position using the minus or plus functions stated above with the speed that was sent from the python GUI.

This way of handling is beneficial mainly since while running the profile we can specify exactly the velocity for each position to be reached, when the new value is updated from the python script. This should allow for the faster or slower movement occasionally, which is one of the requirements.

- `loop()`: Main loop that processes serial commands, sets motor positions, and runs the `sendPos` coroutine.
