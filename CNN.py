import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
import json

# Load the data from 'all_frames.json'
with open('TSP/all_frames.json', 'r') as file:
    data = json.load(file)

# Preprocess the data
images = np.array([frame['frame'] for frame in data])
labels = np.array([int(frame['label']) for frame in data])

# Reshape and normalize the images
images = images.reshape((images.shape[0], 27, 19, 1)).astype('float32') / 255.0

# Create train/test split
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=42)

# Define the model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(27, 19, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Set hyperparameters
epochs = 10
batch_size = 32
validation_split = 0.4

# Train the model
history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split)

# Plot Training and Validation Loss
plt.figure(figsize=(5, 5))
plt.plot(history.history['loss'], label='Train Loss', color='orange')
plt.plot(history.history['val_loss'], label='Validation Loss', color='blue')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Training and Validation Loss')
plt.show()

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(x_test, y_test)

# Print test accuracy
print("Test Accuracy:", test_accuracy)

# Confusion Matrix
plt.figure(figsize=(8, 6))
predictions = model.predict(x_test)
predicted_classes = np.argmax(predictions, axis=1)
conf_matrix = confusion_matrix(y_test, predicted_classes)

sns.heatmap(conf_matrix, annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title('Confusion Matrix')
plt.show()
