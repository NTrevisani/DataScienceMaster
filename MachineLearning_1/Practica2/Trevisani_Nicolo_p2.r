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

library(ggplot2)

# Miro si puedo reducir la dimensionalidad del problema con PCA
xTrain <- as.data.frame(xTrain)

# Busco las componentes principales
xTrain.pca <- prcomp(xTrain, scale = TRUE, center = TRUE)

# Pinto el porcentage de varianza cumulada explicado por cada componente principal
suma = sum(xTrain.pca$sdev)
plot.pca <- xTrain.pca$sdev / sum(xTrain.pca$sdev)
tot.pca <- length(plot.pca)
pcas <- cbind(plot.pca, 1:tot.pca)
pcas <- as.data.frame(pcas)

# Varianza
ggplot(data=pcas[1:20,],
       aes(x=V2, y = plot.pca, group=1)) + 
       geom_bar(stat="identity", fill="steelblue") +
       geom_text(aes(label=format(round(plot.pca*100,1), nsmall = 1)), vjust=-0.3, size=3.5) +
       geom_line(color="black") +
       geom_point() + 
       ggtitle("Variance plot") +
       labs(y = "Variance", x = "Dimension") +  
       theme_minimal()

# Varianza cumulada
ggplot(data=pcas[1:20,],
       aes(x=V2, y = cumsum(plot.pca), group=1)) + 
       geom_bar(stat="identity", fill="steelblue") +
       geom_text(aes(label=format(round(cumsum(plot.pca*100),1), nsmall = 1)), vjust=-0.3, size=3.5) +
       geom_line(color="black") +
       geom_point() + 
       ggtitle("Cumulative variance plot") +
       labs(y = "Cumulative variance", x = "Dimension") +  
       theme_minimal()

# Considero que el 95% de la varianza es suficiente = 203 componentes principales
print(format(round(cumsum(plot.pca[1:220]*100),1), nsmall = 1))

xTrain.norm <- xTrain.pca$x[, 1:203]

head(xTrain.norm)

xTrain.norm <- as.data.frame(scale(xTrain.norm))

head(xTrain.norm)

# Aplico al dataset the test la misma normalización que al dataset de entrenamiento
# https://datascience.stackexchange.com/questions/13971/standardization-normalization-test-data-in-r

trainMean <- apply(xTrain.norm, 2, mean)
trainSd   <- apply(xTrain.norm, 2, sd)

xTest <- as.data.frame(xTest)

xTest.pca <- predict(xTrain.pca, newdata = xTest)
xTest.norm <- xTest.pca[, 1:203]
xTest.norm <- sweep(sweep(xTest.norm, 2L, trainMean), 2, trainSd, "/")

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

nrow(train)

# Dataset de validación
x_valid    <- xTrain.norm[-indtrain,]
y_valid    <- yTrain[-indtrain]
rain_valid <- rain[-indtrain]
valid      <- x_valid

# Añado las variables objetivo
valid['y'] <- y_valid
valid['rain'] <- as.factor(rain_valid)

# Miro el dataset
head(valid)

nrow(valid)

# Dataset de test (solo tengo la x, voy a producir la y en el ejercicio)

test <- xTest.norm
head(test)

# Defino el modelo
model.rain <- keras_model_sequential() 

model.rain %>% 
  layer_dense(units = 50, input_shape = ncol(train)-2, activation = "relu", 
              kernel_regularizer = regularizer_l2(0.01)) %>% 
  layer_dropout(0.5) %>%
  layer_dense(units = 10, activation = "relu", kernel_regularizer = regularizer_l2(0.01)) %>%
  layer_dropout(0.5) %>%
  layer_dense(units = 2 , activation = "sigmoid")
str(model.rain)

# Compilo el modelo
model.rain %>% compile(
  optimizer = optimizer_rmsprop(lr = 0.0005), # optimizer_adagrad(lr = 0.01),
  loss = "binary_crossentropy",
  metrics = list("binary_accuracy","categorical_accuracy","accuracy")
)

# Entreno el modelo

my.train.x <- as.matrix(train[ , 1:ncol(test)])
my.train.y <- to_categorical(train$rain, 2)

my.valid.x <- as.matrix(valid[ , 1:ncol(test)])
my.valid.y <- to_categorical(valid$rain, 2)

history <- model.rain %>% fit(x = my.train.x, 
                              y = my.train.y, 
                              epochs = 100, 
                              batch_size = 100,
                              validation_data = list(my.valid.x, my.valid.y),
                              callbacks = list(
                              callback_early_stopping(patience = 10),
                              callback_model_checkpoint(filepath=paste0('lluvia_yes_no.h5'),
                                                        monitor = "val_loss", 
                                                        save_best_only = T)))

plot(history)

k_clear_session()

# Pinto la matriz de confusión 
pred.rain <- model.rain %>% predict_classes(my.valid.x)
table(valid$rain, pred.rain)

# Cargo el modelo, para ver si se ha guardado bien
model.rain.loaded <- load_model_hdf5(filepath = "lluvia_yes_no.h5")

pred.rain.loaded <- model.rain.loaded %>% predict_classes(my.valid.x)
table(valid$rain, pred.rain.loaded)

# Defino el modelo
model.quantity <- keras_model_sequential() 

model.quantity %>% 
  layer_dense(units = 1000, input_shape = ncol(train)-2, activation = "relu") %>% #, 
              #kernel_regularizer = regularizer_l2(0.01)) %>% 
  layer_dropout(0.5) %>%

  layer_dense(units = 500, activation = "relu") %>% #, 
              #kernel_regularizer = regularizer_l2(0.01)) %>%
  layer_dropout(0.5) %>%

  layer_dense(units = 200, activation = "relu") %>% #, 
              #kernel_regularizer = regularizer_l2(0.01)) %>%
  layer_dropout(0.5) %>%

layer_dense(units = 1 , activation = "linear")
str(model.quantity)

# Compilo el modelo
model.quantity %>% compile(
  optimizer = optimizer_rmsprop(lr = 0.0001), #optimizer_adagrad(lr = 0.01), #,
  loss = "mse",
)

# Creo los datasets con sólo días de lluvia
quantity.train <- train[train$rain == 1,]
head(quantity.train)

quantity.valid <- valid[valid$rain == 1,]
head(quantity.valid)

# Entreno el modelo

quantity.train.x <- as.matrix(quantity.train[, 1:ncol(test)])
quantity.train.y <- quantity.train$y

quantity.valid.x <- as.matrix(quantity.valid[, 1:ncol(test)])
quantity.valid.y <- quantity.valid$y

history.quantity <- model.quantity %>% fit(x = quantity.train.x, 
                              y = quantity.train.y, 
                              epochs = 100, 
                              batch_size = 50,
                              validation_data = list(quantity.valid.x, quantity.valid.y),
                              callbacks = list(
                              callback_early_stopping(patience = 50,
                                                      restore_best_weights = T,
                                                      monitor='val_loss'),
                              callback_model_checkpoint(filepath=paste0('lluvia_cantidad.h5'),
                                                        monitor = "val_loss", 
                                                        save_best_only = T))
                              )

plot(history.quantity)

k_clear_session()

# Cargo el modelo de cantidad de lluvia
model.quantity.loaded <- load_model_hdf5(filepath = "lluvia_cantidad.h5")

# Construyo la predicción completa
pred.quantity <- predict(model.quantity.loaded, my.valid.x)
pred.rain.num <- as.numeric(pred.rain.loaded)

pred.quantity.complete <- pred.rain.num * pred.quantity

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((valid$y - as.vector(pred.quantity.complete))^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(valid$y, as.vector(pred.quantity.complete),  method = "spearman")
corr.full

# Ratio de varianzas - mejor si cerca de 1
variance.ratio.full <- var(as.vector(pred.quantity.complete)) / var(valid$y)
variance.ratio.full

# Pinto los valores original contra la predicción
plot(pred.quantity.complete, valid$y)
abline(0,1)

plot(quantity.train.y)

plot(predict(model.quantity.loaded, quantity.valid.x))

plot(predict(model.quantity.loaded, quantity.valid.x), quantity.valid.y,
    xlim = c(0,1),
    ylim = c(0,1))

# Computo la predicción sobre el dataset de test
pred.test.lluvia <- model.rain %>% predict_classes(test)
pred.test.quantity <- as.numeric(predict(model.quantity.loaded, test))

pred.test.complete <- pred.test.lluvia * pred.test.quantity
plot(pred.test.complete)

# Vuelvo a las unidades originales
final.prediction <- max.rain * pred.test.complete
plot(final.prediction)

# Guardo el fichero de predicciones
save(final.prediction, file = "yTest.rda")

# Miro si se ha guardado
yTest <- load(file = "yTest.rda")
yTest

plot(final.prediction)
