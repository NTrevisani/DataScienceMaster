# The problem can be represented by a binomial distribution
# with the following parameters

# Number of repetitions of the binary experiment
questions  <- 10

# Success probability
probability <- 0.2

# Let's calculate the expected value
# For a binomial distribution: 
# exp = n_repetitions * success_probability

expected <- questions * probability
print(paste("The expected value is:", expected))

# Now calculate the standard deviation
# For a binomial distribution: 
# std_dev = (n_repetitions * success_probability)(1 - success_probability) =
# = exp * (1 - success_probability)

std.dev <- sqrt(expected*(1 - probability))

print(paste("The standard deviation is:", format(round(sqrt(std.dev), 2), nsmall = 2)))

# Calculate the probability of guessing 0,1,2,..,10 questions

# dbinom is the R command we need
prob.vec <- dbinom(0:10,questions,probability)

print("The probability to guess:")
for (i in 0:10){
    if (i == 1)
        print(paste(i,"question:",format(round(prob.vec[i+1], 8), nsmall = 8)))
    else
        print(paste(i,"questions:",format(round(prob.vec[i+1], 8), nsmall = 8)))
}

print(paste("Luckily, the sum of all the probabilities is:", sum(prob.vec)))

# Calculate the probability of guessing at least i questions

# pbinom is the R command we need
prob.cumulative <- pbinom(0:10, questions, probability)

print("The probability to guess at least:")
for (i in 0:10){
    if (i == 1)
        print(paste(i,"question:",format(round(prob.cumulative[i+1], 8), nsmall = 8)))
    else
        print(paste(i,"questions:",format(round(prob.cumulative[i+1], 8), nsmall = 8)))
}

# Now, let's plot the probabilities...

barplot(prob.vec, names.arg = c(0:10), xlab = "Correct answers", ylab = "Probability",
       main = "Probability to guess n correct answers")

# ... and the cumulative probabilities
# (probability to guess at least n answers)

barplot(prob.cumulative, names.arg = c(0:10), xlab = "Minimum number of correct answers", ylab = "Probability",
       main = "Probability to guess at least n correct answers")

# Load the necessary library and the file

# Useful to manage and plot data.frames
library("tidyverse")

# Load the file
got <- read_csv("GOT.csv")
str(got)

# Let's see how the number of deaths per episode is distributed
death.table <- table(got$NumDeaths)

barplot(death.table, xlab="Number of deaths", ylab="Number of episodes",
       main = "Number of deaths per episode")

# The distribution, as we guessed, is very similar to a Poisson
# Let's extract the key value of the distribution

# lambda = mean value of the distribution
# sqrt(lambda) = standard deviation of the distribution
lambda <- mean(got$NumDeaths)
print(paste("The expected value of deaths in an episode is", format(round(lambda, 2), nsmall = 2)))
print(paste("The standard deviation is", format(round(sqrt(lambda), 2), nsmall = 2)))

# The probability to have more than 4 deaths in an episode can be
# calculated using the 'ppois' function.
# Since 'ppois' returns the probability to have 4 or less deaths,
# we have to consider (1 - ppois(4, lambda))

p.4 <- (1 - ppois(4, lambda))
print(paste("The probability to have more than 4 deaths in an episode is", 
            format(round(p.4*100, 2), nsmall = 2),"%"))

# Let's plot the distribution of the mean number of deaths per episode
# versus the number of episode in the season
death.episode.mean    <- c(tapply(X = got$NumDeaths, INDEX = got$Episode, mean))
death.episode.std.dev <- c(tapply(X = got$NumDeaths, INDEX = got$Episode, sd))

death.episode.std.dev.up   <- death.episode.mean + death.episode.std.dev
death.episode.std.dev.down <- death.episode.mean - death.episode.std.dev

plot(c(1:10), death.episode.mean, ylim = c(0,9), type = "l",
    xlab = "Episode", ylab = "Mean number of deaths",
    main = "Mean number of deaths per episode across the different seasons")

polygon(c(c(1:10), c(10:1)), c(death.episode.std.dev.up, rev(death.episode.std.dev.down)), col = "grey80", border = NA)
lines(c(1:10), death.episode.mean, ylim = c(0,9))

legend("topleft",lty=1, "Deaths per episode +- std. dev.", 
       col = "black",
      fill = "grey80")

death.prob <- dpois(0:10, lambda)

print("The probability to have:")
for (i in 0:10){
    if (i == 1)
        print(paste(i,"death:",format(round(death.prob[i+1], 8), nsmall = 8)))
    else
    print(paste(i,"deaths:",format(round(death.prob[i+1], 8), nsmall = 8)))
}

print(paste("In this, the sum of these probabilities is:",format(round(sum(death.prob), 8), nsmall = 8)))
print(paste("This means that the probability to have more than 10 deaths in an episode is", 
            format(round(1 - sum(death.prob), 8), nsmall = 8)))

# The distribution describing this measurement is a gaussian (normal)
# with the following parameters:

# Mean of the distribution and expected value
mean <- 180

# Standard deviation
std.dev <- 25

# To get the probability of a person to have more than 225 mg/dL
# we have to calculate the cumulative until 225 mg/dL and 
# take (1 - cumulative(225 mg/dL))

prob.more.225 <- 1 - pnorm(225,180,25)
print(paste("The probability for a person to have more than 225 mg/dL of cholesterol is:",
            format(round(prob.more.225, 4), nsmall = 4)))

# To get the value of cholesterol that encloses the 95%
# of the population, we have to use the 'qnorm' function

p <- 0.95

perc.95 <- qnorm(p,mean,std.dev)
print(paste("95% of the population has a value of cholesterol of:",
            format(round(perc.95, 0), nsmall = 0),"or less"))

# Considering that the mean value of cholesterol is 180 mg/dL
# and that it cannot assume negative values, it makes sense to 
# plot the probability density function (p.d.f.) and the 
# distribution function between 0 and 360.

# Define x coordinate
x <- seq(0, 360, length=3600)

# Produce a vector with the p.d.f. evaluated
# in each point of x
pdf <- dnorm(x,mean,std.dev)

# Produce a vector with the distribution function evaluated
# in each point of x
dist.func <- pnorm(x,mean,std.dev)

# Now plot the distributions and save them into a pdf file

# Save everything that follows in
# "Gaussian_distribution.pdf"
pdf("Gaussian_distribution.pdf")

par(mfrow=c(2,1)) 

# p.d.f. plot
plot(x, pdf, type="l", lty=1, 
     xlab="Cholesterol level [mg/dL]", ylab="Probability density", 
     main="Probability density function of cholesterol level")

# Distribution function plot
plot(x, dist.func, type="l", lty=1, 
     xlab="Cholesterol level [mg/dL]", ylab="Distribution function", 
     main="Distribution function of cholesterol level")

# Stop saving things in "Gaussian_distribution.pdf"
dev.off()
