# función que genera la distribución

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
            y <- c(y, rnorm(1, model, my.sigma))        
    }
    my.out.table <- cbind(y, sigma)
    return(as.data.frame(my.out.table))
}

my.x <- runif(40, -3, 3)

pars = c(-2, -1, 2, 1)
sigma = 4

my.pol.3 <- get.pol.n(my.x, pars, sigma, 0)

plot(my.x, my.pol.3$y)

# función que máximiza la likelihood

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

# función que saca los parametros del ajuste a un polinomio de grado 'grade'

get.aplha <- function(vec.x, vec.y, grade){
    ones <- rep(c(1), length(vec.x))
    mat.x <- cbind(ones,vec.x)
    if (grade > 1){
        for (i in 2:grade){
            mat.x <- cbind(mat.x, vec.x^i)
        }
    }
    x.T.x <- solve(t(mat.x) %*% mat.x)
    all.x <- x.T.x %*% t(mat.x)
    alpha <- all.x %*% vec.y
    return(alpha)
}

# función que mide la distancia entre los puntos y la curva que máximiza la likelihood

my.loss <- function(vec.x, mat.y, pars){
    ones <- rep(c(1), length(vec.x))    
    mat.x <- cbind(ones, vec.x)
    if (length(pars) > 2){
        for (i in 2:(length(pars)-1)){
            mat.x <- cbind(mat.x, vec.x^i)
        }
    }
    fit.value <- mat.x %*% pars
    dist <- mat.y - fit.value
    return(sum(dist**2))
}

my.plotter <- function(the.alpha){
    cols <- rainbow(10)
    pars <- c(0,0,0,0,0,0,0,0)
    for (i in 1:length(the.alpha)){
        pars[i] = the.alpha[i]
    }
    curve(pars[1]*x**0 
        + pars[2]*x**1
        + pars[3]*x**2
        + pars[4]*x**3
        + pars[5]*x**4
        + pars[6]*x**5
        + pars[7]*x**6
        + pars[8]*x**7,
          add = T,
          col = cols[i])
}

# Pinto mis datos
plot(my.x, my.pol.3$y)

# Ajusto los primeros eventos de mis datos a polinomios de grado 1 -> 7

my.fit <- c()
my.dist <- c()
cols <- rainbow(10)

for (i in 1:7){
    print(i)
    fit <- get.aplha(my.x[1:20], my.pol.3[1:20,1], i)
    my.fit <- c(my.fit, fit)
    my.plotter(fit)
    print(fit)
    dist <- my.loss(my.x[21:40], my.pol.3[21:40,1], fit)
    my.dist <- c(my.dist, dist)
}
