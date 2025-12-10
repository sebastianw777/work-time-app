import getpass
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import datetime

current_user = getpass.getuser()

timer_on = False
seconds = 0
minutes = 0
hours = 0

file_path = "work_log.txt"

#Reset time
def reset():
    global seconds, minutes, hours
    seconds = 0
    minutes = 0
    hours = 0

#Updating actual date
def update_date():
    global now
    now = datetime.now().replace(microsecond=0)
    date_label.config(text=now)
    root.after(1000, update_date)

#Check if running
def start_work():
    global timer_on
    if timer_on == False:
        timer_on = True
        save_to_file("START")
        timer()
        messagebox.showinfo("Info", "Work started")
    else:
        messagebox.showerror("Info", "Work already started")

def timer():
    global timer_on
    if timer_on == True:
        global seconds, minutes, hours

        #Timer system
        seconds += 1

        if seconds == 60:
            seconds -= 60
            minutes += 1
        if minutes == 60:
            minutes -= 60
            hours += 1

        time_label.config(text=f"{hours}h {minutes}m {seconds}s")
        
        root.after(1000, timer)

def stop_timer():
    warning = messagebox.askyesno("Info", "Stop work?")

    if warning:
        global timer_on
        timer_on = False
        save_to_file("STOP")
        messagebox.showinfo("Info", f"Worked time: {hours} hous {minutes} minutes {seconds} seconds")
        reset()

def save_to_file(action):
    global now, hours, minutes, seconds, current_user
    entry = f"{now} | {current_user} | {action} | {hours:02d}:{minutes:02d}:{seconds:02d}\n"
    with open("work_log.txt", "a", encoding="utf-8") as f:
        f.write(entry)

#Interface
root = Tk()
root.title("Work time")
root.resizable(height=False, width=False)

frame = tk.Frame(root, padx=20, pady=20)
frame.grid(row=0, column=0)

tk.Label(frame, text="Work time").grid(row=0, column=0)
time_label = tk.Label(frame, text="0h 0m 0s")
time_label.grid(row=1, column=0)

tk.Label(frame, text=f"Logged as: {current_user}").grid(row=0, column=2, padx=50)
date_label = tk.Label(frame, text="Actual date")
date_label.grid(row=1, column=2)

tk.Button(frame, text="Start work", command=start_work).grid(row=0, column=3, pady=10, padx=10)
tk.Button(frame, text="End work", command=stop_timer).grid(row=1, column=3, padx=10)


update_date()
root.mainloop()