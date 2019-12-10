#!/usr/bin/env python
# coding: utf-8

# fichero original:
# 
# https://datosabiertos.malaga.eu/recursos/ambiente/calidadaire/2018.json

# In[177]:


# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
    
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
calidad_aire = pd.read_csv("calidad_aire_2018.csv") 
    
# Preview the first 5 lines of the loaded data 
calidad_aire.head()
list(calidad_aire)

# Remove repeated/useless columns 
calidad_aire = calidad_aire.drop(calidad_aire.columns[[0,1,2,3,4,5,6,7,8,11,18]], axis=1)
calidad_aire.head()


# In[178]:


list(calidad_aire)[2:]


# In[179]:


droplist = calidad_aire.dtypes != object
droplist[0:2] = False
droplist


# In[180]:


calidad_aire_num = calidad_aire.drop(calidad_aire.columns[calidad_aire.dtypes == object], axis=1)
calidad_aire_num.head()


# In[181]:


droplist = calidad_aire.dtypes != object
droplist[0:2] = False
droplist

calidad_aire_obj = calidad_aire.drop(calidad_aire.columns[droplist], axis=1)
calidad_aire_obj.head()


# In[182]:


# Pinto una variable numerica: BIEN

calidad_aire_num.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = 'properties/pm1',
            colormap='viridis',
            s = 5)


# In[183]:


all_z_variables = list(calidad_aire)[3:]
print(all_z_variables)


# In[184]:


# Intento hacer un loop sobre todas las variables numericas BIEN!

for var in calidad_aire_num.columns[6:]:

    print(var)    
    
    calidad_aire.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = var, #calidad_aire['properties/pm1'], #'properties/pm1',
            colormap='viridis',
            s = 5)


# In[189]:


# Intento hacer un loop sobre todas las variables categoricas

for var in calidad_aire_obj.columns[2:]:

    print(calidad_aire_obj[var].unique())    
    colors = np.array(calidad_aire_obj[var].unique())
    
    calidad_aire.plot.scatter(x = 'geometry/coordinates/0/4/0', 
        y = 'geometry/coordinates/0/4/1', 
        c = colors[var], #calidad_aire['properties/pm1'], #'properties/pm1',
        colormap='viridis',
        s = 5)
    
    
    #plt.scatter(x,y, c=colors[z])


# In[ ]:





# In[ ]:




