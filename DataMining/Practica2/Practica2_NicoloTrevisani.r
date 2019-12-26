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
print(paste(meteo$rain[1:10],meteo$y[1:10]))

N <- nrow(meteo)

# creo el dataset de 'entrenamiento'
meteo.calib <- meteo[1:7300,]

# creo el dataset de 'test'
meteo.test <- meteo[7301:N,]












