# Llamo las librerias
# Cargo las librerias necesarias
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


# Cargo el dataset
uso_bici = pd.read_csv("bici_pc.csv",
                       sep = ';',
                       skiprows = 4)

# Cambio de nombre a la columna que no se entiende
uso_bici['Comunidad'] = uso_bici['Unnamed: 0']

# Elimino las columnas que no voy a usar
uso_bici = uso_bici.drop(uso_bici.columns[[0,-2]], axis=1)

# Imprimo el dataset
uso_bici.head()

# Hago un plot
fig = uso_bici.groupby('Comunidad')['Falta de una red completa de carriles bici'].mean().plot(kind='bar',
    title = 'Falta de una red completa de carriles bici')

plt.axhline(y=uso_bici.loc[0,'Falta de una red completa de carriles bici'], color='r', linestyle='-')

# Lo guardo
fig.get_figure().savefig('test_plot.pdf')
