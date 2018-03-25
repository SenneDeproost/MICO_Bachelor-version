# This example script compares FLORIS predictions with steady-state SOWFA data as obtained
# throught the simulations described in:
#

import numpy as np

import matplotlib as mpl
from matplotlib import pyplot as plt

from scipy.io import loadmat
import pickle

from Parameters import FLORISParameters
from Circle_assembly import floris_assembly_opt_AEP

# Load steady-state power data from SOWFA
#ICOWESdata = loadmat('YawPosResults.mat')

# visualization: define resolution
resolution = 75

# Define turbine characteristics
rotorDiameter = 126.4
rotorArea = np.pi*rotorDiameter*rotorDiameter/4.0
axialInduction = 1.0/3.0 # used only for initialization
generator_efficiency = 0.944
hub_height = 90.0
NREL5MWCPCT = pickle.load(open('WISDEM/FLORIS_SE/NREL5MWCPCT.p'))
datasize = NREL5MWCPCT.CP.size

#DEBUG
#wind = {"angle": 0, "speed": 8}
#a = {"location": {"x": 1000, "y": 20}, "yaw": 0}
#b = {"location": {"x": 55, "y": 20}, "yaw": 0}
#c = {"location": {"x": 55, "y": 20}, "yaw": 50}

myFloris = floris_assembly_opt_AEP(nTurbines=2, nDirections=1, optimize_yaw=False,
                                    optimize_position=False,
                                    datasize=datasize, nSamples = resolution*resolution)

# use default FLORIS parameters
myFloris.parameters = FLORISParameters()

# load turbine properties into FLORIS
myFloris.curve_wind_speed = NREL5MWCPCT.wind_speed
myFloris.curve_CP = NREL5MWCPCT.CP
myFloris.curve_CT = NREL5MWCPCT.CT
myFloris.axialInduction = np.array([axialInduction, axialInduction])
myFloris.rotorDiameter = np.array([rotorDiameter, rotorDiameter])
myFloris.rotorArea = np.array([rotorArea, rotorArea])
myFloris.hubHeight = np.array([hub_height, hub_height])
myFloris.generator_efficiency = np.array([generator_efficiency, generator_efficiency])


def calcProduction(turbine_a, turbine_b, wind):

    a_x = turbine_a["location"]["x"]
    b_x = turbine_b["location"]["x"]
    a_y = turbine_a["location"]["y"]
    b_y = turbine_b["location"]["y"]

    a_yaw = turbine_a["yaw"]
    b_yaw = turbine_b["yaw"]

    turbineXinit = np.array([a_x, b_x])
    turbineYinit = np.array([a_y, b_y])

    myFloris.turbineX = turbineXinit
    myFloris.turbineY = turbineYinit
    myFloris.yaw = np.array([a_yaw, b_yaw])

    # Define site measurements
    windDirection = wind["angle"]
    myFloris.windrose_directions = np.array([windDirection])
    wind_speed = wind["speed"]    # m/s
    myFloris.windrose_speeds = wind_speed
    myFloris.air_density = 1.1716

    myFloris.run()
    baselinePower = np.sum(myFloris.floris_power_0.wt_power)
    return baselinePower
