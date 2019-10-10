import numpy

my_data = numpy.loadtxt("data/populations.txt")

species = numpy.array(["hare","lynx","carrot"])

best_species = species[[my_data[:,1:].argmax(axis = 1)]]

years = numpy.array(my_data[:,0], dtype = "int_")

my_dict = {}

for key, value in zip(years, best_species):
    my_dict[key] = value

print("Most abundant species, year by year:")
for i in my_dict.keys():
    print(i, my_dict[i])
