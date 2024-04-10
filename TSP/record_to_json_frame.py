import cv2
import numpy as np
import json
import time
from support_functions import TSPDecoder, AsciiDecoder

rows = 27
columns = 19

# Initialize the TSPDecoder
TSP = TSPDecoder(rows=rows, columns=columns)

tot = np.zeros((rows, columns))

# Initialize a list to store recorded data
data = []

# Flag for drawing mode.
# when starting to draw the flag 'sep' needs to be True
# read the frame when a digit is pressed.
sep = False

while TSP.available:
    # Read frame from TSPDecoder
    grid = TSP.readFrame()
    tot = np.maximum(tot, grid)

    tmp = cv2.resize(tot, (rows*10, columns*10))

    # Visualizing the frame
    cv2.imshow("Drawing", tmp.astype(np.uint8))
    key = cv2.waitKey(1)
    key = AsciiDecoder(key)

    # Record the drawing data only when a digit key is pressed
    # if the key is digit, append the data. with sep --> true. the sep goes False only 'c' is pressed
    if key.isdigit():
        sep = not sep
        data.append({
            "time": time.time(),  # Timestamp
            "label": key,  # Label for the drawn digit
            "sep": sep,  # Separator boolean
            "frame": grid  # Frame data
        })

    # Toggle drawing mode if 'c' is pressed
    if key == "c":
        tot = np.zeros((rows, columns))  # Clear the drawing
        #sep = False  # Reset the sep flag

    # Exit if 'q' is pressed
    if key == 'q':
        if data:  # Check if data is not empty
            with open('air_2.json', 'a') as json_file:  # Append mode
                json.dump(data, json_file, indent=0)
        exit()

# Release resources
cv2.destroyAllWindows()
