library(arulesViz)
library(arules)
#library(tidyverse)

data(Mushroom)
str(Mushroom)

head(Mushroom)
print("----------------------")

transactions <- as(Mushroom, "transactions")
transactions
print("----------------------")

rApriori <- apriori(transactions, parameter = list(support = 0.1, minlen = 2, maxlen = 20))
print("----------------------")

iEclat <- eclat(transactions, parameter = list(support = 0.1, minlen = 2, maxlen = 20))
rEclat <- ruleInduction(iEclat, transactions, confidence = 0)

summary(rApriori)
print("----------------------")

summary(rEclat)
print("----------------------")

# Algoritmo apriori
indRedundant.apriori <- which(is.redundant(rApriori))
length(indRedundant.apriori)
length(indRedundant.apriori) / length(rApriori) #2560630
length(rApriori) - length(indRedundant.apriori)

# Algoritmo eclat
indRedundant.eclat <- which(is.redundant(rEclat))
length(indRedundant.eclat)
length(indRedundant.eclat) / length(rEclat) #2995184
length(rEclat) - length(indRedundant.eclat)

rAprioriFiltered <- rApriori[!is.redundant(rApriori)]
rAprioriFiltered

rEclatFiltered <- rEclat[!is.redundant(rEclat)]
rEclatFiltered

length(subset(rAprioriFiltered, subset = rhs %in% c("Class=poisonous")))
inspect(subset(rAprioriFiltered, subset = rhs %in% c("Class=poisonous")))

length(subset(rAprioriFiltered, subset = lhs %in% c("Class=poisonous")))
inspect(subset(rAprioriFiltered, subset = lhs %in% c("Class=poisonous")))

length(subset(rEclatFiltered, subset = rhs %in% c("Class=poisonous")))
inspect(subset(rEclatFiltered, subset = rhs %in% c("Class=poisonous")))

length(subset(rEclatFiltered, subset = lhs %in% c("Class=poisonous")))
inspect(subset(rEclatFiltered, subset = lhs %in% c("Class=poisonous")))

length(subset(rAprioriFiltered, subset = rhs %in% c("Class=edible")))
inspect(subset(rAprioriFiltered, subset = rhs %in% c("Class=edible")))

length(subset(rAprioriFiltered, subset = lhs %in% c("Class=edible")))
inspect(subset(rAprioriFiltered, subset = lhs %in% c("Class=edible")))

length(subset(rEclatFiltered, subset = rhs %in% c("Class=edible")))
inspect(subset(rEclatFiltered, subset = rhs %in% c("Class=edible")))

length(subset(rEclatFiltered, subset = lhs %in% c("Class=edible")))
inspect(subset(rEclatFiltered, subset = lhs %in% c("Class=edible")))

inspect(rEclat)
