import json
import numpy as np

def generate_similar_frame(original_frame):
    noise = np.random.normal(scale=0.001, size=original_frame.shape)  # 노이즈 생성
    noisy_frame = original_frame.copy()  # 원본 프레임 복사
    non_zero_indices = np.where(original_frame > 0)  # 0이 아닌 양수의 인덱스 찾기
    noisy_frame[non_zero_indices] += noise[non_zero_indices]  # 노이즈를 추가할 인덱스에만 더하기
    # 음수를 0으로 변환
    noisy_frame[noisy_frame < 0] = 0
    return noisy_frame

def generate_synthetic_data(input_file, num_samples_per_label, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    synthetic_data = []
    for entry in data:
        label = entry['label']
        for _ in range(num_samples_per_label):
            sample = {
                "time": entry["time"],
                "label": label,
                "sep": True,
                "frame": generate_similar_frame(np.array(entry["frame"])).tolist()  # NumPy 배열을 리스트로 변환하여 저장
            }
            synthetic_data.append(sample)

    with open(output_file, 'w') as file:
        json.dump(synthetic_data, file, indent=4)

# 예시 사용법
input_file = "Data/all_frames.json"
output_file = "Data/output_4x100x10.json"
num_samples_per_label = 10
generate_synthetic_data(input_file, num_samples_per_label, output_file)
