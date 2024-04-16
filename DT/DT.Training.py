import tensorflow as tf
from sklearn.model_selection import train_test_split
import json
import numpy as np
import matplotlib.pyplot as plt
import sklearn.tree
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns


# Load and combine MNIST dataset

# Load the JSON file
with open("../TSP/all_frames.json", 'r') as file:
    data = json.load(file)

# Extract features (x) and labels (y) from the JSON data
x = np.array([line["frame"] for line in data])
y = np.array([int(line["label"]) for line in data])

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Reshape the data for Decision Tree
x_train_flat = x_train.reshape(x_train.shape[0], -1)
x_test_flat = x_test.reshape(x_test.shape[0], -1)

# Build your Decision Tree model here
decision_tree_model = sklearn.tree.DecisionTreeClassifier(max_depth=5, min_samples_split=2)
decision_tree_model.fit(x_train_flat, y_train)


# Evaluate the model
y_pred = decision_tree_model.predict(x_test_flat)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print accuracy
print("Accuracy:", accuracy)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title('Confusion Matrix for Decision Tree')
plt.show()