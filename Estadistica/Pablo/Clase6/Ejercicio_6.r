get.y <- function(x, intercept, angular.coeff, std.dev.a, std.dev.b){
    my.output <- c()
    my.sigma.vec <- c()
    for (value in x){
        my.sigma  <- std.dev.a + std.dev.b * value^2
        my.sigma.vec <- c(my.sigma.vec, my.sigma) 
        my.output <- c(my.output, rnorm(1, (angular.coeff*value + intercept), my.sigma))
    }
    my.out.table <- cbind(my.output, my.sigma.vec)
    return(as.data.frame(my.out.table))
}

my.x <- runif(10)
my.x

my.y <- get.y(my.x, 0, 2, 0.1, 0)
my.y

my.ML <- function(vec.x, mat.y){
    cov.y <- diag(mat.y$my.sigma.vec)
    ones <- rep(c(1), length(vec.x))
    mat.x <- cbind(ones, vec.x)
    x.T <- t(mat.x)
    xT.cov.x <- solve(x.T %*% solve(cov.y) %*% mat.x)
    xT.cov.y <- x.T %*% solve(cov.y) %*% mat.y$my.output
    my.params <- xT.cov.x %*% xT.cov.y
    return(my.params)
}
theta <- my.ML(my.x, my.y)

theta

plot(my.x, my.y$my.output)
abline(theta)








