## Required packages:

install.packages("MASS")
install.packages("stats")
install.packages("readr")
install.packages("mclust")
install.packages("caret")
install.packages("e1071")
install.packages("sparcl")
install.packages("kohonen")
install.packages("cluster")
install.packages("FNN")

## Statistical tools:

library(MASS)
library(stats)

## Reading data:

library(readr)

## Clustering methods:
library(mclust)
library(caret)
library(e1071)
library(sparcl)
library(kohonen)
library(cluster)
library(FNN)

require(magrittr)

# GENERA FIGURA 1
set.seed(4)
x <- matrix(rnorm(100 * 2), ncol = 2)
x[1:25, 1] <- x[1:25, 1] + 1
x[1:25, 2] <- x[1:25, 2] - 2
k <- 3
par(mfrow = c(2,3))
j = 6
while(j > 0) {
      j <- j - 1
      set.seed(j+1)
      km <- kmeans(x, centers = k)
      plot(x, ty = "n", xlab = "", ylab = "")
      for (i in 1:k) {
            points(x[km$cluster == i, ], pch = 19, col = i)
      }
      mtext(format(km$tot.withinss, digits = 2)) 
}

# GENERA FIGURA 2
set.seed(2)
x <- matrix(rnorm(45 * 2), ncol = 2)
x[1:15, 1] <- x[1:15, 1] + 2
x[1:15, 2] <- x[1:15, 2] + 2
x[16:30, 2] <- x[16:30, 2] - 4
x[16:30, 1] <- x[16:30, 1] - 2
x[31:45, 1] <- x[31:45, 1] - 4
x[31:45, 2] <- x[31:45, 2] + 1 
plot(x, ty = "n", xlab = "")
points(x[1:15, ], col = 2, pch = 19)
points(x[16:30, ], col = 3, pch = 19)
points(x[31:45, ], col = 4, pch = 19)

# GENERA FIGURA 3
require(sparcl) # colorea las hojas del dendrograma de forma facil
hc <- hclust(dist(x), method = "complete")
par(mfrow=c(1,3))
y1 <- cutree(hc, k = 1)
ColorDendrogram(hc, y = y1, ylab = "", xlab = "", branchlength = 10)
y2 <- cutree(hc, h = 11)
ColorDendrogram(hc, y = y2, ylab = "", xlab = "", branchlength = 10)
abline(h = 11, lty = 2)
y3 <- cutree(hc, h = 6)
ColorDendrogram(hc, y = y3, ylab = "", xlab = "", branchlength = 10)
abline(h = 6, lty = 2)

# GENERA FIGURA 4
set.seed(1)
x <- matrix(rnorm(20), ncol = 2)
hc <- hclust(dist(x))
par(mfrow = c(1,2))
plot(x, ty = "n", xlab = "", ylab = "", asp = 1)
text(x[hc$order,1], x[hc$order,2], hc$order)
plot(hc, xlab = "", ylab = "", main = "", hang = -1)

set.seed(1)
x <- matrix(rnorm(20), ncol = 2)
hc <- hclust(dist(x))
par(mfrow = c(2,3))
# plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 1")
# text(x[hc$order,1], x[hc$order,2], hc$order)
plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 1")
text(x[hc$order,1], x[hc$order,2], hc$order)
rect(0.5,0.7,0.9,1.1, border = "green", lwd = 2)

plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 2")
text(x[hc$order,1], x[hc$order,2], hc$order)
rect(0.5,0.7,0.9,1.1, border = "green", lwd = 2)
rect(0.22,0.67,0.95,1.3, border = "brown", lwd = 2)

plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 3")
text(x[hc$order,1], x[hc$order,2], hc$order)
rect(0.5,0.7,0.9,1.1, border = "green", lwd = 2)
rect(0.22,0.67,0.95,1.3, border = "brown", lwd = 2)
rect(0.1,-0.15,0.6,0.45, border = "purple", lwd = 2)

plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 4")
text(x[hc$order,1], x[hc$order,2], hc$order)
rect(0.5,0.7,0.9,1.1, border = "green", lwd = 2)
rect(0.22,0.67,0.95,1.3, border = "brown", lwd = 2)
rect(0.1,-0.15,0.6,0.45, border = "purple", lwd = 2)
rect(-0.95,-0.75,-0.6,0.15, border = "red", lwd = 2)

plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 5")
text(x[hc$order,1], x[hc$order,2], hc$order)
rect(0.5,0.7,0.9,1.1, border = "green", lwd = 2)
rect(0.22,0.67,0.95,1.3, border = "brown", lwd = 2)
rect(0.1,-0.15,0.6,0.45, border = "purple", lwd = 2)
rect(-0.95,-0.75,-0.6,0.15, border = "red", lwd = 2)
rect(-0.7,0.45,-0.1,1.6, border = "cyan", lwd = 2)

plot(x, ty = "n", xlab = "", ylab = "", asp = 1, main = "Iter 6")
text(x[hc$order,1], x[hc$order,2], hc$order)
rect(0.5,0.7,0.9,1.1, border = "green", lwd = 2)
rect(0.22,0.67,0.95,1.3, border = "brown", lwd = 2)
rect(0.1,-0.15,0.6,0.45, border = "purple", lwd = 2)
rect(-0.95,-0.75,-0.6,0.15, border = "red", lwd = 2)
rect(-0.7,0.45,-0.1,1.6, border = "cyan", lwd = 2)
rect(0,-0.3,1,1.4, border = "orange", lwd = 2)

# GENERA FIGURA 6
set.seed(1)
x <- matrix(rnorm(50), ncol = 2)
par(mfrow=c(1,3))
plot(hclust(dist(x), method = "complete"), col = "blue", axes = FALSE,
     main = "Complete Linkage")
plot(hclust(dist(x), method = "average"), col = "red", axes = FALSE,
     main = "Average linkage")
plot(hclust(dist(x), method = "single"), col = "olivedrab", axes = FALSE,
     main = "Single linkage")

? kmeans

str(iris)
library(ggplot2)
ggplot( data = iris, 
  aes(x = Sepal.Length,y = Sepal.Width)) +  
  geom_point(aes(color= Species)) +
  ggtitle("Sepal Length Vs Width")

kmModel<-kmeans(iris[,-5],3,nstart=1)
summary(kmModel)

## Point center of two attributes
plot(iris[,c(1,2)],col=kmModel$cluster,main="K-Means")

kmModel$cluster
kmModel$withinss ## Vector of within-cluster sum of squares, one component per cluster
kmModel$betweenss ## The between-cluster sum of squares

confusionMatrix(as.factor(as.numeric(iris[,5])),as.factor(kmModel$cluster))

k<-3
par(mfrow=c(2,3))
j<-6
while(j>0){
  set.seed(j)
  j<-j-1
  km<-kmeans(iris[,-5],centers=k)
  plot(iris[,c(1,2)],type="n")
  for(i in 1:k){
    points(iris[km$cluster==i,c(1,2)],pch=19,col=i)
  }
  mtext(format(km$tot.withinss,digits=2))
}

## How many clusters should we use?
totWithinss<-c(1:15)
for(i in 1:15){
  kmModel<-kmeans(iris[,-5],centers=i,nstart=1)
  totWithinss[i]<-kmModel$tot.withinss
}
plot(x=1:15,y=totWithinss,type="b",
  xlab="N. Of Cluster",ylab="Within groups sum of squares")

# Reading dataset
mnist_data <- read_csv("~/Dropbox/M1966_DataMining/datasets/train.csv")
nrows <- 10000
indSample <- sample(dim(mnist_data)[1], nrows, replace = FALSE)
mnist_data <- mnist_data[indSample,]

kmModel<-kmeans(mnist_data[,-1], centers=10, nstart=1)
# Evaluatin the discrimination:
par(mfrow=c(3,4))
for (i in 1:10){
  hist(mnist_data$label[which(kmModel$cluster == i)])
}

# Building a 3*3 grid
par(mfrow=c(3,4))
for (i in 1:10){
  # Changing i-th center to matrix
  mat <- matrix(as.numeric(kmModel$centers[i,]), nrow = 28, ncol=28, byrow = FALSE)
  # plot
  image(mat, main=paste0("K Means ", i), col=paste("gray", 1:99,sep=""), asp = 1)
}

cmModel <- cmeans(mnist_data[,-1], 10, iter.max = 1000)

## load data
# Predictors: Z500,T850,T700,T500,2T,Q850,Q500,SLP
load("meteo.RData")
longitud <- seq(-10,4,2) #con un paso de 2º
latitud <- seq(36,44,2) #con un paso de 2º
years <- 1979:2008
# Predictand: precipitation in Lisboa.
location <- c(-9.15,38.7)

## See, for example, ? seq.Date and ? months
fechas <- seq.Date(from = as.Date("1979/1/1"), to = as.Date("2008/12/31/"), by = "day")
months(fechas)

#install.packages(c('fields','FNN','class'))

library(fields)
library(FNN)
library(class)

par(mfrow=c(2,2))

image.plot(x = longitud, y = latitud, z = t(matrix(x[1,1:(length(longitud)*length(latitud))], nrow=length(latitud), ncol=length(longitud))), xlab = "longitud", ylab = "latitud", main = "Geopotential 500 hPa")
image.plot(x = longitud, y = latitud, z = t(matrix(x[1,121:(120+length(longitud)*length(latitud))], nrow=length(latitud), ncol=length(longitud))), xlab = "longitud", ylab = "latitud", main = "Temperature 500 hPa")
image.plot(x = longitud, y = latitud, z = t(matrix(x[1,241:(240+length(longitud)*length(latitud))], nrow=length(latitud), ncol=length(longitud))), xlab = "longitud", ylab = "latitud", main = "Specific Humidity 500 hPa")
image.plot(x = longitud, y = latitud, z = t(matrix(x[1,281:(280+length(longitud)*length(latitud))], nrow=length(latitud), ncol=length(longitud))), xlab = "longitud", ylab = "latitud", main = "Sea Level Pressure")

# train and test separation (75% and 25%, respectively)
indtrain = sort(sample(length(y), round(0.75*length(y))))

# 75% train
x.train = x[indtrain, ]
y.train = y[indtrain]

# 25% test
x.test = x[-indtrain, ]
y.test = y[-indtrain]

kmModel <- kmeans(x.train, 100, iter.max = 1000, nstart =20)

yCentroid <- knn.reg(train = x.train, test = kmModel$centers, y = y.train, k = 1)

# knn.reg application
pred <- knn.reg(train = kmModel$centers, test = x.test, y = yCentroid$pred, k = 1)


