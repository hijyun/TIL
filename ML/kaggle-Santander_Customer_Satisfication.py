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

# # 분류 실습 - 캐글 산탄데르 고객 만족 예측

# _참고 : 권철민 <파이썬 머신러닝 완벽 가이드>, 위키북스_

# ## Data preprocessing

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

cust_df = pd.read_csv("data/santander-customer-satisfaction/train_santander.csv")

# 클래스 값 칼럼을 포함한 피처가 371개 존재합니다.

print('dataset shape:', cust_df.shape)

cust_df.head(3)

# 111개의 피처가 float형, 260개의 피처가 int형으로 모든 피처가 숫자 형이며, Null값은 없습니다.

cust_df.info()

# * 전체 데이터에서 만족과 불만족의 비율

print(cust_df['TARGET'].value_counts())
unsatisfied_cnt = cust_df[cust_df['TARGET']==1].TARGET.count()
total_cnt = cust_df.TARGET.count()
print('unsatisfied 비율은 {0: .2f}'.format(unsatisfied_cnt / total_cnt))

cust_df.describe()

print(cust_df['var3'].value_counts())

# var3 칼럼의 경우 min 값이 -999999입니다. NaN이나 특정 예외 값을 -999999로 변환했을 것으로 보입니다. var3은 숫자형이고 다른 값에 비해 -999999는 편차가 너무 심하므로 가장 많은 2로 변환하겠습니다.

# +
cust_df['var3'].replace(-999999, 2, inplace=True)
cust_df.drop('ID',axis =1, inplace=True)

# 피처 세트와 레이블 세트 분리. 레이블 칼럼은 DataFrame의 맨 마지막에 위치해 칼럼 위치 -1로 분리
X_features = cust_df.iloc[:, :-1]
y_labels = cust_df.iloc[:,-1]
print('피처 데이터 shape{0}'.format(X_features.shape))
# -

# * trn / tst 분리

# +
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_features, y_labels,
                                                   test_size = 0.2, random_state = 0)

train_cnt = y_train.count()
test_cnt = y_test.count()
print('학습 데이터 shape{0}, 테스트 shape{1}'.format(X_train.shape, X_test.shape))

print('학습 세트 레이블 값 분포 비율')
print(y_train.value_counts()/train_cnt)
print('\n 테스트 세트 레이블 값 분포 비율')
print(y_test.value_counts()/test_cnt)
# -

# 학습과 테스트 데이터 세트 모두 TARGET의 값의 분포가 원본 데이터와 유사하게 전체 데이터의 4%정도의 불만족 값(값1)으로 만들어졌습니다.

# ## Train - XGBoost 

# XGBoost의 학습 모델을 생성하고 예측 결과를 ROC AUC로 평가해 보겠습니다. 사이킷런 래퍼인 XGBClassifier를 기반으로 학습을 수행합니다. 평가 데이터 세트는 앞에서 분리한 테스트 데이터 세트를 이용하겠습니다. 사실 테스트 데이터 세트를 XGBoost의 평가 데이터 세트로 사용하면 과적합의 가능성을 증가시킬 수 있지만, 여기서는 이런 점만 주지하고 넘어가도록 하겠습니다. 

# +
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score

# n_estimators는 500으로, random status는 예제 수행 시마다 동일 예측 결과를 위해 설정.
xgb_clf = XGBClassifier(n_estimators = 500, random_statue=156)

xgb_clf.fit(X_train, y_train, early_stopping_rounds = 100,
           eval_metric="auc", eval_set=[(X_train, y_train), (X_test, y_test)])

xgb_roc_score = roc_auc_score(y_test, xgb_clf.predict_proba(X_test)[:,1],average='macro')

print('ROC AUC: {0: .4f}'.format(xgb_roc_score))
# -
# ### 하이퍼 파라미터 튜닝

# +
from sklearn.model_selection import GridSearchCV

# 하이퍼 파라미터 테스트의 수행 속도를 향상시키기 위해 n_estimators를 100으로 감소
xgb_clf = XGBClassifier(n_estimators = 100)
params = {'max_depth':[5,7],
         'min_child_weight':[1,3],
         'colsample_bytree':[0.5,0.75]}

# 하이퍼 파라미터 테스트의 수행 속도를 향상시키기 위해 cv를 지정하지 않음
gridcv = GridSearchCV(xgb_clf, param_grid=params)
gridcv.fit(X_train, y_train, early_stopping_rounds=30, eval_metric='auc',
          eval_set=[(X_train, y_train), (X_test, y_test)])


# +

print('GridSearchCV 최적 파라미터:', gridcv.best_params_)

xgb_roc_score = roc_auc_score(y_test, gridcv.predict_proba(X_test)[:, 1], average='macro')
print('ROC AUC : {0:.4f}'.format(xgb_roc_score))
# -

# * 피처 중요도
#

# +
from xgboost import plot_importance
import matplotlib.pyplot as plt
# %matplotlib inline

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
plot_importance(xgb_clf, ax=ax, max_num_features=20, height=0.4)
# -

# # 모델 개선해보기

# +
import shap

# JS 시각화 라이브러리 로드하기
shap.initjs()

# SHAP 값으로 모델의 예측을 설명하기
# 설명체는 LightGBM, CATBoost, scikit-learn 모델을 입력받을 수 있다.

explainer = shap.TreeExplainer(xgb_clf)
shap_values = explainer.shap_values(X_train)
shap.summary_plot(shap_values,X_train, plot_type='bar',feature_names = X_features.columns.tolist())

# 모든 피처에 대해 SHAP 값을 계산하고, 영향력을 시각화하는 코드
shap.summary_plot(shap_values, X_train,feature_names = X_features.columns.tolist())
# -

shap_df = pd.DataFrame(shap_values, columns =X_features.columns.tolist() )
shap_df = shap_df .apply(abs)

shap_sum = []
for col in X_features.columns.tolist():
    shap_sum.append(shap_df[col].sum())

shap_dict = dict(zip(X_features.columns.tolist(),shap_sum))

# +
val_reverse = sorted(shap_dict.items(), 

                              reverse=True, 

                              key=lambda item: item[1])


sort_val = [key for key, _ in val_reverse]

# +
X_features = cust_df.loc[:, sort_val[:20]]
y_labels = cust_df.iloc[:,-1]
print('피처 데이터 shape{0}'.format(X_features.shape))

# n_estimators는 500으로, random status는 예제 수행 시마다 동일 예측 결과를 위해 설정.
final_clf = XGBClassifier(colsample_bytree=0.75, max_depth= 5, min_child_weight=10, random_statue=156)

final_clf.fit(X_train, y_train, early_stopping_rounds = 100,
           eval_metric="auc", eval_set=[(X_train, y_train), (X_test, y_test)])

xgb_roc_score = roc_auc_score(y_test, final_clf.predict_proba(X_test)[:,1],average='macro')

print('ROC AUC: {0: .4f}'.format(xgb_roc_score))
# -


