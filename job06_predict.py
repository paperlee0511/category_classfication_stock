# 오늘헤드라인 뉴스 긁어서 예측 정확도 보기

import pickle
import pandas as pd
import numpy as np
from keras.utils import to_categorical
from konlpy.tag import Okt
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import re



df = pd.read_csv('./crawling_data/naver_headline_news_20250418.csv')
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(df.head())
df.info()
print(df.category.value_counts())

X = df.titles
Y = df.category

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
label = encoder.classes_
print(label)

# 트랜스폼, p트랜스폼? 알아보기
labeled_y = encoder.transform(Y)
onehot_y = to_categorical(labeled_y)
print(onehot_y)

# 전처리 똑같이 하기 뭐랑? job4, 5? 에서했던 전처리 똑같이 해주기
okt =Okt()
for i in range(len(X)):
    # 숫자, 영어 지우기
    X[i] = re.sub('[^가-힣]', ' ', X[i])
    X[i] = okt.morphs(X[i], stem=True)
print(X)

for idx, sentence in enumerate(X):
    words = []
    for word in sentence:
        print(word)
        if len(word) > 1:
            words.append(word)
    X[idx] = ' '.join(words)

print(X[:10])
# 앞에 0을 넣는것은 앞에 데이터를 넣으면 학습할 때 기억이 희미해지는것을 완화하기 위해
# 모르는 단어는 0으로 바뀜
# 토크나이저 알아보기

with open('./models/token_max_25.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_x = token.texts_to_sequences(X)
print(tokened_x[:5])

# 25개보다 길면 뒤쪽으로 잘라냄
for i in range(len(tokened_x)):
     if len(tokened_x[i]) > 25:
         tokened_x[i] = tokened_x[i][:25]

x_pad = pad_sequences(tokened_x, 25)
print(x_pad)

model = load_model('./models/news_section_classfication_model_0.7365208268165588.h5')
preds = model.predict(x_pad)
print(preds)

# 예측한것이 이코노미다. 바꿔볼것
predict_section = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0 # 이렇게 하고 아래, 두번째 값이 최댓값이 됨
    second = label[np.argmax(pred)]
    predict_section.append([most, second])
print(predict_section)

df['predict'] = predict_section
print(df[['category', 'predict']].head(30))

score = model.evaluate(x_pad, onehot_y)
print(score[1])

df['OX'] = 0
for i in range(len(df)) :
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = 1
print(df.OX.mean()) #

# 다 끝났으니 리콰이먼츠 만들기
# pip freeze > requirements.txt
