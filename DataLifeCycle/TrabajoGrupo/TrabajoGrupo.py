#!/usr/bin/env python
# coding: utf-8

# # Proyecto de Ciclo de vida de los datos

# ### Preparado por:
# - Fernando
# - Eduardo
# - Cédric
# - Nicolò

# fichero original:
# 
# https://datosabiertos.malaga.eu/recursos/ambiente/calidadaire/2018.json

# In[1]:


# Load the Pandas libraries
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
    
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


# In[2]:


list(calidad_aire)[2:]


# In[3]:


droplist = calidad_aire.dtypes != object
droplist[0:2] = False
droplist


# In[4]:


calidad_aire_num = calidad_aire.drop(calidad_aire.columns[calidad_aire.dtypes == object], axis=1)
calidad_aire_num.head()


# In[101]:


droplist = calidad_aire.dtypes != object
droplist[0:2] = False
droplist

calidad_aire_obj = calidad_aire.drop(calidad_aire.columns[droplist], axis=1)

calidad_aire_obj.head()


# In[6]:


# Pinto una variable numerica: BIEN

calidad_aire_num.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = 'properties/pm1',
            colormap='viridis',
            s = 5)


# In[7]:


all_z_variables = list(calidad_aire)[3:]
print(all_z_variables)


# In[8]:


# Intento hacer un loop sobre todas las variables numericas BIEN!

for var in calidad_aire_num.columns[6:]:

    print(var)    
    
    df_tmp = calidad_aire_num[['geometry/coordinates/0/4/0','geometry/coordinates/0/4/1',var]]
    df_tmp.dropna(how='any')
    
    #calidad_aire_num.plot.
    df_tmp.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = var, #calidad_aire['properties/pm1'], #'properties/pm1',
            colormap='viridis',
            s = 5)


# In[9]:


# Lista de colores para mapear con los valores de la variable
color = np.array(['green','olivedrab','darkgoldenrod','orange','red',"purple"])
# Lista de valores de la variable cada una tiene un color
category = np.array(['good', 'moderate', 'unhealthy-low','unhealthy', 'unhealthy-high', 'nan'])
# Diccionario que mapea el valor de la variable como clave y el color como valor de la clave
dictCol = dict(zip(category, color))

# Método al que se le pasa un valor(clave) y obtiene su color asociado
def attribute_color(valor):
    # Si el valor pasado es un nan se detecta como float y se devuelve su color asociado
    if isinstance(valor, float):
        return dictCol.get(str(valor))
    else:
        return dictCol.get(valor)


# In[10]:


# Intento hacer un loop sobre todas las variables categoricas

#Crea el eje de la barra de color
bounds = np.linspace(0,7,7)
# Mapa de colores
cmap = mpl.colors.ListedColormap(color)

# Pinto solo la primera variable, no se si las demás tienen los mismos valores discretos.
for var in calidad_aire_obj.columns[2:]:

    # Variables que contiene el plotteo
    fig, ax = plt.subplots()

    df_tmp = calidad_aire_obj[['geometry/coordinates/0/4/0','geometry/coordinates/0/4/1',var]]
    df_tmp = df_tmp.dropna(how = 'any')
    
    # Cada observación de la variable se le asigna un color respecto a su valor discreto y se crea una lista de colores.
    color_variable = list()
    for i in df_tmp.index: #range(len(df_tmp[var])):
        color_variable.append(attribute_color(df_tmp[var][i]))
    # La lista de colores será la que se le pase al scatter plot en el parámetro c.
    ax.scatter(x = df_tmp['geometry/coordinates/0/4/0'], 
        y = df_tmp['geometry/coordinates/0/4/1'], 
        c = color_variable,#calidad_aire['properties/pm1'], #'properties/pm1',
        s = 5)
    
    # Situa la barra de color
    ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
    # Crea la barra de color
    cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
    spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
    # Define la posición de los ticks de la barra de color y las etiquetas a usar
    cb.set_ticks(cb.get_ticks()+0.589)
    cb.set_ticklabels(category)
    
    #plt.scatter(x,y, c=colors[z])


# In[106]:


calidad_aire_obj.head()


# In[117]:


# Quiero pasar de variables categoricas a numeros.
# e.g. Unhealthy-high = 0, Unhealthy = 1

calidad_aire_obj_num = calidad_aire_obj.copy()
calidad_aire_obj_num.head()


calidad_aire_obj_num.iloc[:,2:] = -1 
calidad_aire_obj_num.head()

calidad_aire_obj_num[calidad_aire_obj.iloc[:,2:] == 'good'] = 4
calidad_aire_obj_num[calidad_aire_obj.iloc[:,2:] == 'moderate'] = 3
calidad_aire_obj_num[calidad_aire_obj.iloc[:,2:] == 'unhealthy-low'] = 2
calidad_aire_obj_num[calidad_aire_obj.iloc[:,2:] == 'unhealthy'] = 1
calidad_aire_obj_num[calidad_aire_obj.iloc[:,2:] == 'unhealthy-high'] = 0
calidad_aire_obj_num[calidad_aire_obj_num.iloc[:,2:] == -1] = np.NaN


calidad_aire_obj_num.head()


# In[12]:


# Intento hacer un loop sobre todas las variables categoricas

for var in calidad_aire_obj.columns[2:]:

    print(calidad_aire_obj[var].unique())    
    colors = np.array(calidad_aire_obj[var].unique())
    
    df_tmp = calidad_aire_obj[['geometry/coordinates/0/4/0','geometry/coordinates/0/4/1',var]]
    df_tmp.dropna(how='any')

    #calidad_aire
    df_tmp.plot.scatter(x = 'geometry/coordinates/0/4/0', 
        y = 'geometry/coordinates/0/4/1', 
        c = colors[var], #calidad_aire['properties/pm1'], #'properties/pm1',
        colormap='viridis',
        s = 5)
    
    
# https://stackoverflow.com/questions/52108558/how-does-parameters-c-and-cmap-behave-in-a-matplotlib-scatter-plot
#plt.scatter(x,y, c=colors[z])


# In[ ]:





# In[ ]:





# In[ ]:


uso_bici = pd.read_csv("bici_pc.csv",
                       sep = ';',
                       skiprows = 4)
uso_bici


# In[ ]:




