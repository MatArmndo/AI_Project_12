import cv2
from SecondPhase.support_functions import *
from FirstPhase.CNN_v4 import model  # CNN_v3.py 파일로부터 모델 불러오기

rows = 27
cols = 19

# initialize the TSPDecoder
TSP = TSPDecoder(rows=rows, columns=cols)

tot = np.zeros((rows, cols))

# 변수를 초기화합니다.
data = None



while TSP.available:
    # TSP에서 프레임을 읽습니다.
    grid = TSP.readFrame()
    tot = np.maximum(tot, grid)

    tmp = cv2.resize(tot, (rows * 10, cols * 10))

    # 프레임을 시각화합니다.
    cv2.imshow("Drawing", tmp.astype(np.uint8))
    key = cv2.waitKey(1)
    key = AsciiDecoder(key)

    # 'c'가 눌리면 데이터를 초기화합니다.
    if key == "c":
        tot = np.zeros((rows, cols))  # 그림 초기화
        data = None

    # 'v'가 눌리면 예측을 수행합니다.
    if key == 'v':
        if data is None:
            data = grid  # 데이터가 없으면 현재 그리드를 저장합니다.

            # 데이터를 적절한 형식으로 변환합니다.
            data_array = np.expand_dims(data, axis=0)  # 배치 차원을 추가합니다.
            data_array = np.expand_dims(data_array, axis=-1)  # 채널 차원을 추가합니다.
            data_array = data_array.astype('float32') / 255.0  # 데이터를 정규화합니다.

            # 모델을 사용하여 예측을 수행합니다.
            prediction = model.predict(data_array)
            predicted_label = np.argmax(prediction)

            print("Predicted Label:", predicted_label)
            print("prediction: ", prediction)

            # 데이터를 초기화합니다.
            data = None

    # 'q'가 눌리면 종료합니다.
    if key == 'q':
        break

# OpenCV 창을 닫습니다.
cv2.destroyAllWindows()
