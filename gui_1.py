import tkinter as tk
import tkinter.ttk as ttk
import serial
import time

#arduino = serial.Serial(port='COM4',baudrate=115200,timeout=0.1)
arduino = serial.Serial(port='COM5',baudrate=115200,timeout=0, writeTimeout=0) #ensure non-blocking

# List of COM ports 

window = tk.Tk()
command_byte = []

# make a scrollbar
#scrollbar = tk.Scrollbar(window)
#scrollbar.pack(side="right", fill="y")

# Command to be sent to arduino for interpretation 
i = 0
for i in range(11):
    command_byte.append(None)
#command_byte = [None,None,None,None,None,None,None,None,None]    
#command_byte = [0,0,0,0,0,0,0]
# State bits to check if corresponding value has been added to the command byte
PW_state_bit = 0
PF_state_bit = 0
T_on_state_bit = 0
curampl_state_bit = 0
onoff_state_bit = 0
stim_mode_state_bit = 0
channel_nr_state_bit = 0
command_sent = 0

# Button function converters
def PW_button_send(number):
    '''Convert the button value to hex and prints on the terminal'''
#    hex_value = hex(number)
#    print(hex_value)
#    arduino.write(bytes(number,'utf-8'))
    global PW_state_bit
    global command_byte
    if PW_state_bit == 0:
        command_byte[0] = round(number / 50)
        command_byte[1] = 0
        PW_state_bit = 1
    # Update the command_byte label
    command_word_lbl["text"] = f"{command_byte}"
    
def PF_button_send(number):
    '''Convert the button value to hex and prints on the terminal'''
#    hex_value = hex(number)
#    print(hex_value)
#    arduino.write(bytes(number,'utf-8'))
    global PF_state_bit
    global command_byte
    time.sleep(0.05)
    if PF_state_bit == 0:
        if number == PFs[0]: # for 20 Hz timer reload byte is 23869 (0x5D3D, 0x5D = 93, 0x3D = 61) 
            command_byte[2] = 93
            command_byte[3] = 61
            PF_state_bit = 1
        if number == PFs[1]: # for 15 Hz timer reload byte is 9980 (0x26FC, 0x26 = 38, 0xFC = 252)
            command_byte[2] = 38
            command_byte[3] = 252
    # Update the command_byte label
    command_word_lbl["text"] = f"{command_byte}"
    
def T_on_button_send(number):
    global T_on_state_bit
    global command_byte
    if T_on_state_bit == 0:
        for word in Stim_On_timer_vals[number]:
            command_byte[4] = Stim_On_timer_vals[number][0]
            command_byte[5] = Stim_On_timer_vals[number][1]
            command_byte[6] = Stim_On_timer_vals[number][2]
        T_on_state_bit = 1
    # Update the command_byte label
    command_word_lbl["text"] = f"{command_byte}"

# def curampl_button_send(number):
#     global curampl_state_bit
#     if curampl_state_bit == 0:
#         command_byte.append(number)
#         curampl_state_bit = 1
#     # Update the command_byte label
#     command_word_lbl["text"] = f"{command_byte}"

def onoff_button_send(number):
    global onoff_state_bit
    global command_byte
    if onoff_state_bit == 0:
        command_byte[7] = number
        onoff_state_bit = 1
    # Update the command_byte label
    command_word_lbl["text"] = f"{command_byte}"

def get_current_value():
    global curampl_state_bit
    global command_byte
    if curampl_state_bit == 0:
        # Is this integer or string? String -> Integer
        set_current_lvl = float(set_current_lvl_box.get())
        step = 31.4375 # amount of the amplified current [uA] provided by 1 step (1 incremental bit) from the 8-bit IRef (4x [0,503] uA)
        I_ref = round(set_current_lvl * 1000 / step)  # number of 8-bit levels to supply the required current 
        command_byte[8] = I_ref - 1 # taking into account the 0th step
        curampl_state_bit = 1
    # Update the command_byte label
    command_word_lbl["text"] = f"{command_byte}"

def stim_mode_send(number):
    global stim_mode_state_bit
    global command_byte
    if stim_mode_state_bit == 0:
        command_byte[9] = number
        stim_mode_state_bit = 1
    command_word_lbl["text"] = f"{command_byte}"

def get_channel_nr():
    global channel_nr_state_bit
    global command_byte
    if channel_nr_state_bit == 0:
        channel_nr = int(channel_nr_box.get())
        command_byte[10] = channel_nr
        channel_nr_state_bit = 1
    command_word_lbl["text"] = f"{command_byte}"

# def ser_mon_display():
# #    time.sleep(0.05)
# #    print(arduino.readline())
#     while arduino.in_waiting:
#         data = arduino.readline()
#         print(str(data))

def send_command_word():
    """
    Simple test of the command word sending
    """
    global command_sent
    global command_byte
    # command_byte_str.insert(0,'<')
    # command_byte_str.append('>')
#    arduino.write(bytes,(command_byte[0],'utf-8'))
    if (command_sent == 0):
        command_word_lbl["text"] = f"{command_byte}"
        command_byte_str = ','.join(str(x) for x in command_byte)
        command_byte_str = '<' + command_byte_str
        command_byte_str = command_byte_str + '>'
        arduino.write(bytes(command_byte_str, encoding = 'utf-8'));
        time.sleep(1);
        print(command_byte_str);
        command_sent = 1;
    
#    ser_mon_display()

def reset():
    global PW_state_bit
    global PF_state_bit
    global T_on_state_bit
    global curampl_state_bit
    global onoff_state_bit
    global stim_mode_state_bit
    global channel_nr_state_bit
    global command_sent
    global command_byte
    PW_state_bit = 0
    PF_state_bit = 0
    T_on_state_bit = 0
    curampl_state_bit = 0
    onoff_state_bit = 0
    stim_mode_state_bit = 0
    channel_nr_state_bit = 0
    command_sent = 0

    i = 0
    command_byte = []
    for i in range(11):
        command_byte.append(None)
    #command_byte = [0,0,0,0,0,0,0]
    command_word_lbl["text"] = f"{command_byte}"

# Define frames
frame_pw = tk.Frame(height=10, relief=tk.RIDGE,borderwidth=5)
frame_pf = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_stimon = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_curampl = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_onoff = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_stim_mode = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_channel_nr = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_program = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_serial_mon = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_command_word = tk.Frame(relief=tk.RIDGE,borderwidth=5)

# Make frames as grid
frame_pw.grid(row=0,column=0,padx=5,pady=5)
frame_pf.grid(row=0,column=1,padx=5,pady=5)
frame_stimon.grid(row=0,column=2,padx=5,pady=5)
frame_onoff.grid(row=0,column=3,padx=5,pady=5)
frame_curampl.grid(row=0,column=4,padx=5,pady=5)
frame_stim_mode.grid(row=0,column=5,padx=5,pady=5)
frame_channel_nr.grid(row=0,column=6,padx=5,pady=5)
#frame_serial_mon.grid(row=1,column=0,columnspan=5,padx=5,pady=5)
frame_serial_mon.grid(row=1,column=0,padx=5,pady=5)
#frame_command_word.grid(row=1,column=6,columnspan=5,padx=5,pady=5)
frame_command_word.grid(row=1,column=1,columnspan=3,padx=5,pady=5)
frame_program.grid(row=1,column=4,padx=5,pady=5)

# Make a text box for the serial output

log = tk.Text(frame_serial_mon,width=15,height=5,takefocus=0)
log.grid(row=0,column=0)
scrollbar = tk.Scrollbar(frame_serial_mon)
scrollbar.grid(row=0,column=1)
# attach text box to scrollbar
log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log.yview)
#make our own buffer
#useful for parsing commands
#Serial.readline seems unreliable at times too
serBuffer = ""

def readSerial():
    while True:
        c = arduino.read().decode('ascii') # attempt to read a character from Serial
        
        #was anything read?
        if len(c) == 0:
            break
        
        # get the buffer from outside of this function
        global serBuffer
        
        # check if character is a delimeter
        if c == '\r':
            c = '' # don't want returns. chuck it
            
        if c == '\n':
            serBuffer += "\n" # add the newline to the buffer
            
            #add the line to the TOP of the log
            log.insert('0.0', serBuffer)
            serBuffer = "" # empty the buffer
        else:
            serBuffer += c # add to the buffer
    frame_serial_mon.after(10, readSerial)

frame_serial_mon.after(100,readSerial)
# Define labels
    # Frame labels
pw_prompt_lbl = tk.Label(master=frame_pw,text="Pulse width")
pf_prompt_lbl = tk.Label(master=frame_pf,text="Pulse frequency")
stimon_prompt_lbl = tk.Label(master=frame_stimon,text="Stimulation ON time")
curampl_prompt_lbl = tk.Label(master=frame_curampl,text="Set current level")
onoff_prompt_lbl = tk.Label(master=frame_onoff,text="Stimulation on/off")
stim_mode_prompt_lbl = tk.Label(master=frame_stim_mode,text="Stimulation mode")
channel_nr_prompt_lbl = tk.Label(master=frame_channel_nr,text="Channel Number")
    # Pulse widths
PWs = range(50,4050,50)
    # Pulse frequencies
PFs = [15, 20]
    # Stimulation on times
Stim_On_times = [5,10,20,30,60,120]
Stim_On_timer_vals = {
    5: [0,112,2],
    10: [0,0,5],
    20: [0,0,10],
    30: [0,0,15],
    60: [0,0,30],
    120: [0,0,60]
}
    # On/Off options
onoff = [0, 1]
    # Stimulation mode options
stim_modes = [0, 1]
    # time labels
us_lbl = tk.Label(text="us")
ms_lbl = tk.Label(text="ms")
s_lbl = tk.Label(text="s")
    # frequency label
hz_lbl = tk.Label(text="Hz")
    # current label
uA_lbl = tk.Label(text="uA")
mA_lbl = tk.Label(master=frame_curampl, text="mA")
    # Serial monitor label
serial_mon_lbl = tk.Label(master=frame_serial_mon,text="Serial Monitor")

command_word_lbl = tk.Label(master=frame_command_word,text="")
command_word_lbl["text"] = f"{command_byte}"

# Define and organise buttons
k = 0
for i in range(16):
    for j in range(5):

        def PW_btn_press(x = PWs[k]):
            ''' Pulse width event handler to react to the button 
            press with the deft argument of the button value'''
            return PW_button_send(x)

        PW_btn = tk.Button(
            master=frame_pw,
            text=PWs[k],
            bg="black",
            fg="white",
            command = PW_btn_press
        ) 
        PW_btn.grid(row=i+1,column=j)
        k = k+1
k = 0
i = 0
j = 0

for i in range(2):
    def PF_btn_press(x = PFs[k]):
        ''' Pulse frequency event handler to react to the button 
            press with the deft argument of the button value'''
        return PF_button_send(x)

    PF_btn = tk.Button(
        master=frame_pf,
        text=PFs[i],
        bg="black",
        fg="white",
        command = PF_btn_press
    )
    PF_btn.grid(row = 1, column = i)
    k = k + 1
k = 0
i = 0

for i in range(2):
    for j in range(3):
        def T_on_btn_press(x = Stim_On_times[k]):
            return T_on_button_send(x)
        T_on_btn = tk.Button(
            master = frame_stimon,
            text=Stim_On_times[k],
            bg="black",
            fg="white",
            command = T_on_btn_press
        )
        T_on_btn.grid(row = i+1, column = j)
        k = k+1
k = 0
i = 0
j = 0


for i in range(2):
    def on_off_btn_press(x = onoff[i]):
        return onoff_button_send(x)
    if i == 0:
        onoff_btn = tk.Button(
            master = frame_onoff,
            text = "Off",
            bg = "black",
            fg = "white",
            command = on_off_btn_press
        )
        onoff_btn.grid(row = 1, column = 0)
    if i == 1:
        onoff_btn = tk.Button(
            master = frame_onoff,
            text = "On",
            bg = "black",
            fg = "white",
            command = on_off_btn_press
        )   
        onoff_btn.grid(row = 1, column = 1)
    
i = 0

curampl_btn = tk.Button(
    master = frame_curampl,
    text = "Enter",
    bg = "black",
    fg = "white",
    command = get_current_value
)
curampl_btn.grid(row = 1, column = 2)

for i in range(2):
    def stim_mode_btn_press(x = stim_modes[i]):
        return stim_mode_send(x)
    if i == 0:
        stim_mode_btn = tk.Button(master=frame_stim_mode,text="Channel\n scanning\n (pulmonary/\nlaryngeal)", bg = "black", fg = "white", command = stim_mode_btn_press)
        stim_mode_btn.grid(row = 1, column = i)
    if i == 1:
        stim_mode_btn = tk.Button(master=frame_stim_mode,text="Single\n channel\n stimulation", bg = "black", fg = "white", command = stim_mode_btn_press)
        stim_mode_btn.grid(row = 1, column = i)

channel_nr_btn = tk.Button(master=frame_channel_nr,text="Enter",bg="black",fg="white",command=get_channel_nr)
channel_nr_btn.grid(row=1,column=2)

program_btn = tk.Button(master=frame_program,text="Program",bg="black",fg="white",command=send_command_word)
program_btn.grid(row=0,column=0)
reset_btn = tk.Button(master=frame_program,text="Reset",bg="black",fg="white",command=reset)
reset_btn.grid(row=0,column=1)

# Define entry fields
set_current_lvl_box = tk.Entry(master=frame_curampl,bg="black",fg="white")
channel_nr_box = tk.Entry(master=frame_channel_nr,bg="black",fg="white")

# Organise widgets in the window
pw_prompt_lbl.grid(row=0,column=0,columnspan=5, sticky="nsew")
pf_prompt_lbl.grid(row=0,column=0,columnspan=2, sticky="nsew")
stimon_prompt_lbl.grid(row=0,column=0,columnspan=3)
curampl_prompt_lbl.grid(row=0,column=0,columnspan=2, sticky="nsew")
onoff_prompt_lbl.grid(row=0,column=0, columnspan = 2, sticky = "nsew")
set_current_lvl_box.grid(row=1,column=0)
channel_nr_prompt_lbl.grid(row=0,column=0,columnspan=2,sticky = "nsew")
channel_nr_box.grid(row=1,column=0)
mA_lbl.grid(row=1,column=1)
stim_mode_prompt_lbl.grid(row = 0, column = 0, columnspan=2, sticky = "nsew")
serial_mon_lbl.grid(row=1,column=0)
#set_current_lvl_box.insert(0,"Input current level")
command_word_lbl.grid(row = 2, column = 0)

window.mainloop()

#print(set_current_level)
