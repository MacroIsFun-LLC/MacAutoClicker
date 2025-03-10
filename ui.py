import tkinter as tk
from tkinter import ttk
from clicker import is_clicking  # Ensure we get the latest clicking state
from listener import stop_listener  # Ensure we stop the global key listener

running = True

def on_close():
    """ Stop the key listener and close the UI properly """
    global running
    running = False
    stop_listener()  # Stop global key listener
    root.quit()  # Quit Tkinter mainloop
    root.destroy()  # Destroy the UI

def poll_ui():
    """ Updates the UI indicator to show clicking state """
    if is_clicking():
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

# Exit Button (Now properly stops the app)
exit_button = ttk.Button(root, text="Exit", command=on_close)
exit_button.pack(pady=10)

# Indicator (Green = Active, Red = Inactive)
indicator_canvas = tk.Canvas(root, width=100, height=50)
indicator = indicator_canvas.create_rectangle(0, 0, 100, 50, fill="red")
indicator_canvas.pack(pady=10)

# ----------------------
# Start Polling UI and Run Tkinter Loop
# ----------------------
poll_ui()
root.mainloop()
