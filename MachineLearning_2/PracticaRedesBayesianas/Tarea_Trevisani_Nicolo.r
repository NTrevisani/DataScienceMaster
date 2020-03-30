#[grafo.png](attachment:grafo.png)

library(bnlearn)

## Defino el grafo vacío:
dag <- empty.graph(nodes=c("viento", "rocio", "escarcha", "niebla", "neblina", 
                           "lluvia", "granizo", "tormenta", "nieve", "nieveSuelo"))

# Defino los arcos
arc.set <- matrix(c("viento", "lluvia",
                    "viento", "niebla",
                    "viento", "rocio",
                    "rocio",  "niebla",
                    "rocio",  "escarcha",
                    "niebla", "neblina",
                    "lluvia", "tormenta",
                    "tormenta", "granizo",
                    "tormenta", "nieve",
                    "nieve",    "nieveSuelo"),
                  byrow = TRUE, ncol = 2,
                  dimnames = list(NULL, c("from", "to")))
arcs(dag) <- arc.set

print(dag)
plot(dag)

# Verifico la factorización del punto anterior
modelstring(dag)

for (node in nodes(dag)){
    print(paste("NODO: ", node))
    print("----")
    print("PADRES:")
    print(parents(dag, node = node))
    print("----")
    print("HIJOS:")
    print(children(dag, node = node))
    print("====")
}

# Verifico que no haya v-estructuras
vstructs(dag)

dag <- set.arc(dag, from = "neblina", to = "escarcha")
vstructs(dag)

plot(dag)

dag <- set.arc(dag, from = "granizo", to = "lluvia")

mb(dag, "rocio")

dag <- set.arc(dag, from = "lluvia", to = "niebla")
vstructs(dag)

mb(dag, "rocio")

plot(dag)

# Vuelvo a definir los arcos originales
arc.set <- matrix(c("viento", "lluvia",
                    "viento", "niebla",
                    "viento", "rocio",
                    "rocio",  "niebla",
                    "rocio",  "escarcha",
                    "niebla", "neblina",
                    "lluvia", "tormenta",
                    "tormenta", "granizo",
                    "tormenta", "nieve",
                    "nieve",    "nieveSuelo"),
                  byrow = TRUE, ncol = 2,
                  dimnames = list(NULL, c("from", "to")))
arcs(dag) <- arc.set

print(dag)
plot(dag)

# Construyo la red bayesiana a partir de la tabla
meteoro <- read.table("meteoro.txt", header = TRUE)

bn = bn.fit(dag, data = meteoro, method = "bayes")

# Verifico con el código
nparams(bn)

# Nodo granizo
print(bn$granizo$prob)
plot(bn$granizo$prob)

# Nodo niebla
print(bn$niebla$prob)
plot(bn$niebla$prob)

# Vuelvo a pintar el grafo
plot(dag)

# Verifico
dsep(dag, x = "nieve", y = "granizo")

# Verifico
dsep(dag, x = "nieve", y = "granizo", z = "tormenta")

# Verifico
dsep(dag, x = "nieveSuelo", y = "neblina")

# Verifico
dsep(dag, x = "nieveSuelo", y = "neblina", z = "tormenta")

library(gRain)

# Compilo la red
red <- compile(as.grain(bn))

# Fijo el estado del nodo tormenta a 's'
red.tormenta.s = setEvidence(red, nodes = "tormenta", states = "s")

# Consulto la red: P(lluvia=s|tormenta=s) = ?
query1 <- querygrain(red.tormenta.s, nodes = "lluvia", type = "marginal")$lluvia["s"]
print(paste("La probabilidad de lluvia dado que hay tormenta es", query1))

# Consulto la red: P(viento=s|tormenta=s) = ?
query2 <- querygrain(red.tormenta.s, nodes = "viento", type = "marginal")$viento["s"]
print(paste("La probabilidad de viento dado que hay tormenta es", query2))

# Consulto la red: P(lluvia=s,viento=n|tormenta=s) = ?
query3 <- querygrain(red.tormenta.s, nodes = c("lluvia","viento"), type = "joint")["s","s"]
print(paste("La probabilidad de viento dado que hay tormenta es", query3))

# Miro la probabilidad de que llueva, sin poner condiciones
query4 <- querygrain(red, nodes = "lluvia", type = "marginal")$lluvia["s"]

print(paste("La probabilidad de lluvia dado que hay tormenta es", query1, 
            "mientras que sin poner condiciones, la probabilidad de que llueva es", query4,
            ". Eso quiere decir que es más probable que llueva cuando hay tormenta."))

# Miro la probabilidad de que haya viento, sin poner condiciones
query5 <- querygrain(red, nodes = "viento", type = "marginal")$viento["s"]

print(paste("La probabilidad de que haya viento dado que hay tormenta es", query2, 
            "mientras que sin poner condiciones, la probabilidad de que haya viento es", query5,
            ". Eso quiere decir que es más probable que haya viento cuando hay tormenta.",
            "Cuantitativamente, el aumento es del", 100*(query2 / query5 - 1), "%"))

# Fijo el numero de simulaciones a 100
N = 100

# Simulo 100 veces lo que pasa a la red sin poner condiciones
bn.sim <- simulate(red, n = N)

# Verifico que tormenta tenga como valores tantos 's' como 'n'
print(paste("Número de 's'", nrow(bn.sim[bn.sim$tormenta == 's',])))
print(paste("Número de 'n'", nrow(bn.sim[bn.sim$tormenta == 'n',])))

# Miro la probabilidad de que haya tormenta, sin poner condiciones
# para verificar que los números que saco tienen sentido
query.tormenta <- querygrain(red, nodes = "tormenta", type = "marginal")$tormenta
query.tormenta

# Simulo 100 veces lo que pasa a la red si siempre hay tormenta
bn.sim.tormenta.s <- simulate(red.tormenta.s, n = 100)

# Verifico que tormenta siempre tenga como valor 's'
bn.sim.tormenta.s$tormenta

library(ggplot2)

prob.lluvia <- nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$lluvia == 's',])/N
print(paste("Probabilidad de lluvia, dada tormenta:", 
            prob.lluvia))

my.table = table(bn.sim.tormenta.s$lluvia)
plot(my.table, type = "p", ylim = c(0,100))

arrows(1, my.table["n"] + sqrt(my.table["n"]), 
       1, my.table["n"] - sqrt(my.table["n"]), 
       length=0.05, angle=90, code=3)
points(1, 100*(1 - query1), col = "red")

arrows(2, my.table["s"] + sqrt(my.table["s"]), 
       2, my.table["s"] - sqrt(my.table["s"]), 
       length=0.05, angle=90, code=3)
points(2, 100*query1, col = "red")

prob.viento <- nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$viento == 's',])/N
print(paste("Probabilidad de viento, dada tormenta:", 
            prob.viento))

my.table = table(bn.sim.tormenta.s$viento)
plot(my.table, type = "p", ylim = c(0,100))

arrows(1, my.table["n"] + sqrt(my.table["n"]), 
       1, my.table["n"] - sqrt(my.table["n"]), 
       length=0.05, angle=90, code=3)
points(1, 100*(1 - query2), col = "red")

arrows(2, my.table["s"] + sqrt(my.table["s"]), 
       2, my.table["s"] - sqrt(my.table["s"]), 
       length=0.05, angle=90, code=3)
points(2, 100*query2, col = "red")

prob.viento.lluvia <- nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$viento == 's' & bn.sim.tormenta.s$lluvia == 's',])/N
print(paste("Probabilidad de viento y lluvia, dada tormenta:", 
            prob.viento.lluvia))

my.table = table(bn.sim.tormenta.s$viento == 's' & bn.sim.tormenta.s$lluvia == 's')
names(my.table) = c("n", "s")

plot(my.table, type = "p", ylim = c(0,100))

arrows(1, my.table["n"] + sqrt(my.table["n"]), 
       1, my.table["n"] - sqrt(my.table["n"]), 
       length=0.05, angle=90, code=3)
points(1, 100*(1 - query3), col = "red")

arrows(2, my.table["s"] + sqrt(my.table["s"]), 
       2, my.table["s"] - sqrt(my.table["s"]), 
       length=0.05, angle=90, code=3)
points(2, 100*query3, col = "red")

print(paste("La probabilidad de lluvia dado que hay tormenta es", 
            prob.lluvia))
            
prob.lluvia.no_cond <- nrow(bn.sim[bn.sim$lluvia == 's',])/N
print(paste("Mientras que sin poner condiciones, la probabilidad de que llueva es", 
            prob.lluvia.no_cond))

print("Eso quiere decir que es más probable que llueva cuando hay tormenta.")

my.table = table(bn.sim$lluvia)

plot(my.table, type = "p", ylim = c(0,100))

arrows(1, my.table["n"] + sqrt(my.table["n"]), 
       1, my.table["n"] - sqrt(my.table["n"]), 
       length=0.05, angle=90, code=3)
points(1, 100*(1 - query4), col = "red")

arrows(2, my.table["s"] + sqrt(my.table["s"]), 
       2, my.table["s"] - sqrt(my.table["s"]), 
       length=0.05, angle=90, code=3)
points(2, 100*query4, col = "red")

print(paste("La probabilidad de que haya viento dado que hay tormenta es", 
            prob.viento))
            
prob.viento.no_cond <- nrow(bn.sim[bn.sim$viento == 's',])/N
print(paste("Mientras que sin poner condiciones, la probabilidad de que haya viento es", 
            prob.viento.no_cond))

print("Eso quiere decir que es menos probable que haya viento cuando hay tormenta.")

print(paste("Cuantitativamente, disminuye del",
           100 * (prob.viento / prob.viento.no_cond - 1), "%"))

my.table = table(bn.sim$viento)

plot(my.table, type = "p", ylim = c(0,100))

arrows(1, my.table["n"] + sqrt(my.table["n"]), 
       1, my.table["n"] - sqrt(my.table["n"]), 
       length=0.05, angle=90, code=3)
points(1, 100*(1 - query5), col = "red")

arrows(2, my.table["s"] + sqrt(my.table["s"]), 
       2, my.table["s"] - sqrt(my.table["s"]), 
       length=0.05, angle=90, code=3)
points(2, 100*query5, col = "red")

# Uso arc.strength para valorar la significación de los arcos
arc.strength(dag, data = meteoro, criterion = "x2")

# Construyo el DAG usando el algoritmo Tabu search
dag.tabu <- tabu(x = meteoro)
dag.tabu
plot(dag.tabu)

# Construyo el DAG usando el algoritmo hill-climbing
dag.hc <- hc(x = meteoro)
dag.hc
plot(dag.hc)

# BIC score para el DAG original
dag.score <- bnlearn::score(dag, data = meteoro)
dag.score

# BIC score para el DAG generado con el algoritmo Tabu search
dag.tabu.score <- bnlearn::score(dag.tabu, data = meteoro)
dag.tabu.score

# BIC score para el DAG generado con el algoritmo hill-climbing
dag.hc.score <- bnlearn::score(dag.hc, data = meteoro)
dag.hc.score

# Uso simplemente 'plot', porque graphviz.plot me dá el siguiente problema:
graphviz.plot(dag)

print("DAG experto")
plot(dag)

print("DAG tabu")
plot(dag.tabu)
# Uso arc.strength para valorar la significación de los arcos
arc.strength(dag.tabu, data = meteoro, criterion = "x2")

print("DAG hill-climbing")
plot(dag.hc)
# Uso arc.strength para valorar la significación de los arcos
arc.strength(dag.hc, data = meteoro, criterion = "x2")

# Preparo la whitelist
whitelist <- matrix(c("viento", "lluvia",
                      "tormenta", "granizo",
                      "nieve", "nieveSuelo"),
                    ncol = 2,
                    dimnames = list(NULL, c("from", "to")))
# Preparo la blacklst
blacklist <- matrix(c("neblina", "granizo", 
                      "granizo", "neblina",
                      "tormenta", "niebla",
                      "niebla", "tormenta"), 
                    ncol = 2, byrow = TRUE,
                    dimnames = list(NULL, c("from", "to")))

# Construyo el DAG "semiexperto" usando el algoritmo Tabu search
dag.tabu.semiexperto <- tabu(x = meteoro,
                             whitelist = whitelist, 
                             blacklist = blacklist)
dag.tabu.semiexperto
plot(dag.tabu.semiexperto)

dag.tabu.score.semiexperto <- bnlearn::score(dag.tabu.semiexperto, data = meteoro)
dag.tabu.score.semiexperto

# Uso arc.strength para valorar la significación de los arcos
arc.strength(dag.tabu.semiexperto, data = meteoro, criterion = "x2")

# Construyo el DAG "semiexperto" usando el algoritmo hill-climbing search
dag.hc.semiexperto <- hc(x = meteoro,
                             whitelist = whitelist, 
                             blacklist = blacklist)
dag.hc.semiexperto
plot(dag.hc.semiexperto)

dag.hc.score.semiexperto <- bnlearn::score(dag.hc.semiexperto, data = meteoro)
dag.hc.score.semiexperto

# Uso arc.strength para valorar la significación de los arcos
arc.strength(dag.hc.semiexperto, data = meteoro, criterion = "x2")

# Preparo una tabla de resumen con todos los resultados de los scores

summary.table <- matrix(c("DAG experto", dag.score, 
                      "DAG Tabu", dag.tabu.score,
                      "DAG hill-climbing", dag.hc.score,
                      "DAG Tabu semi-experto", dag.tabu.score.semiexperto,
                      "DAG hill-climbing semi-experto", dag.hc.score.semiexperto), 
                    ncol = 2, byrow = TRUE,
                    dimnames = list(NULL, c("DAG", "SCORE")))
summary.table

arc.strength(dag.hc, data = meteoro, criterion = "x2")

arc.strength(dag.tabu, data = meteoro, criterion = "x2")


