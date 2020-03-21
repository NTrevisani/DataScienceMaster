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


