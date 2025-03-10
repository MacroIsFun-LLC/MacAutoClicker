# Auto Clicker (macOS) – A Comprehensive Guide

This **Auto Clicker** tool for macOS leverages **Quartz** for global keyboard listening (hotkeys) and **Tkinter** for a graphical user interface (GUI). It lets you:

1. Start or stop auto-clicking using the **`[`** (start) or **`]`** (stop) hotkeys.
2. Adjust the delay between clicks (speed) in real time with a **slider**.
3. Monitor status via a color-coded indicator in the GUI (green = clicking, red = not clicking).
4. Close the application gracefully using an **Exit** button or the window’s close button.

> **Note**: This tool was tested on macOS due to its reliance on the Quartz library. For other operating systems, different libraries or modifications would be necessary.

---

## Table of Contents

1. [Features](#features)  
2. [Dependencies](#dependencies)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Detailed Code Explanation](#detailed-code-explanation)  
    1. [Global Variables](#1-global-variables)  
    2. [Mouse Click Helpers](#2-mouse-click-helpers)  
    3. [Threading Functions: Start/Stop Clicking](#3-threading-functions-startstop-clicking)  
    4. [Quartz Key Listener](#4-quartz-key-listener)  
    5. [Tkinter Setup](#5-tkinter-setup)  
    6. [UI Polling](#6-ui-polling)  
    7. [Starting Everything](#7-starting-everything)  
6. [Security & Permissions](#security--permissions)  
7. [Troubleshooting](#troubleshooting)  
8. [License](#license)

---

## Features

- **Hotkey-based control**  
  - Press the `[` key to start auto-clicking.  
  - Press the `]` key to stop auto-clicking.
- **User-friendly GUI**  
  - A color-coded indicator showing clicking status (green) or idle (red).  
  - A slider to adjust the click rate from 50ms to 1000ms.  
  - An Exit button to close cleanly.
- **Multithreaded**  
  - A dedicated thread handles continuous clicking.  
  - Another dedicated thread listens for global hotkey presses using Quartz.  
- **Minimal resource usage** when idle.

---

## Dependencies

1. **Python 3.x** (3.7 or higher recommended)  
2. [**pyautogui**](https://pypi.org/project/PyAutoGUI/)  
3. **Tkinter** (usually included with standard Python installations on macOS)  
4. **Quartz** (shipped with macOS-compatible Python frameworks)  
5. **time** (Python standard library)  
6. **threading** (Python standard library)

To install `pyautogui`, run:
```bash
pip install pyautogui
