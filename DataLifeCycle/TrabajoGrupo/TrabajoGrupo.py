#!/usr/bin/env python
# coding: utf-8

# # Proyecto de Ciclo de vida de los datos

# ### Preparado por:
# - Fernando
# - Eduardo
# - Cédric
# - Nicolò

# ## Introducción

# El proyecto se propone encontrar una ciudad en España donde reemplazar una carretera tradicional por un carril bici, teniendo en cuenta principalmente dos aspectos:
# - Las razones por las cuales los ciudadanos no suelen utilizar bicicleta para moverse, y selecionar una ciudad donde entre estas razones sean importantes:
#     - La falta de un carril bici;
#     - El excesivo tráfico.
# - El nivel de contaminación del aire en las distintas zonas de la ciudad, con la idea de quitar tráfico alimentado por combustibles fósiles y empujar el uso de la bicicleta.   

# ## Fuentes de datos

# Para recaudar datos, se han utilizado dos repositorios de datos en abierto de España:
# - El repositorio del Instituto Nacional de Estadistica (INE: https://www.ine.es/)
# - El repositorio datos.gob.es (https://datos.gob.es/)
# 
# En particular, los dataset analizados, se refieren a:
# - Porcentaje de personas de 16 y más años que usualmente no se desplazan caminando o en bicicleta, por comunidad autónoma de residencia y motivos por los que no lo hacen (https://www.ine.es/jaxi/tabla.do?type=pcaxis&path=/t25/p500/2008/p04/l0/&file=04017b.px), proporcionado directamente pr el Instituto Nacional de Estadistica en formato CSV [los decimales son definidos por commas: me descargué el CSV separado por punto-y-commas, y tranformé las commas en puntos <-- nota de curación];
# - Calidad del aire 2018 (https://datosabiertos.malaga.eu/recursos/ambiente/calidadaire/2018.json), proporcionado por el Ayuntamiento de Malaga en formato json y posteriormente tranformado a CSV [esto lo he hecho con un programa encontrado en internet <-- nota de curación].

# ## Analisis de los datos

# ### 1. Elección de la ciudad

# Para elegir la ciudad donde construir el carril bici, se ha inspeccionado un dataset que presenta las razones por las cuales ciudadanos de 16 años o mayores no utilizan habitualmente la bicicleta, agrupados por comunidad autonomia. Entre las diferentes razones, se han inspeccionado las que más parecen poderse resolver a través de la instalación de un carril bici y de una zona con tráfico limitado:
# - Falta de una red completa de carriles bici;
# - Demasiado tráfico;
# - Falta de instalaciones de aparcamiento de bicicletas;
# - Seguridad personal.
# 
# Como se puede observar, aunque Ceuta y Melilla sobresalga para *Falta de una red completa de carriles bici* y *Falta de instalaciones de aparcamiento de bicicletas*, el problema de tener demasiado tráfico y la seguridad personal no se ven como problemas fundamentales.
# 
# De la demás comunidades independientes, Andalucia está entre las que sistematicamente tienen un nivel de atención superior al promedio nacional para los criterios utilizados y, factor no trascurable para este trabajo, el Ayuntamiento de Malaga proprciona datos sobre calidad de aire.

# In[1]:


# Cargo las librerias necesarias
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


# In[2]:


# Cargo el dataset
uso_bici = pd.read_csv("bici_pc.csv",
                       sep = ';',
                       skiprows = 4)

# Cambio de nombre a la columna que no se entiende
uso_bici['Comunidad'] = uso_bici['Unnamed: 0']

# Elimino las columnas que no voy a usar
uso_bici = uso_bici.drop(uso_bici.columns[[0,-2]], axis=1)

# Imprimo el dataset
uso_bici


# In[12]:


uso_bici.groupby('Comunidad')['Falta de una red completa de carriles bici'].mean().plot(kind='bar',
    title = 'Falta de una red completa de carriles bici')

plt.axhline(y=uso_bici.loc[0,'Falta de una red completa de carriles bici'], color='r', linestyle='-')
plt.show()


# In[13]:


uso_bici.groupby('Comunidad')['Demasiado tráfico'].mean().plot(kind='bar',
    title = 'Demasiado tráfico')

plt.axhline(y=uso_bici.loc[0,'Demasiado tráfico'], color='r', linestyle='-')
plt.show()


# In[14]:


uso_bici.groupby('Comunidad')['Falta de instalaciones de aparcamiento de bicicletas'].mean().plot(kind='bar',
    title = 'Falta de instalaciones de aparcamiento de bicicletas')

plt.axhline(y=uso_bici.loc[0,'Falta de instalaciones de aparcamiento de bicicletas'], color='r', linestyle='-')
plt.show()


# In[15]:


uso_bici.groupby('Comunidad')['Seguridad personal'].mean().plot(kind='bar',
    title = 'Seguridad personal')

plt.axhline(y=uso_bici.loc[0,'Seguridad personal'], color='r', linestyle='-')
plt.show()


# ### 2. Elección del sitio donde construir el carril bici

# Para elegir el sitio donde instalar el carril bici, se ha considerado el nivel de calidad de aire en las distintas zonas de la ciudad de Malaga.
# 
# El dataset utilizado presenta dos tipos de datos, por cada una de las sustancias consideradas:
# - la cantidad, en diferentes unidades, de la sustancia;
# - un indicador cuálitativo asociado a la cantidad medida de dicha sustancia.
# 
# Por cada medida, se proporcionan además las coordenadas geografica, de manera que se puede reconstruir un 'mapa' de Malaga donde aparecen las informaciones.
# 
# Observando los datos, nos damos cuenta de que es complicado utilizar las cantidades numericas:
# - pueden tener ordenes de magnitud distintas
#     - no es trivial operar sobre ellas para sacar medias, etc;
#     - hay que conocer, por cada sustancia, los niveles considerado peligrosos.
# 
# Resulta mucho más sencillo operar con los datos categoricos, que ya collevan las informaciones normalizadas con respecto a los niveles recomendados, no obstante haya que hacer un pequeño trabajo de curación para que se puedan hacer analisis númericas. En particular, se asocia a cada valor calitativo, un número:
# - good = 4;
# - moderate = 3;
# - unhealthy-low = 2;
# - unhealthy = 1;
# - unhealthy-high = 0.
# 
# Sacando el promedio de esta 'nota' de calidad de aire por cada punto, se puede obtener un mapa de 'resumen': la zona ideal para poner un carril bici donde ahora está una carretera normal será la que tiene calidad de aire globalmente peor.

# In[7]:


# Cargo las librerias necesarias
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np    


# In[8]:


# Leo el dataset
calidad_aire = pd.read_csv("calidad_aire_2018.csv") 
    
# Miro las primeras lineas del dataset
calidad_aire.head()
#list(calidad_aire)

# Quito las columnas que no voy a usar 
calidad_aire = calidad_aire.drop(calidad_aire.columns[[0,1,2,3,4,5,6,7,8,11,18]], axis=1)

# Miro las primeras lineas del dataset 'limpio'
calidad_aire.head()


# In[9]:


# Lista de los nombres de las columnas del dataset (exluyo las coordenadas)
list(calidad_aire)[2:]


# In[10]:


# Miro cuales variables son 'object': son las variables categoricas ('good', 'moderate', ...)
# Separo el data-frame en dos:
# - uno solo con variables continuas
# - uno solo con variables categoricas

droplist = calidad_aire.dtypes != object
droplist[0:2] = False
droplist


# In[11]:


# Quito las variables categoricas: creo el data-frame de variables continuas
calidad_aire_num = calidad_aire.drop(calidad_aire.columns[calidad_aire.dtypes == object], axis=1)
calidad_aire_num.head()


# In[12]:


# Quito las variables continuas: creo el data-frame de variables categoricas

droplist = calidad_aire.dtypes != object
droplist[0:2] = False
droplist

calidad_aire_obj = calidad_aire.drop(calidad_aire.columns[droplist], axis=1)

calidad_aire_obj.head()


# In[13]:


# Pinto una variable numerica: BIEN

calidad_aire_num.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = 'properties/pm1',
            colormap='viridis',
            s = 5)


# In[14]:


# Hago una lista de las variables 
all_z_variables = list(calidad_aire)[3:]
print(all_z_variables)


# In[15]:


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


# In[16]:


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


# In[17]:


# Intento hacer un loop sobre todas las variables categoricas

#Crea el eje de la barra de color
bounds = np.linspace(0,7,7)
# Mapa de colores
cmap = mpl.colors.ListedColormap(color)

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
        c = color_variable, #calidad_aire['properties/pm1'], #'properties/pm1',
        s = 5)
    ax.title.set_text(var)
    # Situa la barra de color
    ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
    # Crea la barra de color
    cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
    spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
    # Define la posición de los ticks de la barra de color y las etiquetas a usar
    cb.set_ticks(cb.get_ticks()+0.589)
    cb.set_ticklabels(category)


# In[18]:


calidad_aire_obj.head()


# In[19]:


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


# In[46]:


# Añado una columna, que sea el promedio de las columnas, y la pinto

calidad_aire_obj_num['average_quality'] = calidad_aire_obj_num.iloc[:,2:].mean(1)

pl = calidad_aire_obj_num.plot.scatter(x = 'geometry/coordinates/0/4/0', 
            y = 'geometry/coordinates/0/4/1', 
            c = 'average_quality',
            colormap='viridis',
            title = calidad_aire_obj_num.average_quality.name,
            s = 5)

pl.get_figure().savefig('Calidad_aire_average.pdf')


# In[47]:


# Guardo el data-frame en un fichero CSV
calidad_aire_obj_num_save = calidad_aire_obj_num.iloc[:,[0,1,-1]]
calidad_aire_obj_num_save.to_csv("calidad_aire_obj_num_save.csv", index = False)


# In[48]:


# Cargo las imagenes de Malaga que voy a necesitar
img_mapa_urbano = plt.imread("malaga_Mapa_Urbano.png")
img_mapa_satelite = plt.imread("malaga_Mapa_Satelite.png")
img_mapa_relieve = plt.imread("malaga_Mapa_Relieve.png")


# In[50]:


# Miro los extremos de los ejes de mi mapa de calidad de aire
pl.axis()


# In[57]:


# Pinto mi mapa sobre los mapas de Malaga
fig, ax = plt.subplots(figsize=(13, 9))

d = ax.scatter(x = calidad_aire_obj_num['geometry/coordinates/0/4/0'], 
            y = calidad_aire_obj_num['geometry/coordinates/0/4/1'], 
            c = calidad_aire_obj_num['average_quality'],
            cmap='jet',
            s = 5,
            zorder=1)
ext = pl.axis()
ext2 = [-4.6, -4.30, 36.625, 36.837]
ax.imshow(img_mapa_urbano, extent=ext, zorder = 0)

fig.colorbar(d)

d.get_figure().savefig('Malaga_mapa_urbano.pdf')


# In[58]:


# Pinto mi mapa sobre los mapas de Malaga
fig, ax = plt.subplots(figsize=(13, 9))

d = ax.scatter(x = calidad_aire_obj_num['geometry/coordinates/0/4/0'], 
            y = calidad_aire_obj_num['geometry/coordinates/0/4/1'], 
            c = calidad_aire_obj_num['average_quality'],
            cmap='viridis',
            s = 5,
            zorder=1)
ext = pl.axis()
ext2 = [-4.6, -4.30, 36.625, 36.837]
ax.imshow(img_mapa_satelite, extent=ext, zorder = 0)

fig.colorbar(d)

d.get_figure().savefig('Malaga_mapa_satelite.pdf')


# In[56]:


# Pinto mi mapa sobre los mapas de Malaga
fig, ax = plt.subplots(figsize=(13, 9))

d = ax.scatter(x = calidad_aire_obj_num['geometry/coordinates/0/4/0'], 
            y = calidad_aire_obj_num['geometry/coordinates/0/4/1'], 
            c = calidad_aire_obj_num['average_quality'],
            cmap='jet',
            s = 5,
            zorder=1)
ext = pl.axis()
ext2 = [-4.6, -4.30, 36.625, 36.837]
ax.imshow(img_mapa_relieve, extent=ext, zorder = 0)

fig.colorbar(d)

d.get_figure().savefig('Malaga_mapa_relieve.pdf')

