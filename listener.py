import threading
import Quartz
from Quartz import (
    CGEventTapCreate, kCGHeadInsertEventTap, kCGEventTapOptionDefault,
    CGEventMaskBit, kCGEventKeyDown, CGEventGetIntegerValueField, kCGKeyboardEventKeycode,
    CFMachPortCreateRunLoopSource, CFRunLoopAddSource, CFRunLoopRun, CFRunLoopStop, CFRunLoopGetCurrent
)
from clicker import start_clicking, stop_clicking

running = True
run_loop = None

def key_event_handler(proxy, type_, event, refcon):
    """ Handles global keypresses. '[' to start, ']' to stop. """
    if type_ == kCGEventKeyDown:
        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
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

    while running:
        CFRunLoopRun()

def stop_listener():
    """ Stops the key listener loop """
    global running
    running = False
    if run_loop:
        CFRunLoopStop(run_loop)
