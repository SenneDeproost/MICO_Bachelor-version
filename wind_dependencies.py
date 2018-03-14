import math as m
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Dependency lies within a wake zone that is represented by a rectangle with as width the diameter of the blades of the
# and as length infinity.


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

    print a_angle

    a_slope = m.tan(a_angle)

    print a_slope

    corrected_a_angle = a_angle + m.pi/2
    x_corr = m.sin(corrected_a_angle)*radius
    y_corr = m.cos(corrected_a_angle)*radius


    print a_x + m.fabs(m.sin(corrected_a_angle)*radius)



    blade_point_a1 = Point(
        a_x + x_corr,
        a_y + y_corr
    )

    blade_point_a2 = Point(
        a_x - x_corr,
        a_y - y_corr
    )


    plt.plot(a_x, a_y, "bo")
    plt.plot(blade_point_a1.x, blade_point_a1.y, "r+")
    plt.plot(blade_point_a2.x, blade_point_a2.y, "r+")

    plt.show()




def dependsOn(a, b, wind):
    return inWake(a, b, wind)

a = {
    "model": "NREL 5MW",
    "location":
    {
      "x": 5,
      "y": 0
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

wind = {"angle": 0}


inWake(a, b, 70, wind)