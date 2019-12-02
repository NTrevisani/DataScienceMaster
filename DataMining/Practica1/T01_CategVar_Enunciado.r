library(arulesViz)
library(arules)
#library(tidyverse)

data(Mushroom)
str(Mushroom)

head(Mushroom@itemInfo)

for (variable in levels(Mushroom@itemInfo$variables)){
    print(variable)
    for (level in levels(Mushroom@itemInfo$levels)){
        for (label in Mushroom@itemInfo$labels){
            if (grepl(variable, label) & grepl(level, label))
            print(paste("    ",level))
        }
    }
}

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

rhs.poisonous.apriori <- subset(rAprioriFiltered, subset = rhs %in% c("Class=poisonous"))
length(subset(rAprioriFiltered, subset = rhs %in% c("Class=poisonous")))

length(subset(rAprioriFiltered, subset = lhs %in% c("Class=poisonous")))

rhs.poisonous.eclat <- subset(rEclatFiltered, subset = rhs %in% c("Class=poisonous"))
length(subset(rEclatFiltered, subset = rhs %in% c("Class=poisonous")))

length(subset(rEclatFiltered, subset = lhs %in% c("Class=poisonous")))

rhs.edible.apriori <- subset(rAprioriFiltered, subset = rhs %in% c("Class=edible"))
length(subset(rAprioriFiltered, subset = rhs %in% c("Class=edible")))

length(subset(rAprioriFiltered, subset = lhs %in% c("Class=edible")))

rhs.edible.eclat <- subset(rEclatFiltered, subset = rhs %in% c("Class=edible"))
length(subset(rEclatFiltered, subset = rhs %in% c("Class=edible")))

length(subset(rEclatFiltered, subset = lhs %in% c("Class=edible")))

inspect(head(sort(rhs.edible.apriori, by ="lift"),10))

inspect(head(sort(rhs.poisonous.apriori, by ="lift"),10))

par(mfrow=c(1,2)) 

plot.1 <- plot(rhs.poisonous.apriori, jitter = 0)
plot.2 <- plot(rhs.edible.apriori, jitter = 0)

rAprioriClasses <- subset(rAprioriFiltered, subset = rhs %in% c("Class=edible") | rhs %in% c("Class=poisonous"))

rApriori.high.conf <- subset(rAprioriClasses, subset = confidence > 0.98 & support > 0.2)
plot(rApriori.high.conf, method="paracoord")
