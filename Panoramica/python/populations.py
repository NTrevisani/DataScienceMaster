import numpy

# Importing txt file as a numpy array
my_data = numpy.loadtxt("data/populations.txt")

# Create an array with the names of the species
species = numpy.array(["hare","lynx","carrot"])

# Get the most abundant species every year
best_species = species[[my_data[:,1:].argmax(axis = 1)]]

# Create an array with all the years
years = numpy.array(my_data[:,0], dtype = "int_")

# Merging the (year,best_species) arrays in one dictionary, just for printing
my_dict = {}
for key, value in zip(years, best_species):
    my_dict[key] = value

# Printing the result
print("Most abundant species, year by year:")
for i in my_dict.keys():
    print(i, my_dict[i])
