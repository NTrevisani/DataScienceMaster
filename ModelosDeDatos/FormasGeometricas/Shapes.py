import math

PI = math.pi

class Shape(object):
    """Basic class for the managing of geometric shapes."""    
    
    def __str__(self):
        """Print the object as 'An object with attributes '...''.
        
        The actual implementation depends on the object
        and on the number of attributes it has.
        """
        raise NotImplementedError
        
    def __repr__(self):
        raise NotImplementedError        
    
    def perimeter(self):
        raise NotImplementedError

    def area(self):
        raise NotImplementedError

    def __sum__(self, other):
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        return self.area() ==  other.area()  

    def __radd__(self, other):
        return self.__add__(other)

    
class Circle(Shape):
    """A circle of radius 'radius'"""
    
    def __init__(self, radius):
        """Initialize the circle with its radius.
        
        The value must be positive.
        """
        if radius <= 0:
            raise ValueError("Radius must have a positive value")
        else:
            self.radius = radius
                     
    def __str__(self):
        """Print as 'A Circle with radius 'radius''."""
        my_class = type(self).__name__
        msg = "A {0} with radius {1}"
        return msg.format(my_class, self.radius)
    
    def __repr__(self):
        """Represents the object as 'Circle(radius)'."""
        my_class = type(self).__name__
        msg = "{0}({1})"
        return msg.format(my_class, self.radius)
    
    def __add__(self, other):
        """Sum of two Circles or of a Circle and a number.
        
        The sum of two Circles returns a third Circle with
        radius equal to the sum of the radii of the two 
        Circles to be summed.
        The sum of a Circle and a number returns a new Circle
        with radius equal to the radius of the Circle plus
        the number.
        """
        if isinstance(other, int) or isinstance(other, float):
            int_circle = type(self)(other)
            return type(self)(self.radius + int_circle.radius)
        else:
            return type(self)(self.radius + other.radius)

    def perimeter(self):
        """Returns the perimeter of the circle."""
        return self.radius * 2 * PI
    
    def area(self):
        """Returns the are of the circle."""
        return self.radius** 2 * PI
    

class Rectangle(Shape):
    """A rectangle with a base and a height."""
    def __init__(self, base, height):
        if base <= 0:
            raise ValueError("Base must have a positive value")
        else:
            self.base = base            
        if height < 0:
            raise ValueError("Height must have a positive value")
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