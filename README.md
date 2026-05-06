Smart Traffic Management System with AI
This project is an AI-driven traffic signal controller designed to reduce congestion and prioritize emergency vehicles. It solves the common frustration of waiting at a red light when no opposing traffic is present.

Key Features
Dynamic Signal Timing: Uses YOLOv8 to count vehicles in 4 directions (North, South, East, West) and gives the green light to the lane with the highest density.

Emergency Override: Automatically detects ambulances (or priority vehicles) and forces an immediate green light to save lives.

Computer Vision: Implemented using Python, OpenCV, and the Ultralytics YOLOv8 model.

How it Works
The system analyzes real-time snapshots of a 4-way intersection. If an ambulance is detected in any lane, it overrides all other logic. If no emergency is present, it calculates which lane has the most traffic and switches the signal accordingly.

Tech Stack
Language: Python

AI Model: YOLOv8 (Object Detection)

Libraries: OpenCV, Ultralytics
