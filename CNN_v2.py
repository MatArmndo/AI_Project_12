import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns

# 데이터 불러오기
with open('TSP/all_frames.json', 'r') as file:
    data = json.load(file)

# 데이터 전처리
images = np.array([frame['frame'] for frame in data])
labels = np.array([int(frame['label']) for frame in data])  # 라벨 값을 0부터 시작하도록 수정

# 데이터 형태 수정 (RGB 이미지가 아니므로 channel은 1)
images = images.reshape((images.shape[0], 27, 19, 1)).astype('float32') / 255.0

# 훈련 세트와 테스트 세트로 데이터 나누기
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# 모델 정의
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(27, 19, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')  # 라벨의 종류가 4개이므로 출력 뉴런은 4개
])

# 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 모델 학습
history = model.fit(x_train, y_train, epochs=84, validation_split=0.2) # 84 epochs are the most sufficient

# 모델 평가
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print("Test Accuracy:", test_accuracy)

# 혼동 행렬
predictions = np.argmax(model.predict(x_test), axis=1)
conf_matrix = confusion_matrix(y_test, predictions)
sns.heatmap(conf_matrix, annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title('Confusion Matrix')
plt.show()
