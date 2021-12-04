library(psych)

# Data load
tvprog <- read.csv("/Users/jihyun/project/data/manifold/MFdata/tvprog.csv", header=TRUE)
tvprog.X <- na.omit(tvprog[2:9]) # 분석 변수 선택 및 결측값 제거
print(cor(tvprog.X), digit=3) # 상관행렬 출력

tvprog.pca <- princomp(tvprog.X, cor=TRUE) # 주성분 분석
tvprog.pca$sdev^2 # 고유값 출력
summary(tvprog.pca)

# 요인분석의 타당성 - 1. MSA 2. 공분산 검정

# KMO표본적합성 측도 - 요인분석을 할만한지 검토
KMO(tvprog.X) # MSA - measure of sampling adequacy가 적어도 0.5. 0.6이상은 나와야한다.

# Bartlett의 구형성 검정
# H0 : 공통인자가 존재하지 않는다. H1 : 공통인자가 적어도 한 개 존재한다.
tvprog.cor <- cor(tvprog.X)
cortest.bartlett(tvprog.cor, n=nrow(tvprog.X))


