import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras import models, layers, losses

with open(f"../TSP/all_frames.json", 'r') as file:
    jsondata = json.load(file)

X = np.array([line["frame"] for line in jsondata])
y = np.array([int(line["label"]) for line in jsondata])

dim_row = 27
dim_col = 19
iters = 15

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)

batch_size = 16


def drop_remain(X, y):
    remain = X.__len__() % batch_size
    if remain == 0:
        return X, y
    else:
        X = X[:-remain, :, :]
        y = y[:-remain]
        return X, y


X_train, y_train = drop_remain(X_train, y_train)
X_test, y_test = drop_remain(X_test, y_test)
X_val, y_val = drop_remain(X_val, y_val)

model = models.Sequential()
model.add(layers.Input(shape=(dim_row, dim_col), batch_size=batch_size))
model.add(layers.LSTM(64, stateful=True, return_sequences=True))
model.add(layers.LSTM(64, stateful=True, return_sequences=True))
model.add(layers.LSTM(64, stateful=True))
model.add(layers.Dense(10))

model.compile(optimizer='adam',
              loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

hist = {'loss':[],'accuracy':[],'val_loss':[],'val_accuracy':[]}
for i in range(iters):
    epoch_hist = model.fit(X_train, y_train, validation_data=(X_val, y_val),
    epochs=1, batch_size=batch_size, verbose=2, shuffle=False)
    for key in hist.keys():
        hist[key].append(epoch_hist.history[key])
    # model.reset_states()
    for layer in model.layers:
        if hasattr(layer, 'reset_states') and callable(layer.reset_states):
            layer.reset_states()

plt.plot(hist['accuracy'], label='accuracy')
plt.plot(hist['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2, batch_size=batch_size)
print(f"Test Loss: {test_loss}, Test Accuracy: {test_acc}")

import seaborn as sns
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

# Make predictions
y_pred = model.predict(X_test, batch_size=batch_size)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = y_test

# Generate the confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Plot the confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
plt.title('Confusion Matrix')
plt.ylabel('Actual Labels')
plt.xlabel('Predicted Labels')
plt.show()