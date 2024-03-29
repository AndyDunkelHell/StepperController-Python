#include <Arduino.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <AccelStepper.h>
#include <MultiStepper.h>
#include <AceRoutine.h>
#include <TimerOne.h>
#include "CommandHandler.h"

// For use with the Stepper_Controller_Arduino_v2.3.py

using namespace ace_routine;
CommandHandler<10, 90, 15> SerialCommandHandler;

volatile bool emergencyStop = false;

static int stepper_profile[6];
static int stepper_dir[3];
static int k[1];
int val_y = 1; // Placeholder
int ang = 90; // Placeholder
int j1 = 0;
int j2 = 0;

int minPulseWidth = 40; // min. Pulse Time (Handbuch S. 95)

bool err = false;
bool motorXenable = false;
bool motorYenable = false;
bool motorZenable = false;
bool connBool = false; // Bool to state Connection Status
bool motorVal = false; // Bool to state if Motor Values or DIR have been Received
bool m_run = true;
// ==================== Hinweise ARDUINO MEGA ====================
// https://docs.arduino.cc/hardware/mega-2560
// InputVoltage --> 7-12V
// InputCurrent -->

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

// --> CLOSED LOOP erst ab 60 U/min -- 70 mm/s (Angabe vom Igus )
// Minimale Periodenzeit = 40us (Handbuch S. 95)

// DIGITALE AUSGÄNGE
// X3.1   Bereit
// X3.2   Aktiv
// X3.3   Referenziert
// X3.4   Alert
// X3.5   Error

// DIGITALER EINGANG
// X2.1   Takt
// X2.2   Richtung
// X2.7   ENA
// X2.8   Endlagenschalter positiv
// X2.9   Endlagenschalter negativ
// X2.10  Fehler quittiert

// ===== Switches ======
#define CCWSwitchX 50 // Endlagenschalter negativ
#define CWSwitchX 52  // Endlagenschater positiv

#define CCWSwitchY 46 // Endlagenschalter negativ
#define CWSwitchY 48  // Endlagenschater positiv

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

// AccelStepper deklarieren
AccelStepper motorX(1, STEP_X_PIN, DIR_X_PIN);
AccelStepper motorY(1, STEP_Y_PIN, DIR_Y_PIN);
AccelStepper motorZ(1, STEP_Z_PIN, DIR_Z_PIN);

// Multistepper deklarieren
MultiStepper multiStepper;

// MM to Steps
int stepMode = 64;
float mmPerStep = float(200 * stepMode) / float(70);  // step/mm
float stepsPermm = float(70) / float(200* stepMode); // mm/step
int middlePointX = 150 * int(mmPerStep);  // steps to Middle X
int middlePointY =  70 * int(mmPerStep); // steps to Middle Y
int middlePointZ =  70 * int(mmPerStep); // steps to Middle Z

float manualSpeed = 25 * stepMode;
int profileSpeed = 100 * stepMode;
int stepmaxSpeed = 20*stepMode;
int accel = 100 * stepMode;

// Homing
bool homingDoneX = false;
bool homingDoneY = true;
bool homingDoneZ = true;
bool profileBool = false;

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

void conn(CommandParameter &parameters){

    Serial.print(F("Connection confirmed and Motors Started!")); // When Connected Return to Python initiating the Motors
    setUpMultistepper();
    startMotorX();
    startMotorY();
    startMotorZ();
    connBool = false;
    delay(100);
   
    
}

void finishProfile(CommandParameter &parameters){
    profileBool = false;
    k[0] = 0;

}

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

void updateMotors (CommandParameter &parameters){
  int int1 = parameters.NextParameterAsInteger();
  stepper_dir[0] = int1;
  int int2 = parameters.NextParameterAsInteger();
  stepper_dir[1] = int2;
  int int3 = parameters.NextParameterAsInteger();
  stepper_dir[2] = int3;
  //Serial.println(int1); 
}

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

void updateMode (CommandParameter &parameters){
  int k1 = parameters.NextParameterAsInteger();
  Serial.print(k1); 
  delay(100);
  k[0] = k1;
  
}

void stopAndpowerOffMotorX() // stop with deacceleration
{
  if (motorXenable == true)
  {
    motorX.disableOutputs();
    motorX.stop();
    
    motorXenable = false;
  }
}

void stopAndpowerOffMotorY() // stop with deacceleration
{
  if (motorYenable == true)
  {
    motorY.disableOutputs();
    motorY.stop();
    
    motorYenable = false;
  }
}

void stopAndpowerOffMotorZ() // stop with deacceleration
{
  if (motorZenable == true)
  {
    motorZ.disableOutputs();
    motorZ.stop();
    
    motorZenable = false;
  }
}

void disconn(CommandParameter &parameters){
  emergencyStop = true;
}

void emergencyStopISR(){
  if (emergencyStop){

    Serial.println(404);

    stopAndpowerOffMotorX();
    stopAndpowerOffMotorY();
    stopAndpowerOffMotorZ();

    k[0] = 0;

    stepper_dir[0] = 0;
    stepper_dir[1] = 0;
    stepper_dir[2] = 0;

  }
  emergencyStop = false;
}


void setup() {
  
  Serial.begin(250000);

  Timer1.initialize(1000);
  Timer1.attachInterrupt(emergencyStopISR);

  SerialCommandHandler.AddCommand(F("RES"), reset_m);
  pinMode(RES_X_PIN, OUTPUT);
  digitalWrite(RES_X_PIN, LOW);

  pinMode (RES_Y_PIN, OUTPUT);
  digitalWrite(RES_Y_PIN, LOW);

  SerialCommandHandler.AddCommand(F("connect"), conn);
  SerialCommandHandler.AddCommand(F("DC"), disconn);
  SerialCommandHandler.AddCommand(F("UM"), updateMotors);
  SerialCommandHandler.AddCommand(F("UK"), updateMode);
  SerialCommandHandler.AddCommand(F("P"), updateProfile);
  SerialCommandHandler.AddCommand(F("PF"), finishProfile);

  
}

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

void plus_motorY(int spd = manualSpeed){
  motorY.setSpeed(spd);
  motorY.move(1*stepMode);
  motorY.runSpeed();
}
void minus_motorY(int spd = manualSpeed){
  motorY.setSpeed(-spd);
  motorY.move(-1*stepMode);
  motorY.runSpeed();
}

void plus_motorZ(int spd = manualSpeed){
  motorZ.setSpeed(spd);
  motorZ.move(1*stepMode);
  motorZ.runSpeed();
}
void minus_motorZ(int spd = manualSpeed){
  motorZ.setSpeed(-spd);
  motorZ.move(-1*stepMode);
  motorZ.runSpeed();
}


void errorMotor(){
  if(digitalRead(X3_5_X_PIN) == HIGH ){
    Serial.print("e1"); 
    motorX.stop();
    motorX.runToPosition();
  }
  if(digitalRead(X3_5_Y_PIN) == HIGH ){
    Serial.print("e2");
    motorY.stop();
    motorY.runToPosition();
  }
  if(digitalRead(X3_5_Z_PIN) == HIGH ){
    Serial.print("e3");
    motorZ.stop();
    motorZ.runToPosition();
  }
  delay(500);

}

void home_mX(){
  if(homingDoneX == true){
    return;
  }
  
  if(digitalRead(X3_5_X_PIN) == LOW && homingDoneX == false){

    minus_motorX(manualSpeed);
      
  }
  else if(digitalRead(X3_5_X_PIN) == HIGH){
    
      Serial.println(1);
      
      homingDoneX = true;
      delay(1000);  
      digitalWrite(RES_X_PIN, HIGH);
      motorX.setCurrentPosition(0);
      delay(100);
      digitalWrite(RES_X_PIN, LOW);
      //motorX.setCurrentPosition(0);
     while(motorX.currentPosition() != middlePointX){
       plus_motorX(manualSpeed);
    }
      Serial.println(4);
      digitalWrite(RES_X_PIN, HIGH);
      motorX.setCurrentPosition(0);
      delay(100);
      digitalWrite(RES_X_PIN, LOW);   

      k[0] = 0;

  }

}

void home_mY(){

  if(homingDoneY == true){
    return;
  }
  if(digitalRead(X3_5_Y_PIN) == LOW && homingDoneY == false){

    minus_motorY(manualSpeed);
      
  }
  else if(digitalRead(X3_5_Y_PIN) == HIGH){
    
      Serial.println(1);
      
      homingDoneY = true;
      delay(1000);  
      digitalWrite(RES_Y_PIN, HIGH);
      motorY.setCurrentPosition(0);
      delay(100);
      digitalWrite(RES_Y_PIN, LOW);
      //motorX.setCurrentPosition(0);
     while(motorY.currentPosition() != middlePointY){
       plus_motorY(manualSpeed);
    }
      Serial.println(3);
      digitalWrite(RES_Y_PIN, HIGH);
      motorY.setCurrentPosition(0);
      delay(100);
      digitalWrite(RES_Y_PIN, LOW);   

      k[0] = 0;

  }

}

void home_mZ(){
  if(homingDoneZ == true){
    return;
  }
  
  if(digitalRead(X3_5_Z_PIN) == LOW && homingDoneZ == false){

    minus_motorZ(manualSpeed);
      
  }
  else if(digitalRead(X3_5_Z_PIN) == HIGH){
    
      Serial.println(1);
      
      homingDoneZ = true;
      delay(1000);  
      digitalWrite(RES_Z_PIN, HIGH);
      motorZ.setCurrentPosition(0);
      delay(100);   
      digitalWrite(RES_Z_PIN, LOW);
      //motorX.setCurrentPosition(0);
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

void setAllSteppers()
{
  if(k[0] == 4){
      homingDoneY = false;
      home_mX();
    }
  else if(k[0] == 3){
      homingDoneY = false;
      home_mY();
    }
  else if(k[0] == 5){
      homingDoneZ = false;
      home_mZ();
  }

  else if(k[0] == 2){ // TO DO: Define PROFILE mode (k = 2)
    //motorX.setSpeed(manual);
    if (profileBool == true){

      int step_dist1 = stepper_profile[0];//*mmPerStep;
      int step_spd1 = stepper_profile[1] * manualSpeed;
      int step_dist2 = stepper_profile[2];//*mmPerStep;
      int step_spd2 = stepper_profile[3] * manualSpeed;

      //float stepdist2 = stepper_distance[0]*mmPerStep;
      if (motorX.currentPosition() == step_dist1 && motorY.currentPosition() == step_dist2){
        Serial.println(1);
        delay(50);
      }
      if (motorX.currentPosition() != step_dist1 && step_spd1 != 0){
        //Serial.println(stepper_distance[0]);
        int prev_dist = motorX.currentPosition();
        if(prev_dist > step_dist1){
          minus_motorX(step_spd1);
        }else{
          plus_motorX(step_spd1);
        }
        //Serial.println(step_spd1);
      }
      if (motorY.currentPosition() != step_dist2  && step_spd2 != 0){
        int prev_dist2 = motorY.currentPosition();
        if(prev_dist2 > step_dist2){
          minus_motorY(step_spd2);
        }else{
          plus_motorY(step_spd2);
        }
      }

    } 
  }else{
    // Get Direction for each Motor
    int dir_x = stepper_dir[0];
    int dir_y = stepper_dir[1];
    int dir_z = stepper_dir[2];
    if (dir_x + dir_y + dir_z == 0){
      motorVal = false;
    }
    //Serial.println(dir_x);
    if (dir_x == 0){
      plus_motorX(0);
      //motorVal = false;
    }
    if (dir_x == 1){  // Motor 1 PLUS 
      plus_motorX(manualSpeed);
      motorVal = true;
      
    }
    if (dir_x == 2){  // Motor 1 MINUS    
      minus_motorX(manualSpeed);
      motorVal = true;
    }

    if (dir_y == 0){
      plus_motorY(0);
    }

    if (dir_y == 1){  
      plus_motorY(manualSpeed);
      motorVal = true;
    }
    if (dir_y == 2){      
      minus_motorY(manualSpeed);
      motorVal = true;
    }

    if (dir_z == 0){
      plus_motorZ(0);
    }

    if (dir_z == 1){  
      plus_motorZ(manualSpeed);
      motorVal = true;
    }
    if (dir_z == 2){      
      minus_motorZ(manualSpeed);
      motorVal = true;
    }
    }
  }

void loop(){
  SerialCommandHandler.Process();
  setAllSteppers();
  sendPos.runCoroutine();
}

