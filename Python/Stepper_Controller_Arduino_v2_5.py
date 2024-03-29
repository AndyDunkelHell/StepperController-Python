# Import required Packages-----> IMPORTANT Be sure to install them in the correct enviroment for the code to use them
# Recommended: Install Anaconda and then install the packages in the anaconda prompt.
# Make sure that your interpreter is the correct anaconca enviroment (e.g base or your own enviroment)

import serial
import time
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import queue
import threading
import serial.tools.list_ports
import numpy as np
from collections import deque
import os
import ctypes
import configuration
from PIL import Image, ImageTk, ImageSequence
from plotting import streamlit_go_visulize, simulate_weg, store_as_gif, delete_all_figures
from manager import get_alpha, get_beta, init_position, move_to_alpha, move_to_beta
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


myappid = 'UKA.FreeMove.control.version2.5'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
##VARIABLES##
set_ind = 0  # Motor index to be set
set_val = 0  # Motor value to be set

stepperVals = [0.0, 0.0, 0.0, 0.0]  # List to store all values
# List to store the selected Stepper Values (If more than 4 steppers are to be used)
SelecStepperVals = []
# List of all ports available
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
arduino_port = []  # List for selected Arduino Port
conn_bool = False  # Bool for Connection Status
act = 0  # Int for the ammount of activated Motors
k = 0  # Int for mode selection

## Profile mode Vars ##
loaded = False

stepp_vals = []

_looping = False  # Bool for Looping
_func = False
send1 = False  # Bool ENA send to Motor 1
send2 = False  # Bool ENA send to Motor 2
send3 = False  # Bool ENA send to Motor 2

home_mot1 = True  # Home iterable
home_mot2 = True  # Home iterable
home_mot3 = True  # Home iterable

rec_bool = False

stepMode = 64;
mmPerStep = 200 * stepMode // 70;

# Connect Arduino Board with the User inputs, if Connection Fails the app closes and User must start again
def connectBoard(uport="COM3", ubaudrate=250000):
    """
    
    Establishes a serial connection with an Arduino board using the specified port and baudrate. 
    If the connection is successful, it starts a new thread to continuously check the presence of the board. 
    If the connection fails, it raises a ValueError and destroys the main GUI.
    
    Args:
        uport (str, optional): The port to connect to. Defaults to "COM3".
        ubaudrate (int, optional): The baudrate for the connection. Defaults to 250000.
    
    Raises:
        ValueError: If the connection to the Arduino board fails.
    
    Global Variables:
        arduinoData: Stores the serial connection to the Arduino board.
        conn_bool: Boolean value indicating the status of the connection.
        myports: List of available ports.
        arduino_port: The port to which the Arduino board is connected.
    
    """
    global arduinoData
    global conn_bool
    global myports
    global arduino_port
    try:
        #Start serial connection to arduino with the user inputed Ports and baudrate. Read and Send timeout 0.05 seconds
        arduinoData = serial.Serial(uport, baudrate=ubaudrate, timeout=0.05)

    except:
        #if connection fails close the GUI app
        print("CONNECTION TO ARDUINO BOARD FAILED")
        raise ValueError("Wrong Port")
        #GUI.Start()
        MainGUI.root.destroy()
    else:
        #If no error excecute:
        conn_bool = True
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        print(myports)
        arduino_port = [port for port in myports if uport in port][0]
        #Start thread to check the prescense of the board, in case the arduino gets Disconnected
        port_controller = threading.Thread(
            target=check_presence, args=(arduino_port, 0.1,))
        port_controller.daemon = True
        port_controller.start()

#Check arduino presence while app is running

def check_presence(correct_port, interval=0.1):
    """
    
    Continuously checks the presence of the Arduino board at the specified interval. 
    If the Arduino board is disconnected, it updates the global connection status and breaks the loop. 
    Also checks for errors in Motor 1 and Motor 2 and updates the global status accordingly.
    
    Args:
        correct_port (str): The port to which the Arduino board is connected.
        interval (float, optional): The time interval at which to check the presence of the board. Defaults to 0.1.
    
    Global Variables:
        conn_bool: Boolean value indicating the status of the connection.
        glob_status: The global status of the application.
        _looping: Boolean value indicating whether the application is looping.
        _func: Boolean value indicating whether a function is being executed.
    
    """
    global conn_bool
    global glob_status
    global _looping
    global _func
    while conn_bool == True:
        if (_looping != True and _func == False):

            err_line = arduinoData.readline().decode()

            if (err_line == "e1"):
                glob_status.config(
                    text="Error in Motor 1 please Reset", fg="red")
            if (err_line == "e2"):
                glob_status.config(
                    text="Error in Motor 2 please Reset", fg="red")

        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        if arduino_port not in myports:
            print("Arduino has been disconnected!")
            glob_status.config(text="Arduino has been disconnected!", fg="red")
            conn_bool = False
            break
        time.sleep(interval)


def on_closing():
    """
    
    Handles the event of closing the application. 
    Prompts the user for confirmation before quitting. 
    If the user confirms, it sends a '!DC\r' command to the Arduino board and quits the application.
    
    Global Variables:
        arduinoData: The serial connection to the Arduino board.
        MainGUI.root: The root window of the main GUI.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        comm = '!DC\r'
        try:
            arduinoData.write(comm.encode())
        except:
            pass

        MainGUI.root.quit()


class GUI:
    def __init__(self, master):
        """
    Initializes the main GUI for the application. 
    Creates frames for motor positions, motor controls, record controls, and connection controls. 
    Defines buttons for various operations such as moving motors, recording, starting simulation, resetting, and stopping. 
    Also sets up a menu bar with options for loading profiles, adding motors, and viewing help information.
    
    Global Variables:
        arduinoData: The serial connection to the Arduino board.
        conn_bool: Boolean value indicating the status of the connection.
        glob_status: The global status of the application.
    """
        self.mot_i = 2  # Motor index

        # Frame Definitions
        self.master = master

        # Main frames
        self.frame1 = LabelFrame(
            self.master, text='Motor Positions', padx=5, pady=52, bg='black', fg='white')
        self.frame2 = LabelFrame(self.master, text='Motor Controls',  padx=1, pady=1)
        # Motor Frames
        self.motor1 = LabelFrame(self.frame2, text='Motor 1', padx=1,  pady=1)
        self.motor2 = LabelFrame(self.frame2, text='Motor 2', padx=1,  pady=1)
        # Record Frame
        self.rec = LabelFrame(
            self.master, text='Record Controls', padx=1,  pady=1)
        # Connection Frame
        self.control_panel = LabelFrame(
            master, text='Connection Controls', padx=1, pady=1)

        global arduinoData
        global conn_bool

        ## MENU BAR ##
        self.menu_bar = Menu(self.master)
        master.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label= "File", menu=self.file_menu)
        self.file_menu.add_command(label="Load Profiles", command=self.loadProfiles)

        self.edit_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label= "Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Add Motor", command=self.addMotor)

        self.help_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label= "Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.aboutWindow)

        #Grid Definitions for the main Frames
        self.frame1.grid(row=0, column=0, columnspan=1, sticky=N+S+W+E)
        self.frame2.grid(row=0, column=1, columnspan=3, sticky=N+S+W+E)

        self.motor1.grid(row=1, column=0, columnspan=2, pady=10, padx=1)
        self.motor2.grid(row=1, column=2, columnspan=1, pady=10, padx=1)

        self.rec.grid(row=1, column=0, columnspan=4, sticky=W+E)

        self.control_panel.grid(row=2, column=0, columnspan=4,  sticky=W+E)

        ###GUI DEFINITIONS###

        #GUI TITLE
        master.title('Stepper Controller FreeMove v 2.5 ARDUINO')

        ## Buttons ##

        # Define Buttons for Recording
        # Start Recording Button
        self.rec_button = Button(
            self.rec, text='Record', fg='red', padx=40, command=self.f_rec, state="disable")
        # Stop Recording Button
        self.stop_rec_button = Button(
            self.rec, text='Stop Recording', padx=40, command=self.stop_rec, state="disable")

        # Define Buttons for Weg Simulation
        self.sim_window = Button(
            self.rec, text='Start Simulation', fg='red', padx=40, command=self.sim_open)

        # Define Variables for Direction of the Motors
        # Sending to Arduino for each Motor 1 is for PLUS and 2 is For MINUS
        self.var1 = IntVar()
        self.var1.set(1)
        self.var2 = IntVar()
        self.var2.set(1)

        ## Motor 1 Flexion/Extension (MotorX in arduino)##
        # Define Buttons for Moving the Motor1
        self.m1_move = Button(self.motor1, text='Move', fg='red',
                              padx=40, command=self.move1, state="disable")

        # Here we define the Radio Buttons to toggle the Direction of the Motor1
        # Value is the Value to be sent to Arduino
        self.m1_plus = Radiobutton(
            self.motor1, text='Flexion', variable=self.var1, value=1, state="disable")
        self.m1_minus = Radiobutton(
            self.motor1, text='Extension', variable=self.var1, value=2, state="disable")
        
        # Home Motor 1 Button
        self.m1_home = Button(self.motor1, text='Home',
                              padx=40, command=self.home_m1, state="disable")
        
        # Reset/Stop Motor 1 Button 
        self.m1_reset = Button(self.motor1, text='Reset/Stop',
                               padx=40, command=self.reset_m1, state="disable")

        ##  Motor 2 Medial/Lateral (MotorY in arduino)##
        # Define Buttons for Moving the Motor1
        self.m2_move = Button(self.motor2, text='Move', fg='red',
                              padx=40, command=self.move2, state="disable")

        # Here we define the Radio Buttons to toggle the Direction of the Motor2
        self.m2_plus = Radiobutton(
            self.motor2, text='Medial', variable=self.var2, value=1, state="disable")
        self.m2_minus = Radiobutton(
            self.motor2, text='Lateral', variable=self.var2, value=2, state="disable")
        # Home Motor 2 Button
        self.m2_home = Button(self.motor2, text='Home',
                              padx=40, command=self.home_m2, state="disable")

        # Reset/Stop Motor 2 Button
        self.m2_reset = Button(self.motor2, text='Reset/Stop',
                               padx=40, command=self.reset_m2, state="disable")

        # Connection BUTTONS
        
        self.conn_button = Button(self.control_panel, command=self.conn)
        self.conn_button.configure(
            text="Connect Arduino",
            padx=50
        )
        self.conn_button.grid(row=0, column=0, padx=2)

        # Profile BUTTONS
        self.run_profile = Button(self.control_panel, command=self.run_profile)
        self.run_profile.configure(
            text="Run Profile",
            padx=50
        )

        # Emergency Stop BUTTON
        self.e_stop = Button(self.control_panel, command=self.emergencyStop)
        self.e_stop.configure(
            text="STOP",
            padx=50
        )


        ## ALL LABELS ##
        
        # Define Labels for the Motor Positions
        self.m1 = Label(self.frame1, text='Flexion/Extension : ',
                        bg='black', fg='white')
        self.m2 = Label(self.frame1, text='Medial/Lateral : ',
                        bg='black', fg='white')

        # Define Labels for the Motor Values
        self.val_m1 = Label(self.frame1, text='0', bg='black', fg='yellow')
        self.val_m2 = Label(self.frame1, text='0', bg='black', fg='yellow')
        
        # Define Label to illustrate the selected Profile
        self.selec_profile = Label(
            self.control_panel, text='No Profile Selected', bg='white', fg='black')


        ## GUI GRIDS ##
        # Here we define the grid prositions of all the buttons and labels, defined above

        #BUTTONS

        self.m1_move.grid(row=1, column=1, columnspan=2, padx=1, pady=5)
        self.m2_move.grid(row=1, column=1, columnspan=2, padx=1, pady=5)

        self.rec_button.grid(row=0, column=1, padx=4, pady=1)
        self.stop_rec_button.grid(row=0, column=2, padx=4)
        self.sim_window.grid(row=0, column=3, padx=4, pady=1)

        self.m1_home.grid(row=2, column=1, columnspan=2, padx=1, pady=5)
        self.m2_home.grid(row=2, column=1, columnspan=2, padx=1, pady=5)

        self.m1_reset.grid(row=3, column=1, columnspan=2, padx=1, pady=5)
        self.m2_reset.grid(row=3, column=1, columnspan=2, padx=1, pady=5)

        self.m1_plus.grid(row=4, column=1, padx=1, pady=5)
        self.m1_minus.grid(row=4, column=2, padx=1, pady=5)

        self.m2_plus.grid(row=4, column=1, padx=1, pady=5)
        self.m2_minus.grid(row=4, column=2, padx=1, pady=5)
        
        self.selec_profile.grid(row=0, column=4, padx=10)
        self.run_profile.grid(row=0, column=1, padx=2)
        self.e_stop.grid(row=0, column=3, padx=2)

        #LABELS
        self.m1.grid(row=0, column=0)
        self.m2.grid(row=1, column=0)

        self.val_m1.grid(row=0, column=1)
        self.val_m2.grid(row=1, column=1)

        ## GUI STATUS BA ##
        self.status = Label(
            master, bd=1, relief=SUNKEN, anchor=E, text='Status')
        self.status.grid(row=4, column=0, columnspan=4, sticky=W+E)

        global glob_status
        glob_status = self.status
        self.loop()
        self.profile_l = []
        self.l0 = []
        self.l1 = []
        self.l2 = []
        self.l3 = []

    ###FUNCTIONS###

    def emergencyStop(self):
            global send1
            global send2
            global send3
            comm = '!DC\r'
            arduinoData.write(comm.encode())
            if send1:
                self.move1()
            if send2:
                self.move2()
            if send3:
                self.move3()

    def aboutWindow(self):
        """
    
    This method creates a new Toplevel window that displays information about the application. 
    The window contains a label with the application name, version, reference to the GitHub page for more information, 
    the creator's name, and the intended user group.
    
    """
        self.about = Toplevel()
        self.about.title("About Window")
        self.about_info = Label(self.about, text='Stepper Controller 2.5\n \n For more information refer to the GitHub page\n\nCreated By Andres Gonzalez (AndyDunkelHell)\nfor the Klinik der Orthopädie UKA 2023')
        self.about_info.pack()

    ## PROFILE FUNCTIONS ##
    def add_profiles(self):
        """
    This method creates a new frame in the profile menu window, in order to load a profiles, 
    after being loaded it adds its path to the profile path list. 
    It also creates a label with the profile path and an entry field for profile iterations 
    in the new frame.
    """
        profiles_frame = Frame(self.pMenu_profiles, borderwidth=0)
        profiles_frame.pack(pady=5)

        profile_path = self.load_profile()
        self.profile_path_list.append(profile_path)

        self.loaded_profile = Label(
            profiles_frame, text=profile_path)
        self.loaded_profile.configure(
            padx=10
        )
        self.loaded_profile.pack(in_=profiles_frame, side=LEFT)

        self.profile_it = Entry(profiles_frame, width=15)
        self.profile_it.insert(0, "Profile iterations")
        self.profile_it.pack(in_=profiles_frame, side=RIGHT, padx=5)

    def finish_profiles(self):
        """
        This method retrieves the iterations value from the profile menu, appends it to the profile list,
        and opens each profile in the profile path list. It updates the selected profile text with the profile names 
        and the status text with the number of profiles loaded. It also sets the global variable 'loaded' to True.
        """
        iterations_val = ""
        names = []
        global loaded
        for prof in self.pMenu_profiles.winfo_children():
            for it in prof.winfo_children():
                try:
                    
                    iterations_val += it.get() + ","
                except :
                    pass
                else:
                    try:
                        int_profile_i = int(it.get()) # Test if the values can be transformed to int, in order to filter not valid inputs
                    except ValueError as e:
                        self.status.config(text=f"Error: {e}", fg="red")
                        messagebox.showwarning("Invalid Input", "Not valid input in the Profile iterables, please provide a proper number of repetitions")
                        return

        self.profile_l.append([iterations_val[:-1]])

        for path in self.profile_path_list:
             profile_name = os.path.split(path)[1]
             names.append(profile_name)
             open_profile = open(path, "r")
             self.profile_l.append(open_profile.readlines())

        self.selec_profile.config(text=names)
        self.status.config(text='Profile lengths: ' +
                            str(len(self.profile_l)), fg="green")
        loaded = True

    def load_profile(self):
        """
    This method opens a file dialog for the user to select a profile. 
    It returns the name of the selected file. If no file is selected, 
    it updates the status text to 'No Data Selected'.
    """
        global loaded
        arr = np.zeros(4)

        ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
        data = filedialog.askopenfile(initialdir=ROOT_PATH)
        names = []
        try:
            name = data.name
        except:
            self.status.config(text='No Data Selected')
        else:
            return name

    def loadProfiles(self):
        """
    This method creates a new Toplevel window for loading profiles. 
    The window contains two label frames for adding profiles and selecting profiles respectively. 
    It also contains two buttons for adding a profile and loading all profiles. It initializes the profile path list and calls the 
    add_profiles method.
    """
        self.pMenu = Toplevel()
        self.pMenu.title("Load profiles window")

        pMenu_controls = LabelFrame(self.pMenu,text='Add profiles')
        pMenu_controls.grid(row=1, column= 1, columnspan=3, pady=3)

        self.pMenu_profiles = LabelFrame(self.pMenu,text='Select profiles')
        self.pMenu_profiles.grid(row=2, column= 1, columnspan=3, pady=3)

        self.add_profile = Button(
            pMenu_controls, command=self.add_profiles)
        self.add_profile.configure(
            text="Add profile",
            padx=50
        )
        self.add_profile.pack(in_=pMenu_controls, side=LEFT)

        self.finish_profile = Button(
            pMenu_controls, command=self.finish_profiles)
        self.finish_profile.configure(
            text="Load all profiles",
            padx=50
        )
        self.finish_profile.pack(in_=pMenu_controls, side=RIGHT, padx=5, pady=3)
        self.profile_path_list = []
        self.add_profiles()

    def run_profile(self):
        """
    This method runs the loaded profile if the motors are homed. 
    If the motors are not homed, it updates the status text to 'Please Home motors'. 
    If no profile is loaded, it does nothing.
    """
        if loaded == True:
            if home_mot1 == False or home_mot2 == False:
                glob_status.config(text="Please Home motors", fg="red")
                return
            self.update_thread(80, 2, self.profile_l)
        else:
            return


    ## ADD MOTOR FUNCTION ##
    def addMotor(self):
        """
    This method adds a new motor to the application. It increments the motor 
    index and if the maximum number of motors is reached, it disables the add motor option in the edit menu. 

    It creates a new label frame for the motor with move, home, and reset/stop buttons, and anterior and posterior radio buttons. 
    It also displays the anterior/posterior value. If the user cancels the operation, no motor is added.
    """
        if messagebox.askokcancel("Add motor", "Please refer to the Instructions on how to properly add a motor. You have to edit the src code!"):
            self.mot_i += 1
            if self.mot_i == 3:

                self.status.config(text="Motor 3 added! Maximum motor number reached" )
                self.edit_menu.entryconfig(1, state=DISABLED)
                ##
                self.motor3 = LabelFrame(self.frame2, text='Motor 3', padx=1,  pady=1)
                self.motor3.grid(row=1, column=3, columnspan=1, pady=10, padx=1)
                self.var3 = IntVar()
                self.var3.set(1)
                self.m3_move = Button(self.motor3, text='Move', fg='red',padx=40, command=self.move3, state="disable")
                self.m3_plus = Radiobutton(self.motor3, text='Anterior', variable = self.var3, value= 1, state= "disable")
                self.m3_minus = Radiobutton(self.motor3, text= 'Posterior', variable = self.var3, value= 2, state= "disable")
                self.m3_home = Button(self.motor3, text='Home', padx=40, command=self.home_m3, state="disable")
                self.m3_reset = Button(self.motor3, text='Reset/Stop', padx=40, command=self.reset_m3, state="disable")
                self.m3 = Label(self.frame1, text='Anterio/Posterio : ', bg='black', fg='white')
                self.val_m3 = Label(self.frame1, text= '0', bg='black', fg='yellow')
                global glob_val3
                glob_val3 = self.val_m3
                self.m3_move.grid(row=1, column=1, columnspan=2, padx=1, pady=5)
                self.m3_home.grid(row=2, column=1, columnspan=2, padx=1, pady=5)
                self.m3_reset.grid(row=3, column=1, columnspan=2, padx=1, pady=5)
                self.m3_plus.grid(row=4, column = 1, padx=1,pady=5)
                self.m3_minus.grid(row=4, column = 2, padx=1,pady=5)
                self.m3.grid(row=2, column = 0)
                self.val_m3.grid(row=2, column = 1)

    ## SIMULATION FUNCTIONS ##
    def simWeg(self):
        """
    This method simulates the movement of the hand based on the input parameters for alpha (flexion/extension), 
    beta (radial/ulnar), theta (steps for angle calculation), and speed (angular speed). 

    It updates the configuration with the input values, deletes all figures previous figures (previously generated), simulates the movement, 
    and stores the result as a GIF. 

    If the input is invalid, it updates the status text to 'Wrong Input, try again'.
    
    simulate_weg(), delete_all_figures() and store_as_gif() are called from the plotting.py file
    
    The input values are retrieved from the entry fields in the simulation window and are updated in the configuration file.

    If the simulation is successful, it updates the status text to 'Sim Done! Loading GIF Please Wait', opens a new window, and displays the GIF.

    """
        try:
            int_alpha_min = int(self.e_alpha_min.get())
            int_alpha_max = int(self.e_alpha_max.get())

            int_beta_min = int(self.e_beta_min.get())
            int_beta_max = int(self.e_beta_max.get())

            int_theta = int(self.e_theta.get())
            int_speed = int(self.e_speed.get())

            # Flexion/Extension    
            configuration.ALPHA_FE_MIN = int_alpha_min
            configuration.ALPHA_FE_MAX = int_alpha_max

            # Radial/Ulnar
            configuration.BETA_RU_MIN = int_beta_min
            configuration.BETA_RU_MAX = int_beta_max
        
            configuration.DELTA_THETA = int_theta  # Steps for Angle calculation with the Range
            configuration.SPEED_PER_THETA = int_speed  # Angular Speed

            delete_all_figures()
            simulate_weg(self.e_profile.get()) 
            store_as_gif()
        except:
            self.status.config(text="Wrong Input, try again", fg="red")
        else:
            self.status.config(text="Sim Done! Loading GIF Please Wait", fg="green")
            self.gif_show = Toplevel()
            self.gif_show.title("GIF Window")
            self.frameCnt = 72
            self.gif = Image.open('mygif.gif')
            self.gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(self.gif)]
            self.gif_label = Label(self.gif_show)
            self.gif_label.pack()
            self.master.after(0, self.update_gif, 0)

    def update_gif(self, ind):
        """
    This method updates the GIF displayed in the GIF window. 
    It cycles through the frames of the GIF at a rate of one frame per 100 milliseconds. 
    When it reaches the last frame, it loops back to the first frame.
    """
        frame = self.gif_frames[ind]
        ind += 1
        if ind == self.frameCnt:
            ind = 0
        self.gif_label.configure(image=frame)
        self.master.after(100, self.update_gif, ind)

    def sim_open(self):
        """
    This method creates a new Toplevel window for running simulations. 

    The window contains a label frame for controls with entry fields for alpha min and max, beta min and max, theta, speed, and profile name.
        these values are used to simulate the movement of the hand in the simWeg Method. 

    It also contains a button for starting the simulation.

    Additionally, it has four sliders for adjusting the view of flexion/extension (FE), radial/ulnar (RU), alpha (FE), and beta (RU).
    
    Using the Sliders a live Plot is generated it updates the live Plot on display with the slider values.

    The method initializes the current values for the sliders and calls the sim_update method.
    """
        self.sim = Toplevel()
        self.sim.title("Simulation Window")

        sim_controls = LabelFrame(self.sim,text='Controls')
        sim_controls.grid(row=1, column= 1, columnspan=3, pady=10)

        ## Alpha
        alphamin_label = Label(sim_controls, text="Alpha MIN and MAX").grid( row=0, column=0, pady=0, padx = 4)
        self.e_alpha_min = Entry(sim_controls, width=10)
        self.e_alpha_min.insert(0, "Min:-30")
        self.e_alpha_min.grid(row=1, column= 0)

        self.e_alpha_max = Entry(sim_controls, width=10)
        self.e_alpha_max.insert(0, "Max: 45")
        self.e_alpha_max.grid(row=1, column= 1)

        ## Beta
        betamin_label = Label(sim_controls, text="Beta MIN and MAX").grid(sticky="W", row=2, column=0, pady=0, padx = 4)
        self.e_beta_min = Entry(sim_controls, width=10)
        self.e_beta_min.insert(0, "Min:-10")
        self.e_beta_min.grid(row=3, column= 0)

        self.e_beta_max = Entry(sim_controls, width=10)
        self.e_beta_max.insert(0, "Max: 35")
        self.e_beta_max.grid(row=3, column= 1)

        ## Theta
        theta_label = Label(sim_controls, text="Theta").grid(sticky="W", row=4, column=0, pady=0, padx = 4)
        self.e_theta = Entry(sim_controls, width=10)
        self.e_theta.insert(0, "5")
        self.e_theta.grid(row=5, column= 0, columnspan=3)

        ## Speed
        speed_label = Label(sim_controls, text="Speed").grid(sticky="W", row=6, column=0, pady=0, padx = 4)
        self.e_speed = Entry(sim_controls, width=10)
        self.e_speed.insert(0, "320")
        self.e_speed.grid(row=7, column= 0, columnspan=3)


        ## Profile Name
        profile_label = Label(sim_controls, text="Profile Name").grid(sticky="W", row=8, column=0, pady=0, padx = 4)
        self.e_profile = Entry(sim_controls, width=10)
        self.e_profile.insert(0, "profile1")
        self.e_profile.grid(row=9, column= 0, columnspan=3, sticky="W, E", pady=10)

        ##Weg Sim BUTTONS##
        self.sim_weg = Button(sim_controls, command=self.simWeg)
        self.sim_weg.configure(
            text="Simulate Weg",
            padx=4
        )
        self.sim_weg.grid(row=10, columnspan=3,column=0, padx=2)


        self.current_val1 = DoubleVar()
        self.current_val2 = DoubleVar()
        self.current_val3 = DoubleVar()
        self.current_val4 = DoubleVar()



        viewFE_label = Label(sim_controls, text="view - FE").grid(sticky="W", row=11, column=0, pady=0, padx = 4)
        slider1 = Scale(sim_controls, from_= -45, to= 45 , command=self.sim_update, variable= self.current_val1, repeatdelay=500, orient="horizontal")
        slider1.grid(row=12,column=0, columnspan=3)

        viewRU_label = Label(sim_controls, text="view - RU").grid(sticky="W", row=13, column=0, pady=0, padx = 4)
        slider2 = Scale(sim_controls, from_= -45, to= 45, command=self.sim_update, variable= self.current_val2, repeatdelay=500, orient="horizontal")
        slider2.grid(row=14,column=0, columnspan=3)

        alpha_label = Label(sim_controls, text="Alpha - FE").grid(sticky="W", row=15, column=0, pady=0, padx = 4)
        slider3 = Scale(sim_controls, from_= -30, to= 45 , command=self.sim_update, variable= self.current_val3, repeatdelay=500, orient="horizontal")
        slider3.grid(row=16,column=0, columnspan=3)

        beta_label = Label(sim_controls, text="Beta - RU").grid(sticky="W", row=17, column=0, pady=0, padx = 4)
        slider4 = Scale(sim_controls, from_= -10, to= 35 , command=self.sim_update, variable= self.current_val4, repeatdelay=500, orient="horizontal")
        slider4.grid(row=18,column=0, columnspan=3)

        self.sim_update()

    def sim_update(self, var = 0):
        """
    This method updates the simulation based on the current values of the sliders. 
    It initializes the hand and motor positions, moves the hand to the specified alpha (flexion/extension) and beta (radial/ulnar) positions, 
    and visualizes the hand and motor positions. 
    It adjusts the view of the visualization based on the view sliders and displays the visualization in the simulation window.

    It also closes previous figures (to avoid memory problems)  

    """
        hand, motor_y_fe, motor_x_ru = init_position()

        # Move the hand to the fe-position specified by the 'alpha' angle and adjust the motors accordingly.
        move_to_alpha(self.current_val3.get(), hand, motor_y_fe, motor_x_ru)

        # Move the hand to the ru-position specified by the 'beta' angle and adjust the motors accordingly.
        move_to_beta(self.current_val4.get(), hand, motor_x_ru)

        fig, ax = streamlit_go_visulize(hand, motor_y_fe, motor_x_ru)

        canvas = FigureCanvasTkAgg(fig, self.sim)
        ax.view_init(self.current_val1.get(), self.current_val2.get())

        canvas.get_tk_widget().grid(row=1,column=0)
        plt.close(fig)

        return

    ## RECORDING FUNCTIONS ##
    def stop_rec(self):
        """
    This method stops the recording of stepper values. 
    If recording is in progress, it sets the recording flag to False, disables the stop recording button, 
    and changes the color of the record button to red. It then opens a file dialog for the user to save the recorded stepper values as a CSV file. 
    If the user cancels the save operation, it does nothing.
    """
        global rec_bool
        global stepp_vals

        if rec_bool == True:
            rec_bool = False
            self.stop_rec_button.configure(state="disable")
            self.rec_button.config(fg='red')
            outFile = filedialog.asksaveasfile(
                mode='a', defaultextension=".csv")
            if outFile == None:
                return
            for l in stepp_vals:
                outFile.write(l + "\r")
            stepp_vals = []
            outFile.close()

    
    def f_rec(self, r_line=""):
        """
    This method starts the recording of stepper values. 
    If recording is not in progress, it sets the recording flag to True, enables the stop recording button, 
    and changes the color of the record button to green.
    """
        global rec_bool

        if rec_bool != True:
            rec_bool = True
            self.stop_rec_button.configure(state="active")
            self.rec_button.config(fg='green')

    ## HOME FUNCTIONS ##
    
    def home_m1(self):
        """
    This method initiates the homing process for Motor 1. 
    It updates the status text to 'Homing Motor 1' and calls the update_thread method with specific parameters for Motor 1.
    """
        self.status.config(text="Homing Motor 1")
        self.update_thread(72, 4)
        return

    def home_m2(self):
        """
    This method initiates the homing process for Motor 2. 
    It updates the status text to 'Homing Motor 2' and calls the update_thread method with specific parameters for Motor 2.
    """
        self.status.config(text="Homing Motor 2")
        self.update_thread(72, 3)
        return

    def home_m3(self):
        """
    This method initiates the homing process for Motor 3. 
    It updates the status text to 'Homing Motor 3' and calls the update_thread method with specific parameters for Motor 3.
    """
        self.status.config(text="Homing Motor 3")
        self.update_thread(72, 5)
        return

    ## RESET MOTORS FUNCTIONS ##

    def reset_m1(self):
        """
    This method resets Motor 1. 
    It updates the status text to 'Reset Motor 1' and sends a reset command to Motor 1 through the Arduino.

    These methods do not call the Update Thread method because 
    the reset command is better sent directly to the Arduino without going through the queue.
    """
        self.status.config(text="Reset Motor 1")
        arduinoData.write("!RES 1\r".encode())

    def reset_m2(self):
        """
    This method resets Motor 2. 
    It updates the status text to 'Reset Motor 2' and sends a reset command to Motor 2 through the Arduino.
    """
        self.status.config(text="Reset Motor 2")
        arduinoData.write("!RES 2\r".encode())

    def reset_m3(self):
        """
    This method resets Motor 3.
    It updates the status text to 'Reset Motor 3' and sends a reset command to Motor 3 through the Arduino.
    """
        self.status.config(text="Reset Motor 3")
        arduinoData.write("!RES 3\r".encode())

    ## LOOPING ##

    def loop(self):
        """
    This method continuously reads commands from the Arduino.
    If an error occurs in Motor 1, Motor 2 or Motor 3, it updates the status text to indicate the error \
        and calls the move method for the respective motor. 

    If recording is in progress, it appends the received stepper values to the stepper values list.

    It also updates the displayed stepper values for the motors. 

    The method repeats every 12 milliseconds.
    """

        global stepp_vals
        global rec_bool
        global stepMode
        global mmPerStep
        dt = datetime.now()
        if _looping:
            in_line = arduinoData.readline().decode()

            if (in_line != ""):
                if (in_line == "e1"):
                    glob_status.config(
                        text="Error in Motor 1 please Reset", fg="red")
                    self.move1()
                elif(in_line == "e2"):
                    glob_status.config(
                        text="Error in Motor 2 please Reset", fg="red")
                    self.move2()
                elif(in_line == "e3"):
                    glob_status.config(
                    text="Error in Motor 2 please Reset", fg="red")
                    self.move3()
                else:
                    if rec_bool == True:
                        stepp_vals.append(
                            f"{dt.second},{dt.microsecond};{in_line}")
                    l_line = in_line.split(";")
                    if "" not in l_line and len(l_line) >= 2:
                        self.val_m1.config(text=int(l_line[0])//mmPerStep)
                        self.val_m2.config(text=int(l_line[1])//mmPerStep)
                        if self.mot_i == 3:
                            self.val_m3.config(text=int(l_line[2])//mmPerStep)

        self.master.after(12, self.loop)

    ## Enables Motor 1 movement (Mirrored for the other motors just changing the Indexes) ##

    def move1(self):
        """
    This method controls the movement of Motor 1. 
    If Motor 1 is not homed, it updates the status text to 'Please Home motor 1'. 
    If Motor 1 is already moving, it stops the movement, changes the color of the move button to red, 
    and calls the update_thread method with specific parameters to stop the movement. 
    If Motor 1 is not moving, it starts the movement, changes the color of the move button to green, and calls the update_thread method
    with specific parameters to start the movement. It can send either

        -  0 to Stop the movement
        -  1 to move forward
        -  2 to move backwards

    """
        global _looping
        global act
        global send1
        global home_mot1

        if home_mot1 == False:
            glob_status.config(text="Please Home motor 1", fg="red")
            return

        # If already sending: STOP sending and movement
        if send1 == True:
            # Set letter color in the button to red
            self.m1_move.config(fg='red')
            self.update_thread(0, 0)
            act -= 1
            send1 = False
            if(act == 0):
                _looping = False
        else:
            # If not sending: START sending and movement
            send1 = True
            _looping = True
            self.update_thread(0, self.var1.get())
            act += 1
            # Set letter color in the button to green
            self.m1_move.config(fg='green')

    ## Enables Motor 2 movement
    
    def move2(self):
        """
    This method controls the movement of Motor 2. 
    If Motor 2 is not homed, it updates the status text to 'Please Home motor 2'. 
    If Motor 2 is already moving, it stops the movement, changes the color of the move button to red, and calls the update_thread method with 
    specific parameters to stop the movement.
     If Motor 2 is not moving, it starts the movement, changes the color of the move button to green, and calls the update_thread 
     method with specific parameters to start the movement. It can send either

        -  0 to Stop the movement
        -  1 to move forward
        -  2 to move backwards
    """
        global _looping
        global act
        global send2
        global home_mot2

        if home_mot2 == False:
            glob_status.config(text="Please Home motor 2", fg="red")
            return

        if send2 == True:
            self.m2_move.config(fg='red')
            self.update_thread(1, 0)
            act -= 1
            send2 = False
            if(act == 0):
                _looping = False

        else:
            send2 = True
            _looping = True
            self.update_thread(1, self.var2.get())
            act += 1

            self.m2_move.config(fg='green')

    
    def move3(self):
        """
    This method controls the movement of Motor 3. 
    If Motor 3 is not homed, it updates the status text to 'Please Home motor 3'. 
    If Motor 3 is already moving, it stops the movement, changes the color of the move button to red, 
    and calls the update_thread method with specific parameters to stop the movement. 
    If Motor 3 is not moving, it starts the movement, changes the color of the move button to green, and calls the update_thread method 
    with specific parameters to start the movement. It can send either
        -  0 to Stop the movement
        -  1 to move forward
        -  2 to move backwards
    """
        global _looping
        global act
        global send3
        global home_mot3

        if home_mot3 == False:
            glob_status.config(text="Please Home motor 3", fg="red")
            return

        if send3 == True:
            self.m3_move.config(fg='red')
            self.update_thread(2, 0)
            act -= 1
            send3 = False
            if(act == 0):
                _looping = False

        else:
            send3 = True
            _looping = True
            self.update_thread(2, self.var3.get())
            act += 1

            self.m3_move.config(fg='green')

    
    def enaButtons(self):
            """
    This method enables all buttons in the Motor 1, Motor 2, and Motor 3 frames, and in the recording frame. 
    It disables the stop recording button. 
    If the maximum number of motors is not reached, then motor 3 has not been added. 
    Therefore it does not enable the buttons in the Motor 3 frame.
    """
            for child in self.motor1.winfo_children():
                child.configure(state="active")
            for child in self.motor2.winfo_children():
                child.configure(state="active")
            if self.mot_i == 3:
                    for child in self.motor3.winfo_children():
                        child.configure(state="active")
            for child in self.rec.winfo_children():
                child.configure(state="active")
            self.stop_rec_button.configure(state="disable")

    def disableButtons(self):
        """
    This method disables all buttons in the Motor 1, Motor 2, and recording frames. 
    It does not affect the stop recording button.
    """
        for child in self.motor1.winfo_children():
            child.configure(state="disable")
        for child in self.motor2.winfo_children():
            child.configure(state="disable")
        if self.mot_i == 3:
                for child in self.motor3.winfo_children():
                    child.configure(state="disable")
        for child in self.rec.winfo_children():
            child.configure(state="disable")
    
    ## THREADING ##

    def process_queue(self):
        """
    This method processes messages from the queue to display the queued messages sent to the Arduino.
    It tries to get a message from the queue and updates the status text with the message. 
    If the queue is empty, it calls itself again.

    """
        global home_i
        global rec
        global act
        global _looping

        try:
            # Try to get the Messages from the Queue from the threaded Task in run()
            msg = self.queue.get_nowait()
            # Print msg in Terminal
            print(msg, flush=True, end="\r")
            # Update Status with msg
            self.status.config(text=msg, fg="green")
        # If the Queue is empty (Nothing to send or Received)
        except queue.Empty:
            # Excecute Process again
            self.process_queue

    # Connection Function
    def conn(self):
        """
    This method manages the connection to the Arduino board. 
    If the board is not connected, it tries to connect to the board and updates the status text accordingly. 
    If the connection is successful, it sleeps for 1 second, calls the update_thread method with a specific parameter to send the connect
    command to the board, and sets the connection flag to True. 
    If the board is already connected, it enables all buttons, calls the update_thread method with a specific parameter to send the connect 
    command to the board, and updates the connect button text to 'Arduino Connected'.
    """
        global arduinoData
        global conn_bool
        # In case the board was disconnected mid-running we need to connect the board again with the respective Button
        if conn_bool == False:
            try:
                connectBoard(self.uport, self.ubaudrate)
            except:
                print("CONNECTION TO ARDUINO BOARD FAILED")
                self.status.config(text="CONNECTION TO ARDUINO BOARD FAILED", fg="red")
            else:
                time.sleep(1)
                self.update_thread(ind= 67)
                conn_bool = True
        else:
            # Check if the connection Is effective before Activating all Buttons
            self.enaButtons()
            self.update_thread(ind= 67)
            self.conn_button.config(
                text="Arduino Connected", fg="green", bg="grey")


# Main threaded Task
#   If set_ind is equal to 67 (ASCII for c and always unprobable motor index) we will send the Connect command to Board
#   If set_ind is equal to 72 (ASCII for h and always unprobable motor index) we will send the HOME Mode command to Board
#   If set_ind is equal to 80 (ASCII for p and always unprobable motor index) we will send the PROFILE Mode command to Board

    
    def update_thread(self, ind= 0, val = 0, profile_val = []):
        """
    This method updates the global variables for the index, value, and profile value. 
    It starts a new queue and a new threaded task with the queue. 
    It then processes the queue after a delay of 12 milliseconds.
    """
        global set_ind
        global set_val
        global set_profile
        set_ind = ind
        set_val = val
        set_profile = profile_val
        # Starts the Queue to be processed
        self.queue = queue.Queue()
        # Start the ThreadedTask with the Queue
        ThreadedTask(self.queue).start()
        # Procces the Queue
        self.master.after(12, self.process_queue)

def MainGUI():
        """
    This method creates the main GUI for the application. 
    The GUI includes entry fields for the COM port and baud rate, a button for starting the program, and a status bar. 
    The method also sets the protocol for closing the window and the window icon. It starts the main event loop for the GUI.
    """
        # User input for Arduino connection
        MainGUI.root = Tk()
        root = MainGUI.root
        root.title('Stepper Controller Welcome Page')
        COM_label = Label(root, text="COM Port").grid( row=0, column=0, pady=5, padx = 5)
        MainGUI.COM_PORT= Entry(root, width=10)
        MainGUI.COM_PORT.insert(0, "COM4")
        MainGUI.COM_PORT.grid(row=1, column= 0)

        BAUD_RATE_label = Label(root, text="Baudrate").grid( row=0, column=1, pady=5, padx = 5)
        MainGUI.BAUD_RATE= Entry(root, width=10)
        MainGUI.BAUD_RATE.insert(0, "250000")
        MainGUI.BAUD_RATE.grid(row=1, column= 1)

        ##Connection BUTTONS##
        conn_button = Button(root, command=on_closingStart)
        conn_button.configure(
                    text="Start Programm",
                    padx=50
                )
        conn_button.grid(row=2, column=0, padx=2, columnspan=2, pady=5)
        #GUI STATUS BAR
        MainGUI.status = Label(
                    root, bd=1, relief=SUNKEN, anchor=E, text='Provide info from your arduino')
        MainGUI.status.grid(row=4, column=0, columnspan=4, sticky=W+E)

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.iconbitmap("Python\StepperController32.ico")
        MainGUI.root.mainloop()

    
def on_closingStart():
    """
    
    This function is triggered when the start button is clicked on the main GUI. 
    It retrieves the COM port and baud rate from the GUI, and then attempts to connect to the Arduino board using these parameters.
    
    If the COM port is set to "NAM1", the function will ask the user if they want to enter "No Arduino Mode", 
    in which some functions may be disabled or not work. If the user confirms, the main GUI is launched. 
     
    If any other COM port is entered, the function will attempt to connect to the Arduino board. 

    If the connection is unsuccessful, an error message is displayed on the GUI. 
    If the connection is successful, the main GUI is launched.
    
    """
    global UCOM_PORT
    global UBAUD_RATE

    UCOM_PORT = MainGUI.COM_PORT.get() 
    print(UCOM_PORT)
    UBAUD_RATE = MainGUI.BAUD_RATE.get() 
    print(UBAUD_RATE)
    
    if (UCOM_PORT == "NAM1"):
        if messagebox.askokcancel("No Arduino Mode", "Are you sure you want to Enter NO Arduino mode? Some Functions will be disabled/Not Work"):
            MainGUI.main_ui = GUI(MainGUI.root)
            

    else: # Run to start the input for the Port and Baudrate
        try:
            connectBoard(UCOM_PORT, UBAUD_RATE)
        except:
            MainGUI.status.config(text="WRONG ENTRY TRY AGAIN", fg="red")
        else:
            MainGUI.main_ui = GUI(MainGUI.root)

# Threaded Task to enable the GUI while sending Arduino Commands


class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        """
    Initializes the instance of the class. 
    It takes a queue as an argument and sets it as an instance variable. 
    It also sets several global variables, including 'arduinoData', 'set_val', and 'set_profile', and initializes several instance variables, 
    including 'val', 'home_mot1', 'home_mot2', 'home', and 'profile'. The 'val' instance variable is set to the value of 'set_val', 
    and the 'home_mot1', 'home_mot2', 'home', and 'profile' instance variables are all initially set to False.
    """
        super().__init__()
        self.queue = queue
        global arduinoData
        global set_val
        global set_profile
        self.val = set_val
        self.home_mot1 = False
        self.home_mot2 = False
        self.home_mot3 = False
        self.home = False
        self.profile = False

    def run(self):
        """
    This function is the main execution loop for the thread. 
    It handles various commands sent to an Arduino board, including connect, home, and profile commands. 
        - For the connect command, it sends a connect request to the Arduino and updates the GUI with the response. 
        - For the home command, it sends a command to home the motors and updates the GUI with the status of the homing process.
        - For the profile command, it sends a series of commands to the Arduino to execute a predefined profile, 
        updating the GUI with the status of the profile execution. 

    It also handles manual commands (MOVEMENT) if the board is connected. 
    The function uses a queue to handle incoming commands and updates a global status variable with the status of the current operation.
    """
        # If set_ind is a motor Index we must insert the "a" in front for the Arduino to detect
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
                            elif(int_l == 404):
                                    MainGUI.main_ui.enaButtons()
                                    glob_status.config(text = "Emergency Stop", fg= "red")
                                    _func = False
                                    set_ind = 0
                                    self.val = 0
                                    return


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
                                    elif (int_l == 404):  
                                        in_line2 = ""
                                        MainGUI.main_ui.enaButtons()
                                        glob_status.config(text = "Emergency Stop", fg= "red")
                                        _func = False
                                        set_ind = 0
                                        self.val = 0
                                        return
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


MainGUI()

## POSSIBLE COMMANDS:
#"\r" is very important for the CommandHandler to recognize the command
#  The separator is a space between the different parameters to be sent
# !DC\r  --------> DISCONNECT BOARD
# !P val1 spd1 val2 spd2\r  --------> PROFILE POSITIONS AND SPEED FOR EACH MOTOR
# !PF\r  --------> PROFILE FINISHED
# !UK\r --------> CHANGE MODE 1 = Normal, 2 = Profile, 3 = Home Motor 2 and 4 = Home Motor 1
# !UM 1 1 1 0\r  --------> Move motors towards PLUS (1) or towards MINUS (2)
# !connect\r  --------> CONNECT BOARD
