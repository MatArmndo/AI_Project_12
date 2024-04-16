import cv2
import numpy as np
from keras.models import load_model
from support_functions import *

# Load the trained model
model = load_model('trained_model.h5')  # 훈련된 모델 파일명을 넣어주세요

# Initialize TSPDecoder
rows = 27
columns = 19
TSP = TSPDecoder(rows=rows, columns=columns)

tot = np.zeros((rows, columns))


# Function to predict label
def predict_label(grid):
    # Preprocess the grid
    grid = np.expand_dims(grid, axis=0)
    grid = np.expand_dims(grid, axis=-1)
    grid = grid / 255.0

    # Predict label
    prediction = model.predict(grid)
    predicted_label = np.argmax(prediction) + 1  # 클래스를 1부터 시작하도록 수정

    return predicted_label


# Main loop to capture frames and predict labels
while TSP.available:
    # Read frame from TSPDecoder
    grid = TSP.readFrame()
    tot = np.maximum(tot, grid)
    tmp = cv2.resize(tot, (rows * 10, columns * 10))

    # Show frame
    cv2.imshow("Drawing", tmp.astype(np.uint8))
    key = cv2.waitKey(1)

    # Handle key presses
    if key == ord('c'):
        tot = np.zeros((rows, columns))  # Clear the drawing
    elif key == ord('v'):
        # Predict label
        predicted_label = predict_label(tot)
        print("Predicted Label:", predicted_label)

# Release resources
cv2.destroyAllWindows()
