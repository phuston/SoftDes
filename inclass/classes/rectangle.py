"""Dealing with rectangles"""

import numpy as np

## Point and print_point from Think Python
class Point():
    """Represents a point in 2-D space"""
    def __init__(x, y):
        self.x = x
        self.y = y

def print_point(p):
    """Print a Point object in human-readable format"""
    template = "({x}, {y})"
    # See Python string formatting docs
    # https://docs.python.org/2/library/string.html#format-examples
    print template.format(x=p.x, y=p.y)


## TODO:
# - Implement Rectangle class using two points, instead of point + width/length
# - Implement print_rectangle
# - Implement find_center function

class Rectangle():
    def __init__(self, lower_left, upper_right):
        self.lower_left = lower_left
        self.upper_right = upper_right


def find_center(my_rect):
    """
    Return the Point at the center of my_rect Rectangle

    Note: Your doctest may be different depending on your 
    implementation of Rectangle
    >>> p1 = Point(0, 0)
    >>> p2 = Point(6, 4)
    >>> rect = Rectangle(p1, p2)
    >>> print find_center(rect)
    (3.0, 2.0)
    """
    center_x = np.mean([my_rect.lower_left.x, my_rect.upper_right.x])
    center_y = np.mean([my_rect.lower_left.y, my_rect.upper_right.y])

    return (center_x, center_y)

## Challenge problem:
def bounding_box(rects):
    min_x = rects[0].lower_left.x
    min_y = rects[0].lower_left.y
    max_x = rects[0].upper_right.x
    max_y = rects[0].upper_right.y

    for rect in rects:
        if rect.lower_left.x < min_x:
            min_x = rect.lower_left.x
        if rect.lower_left.y < min_y:
            min_y = rect.lower_left.y
        if rect.upper_right.x > max_x:
            max_x = rect.upper_right.x
        if rect.upper_right.y > max_y:
            max_y = rect.upper_right.y

    return Rectangle(Point(min_x, min_y), Point(max_x, max_y))
