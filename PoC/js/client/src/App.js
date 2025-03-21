import React, { useEffect } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Connect to backend

const App = () => {
  useEffect(() => {
    // Send mouse click event when clicked
    const handleClick = (event) => {
      console.log("Mouse Clicked:", { x: event.clientX, y: event.clientY });
      socket.emit("mouse_click", { x: event.clientX, y: event.clientY });
    };

    // Listen for click events from other devices
    socket.on("mouse_click_received", () => {
      console.log("Mouse click received!");
      if (navigator.vibrate) navigator.vibrate(200); // Vibrate phone
      new Audio("HappyNewYear.m4a").play(); // Play sound
    });

    window.addEventListener("click", handleClick);
    return () => window.removeEventListener("click", handleClick);
  }, []);

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
      Click anywhere to send an event!
    </div>
  );
};

export default App;
