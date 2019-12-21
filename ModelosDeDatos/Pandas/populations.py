#!/usr/bin/env python
# coding: utf-8

# # Populations

# In[91]:


import pandas as pd
import numpy as np

df = pd.read_csv('populations.txt',
                 sep='\t',
                 names=['year', 'hare', 'lynx', 'carrot'],
                 index_col='year',
                 skiprows=1)
df.head()


# ## The mean and std of the populations of each species for the years in the period

# In[64]:


df.mean(axis=0)


# In[65]:


df.apply(np.mean)


# In[66]:


df.std(axis=0)


# In[69]:


# numpy uses by default the biased definition of variance
df.apply(np.std, ddof=1)


# ## Which year each species had the largest population

# In[78]:


df.idxmax(axis = 0)


# In[75]:


df.apply(np.argmax)


# ## Which species has the largest population for each year. (Hint: rank and idxmin)

# In[77]:


df.idxmax(axis = 1)


# ## Which years any of the populations is above 50000. (Hint: any)

# In[79]:


df[df > 50000].dropna(how='all').index


# ## The top 2 years for each species when they had the lowest populations. (Hint: rank)

# In[92]:


df.apply(lambda x: x.rank().nsmallest(2).index)


# ## Compare (plot) the change in hare population (see help(np.gradient)) and the number of lynxes. Check correlation (see help(df.corr))

# In[9]:


import numpy as np
import matplotlib as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[10]:


df['hare_gradient'] = np.gradient(df['hare'])

df['lynx'].plot()
df['hare_gradient'].plot()


# In[11]:


df_corr = df[['lynx','hare_gradient']]
df_corr.corr()

