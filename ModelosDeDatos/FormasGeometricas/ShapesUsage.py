#!/usr/bin/env python
# coding: utf-8

# # Object-oriented programming exercise

# ## Importing the Shape module

# In[92]:


from Shapes import Shape, Point, Circle, Rectangle, Triangle


# In[93]:


get_ipython().run_line_magic('run', 'Shapes.py')


# ## Module structure

# The _Shapes_ module contains 5 classes, each one defining one geometric object:
# - Shape: all the other classes inherit from it;
# - Point: a point defined by its (x,y) coordinates. Directly inherits from Shape and all the 2D-object classes inherit from Point. The point is considered as the center of those objects;
# - Circle, Rectangle, Triangle: the actual geometric shapes.

# The *mother* class, Shape, is almost exclusively used as a support for the other classes that inherit from it. There, all the methods (e.g. area, perimeter, ...) raise a NotImplementedError, to force the _children_ classes to explicitly define them, with few exceptions:
# - area comparison methods: 
#     - \_\_eq_\_ ( == )
#     - \_\_ne_\_ ( != )
#     - \_\_lt_\_ ( < ) 
#     - \_\_gt_\_ ( > )
#     - \_\_le_\_ ( <= )
#     - \_\_ge_\_ ( >= )
# - reverse operations (only the commutative ones):
#     - \_\_radd_\_ (reverse sum)
#     - \_\_rmul_\_ (reverse product)

# The area comparison methods have to be defined in the mother class, since areas can be compared among different shapes.
# They just call the actual implementation of the area() method in the children classes and compare the output.

# The *reverse operation* methods, on the other hand, can be considered as special cases: \_\_radd_\_ and \_\_rmul_\_ allow to change the order of the operands and are particularly useful in the cases (float + shape) or (float x shape).
# 
# In fact, if such methods were not implemented, the operation would return an error, even if the sum (shape + float) is correctly defined. Thanks to them, it is possible to change the order of the objects to be summed, so that (float + shape), which is not defined, becomes (shape + float), that the code can handle if  \_\_add_\_ is defined.
# 
# A caveat regarding these methods is that they are not aware if an operation is commutative or not, so they just change the order of the operands: we have to be careful that it is not the same to do (float - shape) or (shape - float).
# 
# To face this feature of reverse operations, \_\_rsub_\_ and \_\_rtruedivide_\_ have been specifically defined in each class, in order to correctly operate on the attributes (e.g., radius of the circle, sides of the triangle, ...) of the figures.

# ## What about putting all the methods in the mother class?

# Probably, it would have been possible to define all the methods of all the classes in the mother class Shape, through a series of *if*, *elif*, and *else* that change the behaviour of the method depending on the geometric shape to operate on, but this would have made the module incompatible with the addition of a new shape just by plugging-in an independently developed piece of code.
# 
# Another possibility would have been to pass the attributes of the geometric shape (e.g. the radius of a circle) as a list: this would have allowed to directly operate all the arithmentic operations on the list of attributes.
# This means that the sum of two circles or the sum of two triangles would have been the same strcure, *code wise*:

# For example, this definition of sum would have been valid for all the classes:
# 
#     def __add__(self, other):
#         if isinstance(other, (int,float)):
#             sum_x, sum_y = Point.half_way(self, self)
#             sum_attributes = self._attributes_list + other
#         elif (isinstance(other, type(self))):
#             sum_x, sum_y = Point.half_way(self, other)
#             sum_attributes = self._attributes_list + other._attributes_list
#         else:
#             self_class = type(self).__name__
#             other_class = type(other).__name__
#             msg = "You cannot sum a {0} and a {1}"
#             raise TypeError(msg.format(self_class, other_class))
#         return type(self)(sum_x, sum_y, sum_radius)

# Two inconvenients are implicit in this approach:
# - the center of the figure (if defined) has to be treated differently with respect to the other attributes;
# - to exploit this feature, also the *children* classes have to be defined in the same way, which may not be completely intuitive.

# ## Instantiating objects

# Let's now instantiate pairs of basic objects, to show how they work.
# - Point: this class directly inherits from Shape and is used to represent the _center_ of the other geometric figures;
# - Circle, Rectangle, and Triangle: inherit from Point and are the actual two-dimensional shapes we want.
# 

# In[85]:


# Two points

p1 = Point(0,0)
print(p1)
print(repr(p1))
print()

p2 = Point(10,10)
print(p2)
print(repr(p2))


# In[91]:


# Two circles

c1 = Circle(0,0,10)
print(c1)
print(repr(c1))
print()

c2 = Circle(-4,2,8)
print(c2)
print(repr(c2))


# In[88]:


# Two triangles

t1 = Triangle(0,0,6,8,10)
print(t1)
print(repr(t1))
print()

t2 = Triangle(5,7,3,4,5)
print(t2)
print(repr(t2))


# In[79]:


# Two rectangles

r1 = Rectangle(0,0,10,10)
print(r1)
print(repr(r1))
print()

r2 = Rectangle(5,11,4,6)
print(r2)
print(repr(r2))


# ## Repr and str

# In the previous examples, together with the definition of the geometric shapes, their _printable_ version and their representations have been shown.
# 
# In particular,  \_\_str_\_ has been implemented in order to return a human-readable description of the object (e.g. 'A Rectangle centered at (0,0) with base 12 and height 10'), while \_\_repr_\_ gives a more formal output ('Rectangle(0,0,12,10)'), the same used in the code to define the object itself.

# ## Some operations between points

# The basic methods implemented for points and inherited by the other figures are:
# - move_along_x: moves the point along x;
# - move_along_y: moves the point along y;
# - set_x: sets the x value of the point to a new value;
# - set_y: sets the y value of the point to a new value;
# - move_to: moves the point to a new pair of coordinates;
# - half_way: returns the x and the y (as two separate numbers, not as Point) of the middle point between two Point objects;
# - distance: returns the distance between two points;
# - get_center: returns the coordinates of the point;
# - get_x: returns the x coordinate of the point;
# - get_y: returns the y coordinate of the point.

# In[7]:


print(p1)
p1.move_along_x(10)
print(p1)


# In[8]:


print(p2)
p2.move_along_y(10)
print(p2)


# In[9]:


print(p1)
p1.set_x(15)
print(p1)
print("x:",p1.get_x())


# In[10]:


print(p2)
p2.set_y(12)
print(p2)
print("y:",p2.get_y())


# In[11]:


p1.move_to(0,0)
p2.move_to(10,10)
print(p1)
print(p2)


# In[12]:


mid_x,mid_y = p1.half_way(p2) 
print(mid_x,mid_y)


# In[13]:


print(p1.distance(p2))


# The methods work also for the classes that inherit from Point:

# In[14]:


print(c1)
c1.move_along_x(10)
print(c1)


# In[15]:


print(t2)
t2.move_along_y(10)
print(t2)


# In[16]:


c1.move_to(0,0)
t2.move_to(-4,2)
print(c1)
print(c2)


# In[17]:


mid_x,mid_y = r1.half_way(c2) 
print(mid_x,mid_y)


# In[18]:


print(c1.distance(t2))


# In[19]:


print(t2.get_center())


# ## Operations between geometric shapes

# Operation between geometric shapes are implemented as requested:
# - the sum of two objects of the same class returns a new object with the parameters (e.g. radius in the case of a circle, base and height for a rectangle, ...) summed one by one. In addition, the center of the new object is the middle point between the centers of the two objects;
# - the sum of an object with a number returns a new object with the parameters equal to the parameters of the original object, plus the number. In this case, the center of the new object is the same as the original object;
# - the difference, product, and division between two objects or between an object and a number work similarly;
# - the same is true for the power of an objet elevated to a number;
# - the power of an object elevated to another object is not accepted.

# <span style="color:red">Important</span>: it is not possible to operate on objects of different classes.

# ### Some examples

# In[20]:


print(c1)
print(c2)
c3 = c1 + c2
print(c3)


# In[21]:


print(r1)
r3 = r1 + 7
print(r3)


# In[22]:


print(t1)
print(t2)
t3 = t1 - t2
print(t3)


# In[23]:


print(c1)
c4 = c1 - 4
print(c4)


# In[24]:


print(r2)
r4 = 15 - r2
print(r4)


# In[25]:


print(t1)
print(t2)
t4 = t1 * t2
print(t4)


# In[26]:


print(c1)
c5 = 20 / c1
print(c5)


# In[53]:


print(r1)
r5 = r1 / 2
print(r5)


# In[56]:


print(t1)
t5 = t1 ** 2
print(t5)


# ### Some exceptions
# 

# Some exceptions have been implemented to guide the user in case some object are wrongly istantiated or some operations give a non-geometric result:
# - A _ValueError_ is raised if the object is created with negative values for some attributes (radius, length of a side, ...);
# - A *TypeError* is raised if we try to operate on two objects of different classes or when we try to elevate an object to another object;
# - A _ValueError_ is issued also when the result of an operation gives a non-geometric result, namely if some of the attributes in the resulting object are negative;
# - In the specific case of triangles, a *ValueError* is produced if one of the sides is larger than the sum of the other two.
# 

# In[28]:


err1 = Circle(0,0,-4)


# In[ ]:


err2 = Rectangle(4,-12,8,-1)


# In[ ]:


err3 = Triangle(-8,-2,-1,4,10)


# In[ ]:


err4 = Triangle(1,2,3,4,15)


# In[ ]:


err5 = c1 + r1


# In[ ]:


err6 = c1 - 20


# In[ ]:


err7 = 1 - r2


# ## Objects attributes

# The methods area() and perimeter() allow to get the corresponding attributes of a figure.

# In[ ]:


print(c1)
print("c1 area is",c1.area())
print("c1 perimeter is",c1.perimeter())


# In[ ]:


print(r1)
print("r1 area is",r1.area())
print("r1 perimeter is",r1.perimeter())


# In[ ]:


print(t1)
print("t1 area is",t1.area())
print("t1 perimeter is",t1.perimeter())


# The areas can be compared directly using the corresponding methods.

# In[ ]:


print(r1.area())
print(t1.area())
print()

print(r1 == t1)
print(r1 != t1)
print(r1 > t1)
print(r1 < t1)
print(r1 >= t1)
print(r1 <= t1)


# The areas can also be directly compared with numbers.

# In[ ]:


print(r1.area())
print()

print(r1 == 120)
print(r1 != 120)
print()

print(r1 <= 120)
print(r1 >= 120)
print()

print(r1 <= 500)
print(r1 >= 500)
print()

print(500 < r1)
print(120 == r1)


# Additionally, specific methods give access to all the attributes of a figure:
# - Circle: 
#     - get_radius; 
#     - set_radius;
# - Rectangle: 
#     - get_base;
#     - get_height;
#     - set_base;
#     - set_height;
# - Triangle:
#     - get_side1;
#     - get_side2;
#     - get_side3;
#     - set_side1;
#     - set_side2;
#     - set_side3.    

# In[ ]:


print(c1)
print()

print(c1.get_center())
print(c1.get_radius())

c1.move_to(2,4)
c1.set_radius(12)

print(c1)


# In[ ]:


print(r1)
print()

print(r1.get_center())
print(r1.get_base())
print(r1.get_height())

r1.move_to(2,4)
r1.set_base(12)
r1.set_height(20)

print(r1)


# In[ ]:


print(t1)
print()

print(t1.get_center())
print(t1.get_side1())
print(t1.get_side2())
print(t1.get_side3())

t1.move_to(2,4)
t1.set_side1(12)
t1.set_side2(20)
t1.set_side3(18)

print(t1)


# By defining such methods, I tried to avoid a direct access to the attributes of the figures, which are *private* variables.
# 
# This is particularly important for variables as the radius of a circle or the sides of a polygon, since they cannot assume negative values.
# 
# In fact, a protection against negative values for the radius, for example, is implemented in set_radius() as a ValueError, but is not present in case the radius is accessed directly.

# Trying to access the radius of a circle:

# In[61]:


c1.radius


# Now it works, but the fact that the name of the variable is \_base represents a warning: it should not be directly modified or used:

# In[62]:


c1._radius


# And in fact, if we do not pay too much attention:

# In[63]:


c1._radius = -12
c1.perimeter()

