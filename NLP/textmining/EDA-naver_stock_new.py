# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from numpy import dot
from numpy.linalg import norm
import numpy as np
import pandas as pd
from konlpy.tag import Hannanum
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import squarify
import re
from nltk.probability import FreqDist
from wordcloud import WordCloud
from collections import Counter

# +
import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns

# %matplotlib inline

mpl.rcParams['axes.unicode_minus'] = False
# -

from matplotlib import font_manager, rc
f_path = "C:/Windows/Fonts/NanumBarunGothicBold.ttf"
font_name = font_manager.FontProperties(fname=f_path).get_name()
rc('font',family = font_name)

# # Data Load

df = pd.read_excel('data/naver.xlsx')

df.drop(['Unnamed: 0'],axis=1,inplace=True)

df.head()

df.tail()

df.columns

df.shape

df.isnull().sum()

df.info()


# # Preprocessing

# ## cleansing

def cleansing(text):
    pattern = "\[.*\]|\s-\s.*" # 대괄호 안에있는 언론사 정보 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[0-9]' # 숫자제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s]' # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)' # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '네이버|파이낸셜뉴스|서울경제|이데일리|머니투데이|뉴스|데일리 뉴스|헤럴드 경제|금지|무단|배포|저작권' 
    text = re.sub(pattern=pattern, repl='', string=text)
    return text    


df['text'] = df['제목']+' '+df['내용'] # 제목과 내용 합치기

df['text'] = df['text'].apply(cleansing) # 데이터 cleansing

# * cleansing 전 후 비교

print('cleansing 전\n',df['제목'][0] + ' ' + df['내용'][0],'\n')
print('cleansing 후\n',df['text'][0])

# ## tokenizing - Komoran

# * Okt, 꼬꼬마, Komoran 형태소 분석기의 속도를 비교해본 결과 가장 빠름
# * Okt에 비해 불안정한 면이 있지만 형태소를 더 세밀하게 나누어 선택

from konlpy.tag import Komoran

komoran = Komoran(userdic='./userdic.txt')  #형태소 분석기 생성


# * komoran 품사표
# 참고 https://docs.komoran.kr/firststep/postypes.html
# ![nn](img/Komoran.png)

def tokenizing(text):
    tagged = komoran.pos(text)
    
    # 일반 명사, 고유 명사, 형용사만 추출
    token = [ word for word,pos in tagged if pos in ['NNG','NNP','VA']] 
    return token


df['token'] = df['text'].apply(tokenizing)

df.head()

df.to_csv('data/newsdata.csv',index=False)

all_token = df['token'].sum()

# # WordCloud & Keyword

# ## Count based

fdist = FreqDist(all_token)

del fdist['네이버'] # 네이버 회사명은 너무 흔하므로 제거

# +
x = np.arange(20)
word = [w for w,f in fdist.most_common(20)]
values =  [f for w,f in fdist.most_common(20)]

plt.figure( figsize=(20,10))
plt.bar(x, values)
plt.xticks(x, word)
plt.show()
# -

wordcloud = WordCloud(font_path = f_path, background_color='white',
                      colormap = "Accent_r",width=1600, height=1000).generate_from_frequencies(fdist) 
plt.figure( figsize=(20,10))
plt.imshow(wordcloud) 
plt.axis('off') 
plt.tight_layout(pad=0)
plt.show()

# ## TF-IDF based

docs = [' '.join(tokens) for tokens in df['token']]

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(docs) #문장 벡터화 진행
idf = tfidf_vectorizer.idf_

tfidf_dict = dict(zip(tfidf_vectorizer.get_feature_names(), idf))

del_list = ['aa','aj','acc','hmm','red','ads','bnp','bat','ads','ddr'
            ,'captcha','echo','cm','if','faq','mts','hello','ecb','ds','hsg','ds',
           'focus','co','em','dw','jp','fw','da','ev','iaas','ktv','gpt','fw','iv','hs','my']
for token in del_list:
    try:
        del tfidf_dict[token]
    except KeyError:
        pass

wordcloud = WordCloud(font_path = f_path, background_color='white',
                      colormap = "Accent_r",width=1600, height=1000).generate_from_frequencies(tfidf_dict) 
plt.figure( figsize=(20,10))
plt.imshow(wordcloud) 
plt.axis('off') 
plt.tight_layout(pad=0)
plt.show()

# # Bi-gram

from nltk import bigrams,ngrams

bigram = bigrams(all_token)
bi_tokens = [words for words in bigram]
bigram_dict = FreqDist(bi_tokens)

del_list = [('무단', '전재'),('전재', '배포'),('저작권', '파이낸셜뉴스'),('서울경제', '무단'),('헤럴드', '경제'),
            ('스냅', '타임'),('미디어', '이데일리'),('경제', '정보'),('데일리 뉴스', '스냅'),('리보', '뉴스'),
            ('뉴스', '데일리 뉴스'),('저작권', '서울경제'),('뉴스', '머니투데이'),('경제', '무단'),('머니투데이', '무단'),
            ('서울경제', '구독'),('파이낸셜뉴스', '무단'),('배포', '금지'),('리얼타임', '뉴스'),('구독', '해주'),
            ('저작권', '무단'),('채널', '구독'),('요', '저작권')
           ]
for token in del_list:
    try:
        del bigram_dict[token]
    except KeyError:
        pass

bigram_dict.most_common(30)

# +
x = np.arange(20)
word = [w for w,f in bigram_dict.most_common(20)]
values =  [f for w,f in bigram_dict.most_common(20)]

plt.figure( figsize=(20,10))
plt.bar(x, values)
plt.xticks(x, word)
plt.xticks(rotation = - 45 )
plt.show()
# -

# # LDA

# * 언어 모델로 Term Frequency 사용

from gensim import corpora, models
import gensim
from gensim.models import CoherenceModel

docs = [ token_list for token_list in df['token']]

dictionary = corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]

# * 최적의 토픽 개수를 선정하여 토픽 모델링 실시

perplexity_values = []
for i in range(2,15):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=i, id2word = dictionary)
    perplexity_values.append(ldamodel.log_perplexity(corpus))

x = range(2,15)
plt.plot(x, perplexity_values)
plt.xlabel("Number of topics")
plt.ylabel("Perplexity score")
plt.show()

coherence_values = []
for i in range(2,15):
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=i, id2word = dictionary)
    coherence_model_lda = CoherenceModel(model=ldamodel, texts=docs, dictionary=dictionary,topn=10)
    coherence_lda = coherence_model_lda.get_coherence()
    coherence_values.append(coherence_lda)

x = range(2,15)
plt.plot(x, coherence_values)
plt.xlabel("Number of topics")
plt.ylabel("coherence score")
plt.show()

NUM_TOPICS =10 #10개의 토픽
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary,) 
for idx, topic in ldamodel.show_topics(formatted=False, num_words= 10):
    print('Topic: {} \nWords: {}'.format(idx, [w[0] for w in topic]))

# * 시각화

# +
import pyLDAvis.gensim as gensimvis

prepared_data = gensimvis.prepare(ldamodel, corpus, dictionary)

# +
import pyLDAvis
import pyLDAvis.gensim  # don't skip this

pyLDAvis.display(prepared_data)

# +
fiz=plt.figure(figsize=(12,24))
for i in range(10):
    df1=pd.DataFrame(ldamodel.show_topic(i), columns=['term','prob']).set_index('term')
    #df1=df.sort_values('prob')
    
    plt.subplot(5,2,i+1)
    plt.title('topic '+str(i+1))
    sns.barplot(x='prob', y=df1.index, data=df1, label='Cities', palette='Reds_d')
    plt.xlabel('probability')
    
plt.show()
# -

# # sentimental analysis

# * 참고( 나중에 추가 ) word2vec을 통한 감성사전 구축
# https://academic.naver.com/article.naver?doc_id=187746773

# * Word2Vec을 활용한 뉴스 기반 주가지수 방향성 예측용 감성 사전 구축
# https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002457345

# * 코드 자료
# https://github.com/seyoongit/news

# +
DONGHAK = pd.read_csv('dic/DONGHAK.txt',engine="python",header=None,sep="\t",encoding='cp949')

DONGHAK=DONGHAK[(DONGHAK != 0).all(1)]
DONGHAK=DONGHAK.reset_index(drop=True)
DONGHAK.set_index([0],inplace=True)
# -

DONGHAK


def setiment_scoring(tokens_list):
    match_word = [x for x in tokens_list if x in DONGHAK.index]
    
    pos = 0
    neg = 0
    neu = 0
    for i in match_word:
        score = DONGHAK.loc[i,2]

        if score > 0 :
            pos += score
        else:
            neg += score
    return (pos,neg,pos+neg)


df['pos'] = [pos for pos,neg,score in df['token'].apply(setiment_scoring)]
df['neg'] = [neg for pos,neg,score in df['token'].apply(setiment_scoring)]
df['sent'] = [score for pos,neg,score in df['token'].apply(setiment_scoring)]

df.head()

# # 영업일 (18시) 기준으로 데이터 그룹화

# ## 당일의 뉴스 개수도 추가


