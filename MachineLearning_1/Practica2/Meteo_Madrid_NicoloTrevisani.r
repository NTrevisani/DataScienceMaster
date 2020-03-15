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

# Me quedo solo con las variables que tengas correlación con y grande
# |corr(y,Xn)| > 0.4

xTest.norm <- xTest.norm[,cor(xTrain.norm, yTrain, method = "spearman") > 0.4 | cor(xTrain.norm, yTrain, method = "spearman") < -0.4]
xTrain.norm <- xTrain.norm[,cor(xTrain.norm, yTrain, method = "spearman") > 0.4 | cor(xTrain.norm, yTrain, method = "spearman") < -0.4]

ncol(xTrain.norm)

# Dataset de entrenamiento
#indtrain   <- sample(1:n, round(0.8*n)) 
x_train    <- xTrain.norm#[indtrain,]
y_train    <- yTrain#[indtrain]
rain_train <- rain#[indtrain]
train      <- x_train

# Añado las variables objetivo
train['y'] <- y_train
train['rain'] <- as.factor(rain_train)

# Miro el dataset
head(train)

# Dataset de test (solo tengo la x, voy a producir la y en el ejercicio)

test <- xTest.norm
head(test)

# Defino el modelo
model.rain <- keras_model_sequential() 

model.rain %>% 
  layer_dense(units = 30, input_shape = ncol(train)-2, activation = "relu", kernel_regularizer = regularizer_l2(0.005)) %>% 
  layer_dropout(0.5) %>%
  layer_dense(units = 10, activation = "relu", kernel_regularizer = regularizer_l2(0.005)) %>%
  layer_dropout(0.5) %>%
  layer_dense(units = 2 , activation = "sigmoid")#"softmax") 
str(model.rain)

# Compilo el modelo
model.rain %>% compile(
  optimizer = optimizer_adagrad(lr = 0.005),
  loss = "binary_crossentropy",
  metrics = "binary_accuracy"
)

# Entreno el modelo

my.train.x <- as.matrix(train[ , 1:ncol(test)])
my.train.y <- to_categorical(train$rain, 2)

history <- model.rain %>% fit(x = my.train.x, 
                              y = my.train.y, 
                              epochs = 500, 
                              batch_size = 20,
                              validation_split = 0.2)

plot(history)


