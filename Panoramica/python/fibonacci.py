# Serie de Fibonacci con un bucle while

# By definition, for N=0 and N=1:
term_N_0 = 0
term_N_1 = 1

# Let's print them
print(term_N_0)
print(term_N_1)

# Initialize the (N-2)-th and the (N-1)-th terms used to calculate the N-th term of the sequence
term_N_minus_2 = term_N_0
term_N_minus_1 = term_N_1

# Current term
term_N = 0

# We start the loop from N=2
N = 2
while N < 20:
    # Actual computation of the N-th term of the sequence   
    term_N = term_N_minus_2 + term_N_minus_1
    print(term_N)    
    # Updating the terms to be summed
    term_N_minus_2 = term_N_minus_1
    term_N_minus_1 = term_N
    # Updating the counter
    N += 1

