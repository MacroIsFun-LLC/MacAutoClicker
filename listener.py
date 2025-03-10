import threading
import Quartz
from Quartz import (
    CGEventTapCreate, kCGHeadInsertEventTap, kCGEventTapOptionDefault,
    CGEventMaskBit, kCGEventKeyDown, CGEventGetIntegerValueField, kCGKeyboardEventKeycode,
    CFMachPortCreateRunLoopSource, CFRunLoopAddSource, CFRunLoopRun, CFRunLoopStop, CFRunLoopGetCurrent,
    CGEventTapEnable
)
from clicker import start_clicking, stop_clicking  # Now properly controls clicking

running = True
run_loop = None
tap = None  # Keep a reference to the event tap

def key_event_handler(proxy, type_, event, refcon):
    """ Handles global keypresses. '[' to start clicking, ']' to stop clicking. """
    if type_ == kCGEventKeyDown:
        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        if keycode == 33:  # '[' key
            print("Detected '[' key - Starting clicking")
            start_clicking()
        elif keycode == 30:  # ']' key
            print("Detected ']' key - Stopping clicking")
            stop_clicking()
    return event

def start_key_listener():
    """ Sets up a global key listener via Quartz and runs a CFRunLoop. """
    global run_loop, tap
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
    CGEventTapEnable(tap, True)  # Ensure the event tap is enabled

    while running:
        CFRunLoopRun()

def stop_listener():
    """ Stops the key listener loop and disables the event tap """
    global running
    running = False
    if tap:
        CGEventTapEnable(tap, False)  # Disable the event tap
    if run_loop:
        CFRunLoopStop(run_loop)  # Stop the listener loop
