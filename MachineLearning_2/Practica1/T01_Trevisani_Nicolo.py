#!/usr/bin/env python
# coding: utf-8

# # Métodos kernel para clasificación

# ### 1. Elige un conjunto de datos para clasificación binaria.

# I am going to consider the dataset "Rain in Australia", which aims to predict wether the next day it will rain or not, based on some atmospheric measurements:
# 
# https://www.kaggle.com/jsphyg/weather-dataset-rattle-package/data

# In[1]:


# Import basic libraries
import numpy  as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
my_file = "weatherAUS.csv"
rain = pd.read_csv(my_file)


# In[2]:


# Look at the available variables
for var in rain.columns:
    print(var)


# In[3]:


# Transform the discrete variable from 'yes/no' to '1/0'
rain.RainTomorrow[rain.RainTomorrow == 'No'] = 0
rain.RainTomorrow[rain.RainTomorrow == 'Yes'] = 1

# Now, convert it into float
rain.RainTomorrow = rain.RainTomorrow.astype(float)
rain.dtypes


# In[4]:


rain.head()


# In[5]:


# Many cities are available: maybe we can focus on just one of them
print(set(rain.Location))

brisbane = rain[rain.Location == "Brisbane"]
brisbane.head()


# In[6]:


# Evaporation and Sunshine are empty: let's remove them
# I shall remove also categorical variables, like the wind direction
# I know the location, so I can remove it, and I am not interested in the date
droplist = ["Evaporation", "Sunshine", "WindGustDir", "WindDir9am", "WindDir3pm", "Location", "Date", "RainToday", "RISK_MM"]
brisbane_slim = brisbane.drop(droplist, axis = 1)

brisbane_slim.dropna(how='any', inplace = True)
len(brisbane_slim)


# In[7]:


# Check the correlation among variables,
# to see if it is possible to remove some of them
# (https://stackoverflow.com/questions/29432629/plot-correlation-matrix-using-pandas)

f = plt.figure(figsize=(19, 15))
plt.matshow(brisbane_slim.corr(), fignum=f.number)
plt.xticks(range(brisbane_slim.shape[1] - 1), brisbane_slim.columns, fontsize=14, rotation=45)
plt.yticks(range(brisbane_slim.shape[1] - 1), brisbane_slim.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)


# In[8]:


# The correlation is high between some of the variables:
# MinTemp - Temp9am
# MaxTemp - Temp3pm
# Pressure9am - Pressure3pm

droplist2 = ["Temp9am", "Temp3pm", "Pressure3pm", "Cloud9am", "Cloud3pm"]
brisbane_slim = brisbane_slim.drop(droplist2, axis = 1)


# In[9]:


# Check again the correlation
f = plt.figure(figsize=(19, 15))
plt.matshow(brisbane_slim.corr(), fignum=f.number)
plt.xticks(range(brisbane_slim.shape[1] - 1), brisbane_slim.columns, fontsize=14, rotation=45)
plt.yticks(range(brisbane_slim.shape[1] - 1), brisbane_slim.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params(labelsize=14)


# In[10]:


brisbane_slim.head()


# ### 2. Visualiza (algunos de) los datos.

# In[11]:


# MinTemp vs Humidity3pm
plt.scatter(brisbane_slim.iloc[0:200, 0], 
            brisbane_slim.iloc[0:200, 7], 
            c=brisbane_slim.iloc[0:200, -1], 
            s=50, 
            cmap='bwr');


# In[12]:


# Plot all the variables pairs, one by one
import seaborn as sns
sns.pairplot(brisbane_slim, hue = 'RainTomorrow')


# ### 3. Separa los datos en un conjunto de training y otro de test.

# In[13]:


# To avoid large triaing time, I keep just 1000 events.
# Let's create the training and test subsets by taking this into account

from sklearn.model_selection import train_test_split

# I consider, in total, only 1000 events
brisbane_1000 = brisbane_slim[0:1000]

# test sample gets 20% of the total events (in this case, 200)
test_size = 0.2

# Split between train and test
X_train, X_test, y_train, y_test = train_test_split(
    brisbane_1000.iloc[:,0:-1], brisbane_1000.iloc[:,-1], test_size=test_size, random_state=0)


# ### 4. Entrena una SVM sobre los datos de training. Busca los parámetros óptimos usando GridSearchCV.

# In[14]:


from sklearn import datasets, svm
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

# Uso el kernel gaussiano
kernel = 'rbf'

# fit the model
clf = SVC(kernel='rbf')

clf.get_params().keys()


# In[21]:


from sklearn.model_selection import GridSearchCV
from time import time

# Full grid: it takes too much time
"""
param_grid = {'C': [1E2, 5E2, 1E3, 5E3, 1E4],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], 
              'kernel': ['linear', 'rbf', 'poly'],}
"""
# This looks as a better compromise between detail in the grid and time needed
param_grid = {'C': [1E1, 1E2, 5E2, 1E3, 5E3],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], 
              'kernel': ['rbf', 'linear'],}

t0 = time()

grid = GridSearchCV(SVC(), param_grid, cv=3)
grid.fit(X_train, y_train)
clf = grid.best_estimator_

print("Elapsed time: %0.3fs"%(time() - t0))
print("Best estimator found by grid search:")
print(grid.best_params_)


# ### 5. Prueba el clasificador sobre los datos de test y reporta el resultado.

# In[22]:


# Evaluate the prediction of the SVM
y_pred = clf.predict(X_test)


# In[23]:


# Print a summary of the performance
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))


# In[24]:


# Confusion matrix
from sklearn.metrics import confusion_matrix

print(confusion_matrix(y_test, y_pred))


# In[19]:


# Confusion matrix, but slightly nicer
from sklearn.metrics import confusion_matrix

# use seaborn plotting defaults
import seaborn as sns; sns.set()

mat = confusion_matrix(y_test, y_pred)
fig, ax = plt.subplots(figsize=(7,6))

sns.set(font_scale=1.3)
sns.heatmap(mat.T, square=False, annot=True, fmt='d', cbar=False,
            xticklabels=set(y_pred),
            yticklabels=set(y_pred),
            cmap=sns.cubehelix_palette(light=1, as_cmap=True))

