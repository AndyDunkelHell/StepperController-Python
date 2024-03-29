# Class Stepper_Controller_Arduino_v2_5.ThreadedTask(master)

Bases: *Thread*

## `run()`

This function is the main execution loop for the thread. It handles various commands sent to an Arduino board, including connect, home, and profile commands.

- For the connect command, it sends a connect request to the Arduino and updates the GUI with the response.

- For the home command, it sends a command to home the motors and updates the GUI with the status of the homing process.

- For the profile command, it sends a series of commands to the Arduino to execute a predefined profile,

updating the GUI with the status of the profile execution.

It also handles manual commands (*MOVEMENT*) if the board is connected. 

The function uses a **queue** to handle incoming commands and updates a global status variable with the status of the current operation.

    # Main threaded Task
    #   If set_ind is equal to 67 (ASCII for c and always unprobable motor index) we will send the Connect command to Board
    #   If set_ind is equal to 72 (ASCII for h and always unprobable motor index) we will send the HOME Mode command to Board
    #   If set_ind is equal to 80 (ASCII for p and always unprobable motor index) we will send the PROFILE Mode command to Board
    run(self):
        comm = "!UM"

            global set_ind
            global stepperVals
            global SelecStepperVals
            global k
            global glob_status
            global _looping
            global _func
            global home_mot1
            global home_mot2

            global stepMode
            global mmPerStep

            try:
                # The Value must be an Integer
                inty = int(self.val)
            except:
                self.queue.put("UNKNOWN COMMAND : " + self.val)
            else:
                SelecStepperVals = stepperVals[:4]  # see Variable Definition
                if set_ind == 67:  # Connect command
                    arduinoData.write('!connect\r'.encode())
                    # Send "c" To arduino to Stablish connection
                    in_line = arduinoData.readline().decode()
                    if in_line != "":
                        glob_status.config(text= in_line)

                if set_ind == 72:  # Home Command
                    k = self.val
                    _func = True
                    MainGUI.main_ui.disableButtons()
                    changingMode = True
                    while changingMode:  # Repeat and assure command detection
                        k_send = '!UK ' + str(k) + "\r"
                        arduinoData.write(k_send.encode())
                        in_line2 = arduinoData.readline().decode()
                        try:
                            dif = int(in_line2)
                        except:
                            glob_status.config(text = "Performing action please wait. ", fg= "orange")
                        else:
                            if dif == k:  # Ensure the Mode Change has been Acknolegded by the Arduino by comparing the incomming value for k and the one we send
                                glob_status.config(text= "Mode activated: "+str(dif), fg= "orange")
                                print("Mode activated: "+str(dif))
                                changingMode = False
                                break

                    while self.home != True:
                            in_line3 = arduinoData.readline().decode()
                            time.sleep(0.12)
                            try:
                                int_l = int(in_line3)
                                print(in_line3)
                            except:
                                glob_status.config(text = "Homing Motor", fg= "orange")
                            else:
                                if (int_l == 1):
                                    glob_status.config(text= "Bitte fehler Quittieren", fg= "red")
                                elif(int_l == 4):
                                    home_mot1 = True
                                    glob_status.config(text= "Done Homing Motor 1!", fg= "green")
                                    set_ind = 0
                                    self.val = 0
                                    self.home = True
                                    _func = False
                                    MainGUI.main_ui.enaButtons()
                                    time.sleep(0.5)
                                    break
                                elif(int_l == 3):
                                    home_mot2 = True
                                    glob_status.config(text= "Done Homing Motor 2!", fg= "green")
                                    set_ind = 0
                                    self.val = 0
                                    self.home = True
                                    _func = False
                                    MainGUI.main_ui.enaButtons()
                                    time.sleep(0.5)
                                    break


                if set_ind == 80:  # Profile Command

                    k = set_val
                    _func = True
                    j = 0
                    changingMode = True
                    MainGUI.main_ui.disableButtons()
                    while changingMode:  # Repeat and assure command detection
                        k_send = '!UK ' + str(k) + "\r"
                        arduinoData.write(k_send.encode())
                        in_line2 = arduinoData.readline().decode()
                        try:
                            dif = int(in_line2)
                        except:
                            glob_status.config(text = "Performing action please wait. ", fg= "orange")

                        else:
                            if dif == k:  # Ensure the Mode Change has been Acknolegded by the Arduino by comparing the incomming value for k and the one we send
                                glob_status.config(text= "Mode activated: "+str(dif), fg= "orange")
                                changingMode = False
                                break
                    while j < len(set_profile):
                        i = 1
                        if j == 0 :
                            profile_iter = set_profile[0][0].split(",")
                            j += 1
                            continue
                        while i <= int(profile_iter[j-1]):
                            for x in set_profile[j]:  # Send data from profile File line by line to the arduino
                                time.sleep(0.012)
                                l_x = x.split(",")
                                self.profile = False

                                x1 = int(l_x[0])*mmPerStep
                                x2 = l_x[1]
                                x3 = int(l_x[2])*mmPerStep
                                x4 = l_x[3]

                                p_send = '!P ' + str(x1) + ' ' + str(x2) + ' ' + str(x3) + ' ' + str(x4) + "\r"
                                arduinoData.write(p_send.encode())
                                while self.profile != True:  # Loop until we Receive confirmation for each line x
                                    in_line2 = arduinoData.readline().decode()
                                    try:
                                        int_l = int(in_line2)

                                    except:
                                        stat_text = 'Profile ' + str(j) + ' Max: ' + profile_iter[j-1] + ' Iteration number: ' + str(i) + ' ' + p_send
                                        glob_status.config(text = stat_text, fg= "orange")
                                    else:
                                        #CONFIRM
                                        if (int_l == 1):  # If 1 is received from the arduino in this case it means that the Motor has reached the desired Position
                                            in_line2 = ""
                                            self.profile = True
                                            continue
                    i += 1
                    j += 1
                    p_fertig = "!PF\r"
                    arduinoData.write(p_fertig.encode())
                    glob_status.config(text = "Profile finished", fg= "green")
                    MainGUI.main_ui.enaButtons()
                    _func = False
                    set_ind = 0
                    self.val = 0

                if (conn_bool == True):  # Only send manual commands if the board is connected
                        try:
                            SelecStepperVals[set_ind] = self.val
                            stepperVals[set_ind] = self.val
                            # Add all desired values to the starting command it should go to the arduino as Follows:
                            # !UM 1 1 1 0\r (Example)
                        except:
                            return
                        for x in SelecStepperVals:
                            comm +=  " " + str(int(x))
                            
                        self.queue.put(comm)
                        comm = comm + "\r"
                        arduinoData.write(comm.encode())
