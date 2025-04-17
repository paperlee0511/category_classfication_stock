import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran  # korea natural languge
from sklearn.preprocessing import label_binarize, LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re


df =pd.read_csv('./crawling_data/news_title_data.csv')
df.info()
print(df.head(30))

# 전처리 하기
# 카테고리별 데이터가 불균일하면 많은것을 버려야 한다.
print(df.category.value_counts())

X = df.titles
Y = df.category

print(X[1])
okt = Okt()
okt_x = okt.morphs(X[1])
print(okt_x)
okt_x = okt.morphs(X[1], stem=True)
print(okt_x)

komoran = Komoran()
komoran_x = komoran.morphs(X[1])
print(komoran_x)

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
# Culture는 인덱스 0, Economic 은 1
# 엔코더 저장하기
with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_y = to_categorical(labeled_y)
print(onehot_y)
cleaned_x = re.sub('[^가-힣]', ' ', X[1])
print(X[1])
print(cleaned_x)

# X 전처리
for i in range(len(X)):
    X[i] = re.sub('[^가-힣]',' ', X[i])
    X[i] = okt.morphs(X[i], stem = True)
    if i % 1000 == 0:
        print(i)
print(X)

#sentence를 문자로 받음
for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        print(word)
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)

print(X)

# 토크나이저 : 형태소에 라벨을 붙여준다.
# 무엇에 라벨을 붙여줄지 없으니.
# 이 토큰한테 정보를 주고,
token = Tokenizer()
token.fit_on_texts(X) # 이 X안에 문장들, 형태소들에 라벨을 부여한다.
tokened_x = token.texts_to_sequences(X)
print(tokened_x)
wordsize = len(token.word_index) + 1 # word index : 형태소들에 라벨을 쫙 붙여줬는데 그 인덱스
print(wordsize)

# 길이 맞춰줘야함, 긴것을 자르면 데이터 손실이니 짧은것 앞에 0을 붙일거임
# 최댓값 찾는 알고리즘
max = 0
for sentence in tokened_x :
    if max < len(sentence) :
        max = len(sentence)
print(max)

with open('./models/token_max_{}.pickle'.format(max), 'wb') as f:
    pickle.dump(token, f)

# 길이에 맞게 모자란만큼 0으로 채워짐
x_pad = pad_sequences(tokened_x, max)
print(x_pad)

x_train, x_test, y_train, y_test = train_test_split(
    x_pad, onehot_y, test_size= 0.1)

print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

np.save('./crawling_data/title_x_train_wordsize{}'.format(wordsize), x_train)
np.save('./crawling_data/title_x_test_wordsize{}'.format(wordsize), x_test)
np.save('./crawling_data/title_y_train_wordsize{}'.format(wordsize), y_train)
np.save('./crawling_data/title_y_test_wordsize{}'.format(wordsize), y_test)


