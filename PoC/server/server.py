import asyncio
import websockets
import os
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path="../../.env")

IP_ADDR = os.getenv("IP_ADDR")


# WebSocket server to listen for click events and print coordinates


async def handle_click(websocket):
    print("Server is waiting for a connection...")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                x, y = data.get("x"), data.get("y")
                print(f"Mouse click detected at coordinates: ({x}, {y})")
            except json.JSONDecodeError:
                print(f"Invalid JSON received: {message}")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed by client")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Connection with client closed.")


# Start the WebSocket server
async def main():
    server = await websockets.serve(handle_click, IP_ADDR, 8765)
    print(
        "Server is listening on ws://" + IP_ADDR + ":8765"
    )  # Log when the server starts listening
    try:
        await server.wait_closed()  # Wait for the server to shut down (it will keep running indefinitely)
    except asyncio.CancelledError:
        print(
            "Server was cancelled and is shutting down."
        )  # Log when the server is cancelled


# Run the server
if __name__ == "__main__":
    try:
        asyncio.run(main())  # Start the server
    except Exception as e:
        print(
            f"Server encountered an error: {e}"
        )  # Log if an error occurs while running the server
