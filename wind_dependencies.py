import math as m
import matplotlib.pyplot as plt
from sympy import *
from sympy.geometry import *
import numpy as np
import matplotlib.patches as patches

# Dependency lies within a wake zone that is represented by a rectangle with as width the diameter of the blades of the
# and as length infinity.

plt.xlim(-200, 200)
plt.ylim(-200, 200)

class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init


def linearFun(x_point, y_point, slope, x):
    return slope * (x - x_point) + y_point



def inWake(a, b, a_angle, wind):
    diameter = 40
    a_x = a["location"]["x"]
    a_y = a["location"]["y"]
    wind_angle = wind["angle"]
    radius = diameter/2

    a_angle = m.radians(a_angle)

    a_slope = m.tan(a_angle)

    corrected_a_angle = a_angle + m.pi/2

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
    print(wind_angle)
    zone_length = 200

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


    plt.plot([blade_point_a1.x, blade_point_a2.x], [blade_point_a1.y, blade_point_a2.y], "black")
    plt.plot(a_x, a_y, "bo")
    plt.plot(blade_point_a1.x, blade_point_a1.y, "r+")
    plt.plot(blade_point_a2.x, blade_point_a2.y, "r+")

    b_circle = plt.Circle((b["location"]["x"], b["location"]["y"]), radius)




    plt.plot(zone_end1.x, zone_end1.y, "g+")
    plt.plot(zone_end2.x, zone_end2.y, "g+")

    plt.plot([blade_point_a1.x, zone_end1.x], [blade_point_a1.y, zone_end1.y], "orange")
    plt.plot([blade_point_a2.x, zone_end2.x], [blade_point_a2.y, zone_end2.y], "orange")

    plt.xlim(-200, 200)
    plt.ylim(-200, 200)

    plt.gcf().gca().add_artist(b_circle)

    plt.show()




def dependsOn(a, b, wind):
    return inWake(a, b, wind)

a = {
    "model": "NREL 5MW",
    "location":
    {
      "x": 20,
      "y": 20
    }
  }

b = {
    "model": "NREL 5MW",
    "location":
    {
      "x": 5,
      "y": 5
    }
  }

wind = {"angle": 15}


inWake(a, b, 0, wind)