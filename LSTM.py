import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

# 1. IMDb 데이터셋 준비
max_features = 10000  # 사용할 단어의 최대 개수
maxlen = 200  # 문장의 최대 길이

print("IMDb 데이터 로드 중...")
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

# 데이터 전처리: 패딩
x_train = pad_sequences(x_train, maxlen=maxlen)
x_test = pad_sequences(x_test, maxlen=maxlen)

# 2. LSTM 모델 생성 및 학습
model = Sequential([
    Embedding(max_features, 128, input_length=maxlen),  # 임베딩 레이어
    LSTM(128, return_sequences=False),  # LSTM 레이어
    Dropout(0.5),  # 드롭아웃
    Dense(1, activation='sigmoid')  # 이진 분류
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("모델 학습 중...")
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.2)

# 3. 입력 문장 예측
def predict_sentiment(model, tokenizer, sentence, maxlen):
    # 입력 문장을 정수 시퀀스로 변환
    tokens = tokenizer.texts_to_sequences([sentence])
    tokens_pad = pad_sequences(tokens, maxlen=maxlen)

    # 모델로 예측
    prediction = model.predict(tokens_pad)
    return "긍정" if prediction[0][0] > 0.5 else "부정"

# IMDb 데이터셋의 단어 사전을 기반으로 Tokenizer 생성
word_index = imdb.get_word_index()
word_index = {k: (v + 3) for k, v in word_index.items()}  # IMDb 데이터셋의 어휘 오프셋
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# Tokenizer 객체 생성
index_to_word = {value: key for key, value in word_index.items()}
tokenizer = Tokenizer(num_words=max_features)
tokenizer.word_index = word_index

# 사용자 입력 받기
while True:
    sentence = input("문장을 입력하세요 (종료: 'exit'): ")
    if sentence.lower() == "exit":
        print("프로그램 종료.")
        break
    sentiment = predict_sentiment(model, tokenizer, sentence, maxlen)
    print(f"'{sentence}' -> {sentiment}")
