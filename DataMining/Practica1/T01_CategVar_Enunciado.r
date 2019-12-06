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

library(caret)

mushrooms <- read.csv("mushrooms.csv")

# Elimino la columna 17 (veil.type)
mushrooms <- mushrooms[,-17]
str(mushrooms)

nrow(mushrooms)

n = nrow(mushrooms)
n

indtrain = sample(1:n, 0.75*n)

mushrooms.train = mushrooms[indtrain, ]
mushrooms.test = mushrooms[-indtrain, ]

nrow(mushrooms.train)
nrow(mushrooms.test)

trainCV <- trainControl(method = "repeatedcv",
                        ## 3-fold CV
                        number = 3,
                        ## repeated 50 times
                        repeats = 50)

my.train <- train(class ~ ., data = mushrooms.train, 
                 method = "rpart2", 
                 trControl = trainCV,
                 # test tree depth in 1:15
                 tuneLength = 15)


plot(my.train)

pred.train = predict(my.train, newdata = mushrooms.train)
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

pred = predict(my.train, newdata = mushrooms.test)
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred, mushrooms.test$class))) / dim(mushrooms.test)[1]

library(ISLR)
library(rpart)
library(rpart.plot)

t.rpart = rpart(formula = class ~ ., data = mushrooms.train, maxdepth = 10)
rpart.plot(t.rpart)

pred.rpart.train = predict(t.rpart,  newdata = mushrooms.train, type = "class")
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.rpart.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

pred.rpart.test = predict(t.rpart,  newdata = mushrooms.test, type = "class")
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred.rpart.test, mushrooms.test$class))) / dim(mushrooms.test)[1]

library(tree)

t.tree = tree(formula = class~.,data = mushrooms.train, minsize = 1)
plot(t.tree)
text(t.tree, pretty = F)

pred.tree.train = predict(t.tree,  newdata = mushrooms.train, type = "class")
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.tree.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

pred.tree.test = predict(t.tree,  newdata = mushrooms.test, type = "class")
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred.tree.test, mushrooms.test$class))) / dim(mushrooms.test)[1]

t.rpart.2.var <- rpart(formula = class ~ odor + spore.print.color, data = mushrooms.train, minsplit = 1, minbucket = 1 )
rpart.plot(t.rpart.2.var)

pred.rpart.2.var.test = predict(t.rpart.2.var,  newdata = mushrooms.test, type = "class")
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred.rpart.2.var.test, mushrooms.test$class))) / dim(mushrooms.test)[1]

pred.rpart.2.var.train = predict(t.rpart.2.var,  newdata = mushrooms.train, type = "class")
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.rpart.2.var.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

t.tree.2.var = tree(formula = class~ odor + spore.print.color,data = mushrooms.train, minsize = 1)
plot(t.tree.2.var)
text(t.tree.2.var, pretty = F)

pred.tree.2.var.test = predict(t.tree.2.var,  newdata = mushrooms.test, type = "class")
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred.tree.2.var.test, mushrooms.test$class))) / dim(mushrooms.test)[1]

pred.tree.2.var.train = predict(t.tree.2.var,  newdata = mushrooms.train, type = "class")
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.tree.2.var.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

t.rpart.2.other.var <- rpart(formula = class ~ gill.size + bruises, data = mushrooms.train, minsplit = 1, minbucket = 1 )
rpart.plot(t.rpart.2.other.var)

pred.rpart.2.other.var.train = predict(t.rpart.2.other.var,  newdata = mushrooms.train, type = "class")
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.rpart.2.other.var.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

pred.rpart.2.other.var.test = predict(t.rpart.2.other.var,  newdata = mushrooms.test, type = "class")
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred.rpart.2.other.var.test, mushrooms.test$class))) / dim(mushrooms.test)[1]

table(pred.rpart.2.other.var.train, mushrooms.train$class)

t.tree.2.other.var = tree(formula = class~ gill.size + bruises, data = mushrooms.train, minsize = 1)
plot(t.tree.2.other.var)
text(t.tree.2.other.var, pretty = F)

pred.tree.2.other.var.train = predict(t.tree.2.other.var,  newdata = mushrooms.train, type = "class")
print("Accuracy medida en la muestra de entrenamiento:")
sum(diag(table(pred.tree.2.other.var.train, mushrooms.train$class))) / dim(mushrooms.train)[1]

pred.tree.2.other.var.test = predict(t.tree.2.other.var,  newdata = mushrooms.test, type = "class")
print("Accuracy medida en la muestra de test:")
sum(diag(table(pred.tree.2.other.var.test, mushrooms.test$class))) / dim(mushrooms.test)[1]

table(pred.tree.2.other.var.train, mushrooms.train$class)


