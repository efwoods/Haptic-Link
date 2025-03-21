import pyautogui
import requests
from dotenv import load_dotenv
import os
import threading
import time
import logging
import signal
import sys
from mouse_click import start_listener


# Function to send signal to the iPhone
def send_haptic_feedback(url):
    try:
        logging.info("Sending vibration signal to iPhone...")
        response = requests.post(url)  # Sending a POST request to trigger the vibration
        if response.status_code == 200:
            logging.info("Signal sent successfully!")
        else:
            logging.warning(f"Failed to send signal: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending signal: {e}")


def main():
    load_dotenv()
    iphone_ip = os.getenv("IPHONE_IP")
    url = f"http://{iphone_ip}:5000/vibrate"  # Replace with your iPhone's IP
    # Start listening for mouse clicks in a separate thread
    listener_thread = start_listener()

    # Simulating other tasks in the main program
    try:
        while True:
            print(f"Main thread: {threading.current_thread().name} - Running...")
            time.sleep(2)  # Simulate some task
            send_haptic_feedback(url)  # Simulating haptic feedback based on logic
    except KeyboardInterrupt:
        pass  # Gracefully handle program termination


if __name__ == "__main__":
    main()
