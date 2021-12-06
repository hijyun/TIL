# Data load
job <- read.csv("/Users/jihyun/project/data/manifold/MFdata/job.csv", header=TRUE)
job.X <- job[,c("x1", "x2", "x3")]
job.Y <- job[,c("y1","y2","y3")]

# 정준 상관 분석
library(yacca)
yacca::cca(job.X, job.Y)
library(CCA)
CCA::cc(job.X, job.Y)

# 정준상관계수 출력
job.cc <- cc(job.X, job.Y)
job.cc$cor

# 정준계수 출력
job.cc$xcoef # x의 원정준계수
job.cc$ycoef # y의 원정준계수

# 표준화된 정준계수
job.cc$xcoef * sapply(job.X, sd) # x집단의 표준화된 정준계수
job.cc$ycoef * sapply(job.Y, sd) # y집단의 표준화된 정준계수

# 정준 점수 
X.score <- job.cc$scores$xscores
colnames(X.score) <- paste0("ChrVar", 1:3)
Y.score <- job.cc$scores$yscores
colnames(Y.score) <- paste0("SatVar", 1:3)
job.score <- cbind(X.score, Y.score)
rownames(job.score) <- job$job
round(job.score, digits=3)

# 정준점수 플롯
plot(job.score[,1:2], pch=1, col='blue', xlim=c(-2,2),ylim=c(-2,2)) 
abline(v=0,h=0,lty=2)
text(job.score[,1:2], labels=1:14, pos=4, col="red")

plot(job.score[,4:5], pch=1, col='blue', xlim=c(-2,2),ylim=c(-2,2))
abline(v=0,h=0,lty=2)
text(job.score[,4:5], labels=1:14, pos=4, col="red")

plot(job.score[,c(1,4)], pch=1, col='blue', xlim=c(-2,2),ylim=c(-2,2))
abline(v=0,h=0,lty=2)
text(job.score[,c(1,4)], labels=1:14, pos=4, col="red")

# 정준적재 (Canonical Loading)
job.cc$scores$corr.X.xscores # x-정준적재
job.cc$scores$corr.Y.yscores # y-정준적재

# 정준적재 플롯
job.loading <- rbind(job.cc$scores$corr.X.xscores,
                     job.cc$scores$corr.Y.yscores)
plot(job.loading[,1:2], pch=1, col="red", xlim=c(-1,1),ylim=c(-1,1))
abline(v=0, h=0, lty=2) 
text(job.loading[,1:2], labels=rownames(job.loading),pos=4,col="blue")

# 교차적재 (Cross Loading)
job.cc$scores$corr.X.yscores # x-정준적재
job.cc$scores$corr.Y.xscores # y-정준적재

# 공헌도 - 정준변량들에 의해 설명되는 비율
cxx <- job.cc$scores$corr.X.xscores
CV <- colSums(cxx^2)/nrow(cxx)
Cum.CV <- cumsum(CV)
X.variation <- cbind(CV,Cum.CV)
print(X.variation) # X-변수들의 변이에 대한 정준변량들의 공헌도

cyy <- job.cc$scores$corr.Y.yscores
CW <- colSums(cyy^2)/nrow(cyy)
Cum.CW <- cumsum(CW)
Y.variation <- cbind(CW,Cum.CW)
print(Y.variation) # Y-변수들의 변이에 대한 정준변량들의 공헌도




