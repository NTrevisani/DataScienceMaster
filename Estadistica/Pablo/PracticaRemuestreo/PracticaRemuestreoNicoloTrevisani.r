#Establecemos el directorio para poder leer los datos correctamente
rm(list=ls())
#setwd()
file = "CdP_practica_estadistica.csv"

# Leo el dataset y quito los valores 'na'
my.data <- read.csv(file, sep = ",")
str(my.data)
my.data <- na.omit(my.data)
str(my.data)

# formateo la fecha de manera que pueda seleccionar años y meses
my.data$date <- as.Date(my.data$date, "%d/%m/%Y %H:%M")
str(my.data)

# Selecciono eventos del verano de 2014
my.data.2014 <- my.data[format(my.data$date, "%Y") == 2014
                        & (format(my.data$date, "%m") == '07' 
                        |  format(my.data$date, "%m") == '08'
                        |  format(my.data$date, "%m") == '09'),]
str(my.data.2014)

# Selecciono eventos del verano de 2015
my.data.2015 <- my.data[format(my.data$date, "%Y") == 2015
                        & (format(my.data$date, "%m") == '07' 
                        |  format(my.data$date, "%m") == '08'
                        |  format(my.data$date, "%m") == '09'),]
str(my.data.2015)

# Pinto los datos de temperatura de verano 2014
vector.2014 <- my.data.2014$AVG.Temp.

hist(vector.2014,
    xlab = "Temperatura media [C]",
    ylab = "Frecuencia",
    main = "Histograma de temperatura en verano de 2014")

mean.2014 <- mean(vector.2014)
mean.2014
median.2014 <- median(vector.2014)
median.2014
sd.2014 <- sd(vector.2014)
sd.2014

# Pinto los datos de temperatura de verano 2015
vector.2015 <- my.data.2015$AVG.Temp.

hist(vector.2015,
    xlab = "Temperatura media [C]",
    ylab = "Frecuencia",
    main = "Histograma de temperatura en verano de 2015")

mean.2015 <- mean(vector.2015)
mean.2015
median.2015 <- median(vector.2015)
median.2015
sd.2015 <- sd(vector.2015)
sd.2015

# Pongo los datos en una tabla
my.table <- matrix(c(mean.2014, median.2014, sd.2014,
                    mean.2015, median.2015, sd.2015),ncol = 3, nrow = 2, byrow = T)
colnames(my.table)<-c("media", "mediana", "desviacion tipica")
rownames(my.table)<-c("2014", "2015")
my.table

# Defino una función que produzca una muestra de bootstrap, dado un vector de números
my.bootstrap <- function(vec.x){
    my.N <- length(vec.x)
    my.sample <- sample(1:my.N,my.N,replace=T)
    return(vec.x[my.sample])
}

# Defino una función que, dado un vector de numeros y un numero natural N, 
#produzca una matriz con N muestras de bootstrap
my.bootstrap.generator <- function(my.x, n.samples){
    my.bootstrap.matrix <- matrix(, nrow = length(my.x), ncol = 0)
    for(i in 1:n.samples){
        my.bootstrap.matrix <- cbind(my.bootstrap.matrix, my.bootstrap(my.x))
    }
    return(my.bootstrap.matrix)
}

# Indico cuantas muestras quiero
N = 1000

# EMPIEZO POR 2014

# Produzco las muestras de bootstrap
bootstrap.matrix.2014 <- my.bootstrap.generator(vector.2014, N)

# Calculo los estadisticos
mean.bootstrap.2014 <- mean(apply(bootstrap.matrix.2014, FUN = mean, MARGIN = 2))
mean.bootstrap.2014

sd.bootstrap.2014 <- sqrt(1/(N-1)*sum((apply(bootstrap.matrix.2014, FUN = mean, MARGIN = 2) - mean.2014)^2))
sd.bootstrap.2014

# HAGO LO MISMO PARA 2015

# Produzco las muestras de bootstrap
bootstrap.matrix.2015 <- my.bootstrap.generator(vector.2015, N)

# Calculo los estadisticos
mean.bootstrap.2015 <- mean(apply(bootstrap.matrix.2015, FUN = mean, MARGIN = 2))
mean.bootstrap.2015

sd.bootstrap.2015 <- sqrt(1/(N-1)*sum((apply(bootstrap.matrix.2015, FUN = mean, MARGIN = 2) - mean.2015)^2))
sd.bootstrap.2015

# Pongo los datos en una tabla
my.bootstrap.table <- matrix(c(mean.bootstrap.2014, sd.bootstrap.2014, sd.2014,
                    mean.bootstrap.2015, sd.bootstrap.2015, sd.2015),ncol = 3, nrow = 2, byrow = T)
colnames(my.bootstrap.table)<-c("media", "desviacion tipica bootstrap", "desviacion tipica original")
rownames(my.bootstrap.table)<-c("2014", "2015")
my.bootstrap.table

# Defino una función que produzca una matriz 
# con todas las muestras de jackknife de un vector de números
my.jackknife.generator <- function(my.x){
    my.jackknife.length <- length(my.x) - 1
    my.jackknife.matrix <- matrix(, nrow = my.jackknife.length, ncol = 0)
    for(i in 1:my.jackknife.length){
        if (i %% 100 == 0) print(i) 
        my.jackknife.matrix <- cbind(my.jackknife.matrix, my.x[-i])
    }
    return(my.jackknife.matrix)
}

# EMPIEZO POR 2014

# defino el numero de muestras de jackknife que puedo producir
M = length(vector.2014)

# Produzco las muestras de jackknife
jackknife.matrix.2014 <- my.jackknife.generator(vector.2014)

# Calculo los estadisticos
mean.jackknife.2014 <- mean(apply(jackknife.matrix.2014, FUN = mean, MARGIN = 2))
mean.jackknife.2014

sd.jackknife.2014 <- sqrt(M/(M-1)*sum((apply(jackknife.matrix.2014, FUN = mean, MARGIN = 2) - mean.2014)^2))
sd.jackknife.2014

# HAGO LO MISMO PARA 2015

# defino el numero de muestras de jackknife que puedo producir
M = length(vector.2015)

# Produzco las muestras de jackknife
jackknife.matrix.2015 <- my.jackknife.generator(vector.2015)

# Calculo los estadisticos
mean.jackknife.2015 <- mean(apply(jackknife.matrix.2015, FUN = mean, MARGIN = 2))
mean.jackknife.2015

sd.jackknife.2015 <- sqrt(M/(M-1)*sum((apply(jackknife.matrix.2015, FUN = mean, MARGIN = 2) - mean.2015)^2))
sd.jackknife.2015

# Pongo los datos en una tabla
my.jackknife.table <- matrix(c(mean.jackknife.2014, sd.jackknife.2014, sd.2014,
                    mean.jackknife.2015, sd.jackknife.2015, sd.2015),ncol = 3, nrow = 2, byrow = T)
colnames(my.jackknife.table)<-c("media", "desviacion tipica jacknife", "desviacion tipica original")
rownames(my.jackknife.table)<-c("2014", "2015")
my.jackknife.table
