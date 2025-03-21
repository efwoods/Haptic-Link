# Haptic-Link
This application will allow for haptics to be enabled by a user's apple watch or phone for each time a user clicks a mouse.

## Proof-of-Concept
Plan to Complete in 4 Hours
1. Detect Mouse Clicks on macOS/PC (30-45 mins)

    Use pynput (Python) to detect mouse clicks.
    Run a local Python script to monitor clicks.

2. Communicate with Apple Watch (1 hour)

    Use Shortcuts & Web Requests for rapid prototyping:
        The Python script sends HTTP requests to trigger haptic feedback on the Watch.
        Use a shortcut that plays a haptic feedback pattern.

3. Implement Haptic Intensity Scaling (45 mins)

    Track click frequency to determine intensity.
    If a click is held, trigger light haptic feedback.

4. Test & Debug (1 hour)

    Tune the haptic response timing.
    Check latency between mouse clicks and Watch response.

```bash
pip install pynput requests
```

2. Create a Python Script for Mouse Click Detection

```python
from pynput import mouse
import requests
import time

# Apple Shortcuts webhook URL (replace with yours)
WEBHOOK_URL = "http://your-local-server-or-shortcut-url"

# Tracking mouse activity
last_click_time = 0
click_count = 0

def on_click(x, y, button, pressed):
    global last_click_time, click_count
    
    if pressed:
        current_time = time.time()
        
        # Track frequency of clicks
        if current_time - last_click_time < 1.0:  # Clicking rapidly
            click_count += 1
        else:
            click_count = 1
        
        last_click_time = current_time
        
        # Determine intensity
        intensity = min(click_count, 5)  # Scale from 1 to 5

        # Send request to Apple Watch shortcut
        requests.post(WEBHOOK_URL, json={"intensity": intensity, "held": False})

def on_release(x, y, button):
    # Detect held click
    requests.post(WEBHOOK_URL, json={"intensity": 1, "held": True})

# Start listening for mouse clicks
with mouse.Listener(on_click=on_click, on_release=on_release) as listener:
    listener.join()
```
3. Create an Apple Shortcut to Trigger Haptics

    Open the Shortcuts app on your iPhone.
    Create a new shortcut:
        Add "Receive Web Request" (set method to POST).
        Add "If condition":
            If held is true, trigger a light haptic.
            Otherwise, trigger a haptic with intensity based on intensity.
        Save and copy the webhook URL.
    Replace WEBHOOK_URL in the Python script with this URL.


Execution

    Run the Python script:

```bash

python mouse_haptic.py
```

Click your mouse and feel the Apple Watch haptic feedback!

Expected Outcome in 4 Hours

✅ Mouse clicks trigger haptic feedback on your Apple Watch
✅ Holding a click causes a light buzz
✅ Clicking faster increases intensity

This is the fastest approach without needing a dedicated watchOS app. You can refine it later with a more advanced Bluetooth-based approach.

Do you want to extend this further with a real-time display of click frequency?


## Minimum-Viable-Product

Got it! Here's how we can design the solution where the iPhone and Apple Watch apps function independently of each other, meaning either one can receive the WebSocket data and trigger haptic feedback. Additionally, the MacBook app will send click events to whichever device (iPhone or Apple Watch) is connected, without requiring both to be present at the same time.
Key points for the new structure:

    MacBook App (macOS): Detects mouse clicks and sends WebSocket messages to either the iPhone or Apple Watch (or both if they are present).
    iPhone and Apple Watch Apps: Each app will independently receive WebSocket messages and trigger haptic feedback on its own device.
    No dependency between iPhone and Apple Watch: If the app is installed on either device, it will work independently to receive clicks and trigger feedback. If both are installed, they can both work simultaneously.
    WebSocket server: We'll set up a WebSocket server that can handle communication between the MacBook and whichever device (iPhone or Apple Watch) is connected.

High-Level Architecture:

    MacBook App: Detects mouse clicks and sends messages via WebSocket.
    iPhone/Apple Watch Apps: Each listens for WebSocket messages and triggers haptic feedback.
    Cross-platform: The MacBook app can run on Windows, Linux, or macOS to send WebSocket messages to either the iPhone or Apple Watch, which are running their own apps.

Code Implementation:
MacBook App (macOS): Detect mouse clicks and send WebSocket messages

This app sends mouse click data to either the iPhone or Apple Watch via WebSocket.

```swift
import Cocoa
import Starscream

class MouseClickListener: NSApplication {
    var socket: WebSocket!

    override init() {
        super.init()
        setupWebSocket()
        startMouseClickDetection()
    }

    func setupWebSocket() {
        // Replace with the actual IP of the device (iPhone or Apple Watch)
        var request = URLRequest(url: URL(string: "ws://<device-ip>:<port>")!)
        socket = WebSocket(request: request)
        socket.delegate = self
        socket.connect()
    }

    func startMouseClickDetection() {
        NSEvent.addGlobalMonitorForEvents(matching: .leftMouseDown) { event in
            self.sendClickData(event: event)
        }
    }

    func sendClickData(event: NSEvent) {
        let clickData: [String: Any] = [
            "event": "click",
            "button": "left",
            "position": ["x": event.locationInWindow.x, "y": event.locationInWindow.y]
        ]
        if let message = try? JSONSerialization.data(withJSONObject: clickData, options: []) {
            socket.write(data: message)
        }
    }
}

extension MouseClickListener: WebSocketDelegate {
    func websocketDidConnect(socket: WebSocketClient) {
        print("WebSocket connected.")
    }

    func websocketDidDisconnect(socket: WebSocketClient, error: Error?) {
        print("WebSocket disconnected: \(error?.localizedDescription ?? "No error")")
    }

    func websocketDidReceiveMessage(socket: WebSocketClient, text: String) {
        print("Received message: \(text)")
    }

    func websocketDidReceiveData(socket: WebSocketClient, data: Data) {
        print("Received data: \(data)")
    }
}

let app = MouseClickListener()
app.run()
```

iPhone and Apple Watch Apps: WebSocket client to receive data and trigger haptic feedback

Both the iPhone and Apple Watch apps will independently receive WebSocket messages and trigger the appropriate feedback.
iPhone App (haptic feedback)

```swift

import UIKit
import Starscream
import AudioToolbox

class ClickReceiverViewController: UIViewController, WebSocketDelegate {
    var socket: WebSocket!

    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Connect to WebSocket server (MacBook IP address)
        var request = URLRequest(url: URL(string: "ws://<macbook-ip>:<port>")!)
        socket = WebSocket(request: request)
        socket.delegate = self
        socket.connect()
    }

    func websocketDidConnect(socket: WebSocketClient) {
        print("WebSocket connected")
    }

    func websocketDidDisconnect(socket: WebSocketClient, error: Error?) {
        print("WebSocket disconnected: \(String(describing: error))")
    }

    func websocketDidReceiveMessage(socket: WebSocketClient, text: String) {
        print("Received message: \(text)")
        
        // Handle the received click data
        if let data = text.data(using: .utf8),
           let message = try? JSONDecoder().decode([String: Any].self, from: data) {
            handleMouseClickData(message)
        }
    }

    func websocketDidReceiveData(socket: WebSocketClient, data: Data) {
        // Handle received binary data if needed
    }

    func handleMouseClickData(_ data: [String: Any]) {
        // Trigger vibration on iPhone
        triggerVibration()  // Vibration on iPhone
    }

    func triggerVibration() {
        AudioServicesPlaySystemSound(kSystemSoundID_Vibrate)  // Vibration on iPhone
    }
}
```

Apple Watch App (haptic feedback)

```swift
import WatchKit
import Starscream

class InterfaceController: WKInterfaceController, WebSocketDelegate {
    var socket: WebSocket!

    override func awake(withContext context: Any?) {
        super.awake(withContext: context)

        // Connect to WebSocket server (MacBook IP address)
        var request = URLRequest(url: URL(string: "ws://<macbook-ip>:<port>")!)
        socket = WebSocket(request: request)
        socket.delegate = self
        socket.connect()
    }

    func websocketDidConnect(socket: WebSocketClient) {
        print("WebSocket connected")
    }

    func websocketDidDisconnect(socket: WebSocketClient, error: Error?) {
        print("WebSocket disconnected: \(String(describing: error))")
    }

    func websocketDidReceiveMessage(socket: WebSocketClient, text: String) {
        print("Received message: \(text)")

        // Handle the received click data
        if let data = text.data(using: .utf8),
           let message = try? JSONDecoder().decode([String: Any].self, from: data) {
            handleMouseClickData(message)
        }
    }

    func websocketDidReceiveData(socket: WebSocketClient, data: Data) {
        // Handle received binary data if needed
    }

    func handleMouseClickData(_ data: [String: Any]) {
        // Trigger haptic feedback on Apple Watch
        triggerHapticFeedback()  // Haptic feedback on Apple Watch
    }

    func triggerHapticFeedback() {
        WKInterfaceDevice.current().play(.click)  // Haptic feedback on Apple Watch
    }
}

```

Step 2: Cross-Platform (Linux and Windows)

For Linux and Windows, you can use a Python script to detect mouse clicks and send the data to the iPhone app via WebSocket.

```python
import asyncio
import websockets
from pynput.mouse import Listener
import json

# WebSocket server address (running on the iPhone)
SERVER_URI = "ws://<iPhone-IP>:<port>"

# Function to detect mouse click
def on_click(x, y, button, pressed):
    if pressed:
        message = {
            "event": "click",
            "button": str(button),
            "position": {"x": x, "y": y}
        }
        asyncio.run(send_message(message))

async def send_message(message):
    async with websockets.connect(SERVER_URI) as websocket:
        # Send the message as a JSON string
        await websocket.send(json.dumps(message))

# Start listening to mouse events
with Listener(on_click=on_click) as listener:
    listener.join()

```

Step 3: Testing and Deployment

    Test the MacBook App: Ensure that mouse clicks are detected and sent via WebSocket.
    Test the iPhone/Apple Watch Apps: Ensure that they receive the WebSocket messages and trigger the appropriate haptic feedback.
    Deploy to App Store: Use Xcode to deploy the iPhone and Apple Watch apps to the App Store. If you need to distribute the macOS app, use Notarization for macOS.

Conclusion

    MacBook detects mouse clicks and sends the data to either the iPhone or Apple Watch via WebSocket.
    Both the iPhone and Apple Watch receive the WebSocket messages and provide haptic feedback independently.
    Linux and Windows can use a Python script to send mouse click events to the iPhone app.

This structure allows the app to work with either the iPhone or Apple Watch independently or together, based on which device is available. Let me know if you need further details or assistance with deployment!


## Android Users
To add Android support for the haptic feedback application (where the Android app will receive the WebSocket messages and trigger vibration feedback on mouse clicks), you need to follow a similar architecture to the iPhone and Apple Watch apps.

Here’s how we can approach building an Android app that works similarly to the iPhone and Apple Watch apps:
Steps for Android App Development:

    Android App: The app will receive WebSocket messages from the MacBook app and trigger a vibration when it receives mouse click data.
    WebSocket Client: We'll use the Java WebSocket client library to connect to the WebSocket server and handle messages.
    Haptic Feedback: The Android device will vibrate based on the received WebSocket messages (mouse clicks).

Step 1: Set Up WebSocket Client in Android

We will use org.java-websocket for handling WebSocket connections in Android. To add this dependency, you can include it in the build.gradle file.

```gradle
// In your app-level build.gradle file:
dependencies {
    implementation 'org.java-websocket:Java-WebSocket:1.5.2'  // Add WebSocket dependency
}
```

Step 2: Android Activity with WebSocket

Create an Activity in Android that will receive WebSocket messages and trigger vibration on the Android device when mouse clicks are detected.

Here’s the code for the Android Activity:

```java

package com.example.hapticfeedback;

import android.app.Activity;
import android.os.Bundle;
import android.os.Vibrator;
import android.widget.Toast;

import org.java-websocket.client.WebSocketClient;
import org.java-websocket.handshake.ServerHandshake;

import java.net.URI;
import java.net.URISyntaxException;

public class MainActivity extends Activity {

    private WebSocketClient mWebSocketClient;
    private Vibrator vibrator;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        vibrator = (Vibrator) getSystemService(VIBRATOR_SERVICE);

        // Connect to WebSocket server (replace with MacBook's IP and port)
        try {
            URI uri = new URI("ws://<macbook-ip>:<port>");
            mWebSocketClient = new WebSocketClient(uri) {
                @Override
                public void onOpen(ServerHandshake handshakedata) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(MainActivity.this, "Connected to WebSocket", Toast.LENGTH_SHORT).show();
                        }
                    });
                }

                @Override
                public void onMessage(final String message) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            handleClickData(message);
                        }
                    });
                }

                @Override
                public void onClose(int code, String reason, boolean remote) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(MainActivity.this, "WebSocket Closed", Toast.LENGTH_SHORT).show();
                        }
                    });
                }

                @Override
                public void onError(Exception ex) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Toast.makeText(MainActivity.this, "WebSocket Error: " + ex.getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    });
                }
            };

            // Connect WebSocket
            mWebSocketClient.connect();

        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
    }

    // Handle the received WebSocket message (mouse click data)
    private void handleClickData(String message) {
        // Sample message structure { "event": "click", "button": "left", "position": {"x": 100, "y": 150} }
        if (message.contains("click")) {
            triggerHapticFeedback();
        }
    }

    // Trigger vibration on Android device
    private void triggerHapticFeedback() {
        if (vibrator.hasVibrator()) {
            vibrator.vibrate(100);  // Vibrate for 100 milliseconds
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Close WebSocket connection when activity is destroyed
        if (mWebSocketClient != null) {
            mWebSocketClient.close();
        }
    }
}

```
Step 3: Permissions for Vibration in Android

Ensure your app has the necessary permissions to use vibration on Android. In the AndroidManifest.xml file, add the following permission:

```xml
<uses-permission android:name="android.permission.VIBRATE" />
```
Step 4: Testing the Android App

    Deploy the Android app: Build and install the app on an Android device.
    Ensure WebSocket communication: Make sure the Android device can connect to the MacBook WebSocket server and listen for mouse click events.
    Test vibration: When a mouse click is detected on the MacBook, the Android device should vibrate.

Step 5: Cross-Platform WebSocket Communication

The WebSocket server (on the MacBook) can be shared across all devices (iPhone, Apple Watch, Android) for communication. The MacBook app will send the mouse click data to whichever device (iPhone, Apple Watch, Android) is connected.
Final App Overview

    MacBook App: Detects mouse clicks and sends data to any connected device via WebSocket (iPhone, Apple Watch, Android).
    iPhone App: Receives WebSocket messages and triggers haptic feedback.
    Apple Watch App: Receives WebSocket messages and triggers haptic feedback.
    Android App: Receives WebSocket messages and triggers vibration on the Android device.

Step 6: Deployment to Google Play

Once the Android app is ready, you can deploy it to the Google Play Store following the standard procedure for publishing an app. You’ll need to create a Google Developer account, prepare your app (signed APK/AAB), and submit it for review.
Conclusion

With this Android implementation, you will have an app that works alongside your iPhone and Apple Watch apps to receive mouse click events from the MacBook via WebSocket and provide haptic feedback on Android devices as well.

This completes the cross-platform haptic feedback system for MacBook, iPhone, Apple Watch, and Android devices! Let me know if you need further assistance with the setup.