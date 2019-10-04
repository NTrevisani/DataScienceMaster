# El siguiente codigo deberia obtener los numeros primos que
# existan hasta "n", incluyendo "n", pero contiene errores.

n = 30

# Inicializo la lista de numeros primos
primos = []
primos.append(1)
primos.append(2)

# Itero sobre los numeros
for j in range(2,n+1):
    isPrime = True
    for i in primos[1:]:
        # check if not divisible by elem of list
        if j % i == 0:                
            isPrime = False
    if isPrime == True:
        primos.append(j)
print("La lista de los numeros primos entre 1 y {} es:\n {}".format(n,primos))
