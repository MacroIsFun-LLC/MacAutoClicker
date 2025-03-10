import time
import threading
import pyautogui
import Quartz
from Quartz import (
    CGEventCreateMouseEvent, CGEventPost,
    kCGHIDEventTap, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft
)

clicking = False  # State of clicking
click_lock = threading.Lock()
delay = 0.05  # Default delay

def mac_click(x, y):
    """ Simulates a mouse click at (x, y) """
    down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, (x, y), kCGMouseButtonLeft)
    up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, (x, y), kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, down)
    CGEventPost(kCGHIDEventTap, up)

def click_loop():
    """ Continuously clicks while clicking=True. """
    global clicking
    while True:
        with click_lock:
            if clicking:
                x, y = pyautogui.position()
                mac_click(x, y)
                time.sleep(delay)
            else:
                time.sleep(0.05)  # Idle briefly when not clicking

def start_clicking():
    """ Starts clicking """
    global clicking
    with click_lock:
        clicking = True
    print("Clicking started")  # Debug log

def stop_clicking():
    """ Stops clicking """
    global clicking
    with click_lock:
        clicking = False
    print("Clicking stopped")  # Debug log

def is_clicking():
    """ Returns the current clicking state (for UI updates) """
    global clicking
    return clicking
