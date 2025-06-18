import tkinter as tk
from tkinter import ttk
import threading
import time
import Quartz
from Quartz import (
    CGEventTapCreate, kCGHeadInsertEventTap, kCGEventTapOptionDefault,
    CGEventMaskBit, kCGEventKeyDown, CFMachPortCreateRunLoopSource,
    CFRunLoopAddSource, CFRunLoopRun, CFRunLoopStop, CFRunLoopGetCurrent,
    CGEventGetIntegerValueField, kCGKeyboardEventKeycode,
    CGEventCreateScrollWheelEvent, CGEventPost, kCGHIDEventTap
)

# ----------------------
# Global Variables
# ----------------------
scrolling = False
running = True
scroll_amount = 60
scroll_duration = 5.0
scroll_thread = None
run_loop = None

# ----------------------
# Scroll Function using Quartz
# ----------------------
def mac_scroll(amount):
    scroll_event = CGEventCreateScrollWheelEvent(None, 1, 1, int(-amount))  # Negative = down
    CGEventPost(kCGHIDEventTap, scroll_event)

# ----------------------
# Scroll Loop
# ----------------------
def scroll_loop():
    while running:
        if scrolling:
            tick_interval = 0.05
            ticks = int(scroll_duration / tick_interval)
            for _ in range(ticks):
                if not scrolling or not running:
                    break
                mac_scroll(scroll_amount)
                time.sleep(tick_interval)
            # After scrolling, wait 10 seconds before next cycle
            for _ in range(int(10 / 0.1)):
                if not scrolling or not running:
                    break
                time.sleep(0.1)
        else:
            time.sleep(0.1)

# ----------------------
# Start/Stop Control
# ----------------------
def start_scrolling():
    global scrolling, scroll_thread
    if not scrolling:
        scrolling = True
        if not scroll_thread or not scroll_thread.is_alive():
            scroll_thread = threading.Thread(target=scroll_loop, daemon=True)
            scroll_thread.start()

def stop_scrolling():
    global scrolling
    scrolling = False

# ----------------------
# Global Hotkey Listener
# ----------------------
def key_event_handler(proxy, type_, event, refcon):
    if type_ == kCGEventKeyDown:
        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        if keycode == 33:  # '{' key
            start_scrolling()
        elif keycode == 30:  # '}' key
            stop_scrolling()
    return event

def start_key_listener():
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

    while running:
        CFRunLoopRun()

# ----------------------
# GUI Setup
# ----------------------
root = tk.Tk()
root.title("Auto Scroll")
root.geometry("320x300")
root.attributes('-topmost', True)
root.after(1000, lambda: root.attributes('-topmost', False))

# Exit Button
def on_close():
    global running
    running = False
    if run_loop:
        CFRunLoopStop(run_loop)
    root.destroy()

exit_button = ttk.Button(root, text="Exit", command=on_close)
exit_button.pack(pady=10)

# Scroll Status Indicator
indicator_canvas = tk.Canvas(root, width=100, height=50)
indicator = indicator_canvas.create_rectangle(0, 0, 100, 50, fill="red")
indicator_canvas.pack(pady=10)

# Scroll Amount Slider
scroll_label = ttk.Label(root, text="Scroll Amount: 60")
scroll_label.pack()

def update_scroll_amount(value):
    global scroll_amount
    scroll_amount = int(float(value))
    scroll_label.config(text=f"Scroll Amount: {scroll_amount}")

scroll_slider = ttk.Scale(root, from_=10, to=1000, orient="horizontal", command=update_scroll_amount)
scroll_slider.set(60)
scroll_slider.pack(pady=10)

# Scroll Duration Slider
duration_label = ttk.Label(root, text="Scroll Duration: 5.0 sec")
duration_label.pack()

def update_scroll_duration(value):
    global scroll_duration
    scroll_duration = float(value)
    duration_label.config(text=f"Scroll Duration: {scroll_duration:.1f} sec")

duration_slider = ttk.Scale(root, from_=0.5, to=10.0, resolution=0.1, orient="horizontal", command=update_scroll_duration)
duration_slider.set(5.0)
duration_slider.pack(pady=10)

# UI Polling
def poll_ui():
    indicator_canvas.itemconfig(indicator, fill="green" if scrolling else "red")
    if not running:
        root.quit()
        return
    root.after(200, poll_ui)

# ----------------------
# Launch Threads
# ----------------------
listener_thread = threading.Thread(target=start_key_listener, daemon=True)
listener_thread.start()

poll_ui()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
