#!/usr/bin/env python
# coding: utf-8

# # Métodos kernel escalables

# ### 1. Carga los datos usando la función "fetch_openml".

# In[1]:


import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml

house = fetch_openml(name='house_16H')# , version=4)


# ### 2. Preprocesa los datos y realiza alguna visualización.

# In[2]:


df = pd.DataFrame(data = house.data,    # values
                  columns = house.feature_names)  # 1st row as the column names

df['price'] = house.target

df.head()


# In[3]:


# load Plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go

# initiate the Plotly Notebook mode
init_notebook_mode(connected=True)


# In[4]:


# define a function for 3D plotting using Plotly
def plot_3D(X, y):
    
    trace0 = go.Scatter3d(x = X.iloc[:,0], 
                          y = X.iloc[:,1], 
                          z = y,
                          mode = 'markers',
                          marker = dict(size=6, color='blue', opacity=0.8)
    )

    # set aspect ratio
    scene = dict(aspectmode="manual", aspectratio=dict(x = 1, y = 1, z = 1))

    # define figure properties
    layout = go.Layout(
        scene = scene,
        height = 600,
        width = 900
    )

    # produce the plot
    fig = go.Figure(data = trace0,
                    layout = layout)
    iplot(fig)


# In[5]:


# plot the data in 3D

nEvents = 500
if nEvents > df.shape[0]: 
    nEvents = df.shape[0]

Phi = df.iloc[0:nEvents,[2,6]]

y = df.iloc[0:nEvents, -1]

plot_3D(Phi,y)


# ### 3. Separa los datos en train (2/3) y test (1/3).

# In[6]:


from sklearn.model_selection import train_test_split

# test sample gets 1/3 of the total events
test_size = 1/3

# Split between train and test
X_train, X_test, y_train, y_test = train_test_split(
    df.iloc[:,0:-1], df.iloc[:,-1], test_size=test_size, random_state=0)


# In[8]:


X_train.head()


# ### 4. Entrena un regresor lineal para predecir la variable target (el precio) a partir de las 16 características de entrada. Calcula el Mean Absolute Error (MAE) sobre el conjunto de test. Debería ser alrededor de 25000 EUR.

# In[9]:


from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model
regr.fit(X_train, y_train)

# Obtain predictions corresponding to X_test
y_pred = regr.predict(X_test)

# Compute the Mean Absolute Error
MAE = mean_absolute_error(y_test, y_pred)
print(MAE)


# ### 5. Ahora entrena el método kernel ridge regression usando la aproximación Nyström o RFF y reporta su MAE sobre el conjunto de test. 
# 
# ### Ojo: el regresor en este caso consiste en un Pipeline que contiene la aproximación seguida por una regresión Ridge (lineal); No contiene el método KernelRidge explícitamente. Para encontrar parámetros adecuados puedes usar el método GridSearchCV.

# In[22]:


from sklearn.kernel_approximation import Nystroem
from sklearn import pipeline
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression

# create a pipeline from kernel approximation and linear svm (Nyström)
feature_map_nystroem = Nystroem(random_state=0) #gamma=gamma, n_components=n_components, random_state=0)
nystroem_approx_krr = pipeline.Pipeline([("feature_map", feature_map_nystroem),
                                         ("ridge", LinearRegression())])

print(nystroem_approx_krr.get_params().keys())
print("-------------------------------------")
print("")

# Define the grid
param_grid = {'feature_map__gamma': [0.00001, 0.0001, 0.0005, 0.001, 0.005, 0.01],
              'feature_map__n_components': [10, 20, 50, 100, 500, 1000],}


# Get the best parameters and train the model
grid = GridSearchCV(nystroem_approx_krr, param_grid, cv = 3)
grid.fit(X_train, y_train)
nystroem_approx_krr = grid.best_estimator_
print(grid.best_params_)
print("-------------------------------------")
print("")

# Obtain predictions corresponding to X_test
y_pred = nystroem_approx_krr.predict(X_test)

# Compute the Mean Absolute Error
MAE = mean_absolute_error(y_test, y_pred)
print(MAE)

