# mouse_click.py
import logging
import threading
from pynput.mouse import Listener
import time

# Set up logging to log to both the console and a file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler to log to a file
file_handler = logging.FileHandler("logs/mouse_clicks.log")
file_handler.setLevel(logging.INFO)

# Create a console handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Define the on_click function to log and print mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        # Log to both the file and the console
        logger.info(f"Mouse clicked at ({x}, {y}) with {button}")

        # Print thread information to confirm it's running in a separate thread
        print(f"Mouse click event handled by thread: {threading.current_thread().name}")


# Define a function to run the listener on a separate thread
def listen_for_clicks():
    with Listener(on_click=on_click) as listener:
        listener.join()


# Function to start the listener in a separate thread
def start_listener():
    listener_thread = threading.Thread(
        target=listen_for_clicks, name="MouseListenerThread"
    )
    listener_thread.daemon = (
        True  # Allow the thread to exit when the main program exits
    )
    listener_thread.start()
    return listener_thread


# This block ensures that the code only runs when this script is executed directly,
# not when it is imported into another script.
if __name__ == "__main__":
    print("Starting the mouse click listener...")
    start_listener()
    try:
        while True:
            # Keep the main thread running to allow the listener thread to continue
            print(f"Main thread: {threading.current_thread().name} - Running...")
            time.sleep(2)
    except KeyboardInterrupt:
        pass  # Gracefully handle program termination
