import tkinter as tk
import tkinter.ttk as ttk
import serial
import time

arduino = serial.Serial(port='',baudrate=115200,timeout=0.1)

# Future button converters
def PW_button_send(number):
    '''Convert the button value to hex and prints on the terminal'''
#    hex_value = hex(number)
#    print(hex_value)
    arduino.write(bytes(number,'utf-8'))
    time.sleep(0.05)


def PF_button_send(number):
    '''Convert the button value to hex and prints on the terminal'''
#    hex_value = hex(number)
#    print(hex_value)
    arduino.write(bytes(number,'utf-8'))
    time.sleep(0.05)

def ser_mon_display():
    time.sleep(0.05)
    print(arduino.readline())


window = tk.Tk()

# Define frames
frame_pw = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_pf = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_stimon = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_curampl = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_onoff = tk.Frame(relief=tk.RIDGE,borderwidth=5)
frame_serial_mon = tk.Frame(relief=tk.RIDGE,borderwidth=5)

# Make frames as grid
frame_pw.grid(row=0,column=0,padx=5,pady=5)
frame_pf.grid(row=0,column=1,padx=5,pady=5)
frame_stimon.grid(row=0,column=2,padx=5,pady=5)
frame_curampl.grid(row=0,column=3,padx=5,pady=5)
frame_onoff.grid(row=0,column=4,padx=5,pady=5)
frame_serial_mon.grid(row=1,column=0, columnspan=5,padx=5,pady=5)

# Define labels
    # Frame labels
pw_prompt_lbl = tk.Label(master=frame_pw,text="Pulse width")
pf_prompt_lbl = tk.Label(master=frame_pf,text="Pulse frequency")
stimon_prompt_lbl = tk.Label(master=frame_stimon,text="Stimulation ON time")
curampl_prompt_lbl = tk.Label(master=frame_curampl,text="Set current level")
onoff_prompt_lbl = tk.Label(master=frame_onoff,text="Stimulation on/off")
    # Pulse widths
PWs = range(50,4050,50)
    # Pulse frequencies
PFs = [10, 20]
    # Stimulation on times
Stim_On_times = [5,10,20,30,60,120]
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

# Define entry fields
set_current_lvl_box = tk.Entry(
    master=frame_curampl,
    bg="black",
    fg="white",
)

# Organise widgets in the window
pw_prompt_lbl.grid(row=0,column=0,columnspan=5, sticky="nsew")
pf_prompt_lbl.grid(row=0,column=0,columnspan=2, sticky="nsew")
stimon_prompt_lbl.grid(row=0,column=0)
curampl_prompt_lbl.grid(row=0,column=0,columnspan=2, sticky="nsew")
onoff_prompt_lbl.grid(row=0,column=0)
set_current_lvl_box.grid(row=1,column=0)
mA_lbl.grid(row=1,column=1)
serial_mon_lbl.grid(row=0,column=0)
#set_current_lvl_box.insert(0,"Input current level")

set_current_lvl = set_current_lvl_box.get()

window.mainloop()

#print(set_current_level)
