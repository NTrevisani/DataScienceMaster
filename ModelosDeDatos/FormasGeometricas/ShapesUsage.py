#!/usr/bin/env python
# coding: utf-8

# In[39]:


import importlib

importlib.reload(Shapes)

from Shapes import Shape, Point, Circle, Rectangle


# In[40]:


get_ipython().run_line_magic('run', 'Shapes.py')


# In[44]:


a = Circle(-4,2,5)

print(a)

print(a.perimeter())
print(a.area())

a.move_along_x(4)

print(a)

b = Circle (0,7,5)

a == b


# In[31]:


print(a)


# In[26]:


eval(repr(a))


# In[218]:


b = Circle(3)


# In[219]:


a == b


# In[220]:


print(a + b)


# In[221]:


a + 1.1


# In[224]:


1.1 + a


# In[222]:


c = Rectangle(1,28.274333882308138)


# In[223]:


a == c


# In[6]:


d = Rectangle(-2,-7)
d


# In[149]:


e = Rectangle(0,0)
e


# In[150]:


e.area()


# In[183]:


type(1)


# In[184]:


type(1.)


# In[25]:


get_ipython().run_line_magic('pinfo', 'Circle')


# In[26]:


help(Circle)


# In[ ]:




