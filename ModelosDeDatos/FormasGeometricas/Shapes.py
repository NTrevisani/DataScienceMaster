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
        """Represent the object as 'Object(attributes)'''.
        
        The actual implementation depends on the object
        and on the number of attributes it has.
        """
        raise NotImplementedError        
    
    def perimeter(self):
        """Returns the perimeter of the object.

        The actual implementation depends on the object.
        """
        raise NotImplementedError

    def area(self):
        """Returns the area of the object.

        The actual implementation depends on the object.
        """
        raise NotImplementedError

    def __add__(self, other):
        raise NotImplementedError
        """Sum of two objects or of an object and a number.
        
        The sum of two objects returns a third object with
        each attribute equal to the sum of the corresponding
        attributes of the two objects summed.
        The sum of an object and a number returns a new object
        with each attribute equal to the attribute of the object 
        plus the number.
        """

    def __radd__(self, other):
        """Reverse sum of two objects or of an object and a number.
        """
        return self.__add__(other)

    def __eq__(self, other):
        """Returns True if two object has the same area."""
        return self.area() ==  other.area()  


class Point(Shape):
    """A point of coordinates (x,y)"""
    
    def __init__(self, x, y):
        """Initialize the circle with its coordinates."""
        self.x = x
        self.y = y
        
    def __str__(self):
        """Print as 'A Point with coordinates (x,y)'."""
        my_class = type(self).__name__
        msg = "A {0} with coordinates ({1},{2})"
        return msg.format(my_class, self.x, self.y)

    def __repr__(self):
        """Represents as 'Point(x,y)'."""
        my_class = type(self).__name__
        msg = "{0}({1},{2})"
        return msg.format(my_class, self.x, self.y)

    def move_along_x(self, x_shift):
        """Moves the point along x axis of the quantity 'x_shift'"""
        self.x += x_shift

    def move_along_y(self, y_shift):
        """Moves the point along y axis of the quantity 'y_shift'"""
        self.y += y_shift
        
    
class Circle(Point):
    """A circle of radius centered at ('x','y') with radius 'radius'"""
    
    def __init__(self, x, y, radius):
        """Initialize the circle with its radius.
        
        The value must be positive.
        """
        super().__init__(x,y)
        if radius <= 0:
            raise ValueError("Radius must have a positive value")
        else:
            self.radius = radius
                     
    def __str__(self):
        """Print as 'A Circle centered at (x,y) with radius 'radius''."""
        my_class = type(self).__name__
        msg = "A {0} centered at ({1},{2}) with radius {3}"
        return msg.format(my_class, self.x, self.y, self.radius)
    
    def __repr__(self):
        """Represents as 'Circle(x,y,radius)'."""
        my_class = type(self).__name__
        msg = "{0}({1},{2},{3})"
        return msg.format(my_class, self.x, self.y, self.radius)
    
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
        """Returns the area of the circle."""
        return self.radius** 2 * PI
    

class Rectangle(Point):
    """A rectangle centered at (x,y) with a base and a height."""
    def __init__(self, x, y, base, height):
        super().__init__(x,y)
        if base <= 0:
            raise ValueError("Base must have a positive value")
        else:
            self.base = base            
        if height < 0:
            raise ValueError("Height must have a positive value")
        else:        
            self.height = height
        
    def __str__(self):
        """Print as 'A Rectangle centered at (x,y) 
        with base 'base' and height ''height'."""
        my_class = type(self).__name__
        msg = "A {0} centered at ({1},{2}) with base {3} and height {4}"
        return msg.format(my_class, self.x, self.y, self.base, self.height)
    
    def __repr__(self):
        """Represents as 'Rectangle(x,y,base,height)'."""
        my_class = type(self).__name__
        msg = "{0}({1},{2},{3},{4})"
        return msg.format(my_class, self.x, self.y, self.base, self.height)
        
    def perimeter(self):
        """Returns the perimeter of the rectangle."""
        return 2 * (self.base + self.height)
    
    def area(self):
        """Returns the perimeter of the rectangle."""
        return self.base * self.height
    
    
class Triangle(Point):
    """A triangle centered at (x,y) with 3 sides side1, side2, side3."""
    def __init__(self, x, y, side1, side2, side3):
        super().__init__(x,y)
        if side1 <= 0 or side2 <= 0 or side 3 <= 0:
            raise ValueError("All the sides must have a positive value")
        else:
            self.side1 = side1
            self.side2 = side2
            self.side3 = side3
        
    def __str__(self):
        """Print as 'A Rectangle centered at (x,y) 
        with base 'base' and height ''height'."""
        my_class = type(self).__name__
        msg = "A {0} centered at ({1},{2}) with base {3} and height {4}"
        return msg.format(my_class, self.x, self.y, self.base, self.height)
    
    def __repr__(self):
        """Represents as 'Rectangle(x,y,base,height)'."""
        my_class = type(self).__name__
        msg = "{0}({1},{2},{3},{4})"
        return msg.format(my_class, self.x, self.y, self.base, self.height)
        
    def perimeter(self):
        """Returns the perimeter of the rectangle."""
        return 2 * (self.base + self.height)
    
    def area(self):
        """Returns the perimeter of the rectangle."""
        return self.base * self.height
    
    
if __name__ == '__main__':
    # Print a short description of the module
    print("The module allows to create and manage "
          "geometrical shapes.")
