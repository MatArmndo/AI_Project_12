import json
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization

# Step 1: Read the JSON file
with open('../TSP/all_frames.json', 'r') as file:
    data = json.load(file)

# Step 2 and 3: Parse JSON data and extract frame data and labels
frames = []
labels = []
for item in data:
    frames.append(item['frame'])
    labels.append(int(item['label']))  # Assuming label is integer

# Step 4: Preprocess data and split into input sequences and target values
X = np.array(frames)
y = np.array(labels)

# Assuming you want to reshape your input for LSTM
# If your data already has the desired shape, skip this step
# The shape should be (number_of_samples, time_steps, features)
# Adjust the values according to your data's structure
X = X.reshape(X.shape[0], X.shape[1], X.shape[2])

# Step 5: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Build LSTM model with dropout and batch normalization
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))  # Dropout layer for regularization
model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(1, activation='sigmoid'))  # Assuming binary classification
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 7: Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Print the accuracy
train_accuracy = history.history['accuracy'][-1]
test_accuracy = history.history['val_accuracy'][-1]
print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Testing Accuracy: {test_accuracy:.4f}")
