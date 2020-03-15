library(keras)

df <- load('Madrid_Alumno.rda') 

df

n = length(yTrain)
print(n)

# Preparo la variable de ocurrencia de lluvia
rain = ifelse(yTrain < 1, 0, 1)

# Miro el máximo valor de lluvia, para normalizar la variable 'rain'
# Al final, tengo que acordarme que voy a tener que multiplicar el valor de la predicción en el test para este valor

max.rain <- max(yTrain)
max.rain

# Guardo la predicción original y normalizo
yTrain.original <- yTrain
yTrain <- yTrain / max.rain

# Normalizo los datasets

xTrain <- as.data.frame(xTrain)
xTrain.norm <- as.data.frame(scale(xTrain))

head(xTrain.norm)

# Aplico al dataset the test la misma normalización que al dataset de entrenamiento
# https://datascience.stackexchange.com/questions/13971/standardization-normalization-test-data-in-r

trainMean <- apply(xTrain, 2, mean)
trainSd   <- apply(xTrain, 2, sd)

xTest <- as.data.frame(xTest)
xTest.norm <- sweep(sweep(xTest, 2L, trainMean), 2, trainSd, "/")

head(xTest.norm)

# Dataset de entrenamiento
indtrain   <- sample(1:n, round(0.8*n)) 
x_train    <- xTrain.norm[indtrain,]
y_train    <- yTrain[indtrain]
rain_train <- rain[indtrain]
train      <- x_train

# Añado las variables objetivo
train['y'] <- y_train
train['rain'] <- as.factor(rain_train)

# Miro el dataset
head(train)

# Dataset de validación
indvalid   <- setdiff(1:n, indtrain)      
x_valid    <- as.data.frame(xTrain[indvalid,])
y_valid    <- yTrain[indvalid]
rain_valid <- rain[indvalid]
valid      <- x_valid

# Añado las variables objetivo
valid['y']    <- y_valid
valid['rain'] <- as.factor(rain_valid)

# Miro el dataset
head(train)

# Dataset de test (solo tengo la x, voy a producir la y en el ejercicio)
test <- xTest.norm
head(test)




