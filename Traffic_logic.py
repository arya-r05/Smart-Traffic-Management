import cv2
import os
from ultralytics import YOLO

# Load the AI Mode
model = YOLO('yolov8n.pt')

def analyze_lane(image_path, direction):
    if not os.path.exists(image_path):
        print(f"!!! Error: {image_path} not found in the folder !!!")
        return 0, False, None

    # Run AI Detection
    results = model(image_path, conf=0.4, verbose=False)
    
    vehicle_count = 0
    ambulance_present = False
    
    # Check detections
    for r in results:
        for box in r.boxes:
            label = model.names[int(box.cls[0])]
            # Count common vehicles
            if label in ['car', 'motorcycle', 'bus', 'truck']:
                vehicle_count += 1
            # Emergency Logic: Treat 'bus' or 'truck' as ambulance for this simulation
            if label in ['bus', 'truck']: 
                ambulance_present = True

    return vehicle_count, ambulance_present, results[0].plot()

def start_system():
    lanes = ["North", "South", "East", "West"]
    images = ["north_lane.jpg", "south_lane.jpg", "east_lane.jpg", "west_lane.jpg"]
    data = []

    print("\n--- AI IS ANALYZING THE INTERSECTION ---")
    for i in range(4):
        count, emg, img_plot = analyze_lane(images[i], lanes[i])
        data.append({"name": lanes[i], "count": count, "emergency": emg, "image": img_plot})
        if img_plot is not None:
            print(f"-> {lanes[i]} Lane: {count} vehicles detected.")

    # DECISION LOGIC: 
    # 1st Priority: Any lane with an Emergency vehicle
    # 2nd Priority: Lane with the highest vehicle count
    green_lane = next((l for l in data if l['emergency']), max(data, key=lambda x: x['count']))

    print(f"\nDECISION: Green light given to {green_lane['name']} Lane.")

    # DISPLAY WINDOW
    h, w = 350, 450
    display_list = []
    for d in data:
        if d['image'] is not None:
            resized = cv2.resize(d['image'], (w, h))
            status = "GREEN" if d == green_lane else "RED"
            color = (0, 255, 0) if status == "GREEN" else (0, 0, 255)
            cv2.putText(resized, f"{d['name']}: {status}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            display_list.append(resized)
    
    if len(display_list) == 4:
        top_row = cv2.hconcat([display_list[0], display_list[1]])
        bottom_row = cv2.hconcat([display_list[2], display_list[3]])
        final_view = cv2.vconcat([top_row, bottom_row])
        
        cv2.imshow("Smart Traffic Logic - Bangalore Fix", final_view)
        print("\nWindow opened! Press 'q' or any key on your keyboard to close it.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_system()
