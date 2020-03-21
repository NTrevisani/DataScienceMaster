### ![grafo.png](attachment:grafo.png)

library(bnlearn)

## Defino el grafo vacío:
dag <- empty.graph(nodes=c("Viento", "Rocio", "Escarcha", "Niebla", "Nieblina", 
                           "Lluvia", "Granizo", "Tormenta", "Nieve", "Nieve_Suelo"))

# Defino los arcos
arc.set <- matrix(c("Viento", "Lluvia",
                    "Viento", "Niebla",
                    "Viento", "Rocio",
                    "Rocio",  "Niebla",
                    "Rocio",  "Escarcha",
                    "Niebla", "Nieblina",
                    "Lluvia", "Tormenta",
                    "Tormenta", "Granizo",
                    "Tormenta", "Nieve",
                    "Nieve",    "Nieve_Suelo"),
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

dag <- set.arc(dag, from = "Nieblina", to = "Escarcha")
vstructs(dag)

plot(dag)

dag <- set.arc(dag, from = "Granizo", to = "Lluvia")

mb(dag, "Rocio")

dag <- set.arc(dag, from = "Lluvia", to = "Niebla")
vstructs(dag)

mb(dag, "Rocio")

plot(dag)

# Vuelvo a definir los arcos originales
arc.set <- matrix(c("Viento", "Lluvia",
                    "Viento", "Niebla",
                    "Viento", "Rocio",
                    "Rocio",  "Niebla",
                    "Rocio",  "Escarcha",
                    "Niebla", "Nieblina",
                    "Lluvia", "Tormenta",
                    "Tormenta", "Granizo",
                    "Tormenta", "Nieve",
                    "Nieve",    "Nieve_Suelo"),
                  byrow = TRUE, ncol = 2,
                  dimnames = list(NULL, c("from", "to")))
arcs(dag) <- arc.set

print(dag)
plot(dag)


