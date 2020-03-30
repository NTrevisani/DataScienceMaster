### ![grafo.png](attachment:grafo.png)

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
#print(bn)

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

print(paste("Probabilidad de lluvia, dada tormenta:", 
            nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$lluvia == 's',])/N))

print(paste("Probabilidad de viento, dada tormenta:", 
            nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$viento == 's',])/N))

print(paste("Probabilidad de viento y lluvia, dada tormenta:", 
            nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$viento == 's' & bn.sim.tormenta.s$lluvia == 's',])/N))

print(paste("La probabilidad de lluvia dado que hay tormenta es", 
            nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$lluvia == 's',])/N))
            
print(paste("Mientras que sin poner condiciones, la probabilidad de que llueva es", 
            nrow(bn.sim.tormenta.s[bn.sim$lluvia == 's',])/N))

print("Eso quiere decir que es más probable que llueva cuando hay tormenta.")

print(paste("La probabilidad de que haya viento dado que hay tormenta es", 
            nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$viento == 's',])/N))
            
print(paste("Mientras que sin poner condiciones, la probabilidad de que haya viento es", 
            nrow(bn.sim.tormenta.s[bn.sim$viento == 's',])/N))

print("Eso quiere decir que es más probable que haya viento cuando hay tormenta.")

print(paste("Cuantitativamente, el aumento es del",
           100 * (nrow(bn.sim.tormenta.s[bn.sim.tormenta.s$viento == 's',]) / 
            nrow(bn.sim.tormenta.s[bn.sim$viento == 's',]) - 1), "%"))










