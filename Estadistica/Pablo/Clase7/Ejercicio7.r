get.y <- function(x, intercept, angular.coeff, std.dev.a, std.dev.b){
    y <- c()
    sigma <- c()
    for (value in x){
        my.sigma  <- std.dev.a + std.dev.b * value^2
        sigma <- c(sigma, my.sigma) 
        y <- c(y, rnorm(1, (angular.coeff*value + intercept), sigma))
    }
    my.out.table <- cbind(y, sigma)
    return(as.data.frame(my.out.table))
}

# Esto deberia ser valido para cualquier polinomio.
# parameters es un vector de parametros (e.g. parameters = c(a,b,c))

get.pol.n <- function(x, parameters, std.dev.a, std.dev.b){
    y <- c()
    sigma <- c()
    for (value in x){
        my.sigma  <- std.dev.a + std.dev.b * value^2
        sigma <- c(sigma, my.sigma) 
        model <- 0 
        for (i in 1:length(parameters)){
            model <- model + parameters[i] * value^(i - 1)
            }
            y <- c(y, rnorm(1, model, sigma))        
    }
    my.out.table <- cbind(y, sigma)
    return(as.data.frame(my.out.table))
}

# Defino la likelihood

my.ML <- function(vec.x, mat.y, grade){
    cov.y <- diag(mat.y$sigma)
    ones <- rep(c(1), length(vec.x))
    mat.x <- cbind(ones, vec.x)
    if (grade > 1){
        for (i in 2:grade){
            mat.x <- cbind(mat.x, vec.x^i)
        }
    }
    x.T <- t(mat.x)
    xT.cov.x <- solve(x.T %*% solve(cov.y) %*% mat.x)
    xT.cov.y <- x.T %*% solve(cov.y) %*% mat.y$y
    my.params <- xT.cov.x %*% xT.cov.y
    return(my.params)
}

# Defino los parametros

a <- 1
b <- 2
c <- 0.01
m <- 0.1
n <- 0.04

# Genero los x aleatorios

N <- 100

my.x <- runif(N,0,10)

# Genero las 'y' siguiendo el modelo lineal

par.2 <- c(a,b)

my.pol.1 <- get.pol.n(my.x,par.2,m,n)
plot(my.x,my.pol.1$y)
arrows(my.x, my.pol.1$y - my.pol.1$sigma / 2, my.x, my.pol.1$y + my.pol.1$sigma / 2, length = 0.05, angle = 90, code = 3)

# ajusto al modelo lineal

theta <- my.ML(my.x, my.pol.1, 1)
theta

plot(my.x,my.pol.1$y)
arrows(my.x, my.pol.1$y - my.pol.1$sigma / 2, my.x, my.pol.1$y + my.pol.1$sigma / 2, length = 0.05, angle = 90, code = 3)
abline(theta)

# Defino una función que me calcule el Chi2

my.chi <- function(vec.x, mat.y, vec.parameters){
    cov.y <- diag(mat.y$sigma)
    ones <- rep(c(1), length(vec.x))
    mat.x <- cbind(ones, vec.x)
    x.T <- t(mat.x)
    chi <- ((mat.y$y - mat.x %*% vec.parameters) / mat.y$sigma)^2
    return(sum(chi))
}

# Ahora calculo el Chi2

chi.2.pol1 <- my.chi(my.x, my.pol.1, theta)
chi.2.pol1

my.prob.pol1 <- pchisq(my.chi(my.x, my.pol.1, theta), 98)
my.prob.pol1

print(paste("Obtengo un Chi2 de",chi.2.pol1,"con 98 grados de libertad."))
print(paste("Puedo rechazar este ajuste con una confianza del", my.prob.pol1*100,"%"))

# ajusto al modelo cuadratico

theta.2 <- my.ML(my.x, my.pol.1, 2)
theta.2

plot(my.x,my.pol.1$y)
arrows(my.x, my.pol.1$y - my.pol.1$sigma / 2, my.x, my.pol.1$y + my.pol.1$sigma / 2, length = 0.05, angle = 90, code = 3)
curve(theta.2[1] + theta.2[2]*x + theta.2[3]*x^2, add = T)

# Ahora calculo el Chi2

chi.2.pol2 <- my.chi(my.x, my.pol.1, theta)
chi.2.pol2

my.prob.pol2 <- pchisq(my.chi(my.x, my.pol.1, theta), 98)
my.prob.pol2

print(paste("Obtengo un Chi2 de",chi.2.pol2,"con 97 grados de libertad."))
print(paste("Puedo rechazar este ajuste con una confianza del", my.prob.pol2*100,"%"))

q <- -2 * (log(chi.2.pol1) - log(chi.2.pol2))
q

my.prob.H0 <- pchisq(q, 1)

print(paste("Obtengo un maximum likelihood ratio de", q,"con 1 grado de libertad"))
print(paste("Puedo aceptar la hipotesis 0 (el ajuste correcto es con 2 parametros) con una confianza del",(1 - my.prob.H0)*100,"%"))
