#!/usr/bin/env python
# coding: utf-8

# # Métodos kernel para regresión

# ### 1. Escribe una función que descargue automáticamente el fichero de datos con medidas mensuales de la URL ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt y que lo convierta a un formato numérico (dataframe, numpy arrays, etc.).

# In[73]:


# Download the dataset (if the server responds)
import urllib.request

url = 'ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt'
my_file = urllib.request.urlretrieve(url, 'file.txt')


# ### 2. Obten las variables months y avg_ppmvs.

# In[74]:


# Read the dataset
import pandas as pd
import numpy as np

df = pd.read_csv("file.txt", 
               sep = "   ",
               header = 71)

df.columns = ['year', 'months', '---', '---', 'avg_ppmvs', '---', 'interpolated',  '---', 'trend', 'days', '---', '---', '---', '---']

df = df.drop('---', axis = 1)

df.head(5)


# ### 3. Comprueba si los datos coinciden con los datos usados en la práctica (devueltos por load_mauna_loa_atmospheric_co2()) para las fechas en que existen datos en ambos conjuntos.

# In[75]:


# Prepare the 'load_mauna_loa_atmospheric_co2()' function
from sklearn.datasets import fetch_openml
import matplotlib.pyplot as plt

# Original series
def load_mauna_loa_atmospheric_co2():
    ml_data = fetch_openml(data_id=41187, cache=False)
    months = []
    ppmv_sums = []
    counts = []

    y = ml_data.data[:, 0]
    m = ml_data.data[:, 1]
    month_float = y + (m - 1) / 12
    ppmvs = ml_data.target

    for month, ppmv in zip(month_float, ppmvs):
        if not months or month != months[-1]:
            months.append(month)
            ppmv_sums.append(ppmv)
            counts.append(1)
        else:
            # aggregate monthly sum to produce average
            ppmv_sums[-1] += ppmv
            counts[-1] += 1

    months = np.asarray(months).reshape(-1, 1)
    avg_ppmvs = np.asarray(ppmv_sums) / counts
    return months, avg_ppmvs

X, y = load_mauna_loa_atmospheric_co2()

# Illustration
fig = plt.figure(figsize=(15,8))
plt.scatter(X, y, c='k', zorder = 1)
plt.grid(True)
plt.xlabel("Year")
plt.ylabel(r"CO$_2$ in ppm")
plt.title(r"Atmospheric CO$_2$ concentration at Mauna Loa")
plt.tight_layout()


# Updated series (till today)

# Remove invalid values
df2 = df[df['avg_ppmvs'] > -9.99]

# The series starts on March 1958 (1/4 of year after 1958)
X2 = np.asarray(df2.index / 12 + 1958 + 0.25).reshape(-1, 1)
y2 = df2.avg_ppmvs

plt.scatter(X2, y2, c='k', marker = 'x', zorder = 2)
plt.grid(True)


# ### 4. Busca los mejores hiperparámetros del GP para predecir la serie temporal del CO2 usando datos hasta la fecha más reciente. Compara estos hiperparámetros con los que se encontraron al usar datos hasta diciembre de 2001 (los datos usados en la práctica).

# In[76]:


from sklearn.gaussian_process.kernels import RationalQuadratic
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, WhiteKernel, ExpSineSquared


from time import time

# Kernel with generic parameters
k1 = C(50, (1e1, 1e+3)) * RBF(50,(1e0,1e5))  # long term smooth rising trend
k2 = C(5, (1e1, 1e+2)) * RBF(100,(1e0,1e5))     * ExpSineSquared(length_scale=1.0, length_scale_bounds=(1e-1,1e1),
                     periodicity=1.0, periodicity_bounds="fixed")  # seasonal component
k3 = C(0.5, (1e-2, 1e1)) * RationalQuadratic(length_scale=1.0, length_scale_bounds=(1e-2,1e3),
                                alpha=1.0, alpha_bounds=(1e-1,1e3)) # medium term irregularities
k4 = C(0.1, (1e-3, 1e+1)) * RBF(0.1,(1e-2,1e2))     + WhiteKernel(noise_level=0.1**2,noise_level_bounds=(1e-4, 1e0)) # noise terms
kernel = k1 + k2 + k3 + k4

# Fit the Gaussian Process regressor, and optimize the hyperparameters
gp = GaussianProcessRegressor(kernel=kernel, alpha=0,
                              normalize_y=True, n_restarts_optimizer=1)
t0 = time()


# In[77]:


gp.fit(X2, y2)


# In[78]:


print("Elapsed time: %0.3fs"%(time() - t0))

print("\nLearned kernel: %s" % gp.kernel_)
print("Log-marginal-likelihood: %.3f"
      % gp.log_marginal_likelihood(gp.kernel_.theta))

X_ = np.linspace(X.min(), X.max() + 30, 1000)[:, np.newaxis]
y_pred, y_std = gp.predict(X_, return_std=True)


# ### 5. Haz una figura que muestre la serie temporal completa y una predicción de los próximos 20 años, incluso bandas de confianza.

# In[79]:


# Prepare the X_ for the next 20 years
X_ = np.linspace(X2.min(), X2.max() + 20, 1000)[:, np.newaxis]

# Predict on the new X_
y_pred, y_std = gp.predict(X_, return_std=True)

# plot the prediction
fig = plt.figure(figsize=(15,8))
plt.scatter(X2, y2, c='k')
plt.plot(X_, y_pred)
plt.fill_between(X_[:, 0], y_pred - y_std, y_pred + y_std,
                 alpha=0.5, color='k')
plt.xlim(X_.min(), X_.max())
plt.xlabel("Year")
plt.ylabel(r"CO$_2$ in ppm")
plt.title(r"Atmospheric CO$_2$ concentration at Mauna Loa")
plt.tight_layout()
plt.show()

