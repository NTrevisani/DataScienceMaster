#!/usr/bin/env python
# coding: utf-8

# # Tarea Pandas
# 
# Nicolò Trevisani

# In[54]:


import numpy as np
import pandas as pd


# ## Archivo CSV

# In[59]:


# Leo el dataset y miro su formato

df = pd.read_csv('Centroides_NucleosPoblacion.csv')
df.head()


# 1) ¿Cuántos Municipios tienen más de 100000 habitantes?. ¿Cuál es la segunda ciudad más poblada?. ¿Qué posición ocupa Granada en el ranking de las más pobladas?.

# In[56]:


# Número de Municipios con más de cien mil habitantes
len(df[df.Poblacion > 100000])


# In[33]:


# Segunda ciudad más poblada
df.sort_values(by=['Poblacion'], ascending = False)[1:2].Municipio


# In[9]:


# Posición que ocupa Granada
df2 = df.sort_values(by=['Poblacion'], ascending = False).reset_index()
df2[df2.Municipio == "Granada"].index + 1 # Sumo 1 porque el primer índice es 0


# 2) Escriba los nombres de los 10 municipios con menos población.

# In[32]:


df.sort_values(by=['Poblacion'])[0:10].Municipio


# 3) ¿Cuántos municipios de León tienen más de 6000 habitantes?.

# In[15]:


len(df[df.Provincia == 'León'].Poblacion > 6000)


# 4) ¿Cuál es el municipio situado más al Norte? (Usar el valor de la coordenada "Y" que representa la latitud en grados). Proporcione también la provincia a la que pertenece y su población.

# In[31]:


mun_norte  = df.loc[df.Y.idxmax(axis = 1)].Municipio
prov_norte = df.loc[df.Y.idxmax(axis = 1)].Provincia

print("El municipio más al norte es {0} y se encuentra en la provincia de {1}".format(mun_norte,prov_norte))


# 5) ¿Cual es el municipio de la provincia de Cantabria situado más al Este?. ¿Cual es el situado más al Oeste?.

# In[ ]:


mun_este = df.loc[df[df.Provincia == "Cantabria"].X.idxmax()].Municipio
mun_oeste = df.loc[df[df.Provincia == "Cantabria"].X.idxmin()].Municipio

print("El municipio más al este de Cantabria es {0}, el más el oeste es {1}".format(mun_este,mun_oeste))


# 6) Dígame los nombres de los Municipios más cercano y más lejano a Madrid. Para ello debe calcular la distancia en todos ellos y Madrid. Por supuesto, Madrid no cuenta.

# In[ ]:


# Defino las coordenadas de Madrid
x_madrid = df[df.Municipio == 'Madrid'].X.values
y_madrid = df[df.Municipio == 'Madrid'].Y.values

# Anado la columna 'dist_madrid', con las distancia euclideas de 
# los municipios con respecto a Madrid
df['dist_Madrid'] = (df.X - x_madrid)**2 + (df.Y - y_madrid)**2

# Cross-check: quiero que la distancia de Madrid con Madrid sea 0
df[df.Municipio == 'Madrid']


# In[93]:


# Ahora los resultados
far = df.loc[df['dist_Madrid'].idxmax()].Municipio
close = df.sort_values(by=['dist_Madrid'])[1:2].Municipio.values[0]

print("El municipio más cercano a Madrid es {0}, el más lejano es {1}".format(close, far))


# 7) ¿Cuántos Municipios hay en un radio de 5 grados de la ciudad de Barcelona?

# In[ ]:


# Defino las coordenadas de Barcelona
x_barcelona = df[df.Municipio == 'Barcelona'].X.values
y_barcelona = df[df.Municipio == 'Barcelona'].Y.values

# Anado la columna 'dist_barcelona', con las distancia euclideas de 
# los municipios con respecto a Barcelona
df['dist_Barcelona'] = (df.X - x_barcelona)**2 + (df.Y - y_barcelona)**2

# Cross-check: quiero que la distancia de Barcelona con Barcelona sea 0
df[df.Municipio == 'Barcelona']


# In[99]:


# Ahora los resultados
len(df[df['dist_Barcelona'] < 5])


# 8) Obtenga la media, mediana, desviación estándar, valor máximo y valor mínimo de la población de los municipios de la provincia de Cantabria.

# In[126]:


pobl_cantabria = df[df.Provincia == "Cantabria"].Poblacion

print("Población en Cantabria:")

print("Valor medio: %2d" %(pobl_cantabria.mean()))
print("Mediana: %2d" %(pobl_cantabria.median()))
print("Desviación típica: %2d" %(pobl_cantabria.std()))

print("Valor máximo: %2d" %(pobl_cantabria.max()))
print("Valor mínimo: %2d" %(pobl_cantabria.min()))


# 9) Usando los métodos de agregación, calcular las poblaciones de cada provincia.

# In[123]:


df.groupby('Provincia').Poblacion.sum()


# 10) Dibujar el valor de la población para las diferentes ciudades (usar las funciones vistas en MatPlotLib).

# In[142]:


import matplotlib.pyplot as plt

df.plot.scatter(x='X', 
        y='Y', 
        c = 'Poblacion',
        colormap='YlOrRd',
        s = 5)


# 11) Hacer un gráfico equivalente pero para las diferentes provincias. Seleccionar un punto representativo de las ciudades incluidas en cada provincia.

# In[163]:


# Agrupo por provincia, y me quedo con el Municipio con más población
# (quiero usar sus coordenadas)
df_plot = df.loc[df.groupby('Provincia').Poblacion.idxmax()]

df_plot_2 = df_plot[['Municipio','X','Y']]
df_plot_2['Poblacion'] = df.groupby('Provincia').Poblacion.sum().values

df_plot_2.plot.scatter(x='X', 
        y='Y', 
        c = 'Poblacion',
        colormap='YlOrRd',
        s = 5)

