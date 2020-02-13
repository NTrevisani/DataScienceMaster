#!/usr/bin/env python
# coding: utf-8

# # Métodos kernel para clasificación

# I am going to consider the dataset "Rain in Australia", which aims to predict wether the next day it will rain or not, based on some atmospheric measurements:
# 
# https://www.kaggle.com/jsphyg/weather-dataset-rattle-package/data

# In[30]:


# Import basic libraries
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
my_file = "weatherAUS.csv"
rain = pd.read_csv(my_file)


# In[54]:


# Look at the available variables
for var in rios.columns:
    print(var)


# In[43]:


rain.head()


# In[86]:


# Many cities are available: maybe we can focus on just one of them
print(set(rain.Location))

brisbane = rain[rain.Location == "Brisbane"]
brisbane.head()


# In[91]:


# Evaporation and Sunshine are empty: let's remove them
# I shall remove also categorical variables, like the wind direction
# I know the location, so I can remove it, and I am not interested in the date
droplist = ["Evaporation", "Sunshine", "WindGustDir", "WindDir9am", "WindDir3pm", "Location", "Date", "RainToday", "RISK_MM"]
brisbane_slim = brisbane.drop(droplist, axis = 1)

brisbane_slim.dropna(how='any', inplace = True)
len(brisbane_slim)


# In[100]:


# Check the correlation among variables,
# to see if it is possible to remove some of them
# (https://stackoverflow.com/questions/29432629/plot-correlation-matrix-using-pandas)

f = plt.figure(figsize=(19, 15))
plt.matshow(brisbane_slim.corr(), fignum=f.number)
plt.xticks(range(brisbane_slim.shape[1] - 1), brisbane_slim.columns, fontsize=14, rotation=45)
plt.yticks(range(brisbane_slim.shape[1] - 1), brisbane_slim.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)
#plt.title('Correlation Matrix', fontsize=16);


# In[57]:





# In[ ]:




