import threading
from clicker import click_loop
from listener import start_key_listener
import ui

click_thread = threading.Thread(target=click_loop, daemon=True)
click_thread.start()

listener_thread = threading.Thread(target=start_key_listener, daemon=True)
listener_thread.start()

ui.root.mainloop()
