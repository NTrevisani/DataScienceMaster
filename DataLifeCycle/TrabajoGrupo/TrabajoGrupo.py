#!/usr/bin/env python
# coding: utf-8

# fichero original:
# 
# https://datosabiertos.malaga.eu/recursos/ambiente/calidadaire/2018.json

# In[17]:


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
    
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
calidad_aire = pd.read_csv("calidad_aire_2018.csv") 
    
# Preview the first 5 lines of the loaded data 
calidad_aire.head()

# Remove repeated/useless columns 
calidad_aire = calidad_aire.drop(calidad_aire.columns[[0,1,2,3,4,5,6,7,8]], axis=1)
calidad_aire.head()


# In[18]:


list(calidad_aire)


# In[86]:


all_z_variables = list(calidad_aire)[3:]
print(all_z_variables)


# In[99]:


for var in calidad_aire.columns[6:]:

    print(var)    
    
    calidad_aire.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = var, #calidad_aire['properties/pm1'], #'properties/pm1',
            colormap='viridis',
            s = 5)


# In[ ]:




