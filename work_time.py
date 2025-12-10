import os
import getpass
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

current_user = getpass.getuser() # Current user name

timer_on = False
seconds = 0
minutes = 0
hours = 0

file_path = "work_log.txt" # <- Set Set file path for the work log | created automatically if it doesn't exist

if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Date | User | Action | Time\n")

# Reset time
def reset():
    global seconds, minutes, hours
    seconds = 0
    minutes = 0
    hours = 0

# Updating actual date
def update_date():
    now = datetime.now().replace(microsecond=0)
    date_label.config(text=now)
    root.after(1000, update_date)

# Check if running
def start_work():
    global timer_on
    if not timer_on:
        timer_on = True
        save_to_file("START")
        timer()
        messagebox.showinfo("Info", "Work started")
    else:
        messagebox.showerror("Info", "Work already started")

# Start timer
def timer():
    global timer_on, seconds, minutes, hours
    if timer_on:
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes += 1
        if minutes == 60:
            minutes = 0
            hours += 1

        time_label.config(text=f"{hours}h {minutes}m {seconds}s")
        root.after(1000, timer)

# Stop timer
def stop_timer():
    global timer_on
    warning = messagebox.askyesno("Info", "Stop work?")
    if warning:
        timer_on = False
        save_to_file("STOP")
        messagebox.showinfo("Info", f"Worked time: {hours} hours {minutes} minutes {seconds} seconds")
        reset()

# Save log system
def save_to_file(action):
    global hours, minutes, seconds, current_user
    now = datetime.now().replace(microsecond=0)  # generujemy aktualny czas tu i teraz
    entry = f"{now} | {current_user} | {action} | {hours:02d}:{minutes:02d}:{seconds:02d}\n"
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

# Interface
root = tk.Tk()
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
