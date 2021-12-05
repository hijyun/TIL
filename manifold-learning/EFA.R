
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

comment = '
--------------------------- 인자적재와 특수분산의 추정 ----------------------------
'
# 인자추출 방법 1.주성분인자법  2.주축인자법 3.최대 우도법

# 주성분분석법 (Principal Component Method)
satis <- read.csv("/Users/jihyun/project/data/manifold/MFdata/satis.csv", header=TRUE)
satis.X <- satis[c("x1","x2","x3","x4","x5")]
satis.X.pca <- prcomp(satis.X, center=TRUE, scale=TRUE) # 주성분 분석 
satis.X.pca$sdev^2 # 고유값 출력

satis.X.pca$rotation # 고유벡터 출력
satis.X.pm <- principal(satis.X, cor="cor", nfactors=2, rotate="none")

print(satis.X.pm, digits=3) # 인자분석 결과 출력


comment = '
참고)
Heywood 상황 : 특수성 분산의 추정치가 음수가 되는 경우

'

# 주축인자법(Principal Axis Factor Method)
satis.X.pa <- fa(satis.X, cor="cor", nfactors=2, fm="pa", rotate="none")
print(satis.X.pa, digits = 3)


# 최대우도법(Maximum Likelihood Method)
satis.X.ml <- fa(satis.X,cor="cor",nafactors=2,fm="ml",rotate="none")
print(satis.X.ml,digits=3)

# 인자구조 다이어그램
fa.diagram(satis.X.pa, simple=FALSE, cut=0.4, digit=3)
fa.diagram(satis.X.ml, simple=FALSE, cut=0.0, digit=3)


comment = '
--------------------------- 인자의 회전 ----------------------------
'
# 회전을 하는 이유는 해석을 쉽게하기 위함
# 직교 회전 - 90도를 유지하면서 회전
satis.X.none <- principal(satis.X, nfactors=2, rotate="none") # 회전 안한 경우
print(satis.X.none, digits=3) # 해석이 어렵다.

satis.X.varimax <- principal(satis.X, nfactors=2, rotate="varimax") # 직교회전
print(satis.X.varimax, digits=3)

# 사각 회전 - 90도를 유지하지 않고 회전
satis.X.promax <- principal(satis.X, nfactors=2, rotate="promax")
print(satis.X.promax, digits=3)

comment = '
--------------------------- 인자의 개수 ----------------------------
'
# 잠재변수 인자를 몇개까지 골라야할까?
# 고유값의 크기 - Kaiser의 규칙 (고유값 중 1 보다 큰 개수만큼)
scree(satis.X, hline=1) # Scree 표

comment = '
--------------------------- 인자의 점수화 ----------------------------
'
# 단순 평균(합)을 취하는 방법
satis.cov.ml <- fa(satis.X, cor="cov", nfactors=2, fm="ml") # ML방법
satis.cov.pm <- principal(satis.X, cor="cov", nfactors=2, rotate="varimax")
print(satis.cov.pm, digits=3)

f1 <- (satis.X$x1 + satis.X$x2 + satis.X$x3)/3
f2 <- (satis.X$x4 + satis.X$x5)/2
satis.X.fscore <- cbind(satis.X, f1, f2)
print(satis.X.fscore)

# 회귀적 방법
satis.cor.pm <- principal(satis.X, nfactors=2, rotate="varimax", scores = TRUE)
satis.cor.pm$weights

satis.X.fscore <- cbind(satis.X, satis.cor.pm$scores)
print(satis.X.fscore, digits = 3)
