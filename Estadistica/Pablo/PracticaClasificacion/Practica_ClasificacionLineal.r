# Set the directory to be able to read the data properly
# rm(list=ls())
# setwd("")

#Install the necessary packages
install.packages("R.utils")

# download data from http://yann.lecun.com/exdb/mnist/
download.file("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz",
              "train-images-idx3-ubyte.gz")
download.file("http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz",
              "train-labels-idx1-ubyte.gz")
download.file("http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz",
              "t10k-images-idx3-ubyte.gz")
download.file("http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz",
              "t10k-labels-idx1-ubyte.gz")

# gunzip the files
R.utils::gunzip("train-images-idx3-ubyte.gz")
R.utils::gunzip("train-labels-idx1-ubyte.gz")
R.utils::gunzip("t10k-images-idx3-ubyte.gz")
R.utils::gunzip("t10k-labels-idx1-ubyte.gz")

# load image files
load_image_file = function(filename) {
  ret = list()
  f = file(filename, 'rb')
  readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  n    = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  nrow = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  ncol = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  x = readBin(f, 'integer', n = n * nrow * ncol, size = 1, signed = FALSE)
  close(f)
  data.frame(matrix(x, ncol = nrow * ncol, byrow = TRUE))
}

# load label files
load_label_file = function(filename) {
  f = file(filename, 'rb')
  readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  n = readBin(f, 'integer', n = 1, size = 4, endian = 'big')
  y = readBin(f, 'integer', n = n, size = 1, signed = FALSE)
  close(f)
  y
}

# load images
x_train = load_image_file("train-images-idx3-ubyte")
x_test  = load_image_file("t10k-images-idx3-ubyte")

# load labels
y_train = load_label_file("train-labels-idx1-ubyte")
y_test  = load_label_file("t10k-labels-idx1-ubyte")

# Dibujamos los 6 primeros dígitos de la base de datos
par(mfrow = c(2,3))
for (i in 1:6) {
    image(matrix(as.matrix(x_train[i,1:784]), nrow = 28, ncol = 28))
    title(y_train[i])
}

# Cada dígito está igualmente representado en la muestra
hist(y_train, breaks = -0.5:9.5)

# Seleccionamos un dígito concreto para tratar de predecirlo. Por ejemplo el nueve
# y9 = 1 si el dígito es 9 y 0 en caso contrario
y9 <- y_train;
y9[which(y_train != 9)] <- 0 ; y9[which(y_train == 9)] <- 1

# Construimos un dataframe para entrenar el modelo
dat <- data.frame(y9,x_train)

i<- 1:5000;
j<-5001:10000
#Random sampling
#i<-sample(1:dim(x)[1],5000);
datT <- dat[i,]
datt <- dat[j,]

# Entrenamos primero un modelo lineal
model <- lm(datT$y9~., data = datT)
out <- model$fitted.values
# El histograma muestra valores predichos (incluyendo negativos y mayores que 1)
hist(out)

# Hacemos binaria la salida considerando el umbral 0.5 (a modo de probabilidad)
outbin <- as.double(out > 0.5)

# Tasa de acierto (en entrenamiento)
100*sum(diag(table(datT[,1], outbin))) / length(outbin)

# Tasa de acierto de test
out1<- predict(object=model, newdata = datt);
outbin1 <- as.double(out1 > 0.5)
100*sum(diag(table(datt[,1], outbin1))) / length(outbin1)

model1 <- glm(datT$y9~., data = datT, family = binomial(link = "logit"))


# Problemas de convergencia con tantas variables
# Coefficients: (138 not defined because of singularities)
# Tasa de acierto (Train)
out2 <- model1$fitted.values
outbin2 <- as.double(out2 > 0.5)
100*sum(diag(table(datT[,1], outbin2))) / length(outbin2)

hist(out2)

# Tasa de acierto (test)
out3<- predict(object=model1, newdata = datt);
outbin3 <- as.double(out3 > 0.5)
100*sum(diag(table(datt[,1], outbin3))) / length(outbin3)

#Modelo de regresión lineal
j<-seq(1,784,20)
model <- lm(datT$y9~., data = datT[,j])
out <- model$fitted.values
outbin <- as.double(out > 0.5)
100*sum(diag(table(datT[,1], outbin))) / length(outbin)
out1<- predict(object=model, newdata = datt[,j]);
outbin1 <- as.double(out1 > 0.5)
100*sum(diag(table(datt[,1], outbin1))) / length(outbin1)

#Regresión logística
j<-seq(1,784,20)
model <- glm(datT$y9~., data = datT[,j], family = binomial(link = "logit"))
out <- model$fitted.values
outbin <- as.double(out > 0.5)
100*sum(diag(table(datT[,1], outbin))) / length(outbin)
out1<- predict(object=model, newdata = datt[,j]);
outbin1 <- as.double(out1 > 0.5)
100*sum(diag(table(datt[,1], outbin1))) / length(outbin1)

# Rellena

# Train: primeras 5000 imagenes
i <- 1:5000;

# Test: imagenes de 5001 a 10000
j <- 5001:10000

# el numero que quiero esudiar
N = 0

# y_train: sample de train

# añado una columna a la muestra de train, que vale:
# 1 si es el numero que queremo
# 0 si es otro numero

my.y <- y_train;
my.y[which(y_train != N)] <- 0 ; my.y[which(y_train == N)] <- 1

my.dat <- data.frame(my.y,x_train)

my.dat.train <- my.dat[i,]
my.dat.test  <- my.dat[j,]

# entreno el modelo logistico con 5000 imagenes (considero todos los pixeles de la imagen)

my.model <- glm(my.dat.train$my.y~., data = my.dat.train, family = binomial(link = "logit"))

# Tasa de acierto (Train)
out.train <- my.model$fitted.values
out.bin <- as.double(out.train > 0.5)
100*sum(diag(table(my.dat.train[,1], out.bin))) / length(out.bin)

# Matriz de confusion (Train)
table(my.dat.train[,1], out.bin)

# Tasa de acierto (test)
out.test<- predict(object=my.model, newdata = my.dat.test);
out.bin.test <- as.double(out.test > 0.5)
100*sum(diag(table(my.dat.test[,1], out.bin.test))) / length(out.bin.test)

# Matriz de confusion (test)
table(my.dat.test[,1], out.bin.test)

# Train: primeras 10000 imagenes
i <- 1:10000;

# Test: imagenes de 10001 a 60000
q <- 10001:60000

my.results.vector <-c()

numbers <- seq(0,9)

# el numero que quiero estudiar
for (N in numbers){
    #print(N)

    # y_train: sample de train

    # añado una columna a la muestra de train, que vale:
    # 1 si es el numero que queremo
    # 0 si es otro numero

    my.y <- y_train;
    my.y[which(y_train != N)] <- 0 ; my.y[which(y_train == N)] <- 1

    my.dat <- data.frame(my.y,x_train)

    my.dat.train <- my.dat[i,]
    my.dat.test  <- my.dat[q,]

    # Sample aleatorio de los pixeles que considero
    #j <- sample(0:784, 39)
    j <- seq(1,784,20)

    # Entrenamiento del modelo
    my.model <- glm(my.dat.train$my.y~., data = my.dat.train[,j], family = binomial(link = "logit"))

    # Tasa de acierto (test)
    out.test<- predict(object=my.model, newdata = my.dat.test);
    out.bin.test <- as.double(out.test > 0.5)

    # Guardo la accuracy
    my.results.vector <- c(my.results.vector, 100*sum(diag(table(my.dat.test[,1], out.bin.test))) / length(out.bin.test))
}

names(my.results.vector) <-  numbers
sort.int(my.results.vector, index.return = T)$x

# Train: primeras 10000 imagenes
i <- 1:10000;

my.results.vector <- c()
my.results.matrix <- matrix(, nrow = 1, ncol = 0)

numbers <- seq(0,9)

# el numero que quiero estudiar
for (N in numbers){
    #print(N)

    # y_train: sample de train

    # añado una columna a la muestra de train, que vale:
    # 1 si es el numero que queremo
    # 0 si es otro numero

    my.y <- y_train;
    my.y[which(y_train != N)] <- 0 ; my.y[which(y_train == N)] <- 1

    my.dat <- data.frame(my.y,x_train)

    my.dat.train <- my.dat[i,]

    # Sample aleatorio de los pixeles que considero
    #j <- sample(0:784, 39)
    j <- seq(1,784,20)

    # Entrenamiento del modelo
    my.model <- glm(my.dat.train$my.y~., data = my.dat.train[,j], family = binomial(link = "logit"))

    # test (repetido 10 veces)
    for (z in 1:10){
    
        # Test: 5000 imagenes aleatorias
        q <- sample(10001:60000, 5000)
        my.dat.test  <- my.dat[q,]

        # Tasa de acierto (test)
        out.test<- predict(object=my.model, newdata = my.dat.test);
        out.bin.test <- as.double(out.test > 0.5)

        #print(100*sum(diag(table(my.dat.test[,1], out.bin.test))) / length(out.bin.test))
        
        # Guardo la accuracy
        my.results.vector <- c(my.results.vector, 100*sum(diag(table(my.dat.test[,1], out.bin.test))) / length(out.bin.test))
    }
}

my.results.vector <- matrix(my.results.vector, nrow = 10, ncol = 10)

#my.results.vector

my.mean.values <- apply(my.results.vector, FUN = mean, MARGIN = 2)
my.mean.values

my.vars <- apply(my.results.vector, FUN = var, MARGIN = 2)
my.vars


