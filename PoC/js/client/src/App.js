import React, { useEffect, useState, useRef } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Connect to backend

const App = () => {
  const [isVibrating, setIsVibrating] = useState(false); // To ensure only one vibration/audio play at a time
  const audioRef = useRef(new Audio("HappyNewYear.m4a")); // Reuse the same audio object

  useEffect(() => {
    // Send mouse click event when clicked
    const handleClick = (event) => {
      console.log("Mouse Clicked:", { x: event.clientX, y: event.clientY });
      socket.emit("mouse_click", { x: event.clientX, y: event.clientY });
    };

    // Listen for click events from other devices
    socket.on("mouse_click_received", () => {
      console.log("Mouse click received!");

      // Ensure vibration and audio only play once
      if (!isVibrating) {
        setIsVibrating(true);

        // Check for vibration support and vibrate if available
        if (navigator.vibrate) {
          console.log("Vibration supported on this device");
          navigator.vibrate(200); // Vibrate phone for 200ms
        } else {
          console.log("Vibration not supported on this device");
        }

        // Play audio if it's not already playing
        if (audioRef.current.paused) {
          audioRef.current.play();
        }

        // Reset after a short delay
        setTimeout(() => setIsVibrating(false), 300); // 300ms to reset the state
      }
    });

    window.addEventListener("click", handleClick);
    return () => window.removeEventListener("click", handleClick);
  }, [isVibrating]);

  // Direct vibration test button
  const handleTestVibrate = () => {
    if (navigator.vibrate) {
      console.log("Test: Vibration supported on this device");
      navigator.vibrate(200); // Vibrate phone for 200ms
    } else {
      console.log("Test: Vibration not supported on this device");
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontSize: "24px",
      }}
    >
      <div>
        <h1>Click anywhere to send an event!</h1>
        <button onClick={handleTestVibrate}>Test Vibration</button>
      </div>
    </div>
  );
};

export default App;
