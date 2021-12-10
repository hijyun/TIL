# 예제 데이터
mat <- matrix(c(
  68,119,26,7,
  20,84,17,94,
  15,54,14,10,
  5,29,14,16
), byrow=TRUE, nc=4)

dimnames(mat) <- list(inc=c('BROWN','BLUE','HAZEL','GREEN'), support=c('black','brown','red','blond'))
Nxy <- as.table(mat) 
Nxy

addmargins(Nxy)

# 카이제곱 검정
H <- chisq.test(Nxy, correct=FALSE)
H

# 모자이크 그림
par(mfrow=c(2,2), mar=c(2,1,1,1))

mosaicplot(Nxy, color=TRUE)
mosaicplot(H$observed, color=TRUE, shade = TRUE)
mosaicplot(H$expected, color=TRUE)
spineplot(Nxy, main='Spine plot')

# 대응분석
Mca <- ca(Nxy)
Mca

# 행렬도
plot(Mca)