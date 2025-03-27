import asyncio
from pynput.mouse import Listener
import websockets
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env")

IP_ADDR = os.getenv("IP_ADDR")


# Send mouse click data (including coordinates) to the server
async def send_click(x, y):
    uri = "ws://" + IP_ADDR + ":8765"  # Server URL
    try:
        async with websockets.connect(uri) as websocket:
            # Create a dictionary to hold the mouse click and coordinates
            message = {"click": True, "x": x, "y": y}
            await websocket.send(
                json.dumps(message)
            )  # Send the mouse click and coordinates to the server
            print(
                f"Mouse click sent! Coordinates: {x}, {y}"
            )  # Log the click coordinates
    except Exception as e:
        print(f"Error while sending click: {e}")  # Log any errors while sending data


# Handle mouse click events
def on_click(x, y, button, pressed):
    if pressed:  # Only when the button is pressed
        print(f"Mouse click detected at ({x}, {y})")  # Log the detected coordinates
        asyncio.run(send_click(x, y))  # Send the coordinates to the server


# Start listening for mouse events
def start_mouse_listener():
    with Listener(on_click=on_click) as listener:
        listener.join()


# Run the mouse listener
if __name__ == "__main__":
    start_mouse_listener()
