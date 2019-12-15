#!/usr/bin/env python
# coding: utf-8

# # Populations

# In[51]:


import pandas as pd
import numpy as np

df = pd.read_csv('populations.txt',
                 sep='\t',
                 names=['year', 'hare', 'lynx', 'carrot'],
                 index_col='year',
                 skiprows=1)
df.head()


# ## The mean and std of the populations of each species for the years in the period

# In[6]:


means = df.apply(np.mean)
means


# In[7]:


st_dev = df.apply(np.std)
st_dev


# ## Which year each species had the largest population

# In[8]:


max_years = df.apply(np.argmax)
max_years


# ## Which species has the largest population for each year. (Hint: rank and idxmin)

# In[9]:


max_species = df.idxmax(axis=1)
max_species


# ## Which years any of the populations is above 50000. (Hint: any)

# In[19]:


large_years = df[df > 50000].dropna(how='all').index
large_years


# ## The top 2 years for each species when they had the lowest populations. (Hint: rank)

# In[76]:


df.apply(lambda x: x.rank()).idxmin()


# In[72]:


df.apply(lambda x: pd.Series(x.nsmallest(2).index))


# ## Compare (plot) the change in hare population (see help(np.gradient)) and the number of lynxes. Check correlation (see help(df.corr))

# In[71]:


import numpy as np
import matplotlib as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[99]:


df['hare_gradient'] = np.gradient(df['hare'])

df['lynx'].plot()
df['hare_gradient'].plot()


# In[100]:


df.corr()

