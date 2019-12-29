# Cargo el dataset
meteo <- read.csv("meteo.csv", row.name = 1)

# Pinto las primeras lineas
head(meteo)

# Miro el rango de las variables
plot(1:321,apply(meteo,2,mean),
    xlab = "variable",
    ylab = "range [a.u.]",
    main = "Mean values of the dataset variables")

# Load the libraries for PCA
library("FactoMineR")
library("factoextra")

# Busco las componentes principales
meteo.pca <- prcomp(meteo)

# Pinto la varianza explicada por cada componente
eigenvalues <- get_eig(meteo.pca)
eigenvalues

# Pinto la composición de cada componente principal
# en terminos de las variables
meteo.var <- get_pca(meteo.pca)
head(meteo.var$contrib)

# Contribución de la variable objetivo a la primera componente principal
print(paste("La contribución de la variable objetivo a la primera componente principal es:",
            format(round(meteo.var$contrib[1,1],6), nsmall = 6)))

# Componente principal que recibe la contribución máxima de
# la variable objetivo

best.contrib <- which(meteo.var$contrib[1,] == max(meteo.var$contrib[1,]))

print(paste("La contribución máxima de la variable objetivo es a la componente principal",
            best.contrib,
            ". Hasta dicha componente principal se explica el",
            format(round(eigenvalues$cumulative.variance.percent[best.contrib],4), nsmall = 2),"%",
           "de la varianza"))

# Plot del porcentage de varianza explicado por cada una de
# las primeras 10 componentes principales
fviz_screeplot(meteo.pca, addlabels = TRUE, ylim = c(0, 75))

# Plot del porcentage de varianza cumulada explicado por 
# las primeras 9 componentes principales

plot.eigenvalues <- eigenvalues[1:9,]
plot.eigenvalues$Dimensions <- row.names(plot.eigenvalues)

ggplot(data=plot.eigenvalues, aes(x=Dimensions, y = cumulative.variance.percent, group=1)) + 
        geom_bar(stat="identity", fill="steelblue") +
        geom_text(aes(label=floor(cumulative.variance.percent)), vjust=-0.3, size=3.5) +
        geom_line(color="black") +
        geom_point() + 
        ggtitle("Cumulative variance plot") +
        theme_minimal()

# Contribución de cada variable a la primera componente principal
plot(1:321,meteo.var$contrib[,1])

# Busco las componentes principales
meteo.pca.scale <- prcomp(meteo, scale. = T)

# Pinto la varianza explicada por cada componente
eigenvalues.scale <- get_eig(meteo.pca.scale)
eigenvalues.scale

# Pinto la composición de cada componente principal
# en terminos de las variables
meteo.var.scale <- get_pca(meteo.pca.scale)
head(meteo.var.scale$contrib)

# Contribución de la variable objetivo a la primera componente principal
print(paste("La contribución de la variable objetivo a la primera componente principal es:",
            format(round(meteo.var.scale$contrib[1,1],4), nsmall = 4)))

# Componente principal que recibe la contribución máxima de
# la variable objetivo

best.contrib.scale <- which(meteo.var.scale$contrib[1,] == max(meteo.var.scale$contrib[1,]))

print(paste("La contribución máxima de la variable objetivo es a la componente principal",
            best.contrib.scale,
            ". Hasta dicha componente principal se explica el",
            format(round(eigenvalues.scale$cumulative.variance.percent[best.contrib.scale],4), nsmall = 2),"%",
           "de la varianza"))

# Plot del porcentage de varianza explicado por cada una de
# las primeras 10 componentes principales
fviz_screeplot(meteo.pca.scale, addlabels = TRUE, ylim = c(0, 75))

# Plot del porcentage de varianza cumulada explicado por 
# las primeras 9 componentes principales

plot.eigenvalues.scale <- eigenvalues.scale[1:9,]
plot.eigenvalues.scale$Dimensions <- row.names(plot.eigenvalues.scale)

ggplot(data=plot.eigenvalues.scale, aes(x=Dimensions, y = cumulative.variance.percent, group=1)) + 
        geom_bar(stat="identity", fill="steelblue") +
        geom_text(aes(label=floor(cumulative.variance.percent)), vjust=-0.3, size=3.5) +
        geom_line(color="black") +
        geom_point() + 
        ggtitle("Cumulative variance plot") +
        theme_minimal()

# Contribución de cada variable a las primeras tres componentes principales
plot(1:321,meteo.var.scale$contrib[,1])
plot(1:321,meteo.var.scale$contrib[,2])
plot(1:321,meteo.var.scale$contrib[,3])

# converto la variable objetivo en categórica
rain = ifelse(meteo$y < 1, 0, 1)
meteo$rain = as.factor(rain)
#print(paste(meteo$rain[1:10],meteo$y[1:10]))

N <- nrow(meteo)
M <- ncol(meteo)

# creo el dataset de 'entrenamiento'
meteo.calib <- meteo[1:7300,2:M]

# creo el dataset de 'test'
meteo.test <- meteo[7301:N,2:M]
head(meteo.calib)

# Vuelvo a sacar las componentes principales para 
# el dataset de 'entrenamiento'

# (No considero la variable objetivo)
meteo.pca.calib <- prcomp(meteo.calib[,1:320], scale = TRUE)
meteo.pca.calib$x

# Pinto la varianza explicada por cada componente
eigenvalues.calib <- get_eig(meteo.pca.calib)
eigenvalues.calib

# Plot del porcentage de varianza explicado por cada una de
# las primeras 10 componentes principales
fviz_screeplot(meteo.pca.calib, addlabels = TRUE, ylim = c(0, 65))

# Plot del porcentage de varianza cumulada explicado por 
# las primeras 9 componentes principales

plot.eigenvalues.calib <- eigenvalues.calib[1:9,]
plot.eigenvalues.calib$Dimensions <- row.names(plot.eigenvalues.calib)

ggplot(data=plot.eigenvalues.calib, aes(x=Dimensions, y = cumulative.variance.percent, group=1)) + 
        geom_bar(stat="identity", fill="steelblue") +
        geom_text(aes(label=floor(cumulative.variance.percent)), vjust=-0.3, size=3.5) +
        geom_line(color="black") +
        geom_point() + 
        ggtitle("Cumulative variance plot") +
        theme_minimal()

library(caret)

thresholds <- c(0.6, 0.8, 0.9)#, 0.95)

knn.vector <- c()

zeros <- rep(0,15)
plot(1:15, zeros, type = "l",
     xlab = "Neighbours",
     ylab = "Accuracy (repeated cross validation)",
     main = paste("Accuracy vs number of neighbours"),
     ylim = c(0,1))

# Just counter for the colours
cols <- rainbow(4)
p <- 1

for (i in thresholds){

    print(paste("Entrenamiento usando",i*100,"% de la varianza"))
    
    # cambio el umbral de varianza
    ctrl <- trainControl(method = "cv", 
                     number = 3, 
                     preProcOptions = list(thresh = i))

    # cambio el número de vecinos cercanos
    knn <- train(rain ~ ., meteo.calib, 
                     method = "knn", 
                     preProcess = c("center", "scale", "pca"), 
                     trControl = ctrl,
                     tuneGrid = expand.grid(k = 1:15))
    
    knn.vector <- c(knn.vector, knn)
    
    # imprimo los resultados
    print(knn)
    
    # pinto los resultados (no funciona)
    plot(knn, 
         col = cols[p],
         add = T)
    
    p <- p + 1
}

legend("bottomright", legend=paste("Variance:",thresholds), lwd=2, col=cols)

# Ahora hago la rotación del dataset de test para el espacio de los PCA
# (https://www.datacamp.com/community/tutorials/pca-analysis-r)

# Hago el scale del dataset de test
s.meteo.test <- scale(meteo.test[,1:320], center= meteo.pca.calib$center)

# Ahora puedo hacer la rotación
meteo.pca.test <- s.meteo.test %*% meteo.pca.calib$rotation
head(meteo.pca.test)

# Usando el 90% de la varianza (10 componentes principales),
# y 7 vecinos cercanos, espero obtener el 85% de tasa de acierto

n.pca = 10
ka = 7

library(class)

pred <- knn(train = meteo.pca.calib$x[,1:n.pca], 
            test = meteo.pca.test[,1:n.pca], 
            cl = meteo.calib$rain, 
            k = ka)

# Función para evaluar la tasa de acierto
acc.class = function(x, y) {
  stopifnot(length(x) == length(y))
  return(sum(diag(table(x, y))) / length(x))
}

# El resultado que obtengo aplicando el método al dataset de test
print(paste("Usando", n.pca,"componentes principales y",ka,"vecinos cercanos obtengo una tasa de acierto de:",
            format(round(acc.class(pred, meteo.test$rain)*100,2), nsmall = 2),"%"))

# converto la variable objetivo en categórica
heavy.rain = ifelse(meteo$y < 20, 0, 1)
meteo$heavy.rain = as.factor(heavy.rain)

N <- nrow(meteo)
M <- ncol(meteo)

# creo el dataset de 'entrenamiento'
meteo.calib <- meteo[1:7300,2:M]

# creo el dataset de 'test'
meteo.test <- meteo[7301:N,2:M]
head(meteo.calib)

# Repito el 'entrenamiento'

thresholds <- c(0.6, 0.8, 0.9)#, 0.95)

knn.vector <- c()

zeros <- rep(0,15)
plot(1:15, zeros, type = "l",
     xlab = "Neighbours",
     ylab = "Accuracy (repeated cross validation)",
     main = paste("Accuracy vs number of neighbours"),
     ylim = c(0,1))

# Just counter for the colours
cols <- rainbow(4)
p <- 1

for (i in thresholds){

    print(paste("Entrenamiento usando",i*100,"% de la varianza"))
    
    # cambio el umbral de varianza
    ctrl <- trainControl(method = "cv", 
                     number = 3, 
                     preProcOptions = list(thresh = i))

    # cambio el número de vecinos cercanos
    knn <- train(heavy.rain ~ ., meteo.calib[,-321], 
                     method = "knn", 
                     preProcess = c("center", "scale", "pca"), 
                     trControl = ctrl,
                     tuneGrid = expand.grid(k = 1:15))
    
    knn.vector <- c(knn.vector, knn)
    
    # imprimo los resultados
    print(knn)
    
    # pinto los resultados (no funciona)
    plot(knn, 
         col = cols[p],
         add = T)
    
    p <- p + 1
}

legend("bottomright", legend=paste("Variance:",thresholds), lwd=2, col=cols)

# Usando el 80% de la varianza (4 componente principal),
# y 5 vecinos cercanos, espero obtener el 97% de tasa de acierto

n.pca = 4
ka = 5

library(class)

pred <- knn(train = meteo.pca.calib$x[,1:n.pca], 
            test = meteo.pca.test[,1:n.pca], 
            cl = meteo.calib$heavy.rain, 
            k = ka)

# El resultado que obtengo aplicando el método al dataset de test
print(paste("Usando", n.pca,"componentes principales y",ka,"vecinos cercanos obtengo una tasa de acierto de:",
            format(round(acc.class(pred, meteo.test$rain)*100,2), nsmall = 2),"%"))

print(paste("Días con lluvia (1) y sin lluvia (0) en el dataset de calibración:"))
table(meteo.calib$rain)

print(paste("Días con lluvia fuerte (1) y sin lluvia fuerte (0) en el dataset de calibración:"))
table(meteo.calib$heavy.rain)


print(paste("Días con lluvia (1) y sin lluvia (0) en el dataset de test:"))
table(meteo.test$rain)

print(paste("Días con lluvia fuerte (1) y sin lluvia fuerte (0) en el dataset de test:"))
table(meteo.test$heavy.rain)

# Busco entender por qué el método knn parece no funcionar
# para los días de lluvia fuerte
df.plot <- meteo.pca.calib$x[,1:2]
df.plot <- data.frame(df.plot,meteo.calib$heavy.rain, meteo.calib$rain)
names(df.plot) = c("PC1","PC2","heavy.rain","rain")

# Pinto un scatter plot de las 2 componentes principales
# para días de lluvia y días sin lluvia
df.plot.rain <- df.plot[df.plot$rain == 1,]
df.plot.no.rain <- df.plot[df.plot$rain == 0,]

plot(df.plot.no.rain$PC1, df.plot.no.rain$PC2,
    col = "red",
    main = "Rain scatter plot",
    xlab = "PC1",
    ylab = "PC2")
points(df.plot.rain$PC1,df.plot.rain$PC2,
    col = "blue")
legend("topleft", legend=c("Rain","No rain"), lwd=2, col=c("blue","red"))


# Pinto un scatter plot de las 2 componentes principales
# para días de lluvia fuerte y días sin lluvia
df.plot.heavy.rain <- df.plot[df.plot$heavy.rain == 1,]
df.plot.no.heavy.rain <- df.plot[df.plot$heavy.rain == 0,]

plot(df.plot.no.heavy.rain$PC1,df.plot.no.heavy.rain$PC2,
    col = "red",
    main = "Heavy rain scatter plot",
    xlab = "PC1",
    ylab = "PC2")
points(df.plot.heavy.rain$PC1,df.plot.heavy.rain$PC2,
    col = "blue")
legend("topleft", legend=c("Heavy rain","No rain"), lwd=2, col=c("blue","red"))


