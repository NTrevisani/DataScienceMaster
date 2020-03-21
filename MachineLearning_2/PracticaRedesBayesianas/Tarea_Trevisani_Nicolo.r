### ![grafo.png](attachment:grafo.png)

library(bnlearn)

## Defino el grafo vacío:
dag <- empty.graph(nodes=c("Viento", "Rocio", "Escarcha", "Niebla", "Nieblina", 
                           "Lluvia", "Granizo", "Tormenta", "Nieve", "Nieve_Suelo"))

# Defino los arocs
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

dag$arcs


