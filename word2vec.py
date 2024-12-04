from gensim.models import Word2Vec

# 예제 데이터
sentences = [
    ['the', 'cat', 'sat', 'on', 'the', 'mat'],
    ['the', 'dog', 'barked', 'at', 'the', 'cat']
]

# Word2Vec 모델 학습
model = Word2Vec(sentences, vector_size=50, window=3, min_count=1, sg=1)  # Skip-gram

# 단어 벡터 확인
print("Word vector for 'cat':")
print(model.wv['cat'])

# 단어 유사도 확인
print("\nSimilarity between 'cat' and 'dog':")
print(model.wv.similarity('cat', 'dog'))

# 가장 유사한 단어 찾기
print("\nMost similar to 'cat':")
print(model.wv.most_similar('cat'))