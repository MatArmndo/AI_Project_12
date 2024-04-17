import cv2
from SecondPhase.support_functions import *
from FirstPhase.CNN_v5 import model

rows = 27
cols = 19

# TSPDecoder 초기화
TSP = TSPDecoder(rows=rows, columns=cols)

tot = np.zeros((rows, cols))

# 변수 초기화
data = None

while TSP.available:
    # TSP에서 프레임 읽기
    grid = TSP.readFrame()
    tot = np.maximum(tot, grid)

    tmp = cv2.resize(tot, (rows*10, cols*10))  # c수정된 부분

    # 프레임 시각화
    cv2.imshow("Drawing", tmp.astype(np.uint8))
    key = cv2.waitKey(1)
    key = AsciiDecoder(key)

    if key == "c":
        tot = np.zeros((rows, cols))  # 그림 초기화
        data = None

    if key == 'v':
        if data is None:
            data = grid

            # 데이터 포맷 변환
            data_array = np.expand_dims(data, axis=0)
            data_array = np.expand_dims(data_array, axis=-1)
            data_array = data_array.astype('float32') / 255.0

            # 모델 예측
            prediction = model.predict(data_array)
            predicted_label = np.argmax(prediction)

            print("Predicted Label:", predicted_label)
            print("Prediction:", prediction)

            # 데이터 초기화
            data = None

    if key == 'q':
        break

# OpenCV 창 닫기
cv2.destroyAllWindows()
