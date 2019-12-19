my.bootstrap <- function(vec.x){
    my.N <- length(vec.x)
    my.sample <- sample(1:my.N,my.N,replace=T)
    return(vec.x[my.sample])
}

my.bootstrap.generator <- function(my.x, n.samples){
    my.bootstrap.matrix <- matrix(, nrow = length(my.x), ncol = 0)
    for(i in 1:n.samples){
        my.bootstrap.matrix <- cbind(my.bootstrap.matrix, my.bootstrap(my.x))
    }
    return(my.bootstrap.matrix)
}

my.jackknife.generator <- function(my.x){
    my.jackknife.length <- length(my.x) - 1
    my.jackknife.matrix <- matrix(, nrow = my.jackknife.length, ncol = 0)
    for(i in 1:my.jackknife.length){
        my.jackknife.matrix <- cbind(my.jackknife.matrix, my.x[-i])
    }
    return(my.jackknife.matrix)
}

# Fijo los parametros
my.mean  <- 1.7
my.sigma <- 0.1

# orignal sample size
M <- 1000

# Fijo el numero N de muestras de bootstrap
N = 5000

# Genero la muestra original
my.x = rnorm(M,my.mean,my.sigma)

# Pinto la media y la desviacion standard
meas.mean <- mean(my.x)
meas.sd   <- sd(my.x)

print(meas.mean)
print(meas.sd)

# Produzco las muestras bootstrap
my.bootstrap.samples <- my.bootstrap.generator(my.x, N)

my.bootstrap.mean <- apply(my.bootstrap.samples, MARGIN = 2, FUN = mean)

print(paste("Media muestral de las", N, "muestras de bootstrap:"))
means <- mean(my.bootstrap.mean)
means

print(paste("Desviación típica de la media muestral de las", N, "muestras de bootstrap:"))
sds <- sqrt(1/(N-1)*sum((my.bootstrap.mean - meas.mean)^2))
sds

print(paste("Valor esperado de la desviación típica de la media muestral de una muestra de", M, "elementos:"))
meas.sd / sqrt(M)

my.jackknife.samples <- my.jackknife.generator(my.x)

my.jackknife.mean <- apply(my.jackknife.samples, MARGIN = 2, FUN = mean)

print(paste("Media muestral de las", M, "muestras de jackknife:"))
means <- mean(my.jackknife.mean)
means

print(paste("Desviación típica de la media muestral de las", M, "muestras de jackknife:"))
sds <- sqrt(M/(M-1)*sum((my.jackknife.mean - meas.mean)^2))
sds

print(paste("Valor esperado de la desviación típica de la media muestral de una muestra de", M, "elementos:"))
meas.sd / sqrt(M)
