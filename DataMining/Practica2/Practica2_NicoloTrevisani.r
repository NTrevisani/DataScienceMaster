meteo <- read.csv("meteo.csv", row.name = 1)

head(meteo)

# Load the libraries for PCA
library("FactoMineR")
library("factoextra")

meteo.pca <- PCA(meteo,  graph = FALSE)

get_eig(meteo.pca)

meteo.var <- get_pca_var(meteo.pca)
head(meteo.var$contrib)

print(paste("La constribución de la variable objetivo a la primera componente principal es:",
            format(round(meteo.var$contrib[1,1]*100,4), nsmall = 4),"%"))

?scale
