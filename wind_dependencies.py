import math as m
#import matplotlib.pyplot as plt
from sympy.geometry import *


# Dependency lies within a wake zone that is represented by a rectangle with as width the diameter of the blades of the
# and as length infinity.

# plt.xlim(-200, 200)
# plt.ylim(-200, 200)

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init


def linearFun(x_point, y_point, slope, x):
    return slope * (x - x_point) + y_point



def inWake(a, b, wind):
    diameter = 126.4
    a_x = a["location"]["x"]
    a_y = a["location"]["y"]
    b_x = b["location"]["x"]
    b_y = b["location"]["y"]
    wind_angle = wind["angle"]
    radius = diameter/2


    a_yaw = m.radians(a["yaw"])

    corrected_a_angle = a_yaw + m.pi/2

    # Correcting values for the axis.
    x_corr = m.cos(corrected_a_angle)*radius
    y_corr = m.sin(corrected_a_angle)*radius

    blade_point_a1 = Point(
        a_x + x_corr,
        a_y + y_corr
    )

    blade_point_a2 = Point(
        a_x - x_corr,
        a_y - y_corr
    )

    wind_angle = m.radians(wind_angle) + m.pi
    zone_length = 500

    x_corr = m.cos(wind_angle)*zone_length
    y_corr = m.sin(wind_angle)*zone_length

    zone_end1 = Point(
        blade_point_a1.x + x_corr,
        blade_point_a1.y + y_corr
    )

    zone_end2 = Point(
        blade_point_a2.x + x_corr,
        blade_point_a2.y + y_corr
    )


    #plt.plot([blade_point_a1.x, blade_point_a2.x], [blade_point_a1.y, blade_point_a2.y], "black")
    #plt.plot(a_x, a_y, "bo")
    #plt.plot(blade_point_a1.x, blade_point_a1.y, "r+")
    #plt.plot(blade_point_a2.x, blade_point_a2.y, "r+")

    #b_circle = plt.Circle(Point2D(b_x, b_y), radius)




    #plt.plot(zone_end1.x, zone_end1.y, "g+")
    #plt.plot(zone_end2.x, zone_end2.y, "g+")

    #plt.plot([blade_point_a1.x, zone_end1.x], [blade_point_a1.y, zone_end1.y], "orange")
    #plt.plot([blade_point_a2.x, zone_end2.x], [blade_point_a2.y, zone_end2.y], "orange")

    #plt.xlim(-200, 200)
    #plt.ylim(-200, 200)

    #plt.gcf().gca().add_artist(b_circle)

    #plt.show()

    border1 = Segment(Point2D(blade_point_a1.x, blade_point_a1.y), Point2D(zone_end1.x, zone_end1.y))
    border2 = Segment(Point2D(blade_point_a2.x, blade_point_a2.y), Point2D(zone_end2.x, zone_end2.y))
    b_circle = Circle(Point2D(b_x, b_y), radius)

    if len(intersection(border1, b_circle)) != 0 or len(intersection(border2, b_circle)) != 0:
        return True
    else:
        return False



def dependsOn(a, b, parameters):
    wind = parameters[0]
    return inWake(a, b, wind)
