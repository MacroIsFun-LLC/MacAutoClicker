import tkinter as tk
from tkinter import ttk
from clicker import start_clicking, stop_clicking, is_clicking  # Use function instead of variable
from listener import stop_listener

running = True
delay = 0.05  # Default delay (Make sure this is initialized)

def on_close():
    """ Stop listener and close the UI """
    global running
    running = False
    stop_listener()
    root.destroy()

def update_delay(value):
    """ Updates the click delay """
    global delay
    delay = float(value)
    slider_label.config(text=f"Action Speed: {int(delay * 1000)} ms")

def poll_ui():
    """ Updates the UI indicator """
    if is_clicking():  # Use function instead of direct variable access
        indicator_canvas.itemconfig(indicator, fill="green")
    else:
        indicator_canvas.itemconfig(indicator, fill="red")

    if not running:
        root.quit()
        return
    root.after(200, poll_ui)


# ----------------------
# Tkinter UI Setup
# ----------------------
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x200")
root.protocol("WM_DELETE_WINDOW", on_close)

# Start/Stop Buttons
start_button = ttk.Button(root, text="Start Clicking", command=start_clicking)
start_button.pack(pady=5)

stop_button = ttk.Button(root, text="Stop Clicking", command=stop_clicking)
stop_button.pack(pady=5)

# Exit Button
exit_button = ttk.Button(root, text="Exit", command=on_close)
exit_button.pack(pady=10)

# Indicator (Green = Active, Red = Inactive)
indicator_canvas = tk.Canvas(root, width=100, height=50)
indicator = indicator_canvas.create_rectangle(0, 0, 100, 50, fill="red")
indicator_canvas.pack(pady=10)

# Speed Slider
slider_label = ttk.Label(root, text="Action Speed: 50 ms")
slider_label.pack()

speed_slider = ttk.Scale(root, from_=0.05, to=1.0, orient="horizontal", command=update_delay)
speed_slider.set(0.05)
speed_slider.pack(pady=10)

# ----------------------
# Start Polling UI and Run Tkinter Loop
# ----------------------
poll_ui()
root.mainloop()
