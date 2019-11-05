dice <- 1:6
times <- 50

roll.dice <- sample(dice, times, replace = T)

sample.mean <- mean(roll.dice)
sample.var  <- var(roll.dice)

print(paste("The mean value of the sample generated is", sample.mean))
print(paste("Its variance is", format(round(sample.var, 2), nsmall = 2)))

dice <- 1:6
times <- 50

roll.dice1 <- sample(dice, times, replace = T)
roll.dice2 <- sample(dice, times, replace = T)

sum.dice <- roll.dice1 + roll.dice2

sample.mean.2 <- mean(sum.dice)
sample.var.2  <- var(sum.dice)

print(paste("The mean value of the sample generated is", sample.mean.2))
print(paste("Its variance is", format(round(sample.var.2, 2), nsmall = 2)))
