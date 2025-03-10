import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import os
from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent, kCGEventScrollWheel, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft
from pynput.mouse import Controller, Button, Controller as PynputController

# State variables
clicking = False
delay = 0.05  # Default delay (50ms)
mouse = Controller()
pynput_mouse = PynputController()

def mac_click(x, y):
    """Simulate a native macOS click at the given coordinates."""
    event_down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    event_up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    event_down.post()
    event_up.post()

def scroll_method_1():
    """First Scroll Method: Using pyautogui."""
    pyautogui.scroll(-50)  # Scroll down by 50 units

def scroll_method_2():
    """Second Scroll Method: Using pynput mouse controller."""
    pynput_mouse.scroll(0, -1)  # Scroll down by 1 unit

def scroll_method_3():
    """Third Scroll Method: Using Quartz CoreGraphics for macOS."""
    scroll_event = CGEventCreateScrollWheelEvent(None, kCGEventScrollWheel, 0, -1)
    scroll_event.post()

def start_clicking():
    """Starts auto-clicking wherever the mouse is."""
    global clicking
    if not clicking:
        clicking = True
        update_indicator(clicking_indicator, "green")
        threading.Thread(target=press_mouse, daemon=True).start()

def stop_clicking():
    """Stops auto-clicking."""
    global clicking
    clicking = False
    update_indicator(clicking_indicator, "red")

def press_mouse():
    """Continuously clicks at the current mouse position."""
    while clicking:
        x, y = pyautogui.position()  # Get mouse position
        try:
            mac_click(x, y)  # Try Quartz click (macOS)
        except:
            mouse.position = (x, y)
            mouse.click(Button.left, 1)  # Fallback to pynput click
        time.sleep(delay)

def update_indicator(indicator, color):
    """Updates the UI indicator color."""
    root.after(0, lambda: indicator_canvas.itemconfig(indicator, fill=color))

def update_delay(value):
    """Updates the clicking speed based on slider input."""
    global delay
    delay = float(value)  # Convert slider value to float
    slider_label.config(text=f"Action Speed: {int(float(value) * 1000)} ms")

def on_key_press(event):
    """Handles keyboard shortcuts."""
    if event.char == '[':  # Start clicking
        start_clicking()
    elif event.char == ']':  # Stop clicking
        stop_clicking()
    elif event.char == ';':  # Scroll down using Method 1
        scroll_method_1()
    elif event.char == "'":  # Scroll down using Method 2
        scroll_method_2()
    elif event.char == '\\':  # Scroll down using Method 3
        scroll_method_3()

# --- Tkinter UI Setup ---
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x200")

# Exit button
exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

# Indicator Canvas
indicator_canvas = tk.Canvas(root, width=100, height=50)
clicking_indicator = indicator_canvas.create_rectangle(0, 0, 100, 50, fill="red")
indicator_canvas.pack(pady=10)

# Speed Control Slider & Label
slider_label = ttk.Label(root, text="Action Speed: 50 ms")
slider_label.pack()

speed_slider = ttk.Scale(root, from_=0.05, to=1.0, orient="horizontal", command=update_delay)
speed_slider.set(0.05)  # Default speed
speed_slider.pack(pady=10)

# Bind Keyboard Shortcuts
root.bind('<KeyPress>', on_key_press)

# Start Tkinter Event Loop
root.mainloop()
