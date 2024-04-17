import cv2
import numpy as np
import json

# Load data from JSON file
try:
  with open('../Data/recorded_data.json', 'r') as json_file:
    data = json.load(json_file)
except FileNotFoundError:
  print("Error: 'recorded_data.json' file not found.")
  exit()

# Loop through each data item
for item in data:
  # Convert frame list back to NumPy array
  frame = np.array(item["frame"], dtype=np.uint8)  # Convert to uint8 for grayscale

  # Resize frame (optional, adjust parameters as needed)
  resized_frame = cv2.resize(frame, (frame.shape[1] * 10, frame.shape[0] * 10))

  # Display frame with label
  cv2.imshow("Grayscale Frame - Label: " + str(item["label"]), resized_frame)
  cv2.waitKey(0)  # Wait for key press to close window

# Release resources
cv2.destroyAllWindows()
