import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import Quartz
from Quartz import (
    CGEventCreateMouseEvent, CGEventPost,
    kCGHIDEventTap, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft,
    CGEventTapCreate, kCGHeadInsertEventTap, kCGEventTapOptionDefault, CGEventMaskBit,
    kCGEventKeyDown, CFMachPortCreateRunLoopSource, CFRunLoopAddSource, CFRunLoopRun,
    CGEventGetIntegerValueField, kCGKeyboardEventKeycode, CFRunLoopStop, CFRunLoopGetCurrent
)

# Global vars
clicking = False
delay = 0.05
running = True  # GUI running flag

def mac_click(x, y):
    down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, down)
    CGEventPost(kCGHIDEventTap, up)

def click_loop():
    global clicking
    while clicking and running:
        x, y = pyautogui.position()
        mac_click(x, y)
        time.sleep(delay)

def start_clicking():
    global clicking
    if not clicking:
        clicking = True
        update_indicator("green")
        threading.Thread(target=click_loop, daemon=True).start()

def stop_clicking():
    global clicking
    clicking = False
    update_indicator("red")

def update_indicator(color):
    if running:
        root.after(0, lambda: indicator_canvas.itemconfig(indicator, fill=color))

def update_delay(value):
    global delay
    delay = float(value)
    slider_label.config(text=f"Action Speed: {int(delay * 1000)} ms")

# Global keyboard monitoring
def key_event_handler(proxy, type_, event, refcon):
    if type_ == kCGEventKeyDown:
        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        if keycode == 33:  # '[' key
            start_clicking()
        elif keycode == 30:  # ']' key
            stop_clicking()
    return event

def start_key_listener():
    tap = CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        CGEventMaskBit(kCGEventKeyDown),
        key_event_handler,
        None
    )
    source = CFMachPortCreateRunLoopSource(None, tap, 0)
    loop = CFRunLoopGetCurrent()
    CFRunLoopAddSource(loop, source, Quartz.kCFRunLoopCommonModes)
    Quartz.CGEventTapEnable(tap, True)

    while running:
        Quartz.CFRunLoopRun()

# Tkinter GUI setup
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("300x200")

root.attributes('-topmost', True)
root.after(1000, lambda: root.attributes('-topmost', False))

exit_button = ttk.Button(root, text="Exit", command=lambda: root.quit())
exit_button.pack(pady=10)

indicator_canvas = tk.Canvas(root, width=100, height=50)
indicator = indicator_canvas.create_rectangle(0, 0, 100, 50, fill="red")
indicator_canvas.pack(pady=10)

slider_label = ttk.Label(root, text="Action Speed: 50 ms")
slider_label.pack()

speed_slider = ttk.Scale(root, from_=0.05, to=1.0, orient="horizontal", command=update_delay)
speed_slider.set(0.05)
speed_slider.pack(pady=10)

# Start key listener thread
listener_thread = threading.Thread(target=start_key_listener, daemon=True)
listener_thread.start()

# Handle graceful shutdown
def on_close():
    global running, clicking
    running = False
    clicking = False
    CFRunLoopStop(CFRunLoopGetCurrent())
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
