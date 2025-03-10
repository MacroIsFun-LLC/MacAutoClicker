import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import Quartz
from Quartz import (
    CGEventCreateMouseEvent, CGEventPost,
    kCGHIDEventTap, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft,
    CGEventTapCreate, kCGHeadInsertEventTap, kCGEventTapOptionDefault,
    CGEventMaskBit, kCGEventKeyDown, CFMachPortCreateRunLoopSource,
    CFRunLoopAddSource, CFRunLoopRun, CFRunLoopStop, CFRunLoopGetCurrent,
    CGEventGetIntegerValueField, kCGKeyboardEventKeycode
)

# ----------------------
# Global Variables
# ----------------------
clicking = False         # Auto-clicker active?
running = True           # App running?
delay = 0.05             # Default delay between clicks
click_thread = None      # Reference to the clicker thread (so we don't spawn multiple)
run_loop = None          # CFRunLoop reference for stopping the tap

# ----------------------
# Mouse Click Helpers
# ----------------------
def mac_click(x, y):
    down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, down)
    CGEventPost(kCGHIDEventTap, up)

def click_loop():
    """ Continuously clicks while clicking=True. """
    while running:
        if clicking:
            x, y = pyautogui.position()
            mac_click(x, y)
            time.sleep(delay)
        else:
            time.sleep(0.05)  # Idle briefly when not clicking

# ----------------------
# Start/Stop Clicking
# ----------------------
def start_clicking():
    global clicking, click_thread
    if not clicking:
        clicking = True
        # If no thread is alive, start one
        if not click_thread or not click_thread.is_alive():
            click_thread = threading.Thread(target=click_loop, daemon=True)
            click_thread.start()

def stop_clicking():
    global clicking
    clicking = False

# ----------------------
# Quartz Key Listener
# ----------------------
def key_event_handler(proxy, type_, event, refcon):
    """ Handles global keypresses. '[' to start, ']' to stop. """
    if type_ == kCGEventKeyDown:
        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        # On macOS, '[' is keycode=33, ']' is keycode=30 (QWERTY layout)
        if keycode == 33:  # '[' key
            start_clicking()
        elif keycode == 30:  # ']' key
            stop_clicking()
    return event

def start_key_listener():
    """ Sets up a global key listener via Quartz and runs a CFRunLoop. """
    global run_loop
    tap = CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        CGEventMaskBit(kCGEventKeyDown),
        key_event_handler,
        None
    )
    if not tap:
        print("ERROR: Unable to create event tap. Run with appropriate privileges?")
        return

    source = CFMachPortCreateRunLoopSource(None, tap, 0)
    run_loop = CFRunLoopGetCurrent()
    CFRunLoopAddSource(run_loop, source, Quartz.kCFRunLoopCommonModes)
    Quartz.CGEventTapEnable(tap, True)

    # Keep the CFRunLoop spinning while running is True
    while running:
        CFRunLoopRun()

# ----------------------
# Tkinter Setup
# ----------------------
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x200")

# Bring window on top for 1 sec
root.attributes('-topmost', True)
root.after(1000, lambda: root.attributes('-topmost', False))

# 1) Exit Button
def on_close():
    global running
    running = False
    # Attempt to stop the CFRunLoop
    if run_loop:
        CFRunLoopStop(run_loop)
    root.destroy()

exit_button = ttk.Button(root, text="Exit", command=on_close)
exit_button.pack(pady=10)

# 2) Indicator
indicator_canvas = tk.Canvas(root, width=100, height=50)
indicator = indicator_canvas.create_rectangle(0, 0, 100, 50, fill="red")
indicator_canvas.pack(pady=10)

# 3) Speed Slider
slider_label = ttk.Label(root, text="Action Speed: 50 ms")
slider_label.pack()

def update_delay(value):
    global delay
    delay = float(value)
    slider_label.config(text=f"Action Speed: {int(delay * 1000)} ms")

speed_slider = ttk.Scale(root, from_=0.05, to=1.0, orient="horizontal", command=update_delay)
speed_slider.set(0.05)
speed_slider.pack(pady=10)

# ----------------------
# UI Polling
# ----------------------
def poll_ui():
    """
    Since we can't safely update Tkinter from the listener thread,
    we poll the state from the main thread.
    """
    # Update the color based on whether we're clicking
    if clicking:
        indicator_canvas.itemconfig(indicator, fill="green")
    else:
        indicator_canvas.itemconfig(indicator, fill="red")

    # If the app is not running, close the GUI
    if not running:
        root.quit()
        return

    # Schedule next poll
    root.after(200, poll_ui)

# ----------------------
# Start Everything
# ----------------------
# 1) Start Key Listener Thread
listener_thread = threading.Thread(target=start_key_listener, daemon=True)
listener_thread.start()

# 2) Begin polling for UI updates in main thread
poll_ui()

# 3) Start Tkinter loop
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
