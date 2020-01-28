# Cargo el dataset
meteo <- read.csv("meteo.csv", row.name = 1)

# Me quedo solo con las variables que tengas correlación con y grande
# |corr(y,Xn)| > 0.4

meteo.slim <- meteo[cor(meteo,  method = "spearman")[1,] > 0.4 | cor(meteo,  method = "spearman")[1,] < -0.4]
ncol(meteo.slim)

head(meteo.slim)

# Fijo el seed, para que el sample que uso para separar en train y test
# de siempre el mismo resultado.
set.seed(23)

# Separo en set de train y de test. En total, uso solo los primeros 5000 días del dataset 
n <- 5000

# indice de train
indtrain <- sample(1:n, round(0.75*n)) 
meteo.slim.train <- meteo.slim[indtrain,]

# indice de test
indtest <- setdiff(1:n, indtrain)      
meteo.slim.test  <- meteo.slim[indtest,]

# Dataset de entrenamiento: meteo.slim.train
# Dataset de test:          meteo.slim.test  

# converto la variable objetivo en categórica
rain = ifelse(meteo.slim$y < 1, 0, 1)
meteo.slim$rain = as.factor(rain)

# Cargo la libreria necesaria para usar los trees
library(tree)

# Quito 'y' y me quedo solo con 'rain' 
meteo.rain <- meteo.slim[,2:ncol(meteo.slim)]

head(meteo.rain)

# Entreno un arbol que dejo crecer sin limites
t.tree = tree(formula = rain ~ ., 
              data = meteo.rain, 
              subset = indtrain, 
              control = tree.control(length(indtrain), 
                                     mincut = 1, 
                                     minsize = 2, 
                                     mindev = 0))

# Pinto el arbol
plot(t.tree)
text(t.tree, pretty = F)

# Cuento las hojas terminales
print(paste("El arbol completo tiene",
length(t.tree$frame$var[t.tree$frame$var == '<leaf>']), "hojas"))

# Ahora uso cross-validation para podar el arbol completo,
# haciendo que sea más generalizable, o más útil para predecir

# Preparo la validación cruzada
tree.cv <- cv.tree(object = t.tree,
                    FUN = prune.tree,
                    K = 10)

# Pinto la accuracy en función de la profundidad
plot(tree.cv$size, tree.cv$dev / length(indtrain), type = "b",
     xlab = "Tree Size", ylab = "CV-RMSE",
     xlim = c(0,10))

# Podo el arbol completo según lo resultados de la validación cruzada
opt.tree <- prune.tree(t.tree, best = 6)

# Pinto el arbol optimo
plot(opt.tree)
text(opt.tree, pretty = F)

summary(opt.tree)

# Preparo los dataset de train y de test
meteo.rain.train <- meteo.rain[indtrain,]
meteo.rain.test <- meteo.rain[-indtrain,]

# Guardo las predicciones del arbol optimo
pred.train = predict(opt.tree, newdata = meteo.rain.train, type = "class")
pred.test  = predict(opt.tree, newdata = meteo.rain.test, type = "class")

# Preparo el dataset de entrenamiento que tenga solo los días de lluvia
# 'cont' en el nombre significa ~continuo (la lluvia ya no es un factor)

meteo.cont.rain <- meteo.slim[meteo.slim$rain == 1,]
meteo.cont.rain <- meteo.cont.rain[1:ncol(meteo.cont.rain)-1]
head(meteo.cont.rain)
nrow(meteo.cont.rain)

# Preparo el dataset de entrenamiento que tenga 
# tanto los días sin lluvia como los días sin lluvia
# 'cont' en el nombre significa ~continuo (la lluvia ya no es un factor)

meteo.cont <- meteo.slim[1:ncol(meteo.slim)-1]
head(meteo.cont)
nrow(meteo.cont)

# Entreno un arbol que dejo crecer sin limites
# Uso el dataset de entrenamiento completo

full.tree = tree(formula = y ~ ., 
              data = meteo.cont, 
              subset = indtrain, 
              method = "cubist",                 
              control = tree.control(length(indtrain), 
                                     mincut = 1, 
                                     minsize = 2, 
                                     mindev = 0))

# Pinto el arbol
plot(full.tree)
text(full.tree, pretty = F)

# Cuento las hojas terminales
print(paste("El arbol completo tiene",
length(full.tree$frame$var[full.tree$frame$var == '<leaf>']), "hojas"))

# Ahora uso cross-validation para podar el arbol completo,
# haciendo que sea más generalizable, o más útil para predecir

# Preparo la validación cruzada
full.tree.cv <- cv.tree(object = full.tree,
                    FUN = prune.tree,
                    K = 10)

# Pinto la accuracy en función de la profundidad
plot(full.tree.cv$size, full.tree.cv$dev / length(indtrain), type = "b",
     xlab = "Tree Size", ylab = "CV-RMSE",
     xlim = c(0,30))

# Podo el arbol completo según lo resultados de la validación cruzada
opt.tree.full <- prune.tree(full.tree, best = 10)

# Pinto el arbol optimo
plot(opt.tree.full)
text(opt.tree.full, pretty = F)

summary(opt.tree.full)

print(opt.tree.full)

# Preparo los dataset de train y de test
meteo.cont.full.train <- meteo.cont[indtrain,]
meteo.cont.full.test <- meteo.cont[-indtrain,]

# Guardo las predicciones del arbol optimo entrenado con todos los eventos (full)
pred.cont.full.train = predict(opt.tree.full, newdata = meteo.cont.full.train)
pred.cont.full.test  = predict(opt.tree.full, newdata = meteo.cont.full.test)

# Entreno un arbol que dejo crecer sin limites
# Uso el dataset de entrenamiento con solo días de lluvia

rain.tree = tree(formula = y ~ ., 
              data = meteo.cont.rain, 
              subset = indtrain, 
              method = "cubist", # uso el método cubist para obtener predicciones continuas
              control = tree.control(length(indtrain), 
                                     mincut = 1, 
                                     minsize = 2, 
                                     mindev = 0))

# Pinto el arbol
plot(rain.tree)
text(rain.tree, pretty = F)

# Cuento las hojas terminales
print(paste("El arbol completo entrenado solo con días de lluvia tiene",
length(rain.tree$frame$var[rain.tree$frame$var == '<leaf>']), "hojas"))

# Ahora uso cross-validation para podar el arbol completo,
# haciendo que sea más generalizable, o más útil para predecir

# Preparo la validación cruzada
rain.tree.cv <- cv.tree(object = rain.tree,
                    FUN = prune.tree,
                    K = 10)

# Pinto la accuracy en función de la profundidad
plot(rain.tree.cv$size, rain.tree.cv$dev / length(indtrain), type = "b",
     xlab = "Tree Size", ylab = "CV-RMSE",
     xlim = c(0,10))

# Podo el arbol completo según lo resultados de la validación cruzada
# Vemos que el arbol optimo deberia tener 5 hojas finales.
opt.tree.rain <- prune.tree(rain.tree, best = 5)

# Pinto el arbol optimo
plot(opt.tree.rain)
text(opt.tree.rain, pretty = F)
print(opt.tree.rain)

# Podriamos pensar que la usar solo 5 hojas implique
# reducir la acpacidad del arbol en describir la variabilidad 
# de la cantidad de lluvia. Intentamos usar 10 hojas
opt.tree.rain.10 <- prune.tree(rain.tree, best = 10)

# Pinto el arbol optimo
plot(opt.tree.rain.10)
text(opt.tree.rain.10, pretty = F)
print(opt.tree.rain.10)

# Preparo los dataset de train y de test
meteo.cont.rain.train <- na.omit(meteo.cont.rain[indtrain,])
meteo.cont.rain.test  <- na.omit(meteo.cont.rain[-indtrain,])

# Guardo las predicciones del arbol optimo
pred.cont.rain.test.all = predict(opt.tree.rain, newdata = meteo.cont.full.test)
pred.cont.rain.test     = predict(opt.tree.rain, newdata = meteo.cont.full.test)

# Guardo las predicciones del arbol con 10 hojas
pred.cont.rain.test.all.10 = predict(opt.tree.rain.10, newdata = meteo.cont.full.test)
pred.cont.rain.test.10     = predict(opt.tree.rain.10, newdata = meteo.cont.full.test)

# Mido el accuracy de la classificación binaria lluvia/no-lluvia
print("Accuracy de la clasificación lluvia/no-lluvia")
100*sum(diag(table(meteo.rain.test[,"rain"], pred.test))) / length(pred.test)

# Miro también 'a ojo' las primeras 20 predicciones, comparadas con el dataset original de test
meteo.rain.test[1:20,"rain"]
pred.test[1:20]

# Y la matriz de confusión, para evaluar los falsos positivos/negativos
table(pred.test, meteo.rain.test$rain)

table(pred.test)
table(meteo.rain.test$rain)

# Construyo la predicción completa
pred.test.num <- as.numeric(pred.test) - 1
pred.cont.full.test.complete <- pred.test.num*pred.cont.full.test

# Pinto los valores original contra la predicción
plot(pred.cont.full.test.complete, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.cont.full.test.complete)^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(meteo.cont.full.test[,'y'], pred.cont.full.test.complete,  method = "spearman")
corr.full

# Construyo la predicción completa
pred.test.num <- as.numeric(pred.test) - 1
pred.cont.rain.test.complete <- pred.test.num*pred.cont.rain.test

# Pinto los valores original contra la predicción
plot(pred.cont.rain.test.complete, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.rain <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.cont.rain.test.complete)^2))
rmse.rain

# Correlación - mejor si es alta
corr.rain <- cor(meteo.cont.full.test[,'y'], pred.cont.rain.test.complete,  method = "spearman")
corr.rain

# Lo mismo, pero con el arbol de 10 hoajs

# Construyo la predicción completa
pred.test.num <- as.numeric(pred.test) - 1
pred.cont.rain.test.complete.10 <- pred.test.num*pred.cont.rain.test.10

# Pinto los valores original contra la predicción
plot(pred.cont.rain.test.complete.10, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.rain <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.cont.rain.test.complete.10)^2))
rmse.rain

# Correlación - mejor si es alta
corr.rain <- cor(meteo.cont.full.test[,'y'], pred.cont.rain.test.complete.10,  method = "spearman")
corr.rain

library(randomForest)

# Ya tengo los datasets de entrenamiento y de test listos:

# Clasificación:
# - Todos los días (lluvia y no-lluvia):
#   - entrenamiento: meteo.rain.train
#   - test: meteo.rain.test



# Predicción continua:
# - Todos los días (lluvia y no-lluvia):
#   - entrenamiento: meteo.cont.full.train
#   - test: meteo.cont.full.test

# - Solo días de lluvia:
#   - entrenamiento: meteo.cont.rain.train
#   - test: meteo.cont.rain.test

# Entreno un random forest para predecir la ocurrencia de la lluvia

rf <- randomForest(rain ~ ., 
                   data = meteo.rain.train,
                   ntree = 1000,
                   importance=TRUE,
                   proximity=TRUE)
rf

# Pinto los errores OOB en función del numero de arboles 
plot(rf$err.rate[, 1], type = "l", xlab = "no. trees", ylab = "OOBerror",ylim = c(0.13,0.16))
grid()

# Repito el entrenamiento con 180 arboles y saco la predicción de test

rf.opt <- randomForest(rain ~ ., 
                   data = meteo.rain.train,
                   ntree = 180,
                   importance=TRUE,
                   proximity=TRUE)
rf.opt

pred.rf.test = predict(rf.opt, meteo.rain.test)

# Entreno un random forest para predecir la ocurrencia de la lluvia
# Uso todos los eventos (lluvia/no-lluvia)

rf.cont.full <- randomForest(y ~ ., 
                   data = meteo.cont.full.train,
                   ntree = 1000,
                   importance=TRUE,
                   proximity=TRUE)

rf.cont.full

# Pinto los errores OOB en función del numero de arboles 
plot(rf.cont.full$mse, type = "l", xlab = "no. trees", ylab = "OOBerror", ylim = c(25,30))
grid()

# Repito el entrenamiento con 200 arboles y saco la predicción de test

rf.cont.full.opt <- randomForest(y ~ ., 
                   data = meteo.cont.full.train,
                   ntree = 200,
                   importance=TRUE,
                   proximity=TRUE)
rf.cont.full.opt

pred.rf.full.opt.test = predict(rf.cont.full.opt, meteo.cont.full.test)

# Entreno un random forest para predecir la ocurrencia de la lluvia
# Uso solo los eventos con lluvia

rf.cont.rain <- randomForest(y ~ ., 
                   data = meteo.cont.rain.train,
                   ntree = 1000,
                   importance=TRUE,
                   proximity=TRUE)

rf.cont.rain

# Pinto los errores OOB en función del numero de arboles 
plot(rf.cont.rain$mse, type = "l", xlab = "no. trees", ylab = "OOBerror", ylim = c(110,120))
grid()

# Repito el entrenamiento con 200 arboles y saco la predicción de test

rf.cont.rain.opt <- randomForest(y ~ ., 
                   data = meteo.cont.rain.train,
                   ntree = 200,
                   importance=TRUE,
                   proximity=TRUE)
rf.cont.rain.opt

pred.rf.cont.rain.opt = predict(rf.cont.rain.opt, meteo.cont.full.test)

# Mido el accuracy de la classificación binaria lluvia/no-lluvia
print("Accuracy de la clasificación lluvia/no-lluvia")
100*sum(diag(table(meteo.rain.test[,"rain"], pred.rf.test))) / length(pred.rf.test)

# Y la matriz de confusión, para evaluar los falsos positivos/negativos
table(pred.rf.test, meteo.rain.test$rain)

# Miro también 'a ojo' las primeras 20 predicciones, comparadas con el dataset original de test
meteo.rain.test[1:20,"rain"]
pred.rf.test[1:20]

table(pred.rf.test)
table(meteo.rain.test$rain)

# Predicción completa
pred.complete.full <- pred.rf.full.opt.test * (as.numeric(pred.rf.test) - 1)

# Pinto los valores original contra la predicción
plot(pred.complete.full, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.complete.full)^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(meteo.cont.full.test[,'y'], pred.complete.full,  method = "spearman")
corr.full

pred.complete.rain <- pred.rf.cont.rain.opt * (as.numeric(pred.rf.test) - 1)

# Pinto los valores original contra la predicción
plot(pred.complete.rain, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.complete.rain)^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(meteo.cont.full.test[,'y'], pred.complete.rain,  method = "spearman")
corr.full

# Ya tengo los datasets de entrenamiento y de test listos:

# Clasificación:
# - Todos los días (lluvia y no-lluvia):
#   - entrenamiento: meteo.rain.train
#   - test: meteo.rain.test



# Predicción continua:
# - Todos los días (lluvia y no-lluvia):
#   - entrenamiento: meteo.cont.full.train
#   - test: meteo.cont.full.test

# - Solo días de lluvia:
#   - entrenamiento: meteo.cont.rain.train
#   - test: meteo.cont.rain.test

# Entreno el modelo para la ocurrencia de la lluvia
lin.model <- glm(rain ~ ., 
                 data = meteo.rain.train, 
                 family = binomial(link = "logit"))

lin.model

# Transformo la predicción continua en categorica (lluvia/no-lluvia)
# Fijo el umbral a 0.5
out.lin.model <- lin.model$fitted.values
out.bin.lin.model <- as.double(out.lin.model > 0.5)

# Histograma de salida del modelo
hist(out.lin.model, main = "Histograma de salida del modelo")

# Histograma de salida del modelo (con variable categorica)
hist(out.bin.lin.model, main = "Histograma de salida del modelo (con variable categorica)")

# Preparo la predicción de clasificación de días de lluvia/no lluvia
out.test.rain <- predict(object = lin.model, newdata = meteo.rain.test);
out.bin.test.rain <- as.double(out.test.rain > 0.5)

# Tasa de acierto (test)
print("Accuracy sobre el datset de test:")
100*sum(diag(table(meteo.rain.test$rain, out.bin.test.rain))) / length(out.bin.test.rain)

print(paste("Días con lluvia (1) y sin lluvia (0) en el dataset de test:"))
table(meteo.rain.test$rain)

# Matriz de confusión de test
print("Matriz de confusión de test:")
table(meteo.rain.test$rain, out.bin.test.rain)

# Entreno el modelo para la cantidad de lluvia
# Selecciono sólo días de lluvia porque la familia de funciones Gamma
# acepta valores mayores de 0

lin.model.cont <- glm(y ~ ., 
                      data = meteo.cont.rain.train,
                      family = Gamma(link = "inverse"))

lin.model.cont

# Miro la salida del modelo
out.lin.model.cont <- lin.model.cont$fitted.values

# Histograma de salida del modelo
hist(out.lin.model.cont,
     breaks = 100,
     xlim = c(0,100),
     main = "Histograma de salida del modelo")

# Miro como el modelo predice sobre el dataset de test
# con solo días de lluvia
out.test.rain.cont <- predict(object = lin.model.cont, 
                              newdata = meteo.cont.rain.test,
                              type = "response")
out.test.rain.cont[1:20]

# Miro como el modelo predice sobre el dataset de test
# con días con lluvia y dias sin lluvia
out.train.rain.cont.all <- predict(object = lin.model.cont, 
                              newdata = meteo.cont.full.test,
                              type = "response")
out.train.rain.cont.all[1:20]

# Produzco las predicciones completas: 
# multiplico la clasificación lluvia/no-lluvia por la cantidad

glm.complete.rain <- out.train.rain.cont.all * (as.numeric(out.bin.test.rain))

for (i in 1:20){
    print(paste(
        format(round(glm.complete.rain[i],2), nsmall = 2), "    ",
        format(round(meteo.cont.full.test[i,1],2), nsmall = 2))
    )
}

# Pinto los valores original contra la predicción
plot(glm.complete.rain, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((meteo.cont.full.test[,'y'] - glm.complete.rain)^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(meteo.cont.full.test[,'y'], glm.complete.rain,  method = "spearman")
corr.full

# Ya tengo los datasets de entrenamiento y de test listos:

# Clasificación:
# - Todos los días (lluvia y no-lluvia):
#   - entrenamiento: meteo.rain.train
#   - test: meteo.rain.test

# Predicción continua:
# - Todos los días (lluvia y no-lluvia):
#   - entrenamiento: meteo.cont.full.train
#   - test: meteo.cont.full.test
#
# - Solo días de lluvia:
#   - entrenamiento: meteo.cont.rain.train
#   - test: meteo.cont.rain.test

# Miro el rango de las variables
plot(1:38,apply(meteo.cont.full.train,2,mean),
    xlab = "variable",
    ylab = "range [a.u.]",
    main = "Mean values of the dataset variables")

# Uso scale para que todas las variables tengan el mismo order de magnitud

# Dataset de entrenamiento (en el caso de knn, más bien de calibración)
meteo.cont.full.train.scale <- scale(meteo.cont.full.train, center = TRUE, scale = TRUE)

# Dataset de test
meteo.cont.full.test.scale <- scale(meteo.cont.full.test, center = TRUE, scale = TRUE)

# Miro el rango de las variables después de haber usado scale
plot(1:38,apply(meteo.cont.full.train.scale,2,mean),
    xlab = "variable",
    ylab = "range [a.u.]",
    main = "Mean values of the dataset variables")

# Cargo las librerias necesarias
library(FNN)
library(caret)

ctrl <- trainControl(method = "cv", 
                     number = 10)

# cambio el número de vecinos cercanos
knn <- train(y ~ ., 
             data = meteo.cont.full.train, 
             method = "knn", 
             preProcess = c("center", "scale"), 
             trControl = ctrl,
             tuneGrid = expand.grid(k = 1:50))

plot(knn)

# knn.reg(train, test = NULL, y, k = 3, algorithm=c("kd_tree", "cover_tree", "brute"))

# Predigo en el dataset de test usando k = 20 vecinos cercanos
k = 20

pred.knn.opt <- knn.reg(train = scale(meteo.cont.full.train[,-1]), 
                        test = scale(meteo.cont.full.test[,-1]), 
                        y = meteo.cont.full.train$y, 
                        k = k)


# Ahora lo mismo, pero con solo 1 vecino (K = 1)
k = 1

pred.knn.1 <- knn.reg(train = scale(meteo.cont.full.train[,-1]), 
                      test = scale(meteo.cont.full.test[,-1]), 
                      y = meteo.cont.full.train$y, 
                      k = k)

# Pinto los valores original contra la predicción - caso k = 20
plot(pred.knn.opt$pred, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.knn.opt$pred)^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(meteo.cont.full.test[,'y'], pred.knn.opt$pred,  method = "spearman")
corr.full

# Pinto los valores original contra la predicción - caso k = 1
plot(pred.knn.1$pred, meteo.cont.full.test[,'y'])
abline(0,1)

# RMSE - mejor si es baja
rmse.full <- sqrt(mean((meteo.cont.full.test[,'y'] - pred.knn.1$pred)^2))
rmse.full

# Correlación - mejor si es alta
corr.full <- cor(meteo.cont.full.test[,'y'], pred.knn.1$pred,  method = "spearman")
corr.full


