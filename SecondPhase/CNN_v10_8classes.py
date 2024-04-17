import os

import numpy as np
import json
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Folder containing JSON files
folder_path = '../Data'

json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

all_images = []
all_labels = []

for file in json_files:
    with open(os.path.join(folder_path, file), 'r') as json_file:
        data = json.load(json_file)
    
    images = np.array([item['frame'] for item in data])
    labels = np.array([item['label'] for item in data])

    all_images.append(images)
    all_labels.append(labels)

# Combine data from all files
images = np.concatenate(all_images, axis=0)
labels = np.concatenate(all_labels, axis=0)

# Normalize images to range [0, 1]
images = images / 255.0

# Convert labels to one-hot encoding
num_classes = 8  # 총 클래스 개수
labels = to_categorical(labels - 1, num_classes=num_classes)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Add channel dimension for Conv2D input
X_train = np.expand_dims(X_train, axis=-1)
X_test = np.expand_dims(X_test, axis=-1)

# Define the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(27, 19, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=5)

# Define data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    vertical_flip=True
)

# Fit the data generator to the training data
datagen.fit(X_train)

# Train the model with data augmentation and early stopping callback
history = model.fit(datagen.flow(X_train, y_train, batch_size=256), epochs=50, validation_data=(X_test, y_test), callbacks=[early_stopping])

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Accuracy:", accuracy)

# Generate predictions
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)

# Plot confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# Save the trained model
model.save('trained_model_8classes.h5')
