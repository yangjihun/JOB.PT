import numpy as np
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense

# 샘플 데이터 생성 (시계열 데이터)
X = np.array([
    [[1], [2], [3]],
    [[2], [3], [4]],
    [[3], [4], [5]]
])
y = np.array([4, 5, 6])

# RNN 모델 생성
model = Sequential()
model.add(SimpleRNN(10, activation='tanh', input_shape=(3, 1)))  # 은닉 유닛 10개
model.add(Dense(1))  # 출력층
model.compile(optimizer='adam', loss='mse')

# 모델 학습
model.fit(X, y, epochs=100, verbose=1)