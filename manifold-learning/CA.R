# Data Load
brand <- read.csv("/Users/jihyun/project/data/manifold/MFdata/brand.csv", header=TRUE)
print(brand)

# 카이제곱검정

brand.tbl <- xtabs(count~age+brand,data=brand) # 분할표
brand.chi <- chisq.test(brand.tbl) # 카이제곱검정
print(brand.chi)

brand.chi$expected # 기대빈도 출력
brand.chi$residuals # 셀 카이값 출력

addmargins(prop.table(brand.tbl, margin=1), margin=2) # 행 백분율 출력
addmargins(round(brand.chi$residuals^2, digit=3)) # 셀 카이제곱 값 계산

# 대응 분석 - Correspondence Analysis
# 이산형 자료에 대한 CCA

library(ca)
brand.ca <- ca(brand.tbl) # 대응분석
plot.ca(brand.ca, map="symmetric") # 대응분석 행렬도 출력

brand.ca$sv # 특이값 출력

summary(brand.ca) # 고유값 출력

brand.ca$rowcoord # 행 표준좌표 (standardized coordinate)
brand.ca$colcoord # 열 표준좌표 (standardized coorinate)

brand.ca$rowcoord%*%diag(brand.ca$sv) # 행 주좌표 (principal coordinate)
brand.ca$colcoord%*%diag(brand.ca$sv) # 열 주좌표 (principal coordinate)
