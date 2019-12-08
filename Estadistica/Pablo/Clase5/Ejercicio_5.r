library(MASS)

my.gauss.2D <- function(mean.x, mean.y, var.x, var.y, cov.xy, N){
    my.cov = matrix(nrow = 2, ncol = 2)
    my.cov[1,1] <- var.x
    my.cov[2,2] <- var.y
    my.cov[1,2] <- cov.xy
    my.cov[2,1] <- cov.xy
    my.output <- as.data.frame(mvrnorm(n = N, mu = c(mean.x, mean.y), Sigma = my.cov))
    names(my.output)[1] <- "x1"
    names(my.output)[2] <- "x2"
    return(my.output)
}

#my.gauss.2D(2,4,1,1,0.3,10)

# Defino los parametros
N <- 1000
mu.x <- 2
mu.y <- 4
sigma.x <- 1
sigma.y <- 1
covariance <- 0.3

x1 <- my.gauss.2D(mu.x,mu.y,sigma.x,sigma.y,covariance,N)
y1 <- matrix(rep(0,length(x1$x1)), ncol = 1)

# Defino los parametros
N <- 1000
mu.x <- 6
mu.y <- 3
sigma.x <- 1
sigma.y <- 1
covariance <- 0.3

x2 <- my.gauss.2D(mu.x,mu.y,sigma.x,sigma.y,covariance,N)
y2 <- matrix(rep(1,length(x1$x1)), ncol = 1)

my.mat.x <- rbind(x1,x2)

my.mat.y <- rbind(y1,y2)

# Sigmoid function

my.sigmoid <- function(z){
    sigm <- 1. / (1 + exp(-z))   
    return(sigm)
}

# Loss function

my.loss <- function(alpha, mat.x, mat.y){
    ones <- matrix(rep(1,nrow(mat.x)), ncol = 1)
    mat.features <- cbind(ones, mat.x)
    # only the y
    sigm <- as.vector(my.sigmoid(alpha %*% t(mat.features)))
    mat.y <- as.vector(mat.y)
    loss <- mat.y * log(sigm) + (1 - mat.y) * log(1 - sigm)
    return(- sum(loss) / nrow(mat.x))
}
my.loss(c(0,1,0),my.mat.x, my.mat.y)

# Gradient

my.grad <- function(alpha, mat.x, mat.y){
    ones <- matrix(rep(1,nrow(mat.x)), ncol = 1)
    # do not consider the y
    # mat.x.only <- mat.x[,-ncol(mat.x)]
    mat.features <- cbind(ones, mat.x)
    # only the y
    sigm <- as.vector(my.sigmoid(alpha %*% t(mat.features)))
    grad <- (sigm - mat.y) * mat.features
    print(colSums(grad))
    return(colSums(grad) / nrow(mat.x))
}
#my.grad(c(0,0,0), my.mat.x, my.mat.y)


# Actual minimization

initial_alpha <- c(0,0,0)
qq <- optim(par = initial_alpha, fn = my.loss, gr = my.grad, mat.x = my.mat.x, mat.y = my.mat.y, method = "BFGS")
qq

qq$par

# z = qq$par[1] + (x1 * qq$par[2]) + (x2 * qq$par[3])

# si no quiero introducir bias, z = 0:
a <- qq$par[1] / qq$par[3]
b <- qq$par[2] / qq$par[3]

#plot(my.mat.x, my.mat.y)

plot(my.mat.x[1:1000,], col = "red", xlim = c(-2,10), ylim = c(0,8))
points(my.mat.x[1001:2000,], col = "blue")
abline(-a,-b)

# Defino los parametros
N <- 1000
mu.x <- 2
mu.y <- 4
sigma.x <- 1
sigma.y <- 1
covariance <- 0.3

new.x1 <- my.gauss.2D(mu.x,mu.y,sigma.x,sigma.y,covariance,N)
new.y1 <- matrix(rep(0,length(x1$x1)), ncol = 1)

# Defino los parametros
N <- 1000
mu.x <- 6
mu.y <- 3
sigma.x <- 1
sigma.y <- 1
covariance <- 0.3

new.x2 <- my.gauss.2D(mu.x,mu.y,sigma.x,sigma.y,covariance,N)
new.y2 <- matrix(rep(1,length(x1$x1)), ncol = 1)

new.mat.x <- rbind(new.x1,new.x2)
new.mat.y <- rbind(new.y1,new.y2)

# recordamos:
# z = qq$par[1] + (x1 * qq$par[2]) + (x2 * qq$par[3])

get.ab.line <- function(parameters, threshold){
    my.a <- (parameters$par[1] - threshold) / parameters$par[3]
    my.b <- (parameters$par[2] - threshold) / parameters$par[3]    
    return(c(my.a,my.b))
}

line.00 <- get.ab.line(qq, 0.0)
line.03 <- get.ab.line(qq, 0.3)
line.05 <- get.ab.line(qq, 0.5)
line.07 <- get.ab.line(qq, 0.7)

# Red --> y = 0
plot(new.mat.x[1:1000,], col = "red", xlim = c(-2,10), ylim = c(0,8))

# Blue --> y = 1
points(new.mat.x[1001:2000,], col = "blue")

abline(-line.00, lwd = 2)
abline(-line.03, col = "green", lwd = 2)
abline(-line.05, col = "yellow", lwd = 2)
abline(-line.07, col = "orange", lwd = 2)

legend("topleft", legend=c("Threshold = 0", "Threshold = 0.3", "Threshold = 0.5", "Threshold = 0.7"),
       col=c("black", "green", "yellow", "orange"), lwd = c(2,2,2,2), lty=c(1,1,1,1), cex=1)

my.confusion.matrix <- function(line.parameters, mat.x, vec.y){
    confusion.matrix = matrix(c(0,0,0,0), ncol = 2, nrow = 2)
    
    # Initialize the 4 entries of the matrix
    
    # True positive (1,1)
    TP = 0
    # True negative (0,0)
    TN = 0
    # False positive (1,0)
    FP = 0
    # False negative (0,1)
    FN = 0
    
    # for each point, if it is below the line assign exp.y = 1, otherwise exp.y = 0
    for (i in 1:nrow(mat.x)){
        if (mat.x[i,2] < -line.parameters[1] - mat.x[i,1] * line.parameters[2])
            exp.y <- 1
        else exp.y <- 0
        # compare exp.y with vec.y and assign to the correct category
        if (exp.y == 1 & vec.y[i] == 1) TP = TP + 1
        else if (exp.y == 0 & vec.y[i] == 0) TN = TN + 1
        else if (exp.y == 1 & vec.y[i] == 0) FP = FP + 1
        else if (exp.y == 0 & vec.y[i] == 1) FN = FN + 1
    }
    confusion.matrix[1,1] = TP
    confusion.matrix[2,2] = TN
    confusion.matrix[1,2] = FP
    confusion.matrix[2,1] = FN    

    # Put labels on the matrix
    rownames(confusion.matrix) <- c("Classified as positive", "Classified as negative")
    colnames(confusion.matrix) <- c("Actually positive", "Actually negative")
    return(confusion.matrix)
}

print("Confusion matrix setting threshold at 0")
my.confusion.matrix(line.00, new.mat.x, new.mat.y)

print("Confusion matrix setting threshold at 0.3")
my.confusion.matrix(line.03, new.mat.x, new.mat.y)

print("Confusion matrix setting threshold at 0.5")
my.confusion.matrix(line.05, new.mat.x, new.mat.y)

print("Confusion matrix setting threshold at 0.7")
my.confusion.matrix(line.07, new.mat.x, new.mat.y)
