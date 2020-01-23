mnist <- read.csv("train.csv")

head(mnist)
nrow(mnist)

# Dataset de entrenamiento
M <- ncol(mnist)
my.train <- mnist[1:1000,2:M]

head(my.train)
nrow(my.train)

# Saco las componente principales
mnist.pca <- prcomp(my.train)

sum(mnist.pca$sdev**2)

print((cumsum(mnist.pca$sdev**2) /  sum(mnist.pca$sdev**2)) * 100)


