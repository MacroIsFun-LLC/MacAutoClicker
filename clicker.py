import time
import threading
import pyautogui
import Quartz
from Quartz import (
    CGEventCreateMouseEvent, CGEventPost,
    kCGHIDEventTap, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft
)

clicking = False
click_lock = threading.Lock()
delay = 0.05

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
    global clicking
    with click_lock:
        clicking = True

def stop_clicking():
    global clicking
    with click_lock:
        clicking = False
