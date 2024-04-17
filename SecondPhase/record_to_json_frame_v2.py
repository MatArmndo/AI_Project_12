import cv2
import numpy as np
import json
from support_functions import TSPDecoder, AsciiDecoder

# Initialize TSPDecoder
rows = 27
columns = 19
TSP = TSPDecoder(rows=rows, columns=columns)

tot = np.zeros((rows, columns))

# Initialize variables
data = []

# Flag for drawing mode
drawing = False
current_label = None

# Function to handle key presses
def handle_key(key):
    global drawing, current_label, data, tot

    if key.isdigit():
        drawing = True
        current_label = int(key)
    elif key == 'c':
        drawing = False
        current_label = None
        tot = np.zeros((rows, columns))
    elif key == 'q':
        save_data()
        exit()

# Function to save recorded data to a JSON file
def save_data():
    # Convert NumPy arrays to Python lists
    for item in data:
        item["frame"] = item["frame"].tolist()

    if data:
        with open('../Data/recorded_flames_fires.json', 'w') as json_file: # it needs to be change everytime being recorded by a person
            json.dump(data, json_file)

# Main loop to capture frames and record data
while TSP.available:
    # Read frame from TSPDecoder
    grid = TSP.readFrame()
    tot = np.maximum(tot, grid)
    tmp = cv2.resize(tot, (rows*10, columns*10))

    # Show frame
    cv2.imshow("Drawing", tmp.astype(np.uint8))
    key = cv2.waitKey(1)
    key = AsciiDecoder(key)

    # Handle key presses
    handle_key(key)

    # Record drawing if in drawing mode and tot is not empty
    if drawing and np.any(tot != 0):
        data.append({
            "label": current_label,
            "frame": np.copy(tot)  # Create a copy of tot to store in data
        })

    # Check if 'c' is pressed and save the data
    if not drawing and current_label is not None:
        data.append({
            "label": current_label,
            "frame": np.copy(tot)  # Create a copy of tot to store in data
        })
        current_label = None
        tot = np.zeros((rows, columns))  # Clear the drawing

# Release resources
cv2.destroyAllWindows()
