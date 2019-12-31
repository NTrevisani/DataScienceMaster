#!/usr/bin/env python
# coding: utf-8

# # Tarea Pandas
# 
# Nicolò Trevisani

# In[1]:


import numpy as np
import pandas as pd


# ## Archivo CSV

# In[2]:


# Leo el dataset y miro su formato

df = pd.read_csv('Centroides_NucleosPoblacion.csv')
df.head()


# 1) ¿Cuántos Municipios tienen más de 100000 habitantes?. ¿Cuál es la segunda ciudad más poblada?. ¿Qué posición ocupa Granada en el ranking de las más pobladas?.

# In[3]:


# Número de Municipios con más de cien mil habitantes
len(df[df.Poblacion > 100000])


# In[4]:


# Segunda ciudad más poblada
df.sort_values(by=['Poblacion'], ascending = False)[1:2].Municipio.values[0]


# In[5]:


# Posición que ocupa Granada
df2 = df.sort_values(by=['Poblacion'], ascending = False).reset_index()
df2[df2.Municipio == "Granada"].index.values[0] + 1 # Sumo 1 porque el primer índice es 0


# 2) Escriba los nombres de los 10 municipios con menos población.

# In[6]:


df.sort_values(by=['Poblacion'])[0:10].Municipio


# 3) ¿Cuántos municipios de León tienen más de 6000 habitantes?.

# In[7]:


len(df[df.Provincia == 'León'].Poblacion > 6000)


# 4) ¿Cuál es el municipio situado más al Norte? (Usar el valor de la coordenada "Y" que representa la latitud en grados). Proporcione también la provincia a la que pertenece y su población.

# In[8]:


mun_norte  = df.loc[df.Y.idxmax(axis = 1)].Municipio
prov_norte = df.loc[df.Y.idxmax(axis = 1)].Provincia

print("El municipio más al norte es {0} y se encuentra en la provincia de {1}".format(mun_norte,prov_norte))


# 5) ¿Cual es el municipio de la provincia de Cantabria situado más al Este?. ¿Cual es el situado más al Oeste?.

# In[9]:


mun_este = df.loc[df[df.Provincia == "Cantabria"].X.idxmax()].Municipio
mun_oeste = df.loc[df[df.Provincia == "Cantabria"].X.idxmin()].Municipio

print("El municipio más al este de Cantabria es {0}, el más el oeste es {1}".format(mun_este,mun_oeste))


# 6) Dígame los nombres de los Municipios más cercano y más lejano a Madrid. Para ello debe calcular la distancia en todos ellos y Madrid. Por supuesto, Madrid no cuenta.

# In[10]:


# Defino las coordenadas de Madrid
x_madrid = df[df.Municipio == 'Madrid'].X.values
y_madrid = df[df.Municipio == 'Madrid'].Y.values

# Anado la columna 'dist_madrid', con las distancia euclideas de 
# los municipios con respecto a Madrid
df['dist_Madrid'] = (df.X - x_madrid)**2 + (df.Y - y_madrid)**2

# Cross-check: quiero que la distancia de Madrid con Madrid sea 0
df[df.Municipio == 'Madrid']


# In[11]:


# Ahora los resultados
far = df.loc[df['dist_Madrid'].idxmax()].Municipio
close = df.sort_values(by=['dist_Madrid'])[1:2].Municipio.values[0]

print("El municipio más cercano a Madrid es {0}, el más lejano es {1}".format(close, far))


# 7) ¿Cuántos Municipios hay en un radio de 5 grados de la ciudad de Barcelona?

# In[12]:


# Defino las coordenadas de Barcelona
x_barcelona = df[df.Municipio == 'Barcelona'].X.values
y_barcelona = df[df.Municipio == 'Barcelona'].Y.values

# Anado la columna 'dist_barcelona', con las distancia euclideas de 
# los municipios con respecto a Barcelona
df['dist_Barcelona'] = (df.X - x_barcelona)**2 + (df.Y - y_barcelona)**2

# Cross-check: quiero que la distancia de Barcelona con Barcelona sea 0
df[df.Municipio == 'Barcelona']


# In[13]:


# Ahora los resultados
len(df[df['dist_Barcelona'] < 5])


# 8) Obtenga la media, mediana, desviación estándar, valor máximo y valor mínimo de la población de los municipios de la provincia de Cantabria.

# In[14]:


pobl_cantabria = df[df.Provincia == "Cantabria"].Poblacion

print("Población en Cantabria:")

print("Valor medio: %2d" %(pobl_cantabria.mean()))
print("Mediana: %2d" %(pobl_cantabria.median()))
print("Desviación típica: %2d" %(pobl_cantabria.std()))

print("Valor máximo: %2d" %(pobl_cantabria.max()))
print("Valor mínimo: %2d" %(pobl_cantabria.min()))


# 9) Usando los métodos de agregación, calcular las poblaciones de cada provincia.

# In[15]:


df.groupby('Provincia').Poblacion.sum()


# 10) Dibujar el valor de la población para las diferentes ciudades (usar las funciones vistas en MatPlotLib).

# In[16]:


import matplotlib.pyplot as plt

df.plot.scatter(x='X', 
        y='Y', 
        c = 'Poblacion',
        colormap='YlOrRd',
        s = 5)


# 11) Hacer un gráfico equivalente pero para las diferentes provincias. Seleccionar un punto representativo de las ciudades incluidas en cada provincia.

# In[17]:


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


# ## Series temporales

# In[54]:


# Leo el dataset en formato csv

df_prec = pd.read_csv('precip.csv', sep=', ')
df_prec.head()


# In[55]:


# Leo el dataset en formato stn

df_stn = pd.read_csv('precip.stn', sep=', ')
df_stn.head()


# 1) Obtener y exportar en csv los datos asociados a las series mensuales, estacionales y anuales

# In[56]:


# Converto la primera columna a formato datetime
df_prec['YYYYMMDD']=pd.to_datetime(df_prec['YYYYMMDD'].astype(str), format='%Y-%m-%d')

# Creo las columnas año, mes y estación
df_prec['year'] = pd.DatetimeIndex(df_prec['YYYYMMDD']).year
df_prec['month'] = pd.DatetimeIndex(df_prec['YYYYMMDD']).month
# https://stackoverflow.com/questions/44124436/python-datetime-to-season/44124490
df_prec['season'] = ((pd.DatetimeIndex(df_prec['YYYYMMDD']).month) % 12 + 3) // 3

df_prec.head()


# In[57]:


# Creo un multi-indice 
index = pd.MultiIndex.from_frame(df_prec[['year', 'season', 'month']], names=['year', 'season', 'month'])

df_prec.set_index(index, inplace = True)

df_prec.drop(columns=['YYYYMMDD', 'year', 'season', 'month'], inplace = True)
df_prec


# In[58]:


# Quiero la media de la precipitaciones cuando voy a agrupar

# Agrupo por año
df_prec.groupby('year').mean().to_csv('prec_year.csv')
df_year = pd.read_csv('prec_year.csv', index_col = 'year')
df_year.head()


# In[59]:


# Agrupo por mes
df_prec.groupby('month').mean().to_csv('prec_month.csv')
df_month = pd.read_csv('prec_month.csv', index_col = 'month')
df_month.head()


# In[60]:


# Agrupo por estación
df_prec.groupby('season').mean().to_csv('prec_season.csv')
df_season = pd.read_csv('prec_season.csv', index_col = 'season')
df_season.head()


# 2) Dibujar la serie temporal asociada al promedio espacial de los datos mensuales, estacionales y anuales.

# In[61]:


# Por cada año (mes, estación) hago el promedio de todas las filas y lo dibujo

# Por año
frame = {'year': df_year.mean(axis=1).index, 'value': df_year.mean(axis=1).values }   
df_plot = pd.DataFrame(frame) 
my_plot = df_plot.plot.scatter(x='year', y = 'value')
my_plot.set_ylim([0,3.5])


# In[62]:


# Por estación
frame = {'season': df_season.mean(axis=1).index, 'value': df_season.mean(axis=1).values }   
df_plot = pd.DataFrame(frame) 
my_plot = df_plot.plot.scatter(x='season', y = 'value')
my_plot.set_ylim([0,3.5])


# In[63]:


# Por mes
frame = {'month': df_month.mean(axis=1).index, 'value': df_month.mean(axis=1).values }   
df_plot = pd.DataFrame(frame) 
my_plot = df_plot.plot.scatter(x='month', y = 'value')
my_plot.set_ylim([0,3.5])


# 3) Dibujar la distribución espacial de las estaciones, así como los valores promedio y máximo.

# In[64]:


# Hago un merge del data-frame de precipitaciones
# y del data-frame de estaciones

# Como primera cosa, preparo el data-frame de precipitaciones,
# poniendo el ID de las estaciones como columna
df_prec_2 = pd.read_csv('precip.csv')
df_prec_t = df_prec_2.T

headers = df_prec_t.iloc[0]
df_prec_t2  = pd.DataFrame(df_prec_t.values[1:], columns=headers)
df_prec_t2['station_id'] = pd.to_numeric(df_prec_t.index[1:])
#df_stn['station_id'].values#.astype(float) 

# Ahora puedo hacer el merge
df_merge = pd.merge(df_prec_t2, df_stn, on='station_id')


# In[67]:


# Transformo las columnas con los valores de precipitaciones
# a float (aparecen como objetos)
df_merge.iloc[:,0:-7] = df_merge.iloc[:,0:-7].astype(float) 


# In[68]:


# añado las columnas mean y max
df_stn['mean'] = df_merge.iloc[:,0:-7].mean(axis=1).values
df_stn['max'] = df_merge.iloc[:,0:-7].max(axis=1).values


# In[69]:


df_stn


# In[72]:


# Ahora puedo hacer el plot (mean)
df_stn.plot.scatter(x='longitude', 
        y='latitude', 
        c = 'mean',
        colormap='YlOrRd',
        s = 5)


# In[71]:


# Ahora puedo hacer el plot (max)
df_stn.plot.scatter(x='longitude', 
        y='latitude', 
        c = 'max',
        colormap='YlOrRd',
        s = 5)


# 4) Calcular la frecuencia de días con precipitaciones mayores (>) de 1 mm.

# In[119]:


# Cuento cuantas entradas del data-frame (por cada linea)
# tienen un valor superior a 0.1
df_stn['rainy_days'] = df_merge.iloc[:,0:-7][df_merge.iloc[:,0:-7] > 0.1].count(axis = 1).values

n_obs = len(df_merge.iloc[:,0:-7].columns)
df_stn['rain_freq'] = df_stn['rainy_days'] / n_obs


# In[120]:


# Añado el plot
df_stn.plot.scatter(x='longitude', 
        y='latitude', 
        c = 'rain',
        colormap='YlOrRd',
        s = 5)

