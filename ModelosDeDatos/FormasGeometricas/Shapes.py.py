#!/usr/bin/env python
# coding: utf-8

# In[214]:


import math

PI = math.pi

class Shape(object):
    
    def __str__(self):
        raise NotImplementedError
        
    def __repr__(self):
        raise NotImplementedError        
    
    def perimeter(self):
        raise NotImplementedError

    def area(self):
        raise NotImplementedError

    def __eq__(self, other):
        return self.area() ==  other.area()  

    def __sum__(self, other):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __radd__(self, other):
        return self.__add__(other)

class Circle(Shape):
    
    def __init__(self, radius):
        if radius < 0:
            print("You inserted a negative value for the radius.")
            print("I changed it for a positive value :)")
            self.radius = abs(radius)
        #elif radius == 0:
        #    self.radius = 1
        else:
            self.radius = radius
                     
    def __str__(self):
        my_class = type(self).__name__
        msg = "A {0} with radius {1}"
        return msg.format(my_class, self.radius)
    
    def __repr__(self):
        my_class = type(self).__name__
        msg = "{0}({1})"
        return msg.format(my_class, self.radius)
    
    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            int_circle = type(self)(other)
            return type(self)(self.radius + int_circle.radius)
        else:
            return type(self)(self.radius + other.radius)

    def perimeter(self):
        return self.radius * 2 * PI
    
    def area(self):
        return self.radius** 2 * PI
    

class Rectangle(Shape):
    
    def __init__(self, base, height):
        if base < 0:
            print("You inserted a negative value for the base.")
            print("I changed it for a positive value :)")
            self.base = abs(base)
        #elif base == 0:
        #    self.base = 1
        else:
            self.base = base
        if height < 0:
            print("You inserted a negative value for the height.")
            print("I changed it for a positive value :)")
            self.height = abs(height)
        #elif height == 0:
        #    self.height = 1
        else:        
            self.height = height
        
    def __str__(self):
        my_class = type(self).__name__
        msg = "A {0} with base {1} and height {2}"
        return msg.format(my_class, self.base, self.height)
    
    def __repr__(self):
        my_class = type(self).__name__
        msg = "{0}({1},{2})"
        return msg.format(my_class, self.base, self.height)
        
    def perimeter(self):
        return 2 * (self.base + self.height)
    
    def area(self):
        return self.base * self.height


# In[215]:


a = Circle(-4)

print(a.perimeter())
print(a.area())
print(a)


# In[216]:


print(a)


# In[217]:


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


# In[142]:


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


# In[ ]:




