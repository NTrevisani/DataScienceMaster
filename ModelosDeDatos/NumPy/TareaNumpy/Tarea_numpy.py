#!/usr/bin/env python
# coding: utf-8

# ## Load NumPy and the dataset

# In[1]:


import numpy as np


# In[2]:


data = np.loadtxt("populations.txt")
data


# ## Mean and std dev of the populations of each species for the years in the period.

# In[3]:


# Mean of each of the three columns of 'data' with species
mean_hare, mean_lynx, mean_carrot = data[:,1:].mean(axis = 0)
print("The mean hares population is {0:.0f}".format(mean_hare))
print("The mean lynx population is {0:.0f}".format(mean_lynx))
print("The mean carrots population is {0:.0f}".format(mean_carrot))


# In[4]:


# Standard deviation of each of the three columns of 'data' with species
std_dev_hare, std_dev_lynx, std_dev_carrot = data[:,1:].std(axis = 0)
print("The standard deviation of hares population is {0:.0f}".format(std_dev_hare))
print("The standard deviation of lynx population is {0:.0f}".format(std_dev_lynx))
print("The standard deviation of carrots population is {0:.0f}".format(std_dev_carrot))


# ## Year in which each species had the largest population.

# In[5]:


# Supporting array, just for printing years as integers
years = np.array(data[:,0], dtype = "int_")

# Indices of the maxima of each of the three columns of 'data' with species
max_hare, max_lynx, max_carrot = data[:,1:].argmax(axis = 0)

# Print the corresponding year, using the indices obtained in the previous step
print("Hares reached their maximum population in",years[max_hare])
print("Lynx reached their maximum population in",years[max_lynx])
print("Carrots reached their maximum population in",years[max_carrot])


# ## Species with the largest population for each year.

# In[6]:


# Supporting arrays, just for printing
species = np.array(["hare","lynx","carrot"])
years = np.array(data[:,0], dtype = "int_")

# Indices of the maximum of each line,
# passed to 'species' array to get the corresponding
# species with the largest population
best_species = species[[data[:,1:].argmax(axis = 1)]]

print("Most abundant species, year by year:")
print(dict(zip(years, best_species)))


# ## Years in which any of the populations is above 50000

# In[7]:


# Check in 'data' if at least one of the three columns with species
# has a population larger than 50000, year by year
more_50000 = years[np.any(data[:,1:] > 50000, axis=1)]
print("In these years, at least one species had a population larger than 50000:")
print(more_50000)


# ##  For each species, the two years with the lowest population

# In[8]:


# Get the sorted populations idices
j = data[:,1:].argsort(axis = 0)


# In[9]:


# Just checking
data[j,(1,2,3)]


# In[10]:


# printing
print("Hares had their minimum populations in",years[j][0:2,0])
print("Lynx had their minimum populations in",years[j][0:2,1])
print("Carrots had their minimum populations in",years[j][0:2,2])


# ## Compare the gradient of hare population and number of lynx and check correlation.

# In[11]:


from matplotlib import pyplot as plt


# In[12]:


# transform columns into variables
year, hares, lynx, carrots = data.T 


# In[13]:


# Get the gradient of hares population
hares_grad = np.gradient(hares)


# In[14]:


# Plot the gradients
plt.axes([0.0, 0.0, 1.0, 1.0]) 
plt.plot(year, hares_grad, year, lynx)
plt.legend(('Hare gradient', 'Lynx population'), loc=(1.05, 0.5)) 


# In[15]:


np.corrcoef([hares_grad, lynx])


# It is evident that there is a strong anti-correlation between the lynx (predator) and the hare (prey) populations.
# 
# This can be observed both in the plot of the hare population gradient versus the lynx population and in the correlation matrix of the two variables. 
# Here it can be seen that when the lynx population increases, the hare population starts to decrease (negative gradient) and that when there are few hares, also the linx start to decrease in number, due to the lack of preys.
# 
# Once the predators are less abundant, the hares start to increase in population again, creating an oscillation of the populations of the two species.
