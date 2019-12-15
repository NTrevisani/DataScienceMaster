library(dplyr)

# Load the players statistics
my.player.file <- read.csv("players_stats.csv")

# Extract the mean value and the standard deviation of the height
mean.height <- mean(my.player.file$Height, na.rm = TRUE)
print(paste("Mean height = ", format(round(mean.height, 0), nsmall = 0),"cm"))

std.dev <- sd(my.player.file$Height, na.rm = TRUE)
print(paste("Standard deviation = ",format(round(std.dev, 0), nsmall = 0),"cm"))

# Plot a histogram representing the players height distribution
hist(my.player.file$Height,
     xlab = "Player height [cm]", ylab = "Absolute frequency",
     main = "NBA players height distribution")

# Adding a green vertical line corresponding to the mean height
abline(v = mean.height, lw = 5, col = "green")

# Adding two red vertical lines corresponding to the mean height +- standard deviation
abline(v = mean.height + std.dev, lw = 2, col = "red")
abline(v = mean.height - std.dev, lw = 2, col = "red")

# Just for curiosity: 

# Total number of players
total.number.players <- nrow(my.player.file)
print(paste("Total number of players:",total.number.players))

# Number of 'short' players
less.180 <- nrow(filter(my.player.file, Height < 180))
print(paste("Number of players shorter than 180 cm:", less.180,"(",
            format(round(100*less.180/total.number.players, 2), nsmall = 2),"%)"))

less.175 <- nrow(filter(my.player.file, Height < 175))
print(paste("Number of players shorter than 175 cm:", less.175,"(",
            format(round(100*less.175/total.number.players, 2), nsmall = 2),"%)"))

# Number of 'tall' players
more.210 <- nrow(filter(my.player.file, Height > 210))
print(paste("Number of players taller than 210 cm:", more.210,"(",
            format(round(100*more.210/total.number.players, 2), nsmall = 2),"%)"))

more.220 <- nrow(filter(my.player.file, Height > 220))
print(paste("Number of players taller than 220 cm:", more.220,"(",
            format(round(100*more.220/total.number.players, 2), nsmall = 2),"%)"))

#Load the dataset

ice.daily <- read.csv("N_seaice_extent_daily_v3.0.csv")

# Check in which month it is more frequent to have the minimum and maximum extent

# A vector of 'labels' for the months
month.vec  <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

# Extract the vector with the month with the minimum extent each year
minimum.months <- unlist(lapply(split(ice.daily, ice.daily$Year), function(x){
    return(x$Month[x$Extent == min(x$Extent)])
}), use.names = FALSE)

# Extract the vector with the month with the maximum extent each year
maximum.months <- unlist(lapply(split(ice.daily, ice.daily$Year), function(x){
    return(x$Month[x$Extent == max(x$Extent)])
}), use.names = FALSE)

# Initializing the vector of frequency for each month
min.month.freq <- numeric(length = 12)
max.month.freq <- numeric(length = 12)

# Transform the vector with the months of minimum extent into a factor
min.month.factor <- (factor(minimum.months))
max.month.factor <- (factor(maximum.months))

# Extract the levels as numbers (by default they come as characters)
min.month.levels <- as.numeric(levels(min.month.factor))
max.month.levels <- as.numeric(levels(max.month.factor))

# Extract the frequencies of the factors
min.month.table <- table(min.month.factor)
max.month.table <- table(max.month.factor)

# Put the correct frequency in the month.freq vector: 
# I read the month.levels vector = c(10,9) and I put the corresponding frequency in month.table in
# the correct entry of month.freq
for (x in min.month.levels){
    ind <- which(min.month.levels == x)
    min.month.freq[x] <- min.month.table[[ind]]
}

for (x in max.month.levels){
    ind <- which(max.month.levels == x)
    max.month.freq[x] <- max.month.table[[ind]]
}

# Barplot for the minimum extent months frequency
barplot(min.month.freq, names.arg = month.vec, xlab = "Month", ylab = "Frequency",
       main = "Month of minimum sea ice extent in the Arctic from 1978 to 2019")

# Barplot for the maximum extent months frequency
barplot(max.month.freq, names.arg=month.vec, xlab = "Month", ylab = "Frequency",
       main = "Month of maximum sea ice extent in the Arctic from 1978 to 2019")

# Plot, month by month, the median value of the extent

# Library to easily manage data.frames
library(tidyverse)

# Defining function to extract an arbitrary quantile of the variable Extent
# from a data frame structured as 'ice.daily'
sea.ice.quantile <- function(data, quant){
    return(quantile(data$Extent, quant))
}

# Supporting vectors for paintings
month     <- 1:12
month.vec <- c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")

# Median, 95% quantile, and 5% quantile for sea-ice extent
medians      <- unlist(lapply(split(ice.daily, ice.daily$Month), sea.ice.quantile, quant = 0.50), 
                     use.names = FALSE)
medians.up   <- unlist(lapply(split(ice.daily, ice.daily$Month), sea.ice.quantile, quant = 0.95), 
                     use.names = FALSE)
medians.down <- unlist(lapply(split(ice.daily, ice.daily$Month), sea.ice.quantile, quant = 0.05), 
                     use.names = FALSE)

# Create a table with (median, month) to ease plotting
my.table <- as.data.frame(cbind(month,medians))

# Median monthly sea-ice extent in 2012 and 2018
year.2012 <- filter(ice.daily, Year == 2012)
medians.2012 <- unlist(lapply(split(year.2012, year.2012$Month), sea.ice.quantile, quant = 0.50), 
                     use.names = FALSE)

year.2018 <- filter(ice.daily, Year == 2018)
medians.2018 <- unlist(lapply(split(year.2018, year.2018$Month), sea.ice.quantile, quant = 0.50), 
                     use.names = FALSE)

# ... and 1980?
year.1980 <- filter(ice.daily, Year == 1980)
medians.1980 <- unlist(lapply(split(year.1980, year.1980$Month), sea.ice.quantile, quant = 0.50), 
                     use.names = FALSE)


# Finally, the plot
plot(month, medians, xaxt = "n", ylim = c(0,20), type = "l",
    xlab = "Month", ylab = expression(paste("Median sea-ice extent [",10^6,"k",m^2,"]")),
    main = "Median monthly sea-ice extent ")
axis(side = 1, at = month, labels = month.vec)

polygon(c(month, rev(month)), c(medians.up, rev(medians.down)), col = "grey80", border = NA)

lines(month, medians, xaxt = "n", ylim=c(0,20))
lines(month, medians.1980, xaxt = "n", col="green")
lines(month, medians.2012, xaxt = "n", col="blue")
lines(month, medians.2018, xaxt = "n", col="red")

legend("topright",lty=1,c("All years (5% - 95% quantile)", "1980", "2012", "2018"), 
       col = c("black", "green", "blue", "red"),
      fill = c("grey80", NA, NA, NA))

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
# var = (n_repetitions * success_probability)(1 - success_probability) =
# = exp * (1 - success_probability)
# std.dev = sqrt(var)

std.dev <- sqrt(expected*(1 - probability))

print(paste("The standard deviation is:", format(round(sqrt(std.dev), 2), nsmall = 2)))

# Calculate the probability of guessing 0,1,2,..,10 questions

# To do it, we need to evaluate the probability density function (p.d.f.)
# so dbinom ('d' as density) is the R command we need
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

# In this case, we have to evaluate the cumulative probability function, and 
# pbinom is the R command we need
prob.cumulative <- pbinom(0:10, questions, probability)

print("The probability to guess at least:")
for (i in 0:10){
    if (i == 1)
        print(paste(i,"question:",format(round(prob.cumulative[i+1], 8), nsmall = 8)))
    else
        print(paste(i,"questions:",format(round(prob.cumulative[i+1], 8), nsmall = 8)))
}

# Create a 2-panel graphics
par(mfrow=c(2,1)) 

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

legend("topleft",lty=1, 
       "Deaths per episode +- std. dev.", 
       col = "black",
       fill = "grey80")

# To estimate the probability to have exactly n deaths
# in an espisode, we have to evaluate the probability density function,
# by using 'dpois'
death.prob <- dpois(0:10, lambda)

print("The probability to have:")
for (i in 0:10){
    if (i == 1)
        print(paste(i,"death:",format(round(death.prob[i+1], 8), nsmall = 8)))
    else
    print(paste(i,"deaths:",format(round(death.prob[i+1], 8), nsmall = 8)))
}

print(paste("In this case, the sum of these probabilities is:",format(round(sum(death.prob), 8), nsmall = 8)))
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
# of the population, we have to use the 'qnorm' ('q' as quantile) 
# function

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

# Now plot the distributions 
par(mfrow=c(2,1)) 

# p.d.f. plot
plot(x, pdf, type="l", lty=1, 
     xlab="Cholesterol level [mg/dL]", ylab="Probability density", 
     main="Probability density function of cholesterol level")

# Distribution function plot
plot(x, dist.func, type="l", lty=1, 
     xlab="Cholesterol level [mg/dL]", ylab="Distribution function", 
     main="Distribution function of cholesterol level")

# Load the necessary library and the file

# Useful to manage and plot data.frames
library("tidyverse")

# Load the file
results <- read_csv("results.csv")
str(results)

# Select only the matches in which Spain plays at home
spain.local.goals <- filter(results, home_team == "Spain")
str(spain.local.goals)

# Create a table of frequencies for the goals scored
goal.table <- table(spain.local.goals$home_score)

# Represent the distribution
barplot(goal.table, xlab = "Number of goals", ylab = "Number of matches",
       main = "Number of goals scored by Spanish selection per home match")

# Let's extract the key value 'lambda' of the distribution (its mean)

lambda <- mean(spain.local.goals$home_score)

# To estimate the probability to score more than 3 goals
# in the next match, we can calculate the probability
# of scoring 3 or less goals and take the complementary

prob.more.3 <- (1 - ppois(3,lambda))

print(paste("The probability to score more than 3 goals in the next match is", format(round(prob.more.3, 2), nsmall = 2)))

prob.goal <- dpois(0:10, lambda)

print("The probability to score:")
for (i in 0:10){
    if (i == 1)
        print(paste(i,"goal:",format(round(prob.goal[i+1], 8), nsmall = 8)))
    else
    print(paste(i,"goals:",format(round(prob.goal[i+1], 8), nsmall = 8)))
}

print(paste("In this case, the sum of these probabilities is:",format(round(sum(prob.goal), 8), nsmall = 8)))
print(paste("This means that the probability to score more than 10 goals in a match is", 
            format(round(1 - sum(prob.goal), 8), nsmall = 8)))
print(paste("The most probable number of goals scored is 2"))

# Probability to win
p.win <- prob.more.3

# What we win
money.win <- 3


# Probability to lose
p.lose <- 1 - p.win

# What we loose
money.lose <- 1


# Expected amount of money gained
money <- (p.win * money.win) - (p.lose * money.lose)

# Result:

word <- 0
phrase <-0

if(money > 0){
    word <- "win"
    phrase <- "Let's bet!"    
} else{
    word <- "lose"
    phrase <- "I would not bet."
}
    
print(paste("The expectation is that for every euro we play, we",word,format(round(abs(money), 2), nsmall = 2),"euros"))
print(phrase)

# The mean waiting time is (a + b)/2, where:

# The train arrives now (no wait)
a <- 0

# Maximum expected waiting time
b <- 100

mean.time <- (a + b)/2

# The standard deviation, on the other hand, 
# is given by: (b - a)/sqrt(12)

var.time <- (b - a)*(b - a)/12

print(paste("The mean waiting time is:", format(round(mean.time, 2), nsmall = 2),"minutes"))
print(paste("The variance is:", format(round(var.time, 2), nsmall = 2),"minutes^2"))
print(paste("The standard deviation is:", format(round(sqrt(var.time), 2), nsmall = 2),"minutes"))

# Simulate the waiting time of 30 people

# Fi the seed just to have every time the same result
set.seed(1)

# Simulate the 30 waiting times, using a uniform distribution
wait.time <- runif(30,0,100)

sample.mean.time = mean(wait.time)
print(paste("The mean waiting time for this sample is:", format(round(sample.mean.time, 2), nsmall = 2)))

sample.var.time <- var(wait.time)
print(paste("The variance for this sample is:", format(round(sample.var.time, 2), nsmall = 2)))

print(paste("The standard deviation for this sample is:", format(round(sqrt(sample.var.time), 2), nsmall = 2)))

# Case n = 30
n <- 30
var.sample.30 <- var.time / n
print(paste("The variance for a sample of",n,"people is:", format(round(var.sample.30, 2), nsmall = 2)))

# Case n = 100
n <- 100
var.sample.100 <- var.time / n
print(paste("The variance for a sample of",n,"people is:", format(round(var.sample.100, 2), nsmall = 2)))

# Simulate 500 random samples of 30 people.

# A huge (30 x 500) matrix
mat.30 <- matrix(runif(30*500,0,100), ncol = 500)

# A vector storing the means of the 500 random samples
mean.vec.30 <- colMeans(mat.30)

# The mean of the 500 mean values
my.mean.30 <- mean(mean.vec.30)

# The variance of the 500 mean values
my.var.30 <- var(mean.vec.30)

print(paste("The mean extracted from 500 samples of 30 people is:", format(round(my.mean.30, 2), nsmall = 2)))
print(paste("The variance extracted from 500 samples of 30 people is:", format(round(my.var.30, 2), nsmall = 2)))

# Now do the same, but for samples of 100 people.

# Simulate 500 random samples of 100 people.

# A huge (100 x 500) matrix
mat.100 <- matrix(runif(100*500,0,100), ncol = 500)

# A vector storing the means of the 500 random samples
mean.vec.100 <- colMeans(mat.100)

# The mean of the 500 mean values
my.mean.100 <- mean(mean.vec.100)

# The variance of the 500 mean values
my.var.100 <- var(mean.vec.100)

print(paste("The mean extracted from 500 samples of 30 people is:", format(round(my.mean.100, 2), nsmall = 2)))
print(paste("The variance extracted from 500 samples of 30 people is:", format(round(my.var.100, 2), nsmall = 2)))

# Plot the 2 previous mean distributions in a 2-panel figure
# and superimpose the corresponding expected normal distribution.

# Prepare the 2-panel figure
par(mfrow=c(2,1)) 

# 30-people sample
hist(mean.vec.30, xlim = c(0,100), ylim = c(0,0.08),
     xlab="Mean waiting time [min]", ylab="Normalised frequency", 
     main="Waiting time distribution of 500 samples of 30 people",
     freq = F)
curve(dnorm(x,50,sqrt(var.sample.30)), from = 0, to = 100, add = TRUE)

# 100-people sample
hist(mean.vec.100, xlim = c(0,100),
     xlab="Mean waiting time [min]", ylab="Normalised frequency", 
     main="Waiting time distribution of 500 samples of 100 people",
     freq = F)

curve(dnorm(x,50,sqrt(var.sample.100)), from = 0, to = 100, add = TRUE)

# Number of repetitions
rep <- 100

# We have 40 cards in the deck
deck <- 40

#  1 - 10 --> bastos
# 11 - 20 --> copas
# 21 - 30 --> espadas
# 31 - 40 --> oros

my.cards <- sample(deck, rep, replace = T)

n.bastos <- 0
for(i in sample(deck, rep, replace = T)){
    if (i < 11)
        n.bastos <- n.bastos + 1
}

print(paste("Out of",rep,"cards extracted,",n.bastos,"are bastos"))

lambda <- 0.01

# Let's try to plot the three functions
par(mfrow=c(3,1)) 

# p.d.f
curve(lambda*exp(-lambda*x),0, 1000,
     xlab = "Kilometers since start of the race [km]",
     ylab = "p.d.f.",
     main = "Probability to fall at a given km of the race")
        

# F(x)
curve(1-exp(-lambda*x),0, 1000,
     xlab = "Kilometers since start of the race [km]",
     ylab = "Cumulative distribution",
     main = "Probability to have fallen after a given amount of km of the race")

# F'(x)
curve(-log(1-x)/lambda,0, 1,
     xlab = "Probability to have fallen",
     ylab = "km travelled",
     main = "Inverse of the cumulative distribution")

# Define a function in R to make things easier
inverse <- function(x, par){return(-log(1-x)/par)}

# Number of races to simulate
n.races <- 1000

# Actual simulation
distance.vector <- inverse(runif(n.races,0,1),lambda)

# Plot the distribution
hist(distance.vector, freq = F,
    xlab = "Distance travelled until the first fall [km]",
    ylab = "Relative frequency",
    main = "Distance travelled until the first fall in 1000 simulated races")
curve(lambda*exp(-lambda*x), add = T)

# Let's try to plot the three functions
par(mfrow=c(3,1)) 

# p.d.f
curve(2/(x**3),1, 10,
     xlab = "Angular size [grades]",
     ylab = "p.d.f.",
     main = "Probability to find an astronomical object of a particular size")
        

# F(x)
curve(1 - 1/(x**2),1, 10,
     xlab = "Angular size [grades]",
     ylab = "Cumulative distribution",
     main = "Probability to find an astronomical object of a particular size or smaller")

# F'(x)
curve(1 / sqrt(1 - x),0, 1,
     xlab = "Probability to find an object smaller than a given angular size",
     ylab = "Angular size [grades]",
     main = "Inverse of the cumulative distribution")

# Define a function in R to make things easier
inverse.two <- function(x){return(1 / sqrt(1 - x))}

# Number of astronomical objects to simulate
n.objects <- 1000

# Actual simulation
objects.vector <- inverse.two(runif(n.objects,0,1))

# Plot the distribution
hist(objects.vector, freq = F, breaks=20, xlim = c(1,21),
    xlab = "Angular size [grades]",
    ylab = "Relative frequency",
    main = "Angular size distribution of 1000 simulated astronomical objects")
curve(2/(x**3), add = T)

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

n.people <- 50
mean.height <- 176
std.dev.height <- 11

height.vector <- rnorm(n.people, mean.height, std.dev.height)
height.vector

sample.mean.height <- mean(height.vector)
sample.var.height  <- var(height.vector)

print(paste("The mean value of the sample generated is", sample.mean.height))
print(paste("Its variance is", format(round(sample.var.height, 2), nsmall = 2)))

n.matches <- 10
mean.goals <- 2.8

goals.vector <- rpois(n.matches, mean.goals)
goals.vector

lambda.measured <- mean(goals.vector)

print(paste("The mean value of goals scored is", lambda.measured))


table <- 1:64
chips <- 32

put.chips <- sample(table, chips, replace = F)
put.chips

my.chessboard <- c(rep(0,64))
my.chessboard[put.chips] <- 1
my.chessboard <- matrix(my.chessboard,nrow = 8,ncol = 8)
my.chessboard

# By default, r prints a matrix transpose and upside down
# This appears to fix it:
image(t(my.chessboard)[,nrow(my.chessboard):1])

# Time (in days) to heal a cold when using the homeopatic medicine:

days <- read.csv("days.txt", header=F)[,]
days

hist(days, freq = F)

t.test(days, mu=6.7, alternative="less")

no.smoking <- read.table("sin_cannabis.txt", header = T)
smoking <- read.table("con_cannabis.txt", header = T)

hist(no.smoking$izq, col=rgb(0,0,1,1/4), xlim = c(2000,4000), breaks = 10, freq = F, ylim = c(0,0.002),
    xlab = "Left hippocampus volume [mm^3]",
    main = "Left hippocampus volume in cannabis smokers and non-smokers")
hist(smoking$izq,    col=rgb(1,0,0,1/4), xlim = c(2000,4000), add = T, freq = F)

legend("topright", legend=c("non-smokers", "smokers"),
       col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), fill = c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), cex=1.0)

hist(no.smoking$der, col=rgb(0,0,1,1/4), xlim = c(2000,5000), breaks = 10, freq = F,
    xlab = "Right hippocampus volume [mm^3]",
    main = "Right hippocampus volume in smokers and non-smokers")

hist(smoking$der,    col=rgb(1,0,0,1/4), xlim = c(2000,5000), freq = F, add = T)

legend("topright", legend=c("non-smokers", "smokers"),
       col=c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), fill = c(rgb(0,0,1,1/4), rgb(1,0,0,1/4)), cex=1.0)

t.test(no.smoking$izq, smoking$izq, alternative="two.sided")

t.test(no.smoking$der, smoking$der, alternative="two.sided")
