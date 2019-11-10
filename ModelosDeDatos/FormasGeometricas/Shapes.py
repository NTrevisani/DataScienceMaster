import math

PI = math.pi

# Basic class to manage shapes.
# All the other classes inherit from it
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
        """Sums two objects or an object and a number.
        
        The sum of two objects returns a third object with
        each attribute equal to the sum of the corresponding
        attributes of the two objects summed and center at the
        half point between the centers of the two objects.
        The sum of an object and a number returns a new object
        with each attribute equal to the attribute of the object 
        plus the number and centered at the same point as the object.
        """
        raise NotImplementedError

    def __radd__(self, other):
        """Reverse sum of an object and a number.
        """
        return self.__add__(other)

    def __sub__(self, other):   
        """Subtracts two objects or an object and a number.
        
        The difference between two objects returns a third object with
        each attribute equal to the difference between the 
        corresponding attributes of the two objects and center at the
        half point between the centers of the two objects.
        The difference between an object and a number returns a new 
        object with each attribute equal to the attribute of the object 
        minus the number and centered at the same point as the object.
        """
        raise NotImplementedError
    
    def __rsub__(self, other):   
        """Reverse difference between an object and a number.
        
        Since subtraction is not a commutative operation, its reverse
        is implemented specifically for each object.
        """
        raise NotImplementedError

    def __mul__(self, other):
        """Multiplies two objects or an object and a number.
        
        The product of two objects returns a third object with
        each attribute equal to the product of the corresponding
        attributes of the two objects and center at the
        half point between the centers of the two objects.
        The product of an object and a number returns a new object
        with each attribute equal to the attribute of the object 
        times the number and centered at the same point as the object.
        """
        raise NotImplementedError

    def __rmul__(self, other):
        """Reverse product of an object and a number.
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """Divides two objects or an object and a number.
        
        The division between two objects returns a third object with
        each attribute equal to the division between the corresponding
        attributes of the two objects and center at the
        half point between the centers of the two objects.
        The division between an object and a number returns a new object
        with each attribute equal to the attribute of the object 
        divided by the number and centered at the same point as the 
        object.
        """
        raise NotImplementedError

    def __rtruediv__(self, other):
        """Reverse division between an object and a number.
        
        Since division is not a commutative operation, its reverse is
        implemented specifically for each object.
        """
        raise NotImplementedError

    def __pow__(self, other):
        """Elevates an object to a number.
        
        The power of an object to a number returns a new object
        with each attribute equal to the attribute of the object 
        elevated to the number and centered at the same point as the 
        object.
        """
        raise NotImplementedError
        
    def __eq__(self, other):
        """Compares two objects or an object and a number.
        
        Returns True if two object has the same area.
        In case one of the two arguments is a number,
        the area of the object is compared with the number.
        """
        if isinstance(other, (int,float)):
            return self.area() == other
        else:
            return self.area() == other.area()  

    def __ne__(self, other):
        """Compares two objects or an object and a number.
        
        Returns True if two object has different area.
        In case one of the two arguments is a number,
        the area of the object is compared with the number.
        """
        if isinstance(other, (int,float)):
            return self.area() != other
        else:
            return self.area() != other.area()  

    def __lt__(self, other):
        """Compares two objects or an object and a number.
         
        Returns True if the first object area is smaller than the second.
        In case one of the two arguments is a number,
        the area of the object is compared with the number.
        """
        if isinstance(other, (int,float)):
            return self.area() < other
        else:
            return self.area() < other.area()  

    def __gt__(self, other):
        """Compares two objects or an object and a number.
        
        Returns True if the first object area is larger than the second.
        In case one of the two arguments is a number,
        the area of the object is compared with the number.
        """
        if isinstance(other, (int,float)):
            return self.area() > other
        else:
            return self.area() > other.area()  

    def __le__(self, other):
        """Compares two objects or an object and a number.
        
        Returns True if the first object area is smaller than 
        or equal to the second.
        In case one of the two arguments is a number,
        the area of the object is compared with the number.
        """
        if isinstance(other, (int,float)):
            return self.area() <= other
        else:
            return self.area() <= other.area()  

    def __ge__(self, other):
        """Compares two objects or an object and a number.
        
        Returns True if the first object area is larger than 
        or equal to the second.
        In case one of the two arguments is a number,
        the area of the object is compared with the number.
        """
        if isinstance(other, (int,float)):
            return self.area() >= other
        else:
            return self.area() >= other.area()  

        
# Class to manage points.
# It inherits from Shape.
# The other classes inherit from it,
# with the point considered as their center
class Point(Shape):
    """A point of coordinates (x,y)."""
    
    def __init__(self, x, y):
        """Initialize the point with its coordinates."""
        if isinstance(x, (int,float)):
            self._x = x
        else:
            raise TypeError("x must be an integer or a float")
        if isinstance(y, (int,float)):
            self._y = y
        else:
            raise TypeError("y must be an integer or a float")
        
    def __str__(self):
        """Print as 'A Point with coordinates (x,y)'."""
        self_class = type(self).__name__
        msg = "A {0} with coordinates ({1},{2})"
        return msg.format(self_class, self._x, self._y)

    def __repr__(self):
        """Represents as 'Point(x,y)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2})"
        return msg.format(self_class, self._x, self._y)

    def move_along_x(self, x_shift):
        """Moves the point along x axis of the quantity 'x_shift'."""
        self._x += x_shift

    def move_along_y(self, y_shift):
        """Moves the point along y axis of the quantity 'y_shift'."""
        self._y += y_shift

    def move_to(self, new_x, new_y):
        """Moves the point to the coordinates ('new_x','new_y')."""
        self._x = new_x
        self._y = new_y
        
    def half_way(self, other):
        """Returns the coordinates of middle point between self and other."""
        half_x = (self._x + other._x) / 2
        half_y = (self._y + other._y) / 2
        return half_x, half_y
        
    def distance(self, other):
        """Returns the distance between self and other."""
        distance_2 = (self._x - other._x)**2 + (self._y - other._y)**2
        return math.sqrt(distance_2)
        
    def get_x(self):
        """Returns the x coordinate of the point."""
        return self._x

    def get_y(self):
        """Returns the y coordinate of the point."""
        return self._y

    def set_x(self, x):
        """Sets the x coordinate of the point to the input value."""
        self._x = x

    def set_y(self, y):
        """Sets the y coordinate of the point to the input value."""
        self._y = y

    def get_center(self):
        """Returns the coordinates of the point."""
        return self._x, self._y
    
    
class Circle(Point):
    """A circle of radius centered at ('x','y') with radius 'r'."""
    
    def __init__(self, x, y, radius):
        """Initializes the circle with its center and its radius.
        
        The radius must be positive.
        """
        super().__init__(x,y)
        if isinstance(radius, (int,float)):
            if radius <= 0:
                raise ValueError("Radius must have a positive value")
            else:
                self._radius = radius
        else:
            raise TypeError("Radius must be an integer or a float")
                     
    def __str__(self):
        """Print as 'A Circle centered at (x,y) with radius 'radius''."""
        self_class = type(self).__name__
        msg = "A {0} centered at ({1},{2}) with radius {3}"
        return msg.format(self_class, self._x, self._y, self._radius)
    
    def __repr__(self):
        """Represents as 'Circle(x,y,radius)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2},{3})"
        return msg.format(self_class, self._x, self._y, self._radius)
    
    def __add__(self, other):
        """Sums two Circles or a Circle and a number.
        
        The sum of two Circles returns a third Circle with
        radius equal to the sum of the radii of the two 
        Circles to be summed  and center at the
        half point between the centers of the two Circles.
        The sum of a Circle and a number returns a new Circle
        with radius equal to the radius of the Circle plus
        the number and centered at the same point as the Circle.
        """
        if isinstance(other, (int,float)):
            sum_radius = self._radius + other
            sum_x, sum_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            sum_radius = self._radius + other._radius
            sum_x, sum_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot sum a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(sum_x, sum_y, sum_radius)
        
    def __sub__(self, other):
        """Subtracts two Circles or a Circle and a number.
        
        The difference between two Circles returns a third Circle with
        radius equal to the difference between the radii of the two 
        Circles and center at the half point between the centers 
        of the two Circles.
        The difference between a Circle and a number returns a new 
        Circle with radius equal to the radius of the Circle minus
        the number and centered at the same point as the Circle.
        """
        if isinstance(other, (int,float)):
            dif_radius = self._radius - other
            dif_x, dif_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            dif_radius = self._radius - other._radius
            dif_x, dif_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot subtract a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(dif_x, dif_y, dif_radius)

    def __rsub__(self, other):   
        """Difference between a number and a Circle.
        """
        return type(self)(self._x, self._y, other - self._radius)

    def __mul__(self, other):
        """Multiplies two Circles or a Circle and a number.
        
        The product of two Circles returns a third Circle with
        radius equal to the product of the radii of the two 
        Circles and center at the half point between the centers 
        of the two Circles.
        The product of a Circle and a number returns a new Circle
        with radius equal to the radius of the Circle times
        the number and centered at the same point as the Circle.
        """
        if isinstance(other, (int,float)):
            mul_radius = self._radius * other
            mul_x, mul_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            mul_radius = self._radius * other._radius
            mul_x, mul_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot multimly a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(mul_x, mul_y, mul_radius)

    def __truediv__(self, other):
        """Divides two Circles or a Circle and a number.
        
        The division of two Circles returns a third Circle with
        radius equal to the division of the radii of the two 
        Circles and center at the half point between the centers 
        of the two Circles.
        The division of a Circle and a number returns a new Circle
        with radius equal to the radius of the Circle divided by
        the number and centered at the same point as the Circle.
        """
        if isinstance(other, (int,float)):
            if other == 0:
                raise ValueError("You cannot divide by 0")
            div_radius = self._radius / other
            div_x, div_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            div_radius = self._radius / other._radius
            div_x, div_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot divide a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(div_x, div_y, div_radius)

    def __rtruediv__(self, other):
        """Ratio between a number and a Circle.
        """        
        if other == 0:
            raise ValueError("You cannot divide by 0")
        return type(self)(self._x, self._y, other / self._radius)
        
    def __pow__(self, other):
        """Elevates a Circle to a number.
        
        The power of a Circle to a number returns a new Circle
        with radius equal to the radius of the Circle,
        elevated to the number and centered at the same point as the 
        Circle.
        """
        if isinstance(other, (int,float)):
            return type(self)(self._x, self._y, self._radius ** other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot elevate a {0} to a {1}"
            raise TypeError(msg.format(self_class, other_class))
        
    def perimeter(self):
        """Returns the perimeter of the circle."""
        return self._radius * 2 * PI
    
    def area(self):
        """Returns the area of the circle."""
        return self._radius** 2 * PI

    def get_radius(self):
        """Returns the radius of the circle."""
        return self._radius
        
    def set_radius(self, radius):
        """Sets the radius of the circle to the input value."""
        if radius <= 0:
            raise ValueError("Radius must have a positive value")
        else:
            self._radius = radius

    
class Rectangle(Point):
    """A rectangle centered at (x,y) with a base and a height."""
    def __init__(self, x, y, base, height):
        super().__init__(x,y)
        if isinstance(base, (int,float)):
            if base <= 0:
                raise ValueError("Base must have a positive value")
            else:
                self._base = base            
        else:
            raise TypeError("Base must be an integer or a float")
        if isinstance(height, (int,float)):
            if height <= 0:
                raise ValueError("Height must have a positive value")
            else:        
                self._height = height
        else:
            raise TypeError("Height must be an integer or a float")
        
    def __str__(self):
        """Print as 'A Rectangle centered at (x,y) 
        with base 'base' and height ''height'."""
        self_class = type(self).__name__
        msg = "A {0} centered at ({1},{2}) with base {3} and height {4}"
        return msg.format(self_class, self._x, self._y, 
                          self._base, self._height)
    
    def __repr__(self):
        """Represents as 'Rectangle(x,y,base,height)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2},{3},{4})"
        return msg.format(self_class, self._x, self._y, 
                          self._base, self._height)
        
    def __add__(self, other):
        """Sums two Rectangles or a Rectangle and a number.
        
        The sum of two Rectangles returns a third Rectangle with
        base equal to the sum of the bases, height equal to the
        sum of the two heights of the two Rectangles
        and center at the half point between the centers 
        of the two Rectangles.
        The sum of a Rectangle and a number returns a new Rectangle
        with base and height equal to the base and height of the 
        Rectangle plus the number and centered at the same point 
        as the Rectangle.
        """
        if isinstance(other, (int,float)):
            sum_base = self._base + other
            sum_height = self._height + other
            sum_x, sum_y = Point.half_way(self, self)
        elif isinstance(other, type(self)):
            sum_base = self._base + other._base
            sum_height = self._height + other._height
            sum_x, sum_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot sum a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(sum_x, sum_y, sum_base, sum_height)

    def __sub__(self, other):
        """Subtracts two Rectangles or a Rectangle and a number.
        
        The difference between two Rectangles returns a third Rectangle 
        with base equal to the difference between the bases, 
        height equal to the difference between the two heights 
        of the two Rectangles and center at the half point between 
        the centers of the two Rectangles. 
        The difference between a Rectangle and a number returns 
        a new Rectangle with base and height equal to the base 
        and height of the Rectangle minus the number and centered 
        at the same point as the Rectangle.
        """
        if isinstance(other, (int,float)):
            dif_base = self._base - other
            dif_height = self._height - other
            dif_x, dif_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            dif_base = self._base - other._base
            dif_height = self._height - other._height
            dif_x, dif_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot subtract a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(dif_x, dif_y, dif_base, dif_height)

    def __rsub__(self, other):   
        """Reverse difference between a number and a Rectangle.
        """
        return type(self)(self._x, self._y, 
                          other - self._base, other - self._height)

    def __mul__(self, other):
        """Multiplies two Rectangles or a Rectangle and a number.
        
        The product of two Rectangles returns a third Rectangle with
        base equal to the product of the bases and height equal to the 
        products of the heights of the two Rectangles and center 
        at the half point between the centers of the two Rectangles.
        The product of a Rectangle and a number returns a new Rectangle
        with base and height equal to the base and height of the 
        Rectangle times the number and centered at the same point 
        as the Rectangle.
        """
        if isinstance(other, (int,float)):
            mul_base = self._base * other
            mul_height = self._height * other
            mul_x, mul_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            mul_base = self._base * other._base
            mul_height = self._height * other._height
            mul_x, mul_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot multiply a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(mul_x, mul_y, mul_base, mul_height)

    def __truediv__(self, other):
        """Divides two Rectangles or a Rectangle and a number.
        
        The division between two Rectangles returns a third Rectangle 
        with base equal to the division between the bases and height 
        equal to the division between the heights of the two Rectangles 
        and center at the half point between the centers 
        of the two Rectangles.
        The division between a Rectangle and a number returns a 
        new Rectangle with base and height equal to the base and height 
        of the Rectangle divided by the number and centered at the same 
        point as the Rectangle.
        """
        if isinstance(other, (int,float)):
            if other == 0:
                raise ValueError("You cannot divide by 0")
            div_base = self._base / other
            div_height = self._height / other
            div_x, div_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            div_base = self._base / other._base
            div_height = self._height / other._height
            div_x, div_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot divide a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(div_x, div_y, div_base, div_height)

    def __rtruediv__(self, other):
        """Reverse division between a number and a Rectangle.
        """        
        if other == 0:
            raise ValueError("You cannot divide by 0")
        return type(self)(self._x, self._y, 
                          other / self._base, other / self._height)
        
    def __pow__(self, other):
        """Elevates a Rectangle to a number.
        
        The power of a Rectangle to a number returns a new Rectangle
        with base and height equal to the base and height of the Rectangle,
        elevated to the number and centered at the same point as the 
        Rectangle.
        """
        if isinstance(other, (int,float)):
            pow_base = self._base ** other
            pow_height = self._height ** other
            return type(self)(self._x, self._y, pow_base, pow_height)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot elevate a {0} to a {1}"
            raise TypeError(msg.format(self_class, other_class))
        
    def perimeter(self):
        """Returns the perimeter of the rectangle."""
        return 2 * (self._base + self._height)
    
    def area(self):
        """Returns the area of the rectangle."""
        return self._base * self._height
    
    def get_base(self):
        """Returns the base of the rectangle."""
        return self._base
        
    def get_height(self):
        """Returns the height of the rectangle."""
        return self._height

    def set_base(self, base):
        """Sets the base of the rectangle to the input value."""
        if base <= 0:
            raise ValueError("Base must have a positive value")
        else:
            self._base = base
    
    def set_height(self, height):
        """Sets the height of the rectangle to the input value."""
        if height <= 0:
            raise ValueError("Height must have a positive value")
        else:
            self._height = height
    
    
class Triangle(Point):
    """A triangle centered at (x,y) with sides side1, side2, side3.
    
    Each side must be shorter than the sum of the other two.
    """
    def __init__(self, x, y, side1, side2, side3):
        super().__init__(x,y)
        if (isinstance(side1, (int,float))
            and isinstance(side2, (int,float))
            and isinstance(side3, (int,float))):
            if side1 <= 0 or side2 <= 0 or side3 <= 0:
                raise ValueError("All the sides must have a positive value")
            elif side1 > side2 + side3:
                raise ValueError("Side1 is longer than the sum of side2 and side3")
            elif side2 > side3 + side1: 
                raise ValueError("Side2 is longer than the sum of side1 and side3")
            elif side3 > side1 + side2: 
                raise ValueError("Side3 is longer than the sum of side1 and side2")
            else:
                self._side1 = side1
                self._side2 = side2
                self._side3 = side3
        else: 
            raise TypeError("All the sides must be integers or floats")
        
    def __str__(self):
        """Print as 'A Triangle centered at (x,y) 
        with sides 'side1', 'side2', 'side3'."""
        self_class = type(self).__name__
        msg = "A {0} centered at ({1},{2}) with sides of length: {3}, {4}, {5}"
        return msg.format(self_class, self._x, self._y, 
                          self._side1, self._side2, self._side3)
    
    def __repr__(self):
        """Represents as 'Triangle(x,y,side1,side2,side3)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2},{3},{4},{5})"
        return msg.format(self_class, self._x, self._y, 
                          self._side1, self._side2, self._side3)
        
    def __add__(self, other):
        """Sum of two Triangles or of a Triangle and a number.
        
        The sum of two Triangles returns a third Triangle with
        each side equal to the sum of the corresponding sides 
        of the two Triangles to be summed
        and center at the half point between the centers 
        of the two Triangles.
        The sum of a Triangle and a number returns a new Triangle
        with each side equal to the side of the Triangle plus 
        the number and centered at the same point as the Triangle.
        """
        if isinstance(other, (int,float)):
            sum_side1 = self._side1 + other
            sum_side2 = self._side2 + other
            sum_side3 = self._side3 + other
            sum_x, sum_y = Point.half_way(self, self)
        elif isinstance(other, type(self)):
            sum_side1 = self._side1 + other._side1
            sum_side2 = self._side2 + other._side2
            sum_side3 = self._side3 + other._side3
            sum_x, sum_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot sum a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(sum_x, sum_y, 
                          sum_side1, sum_side2, sum_side3)

    def __sub__(self, other):
        """Subtracts two Triangles or a Triangle and a number.
        
        The difference between two Triangles returns a third Triangle 
        with each side equal to the difference between the corresponding 
        sides of the two Triangles and center at the half point between 
        the centers of the two Triangles.
        The difference between a Triangle and a number returns a new 
        Triangle with each side equal to the side of the Triangle minus 
        the number and centered at the same point as the Triangle.
        """
        if isinstance(other, (int,float)):
            dif_side1 = self._side1 - other
            dif_side2 = self._side2 - other
            dif_side3 = self._side3 - other
            dif_x, dif_y = Point.half_way(self, self)
        elif isinstance(other, type(self)):
            dif_side1 = self._side1 - other._side1
            dif_side2 = self._side2 - other._side2
            dif_side3 = self._side3 - other._side3
            dif_x, dif_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot subtract a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(dif_x, dif_y, dif_side1, dif_side2, dif_side3)
    
    def __rsub__(self, other):   
        """Difference between a number and a Triangle.
        """
        return type(self)(self._x, self._y, 
                          other - self._side1, 
                          other - self._side2, 
                          other - self._side3)

    def __mul__(self, other):
        """Multiplies two Triangles or a Triangle and a number.
        
        The product of two Triangles returns a third Triangle with
        each side equal to the product of the corresponding sides  
        of the two Triangles and center at the half point between 
        the centers of the two Triangles.
        The product of a Triangle and a number returns a new Triangle
        with each side equal to the side of the Triangle times 
        the number and centered at the same point as the Triangle.
        """
        if isinstance(other, (int,float)):
            mul_side1 = self._side1 * other
            mul_side2 = self._side2 * other
            mul_side3 = self._side3 * other
            mul_x, mul_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            mul_side1 = self._side1 * other._side1
            mul_side2 = self._side2 * other._side2
            mul_side3 = self._side3 * other._side3
            mul_x, mul_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot multiply a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(mul_x, mul_y, mul_side1, mul_side2, mul_side3)

    def __truediv__(self, other):
        """Divides two Triangles or a Triangle and a number.
        
        The division between two Triangle returns a third Triangle with
        each side equal to the division between the corresponding sides
        of the two Triangles and center at the half point between the 
        centers of the two Triangles.
        The division between a Triangle and a number returns a new Triangle
        with each side equal to the side of the Triangle divided 
        by the number and centered at the same point as the Triangle.
        """
        if isinstance(other, (int,float)):
            if other == 0:
                raise ValueError("You cannot divide by 0")
            div_side1 = self._side1 / other
            div_side2 = self._side2 / other
            div_side3 = self._side3 / other
            div_x, div_y = Point.half_way(self, self)
        elif (isinstance(other, type(self))):
            div_side1 = self._side1 / other._side1
            div_side2 = self._side2 / other._side2
            div_side3 = self._side3 / other._side3
            div_x, div_y = Point.half_way(self, other)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot divide a {0} and a {1}"
            raise TypeError(msg.format(self_class, other_class))
        return type(self)(div_x, div_y, div_side1, div_side2, div_side3)

    def __rtruediv__(self, other):
        """Ratio between a number and a Triangle.
        """        
        if other == 0:
            raise ValueError("You cannot divide by 0")
        return type(self)(self._x, self._y, 
                          other / self._side1, 
                          other / self._side2, 
                          other / self._side3)
        
    def __pow__(self, other):
        """Elevates a Triangle to a number.
        
        The power of a Triangle to a number returns a new Triangle
        with each side equal to the corresponding side of the Triangle,
        elevated to the number and centered at the same point as the 
        Triangle.
        """
        if isinstance(other, (int,float)):
            pow_side1 = self._side1 ** other
            pow_side2 = self._side2 ** other
            pow_side3 = self._side3 ** other
            return type(self)(self._x, self._y, 
                              pow_side1, pow_side2, pow_side3)
        else:
            self_class = type(self).__name__
            other_class = type(other).__name__
            msg = "You cannot elevate a {0} to a {1}"
            raise TypeError(msg.format(self_class, other_class))
        
    def perimeter(self):
        """Returns the perimeter of the triangle."""
        return (self._side1 + self._side2 + self._side3)
    
    def area(self):
        """Returns the area of the triangle."""
        p = 0.5 * (self._side1 + self._side2 + self._side3)
        area_2 = p * (p - self._side1) * (p - self._side2) * (p - self._side3)  
        return math.sqrt(area_2)
    
    def get_side1(self):
        """Returns the first side of the triangle."""
        return self._side1

    def get_side2(self):
        """Returns the second side of the triangle."""
        return self._side2

    def get_side3(self):
        """Returns the third side of the triangle."""
        return self._side3

    def set_side1(self, side1):
        """Sets the first side of the triangle to the input value."""
        if side1 <= 0:
            raise ValueError("Side1 must have a positive value")
        elif side1 > self._side2 + self._side3:
            raise ValueError("Now side1 is longer than the sum of side2 and side3")
        elif self._side2 > self._side3 + side1:
            raise ValueError("Now side2 is longer than the sum of side1 and side3")
        elif self._side3 > side1 + self._side2:
            raise ValueError("Now side3 is longer than the sum of side1 and side2")
        else:
            self._side1 = side1

    def set_side2(self, side2):
        """Sets the second side of the triangle to the input value."""
        if side2 <= 0:
            raise ValueError("Side2 must have a positive value")
        elif self._side1 > side2 + self._side3:
            raise ValueError("Side1 is longer than the sum of side1 and side2")
        elif side2 > self._side3 + self._side1:
            raise ValueError("Side2 is longer than the sum of side1 and side3")
        elif self._side3 > self._side1 + side2:
            raise ValueError("Side3 is longer than the sum of side1 and side2")
        else:
            self._side2 = side2

    def set_side3(self, side3):
        """Sets the third side of the triangle to the input value."""
        if side3 <= 0:
            raise ValueError("Side3 must have a positive value")
        elif self._side1 > self._side2 + side3:
            raise ValueError("Side1 is longer than the sum of side2 and side3")
        elif self._side2 > self._side1 + side3:
            raise ValueError("Side2 is longer than the sum of side1 and side3")
        elif side3 > self._side1 + self._side2:
            raise ValueError("Side3 is longer than the sum of side1 and side2")
        else:
            self._side3 = side3

            
if __name__ == '__main__':
    # Print a short description of the module
    print("The module allows to create and manage "
          "geometrical shapes.")
