data <- read.csv("breastcancer.csv")

# Eliminar no predictores (id y última columna vacía)
df <- data[, -c(1, ncol(data)-1, ncol(data))]

# Convertir el factor diagnosis (B y M) a los valores numéricos 0 y 1, respectivamente.
levels(df$diagnosis) <- c(0,1) 
df$diagnosis <- as.numeric(as.character(df$diagnosis))

# Normalizar los datos para evitar problemas de diferente variabilidad
df[-1] <- apply(df[-1], MARGIN = 2, scale)
rm(data)
dim(df)
names(df)

# Pinto la correlación entre las vaiables
library(lattice) # levelplot
cor.matrix <- abs(cor(df))
levelplot(cor.matrix, at = seq(0, 1, 0.1), col.regions = rev(grey.colors(10)),
          scale = list(x = list(rot = 90)))

#install.packages("verification")
#install.packages("caret")
#install.packages("e1071")
library(verification, quietly = TRUE) # roc.area
library(caret, quietly = TRUE) # confusionMatrix

model <- glm(diagnosis ~ ., data = df, family = "binomial")
pred  <- predict(model,df[-1], type = "response")

roc.plot(df$diagnosis,pred,
  main=sprintf("Curva ROC (AUC=%g)", roc.area(obs = df$diagnosis,pred)$A)
)

# Separo el dataset en dos:
# - un sub-set de entrenamiento (75%)
# - un sub-set de test (25%)

N = nrow(df)
indtrain <- sample(1:N, N*0.75)

df.train = df[indtrain,] 
df.test = df[-indtrain,]
nrow(df.train)
nrow(df.test)

model.train <- glm(diagnosis ~ ., data = df.train, family = "binomial")
pred.test  <- predict(model.train, df.test[-1], type = "response")

roc.plot(df.test$diagnosis,pred.test,
  main=sprintf("Curva ROC (AUC=%g)", roc.area(obs = df.test$diagnosis,pred.test)$A)
)

#print(paste(pred.test, df.test[,1]))

#acc.class(pred.test, df.test[,1])

#install.packages('leaps')
library(leaps)
regfit.full <- regsubsets(diagnosis ~., df, nvmax = 30)
full.summary <- summary(regfit.full)
names(full.summary)

par(mfrow=c(2,1), mar=c(4,4,1,1))
plot(full.summary$rsq,xlab="Number of Variables",ylab="RSq", type="l")
plot(full.summary$bic,xlab="Number of Variables",ylab="BIC", type="l")

which.min(full.summary$bic)

plot(regfit.full, scale ="r2")
plot(regfit.full, scale ="bic")

coef(regfit.full, 11)

regfit.fwd <- regsubsets(diagnosis~., data = df, nvmax = 30 , method ="forward")
fwd.summary <- summary(regfit.fwd)

par(mfrow=c(2,1), mar=c(4,4,1,1))
plot(fwd.summary$rsq,xlab="Number of Variables",ylab="RSq", type="l")
plot(fwd.summary$bic,xlab="Number of Variables",ylab="BIC", type="l")

plot(regfit.fwd, scale ="r2")
plot(regfit.fwd, scale ="bic")

# Número optimo de variables
n.var.fwd = which.min(fwd.summary$bic)
n.var.fwd

# Variables óptimas y sus coeficientes
coef(regfit.fwd, n.var.fwd)

regfit.bwd <- regsubsets(diagnosis~., data = df, nvmax = 30 , method ="backward")
bwd.summary <- summary(regfit.bwd)

par(mfrow=c(2,1), mar=c(4,4,1,1))

plot(bwd.summary$rsq,xlab="Number of Variables",ylab="RSq", type="l")
plot(bwd.summary$bic,xlab="Number of Variables",ylab="BIC", type="l")

plot(regfit.bwd, scale ="r2")
plot(regfit.bwd, scale ="bic")

# Número optimo de variables
n.var.bwd = which.min(bwd.summary$bic)
n.var.bwd

# Variables óptimas y sus coeficientes
coef(regfit.bwd, n.var.bwd)

initialModel_0 <- glm(diagnosis ~ 1, data = df, family=binomial(link="logit"))
initialModel_p <- glm(diagnosis ~ ., data = df, family=binomial(link="logit"))

fw <- step(initialModel_0,
  scope = list(lower = formula(initialModel_0), upper = formula(initialModel_p)),
  direction = "forward"
)
summary(fw)

# Para solo hasta 11 (o en general hasta el número optimo de variables) ?
fw$anova
?step

#install.packages("glmnet")
library(glmnet, quiet = TRUE)

# Busco el valor optimo de lambda

# Uso la distancia L1 --> alpha = 1
cv <- cv.glmnet(as.matrix(df[-1]),df$diagnosis,family = "binomial",alpha = 1)
cv$lambda.1se

# Ahora entreno un modelo lineal regularizado a través del valor lambda que me da 'cv.glmnet'
model.l1 <- glmnet(as.matrix(df[-1]), df$diagnosis, family = "binomial", alpha = 1, lambda = cv$lambda.1se)

# Estoy usando norma L1: algunas variables tendrán coeficiente 0
# Las que tienen coeficiente no nulo son las 'buenas'
ind.coef.no.nulos <- which(as.numeric(coef(model.l1)) != 0)
names(df)[ind.coef.no.nulos]
cat(paste("Number of variables selected:", length(ind.coef.no.nulos)))

pred.l1 <- predict(model.l1,as.matrix(df[-1]),type = "response")
auc.l1 <- roc.area(df$diagnosis,pred.l1)$A
roc.plot(df$diagnosis,pred.l1, main=sprintf("Curva ROC Regularización L1 (AUC = %g)", auc.l1))

# Busco el valor optimo de lambda

# Uso la distancia L1 --> alpha = 1
cv <- cv.glmnet(as.matrix(df.train[-1]),
                df.train$diagnosis,
                family = "binomial",
                alpha = 1)
cv$lambda.1se

# Ahora entreno un modelo lineal regularizado a través del valor lambda que me da 'cv.glmnet'
# usando solo el conjunto de entrenamiento
model.train.l1 <- glmnet(as.matrix(df.train[-1]), 
                   df.train$diagnosis, 
                   family = "binomial", 
                   alpha = 1, 
                   lambda = cv$lambda.1se)

# Estoy usando norma L1: algunas variables tendrán coeficiente 0
# Las que tienen coeficiente no nulo son las 'buenas'
ind.coef.no.nulos <- which(as.numeric(coef(model.train.l1)) != 0)
names(df)[ind.coef.no.nulos]
cat(paste("Number of variables selected:", length(ind.coef.no.nulos)))

# ROC del conjunto de train
pred.train.l1 <- predict(model.train.l1,
                        as.matrix(df.train[-1]),
                        type = "response")

auc.train.l1 <- roc.area(df.train$diagnosis,
                        pred.train.l1)$A

roc.plot(df.train$diagnosis,
         pred.train.l1, 
         main=sprintf("Curva ROC Regularización L1 (AUC = %g)", 
         auc.train.l1))

# ROC del conjunto de test
pred.test.l1 <- predict(model.train.l1,
                        as.matrix(df.test[-1]),
                        type = "response")

auc.test.l1 <- roc.area(df.test$diagnosis,
                        pred.test.l1)$A

roc.plot(df.test$diagnosis,
         pred.test.l1, 
         main=sprintf("Curva ROC Regularización L1 (AUC = %g)", 
         auc.test.l1))

# Uso la distancia L2 --> alpha = 0

# Busco el lambda optimo
cv2 <- cv.glmnet(as.matrix(df[-1]),df$diagnosis,family = "binomial",alpha = 0)
cv2$lambda.1se

# Ahora entreno el modelo lineal con el lambda optimo
model.l2 <- glmnet(as.matrix(df[-1]), df$diagnosis, family = "binomial", alpha = 0, lambda = cv2$lambda.1se)
ind.coef.no.nulos.l2 <- which(as.numeric(coef(model.l2)) != 0)
cat(paste("Number of variables selected:", length(ind.coef.no.nulos.l2)))

pred.l2 <- predict(model.l2,as.matrix(df[-1]),type = "response")
auc.l2 <- roc.area(df$diagnosis,pred.l2)$A
roc.plot(df$diagnosis,pred.l2, main=sprintf("Curva ROC Regularización L2 (AUC = %g)", auc.l2))

# Uso la distancia L2 --> alpha = 0

# Busco el lambda optimo
cv2 <- cv.glmnet(as.matrix(df.train[-1]),
                 df.train$diagnosis,
                 family = "binomial",
                 alpha = 0)
cv2$lambda.1se

# Ahora entreno el modelo lineal con el lambda optimo
model.train.l2 <- glmnet(as.matrix(df.train[-1]), 
                         df.train$diagnosis, 
                         family = "binomial", 
                         alpha = 0, 
                         lambda = cv2$lambda.1se)

ind.coef.no.nulos.l2 <- which(as.numeric(coef(model.train.l2)) != 0)
cat(paste("Number of variables selected:", length(ind.coef.no.nulos.l2)))

# Miro como funciona el modelo 'model.l2' sobre el conjunto de train
pred.train.l2 <- predict(model.train.l2, 
                         as.matrix(df.train[-1]),
                         type = "response")

auc.train.l2 <- roc.area(df.train$diagnosis,
                         pred.train.l2)$A

roc.plot(df.train$diagnosis,
         pred.train.l2, 
         main=sprintf("Curva ROC Regularización L1 (AUC = %g)", 
         auc.train.l2))

# Miro como funciona el modelo 'model.l2' sobre el conjunto de test
pred.test.l2 <- predict(model.train.l2, 
                        as.matrix(df.test[-1]),
                        type = "response")

auc.test.l2 <- roc.area(df.test$diagnosis,
                        pred.test.l2)$A

roc.plot(df.test$diagnosis,
         pred.test.l2, 
         main=sprintf("Curva ROC Regularización L1 (AUC = %g)", 
         auc.test.l2))
