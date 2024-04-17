import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns
import cv2

# Load data
with open('../output_0.0001.json', 'r') as file:
    data = json.load(file)

# Preprocess data
images = np.array([frame['frame'] for frame in data])
labels = np.array([int(frame['label']) - 1 for frame in data])

# Apply morphological operations
def apply_morphological_operations(images):
    processed_images = []
    for img in images:
        img = (img * 255).astype(np.uint8)
        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(img, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        processed_images.append(dilation.astype('float32') / 255.0)
    return np.array(processed_images)

processed_images = apply_morphological_operations(images)
processed_images = processed_images.reshape((processed_images.shape[0], 27, 19, 1)).astype('float32')

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(processed_images, labels, test_size=0.2, random_state=42)

# Data Augmentation
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=10,  # Rotate images randomly up to 10 degrees
    width_shift_range=0.05,  # Shift images horizontally by up to 10%
    height_shift_range=0.05,  # Shift images vertically by up to 10%
    horizontal_flip=True,  # Flip images horizontally
    vertical_flip=True,  # Flip images vertically
    fill_mode='nearest'  # Fill in missing pixels with the nearest value
)
datagen.fit(x_train)

# Define model with L2 regularization
# Define model with dropout layers
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(27, 19, 1)),
    # tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),  # 추가된 합성곱 층
    # tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),  # 추가된 합성곱 층
    # tf.keras.layers.Conv2D(256, (3, 3), activation='relu'),  # 추가된 합성곱 층
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(4, activation='softmax')
])

# Define class weights
class_weights = {0: 1, 1: 1.5, 2: 1, 3: 2}

# Compile model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Define early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Train model with data augmentation and early stopping
history = model.fit(datagen.flow(x_train, y_train, batch_size=128),
                    epochs=100,
                    validation_data=(x_test, y_test),
                    callbacks=[early_stopping],
                    class_weight=class_weights)

# Evaluate model
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("Test Accuracy:", test_accuracy)

# Confusion matrix
predictions = np.argmax(model.predict(x_test), axis=1)
conf_matrix = confusion_matrix(y_test, predictions)
sns.heatmap(conf_matrix, annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title('Confusion Matrix')
plt.show()


from sklearn.metrics import classification_report

# Make predictions on the test set
predictions = np.argmax(model.predict(x_test), axis=1)

# Compute classification report
report = classification_report(y_test, predictions, target_names=["Class 1", "Class 2", "Class 3", "Class 4"])

print("Classification Report:")
print(report)

import matplotlib.pyplot as plt

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
