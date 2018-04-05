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
a = {"location": {"x": 1000, "y": 20}, "yaw": 0}
b = {"location": {"x": 55, "y": 20}, "yaw": 0}
c = {"location": {"x": 55, "y": 20}, "yaw": 50}
d = {"location": {"x": 550, "y": 20}, "yaw": 20}
wind = {"angle": 0, "speed": 8.1}



def calcProduction(wind, turbines):

    turbineX = []
    turbineY = []
    turbineYaw = []

    for turbine in turbines:
        turbineX.append(turbine["location"]["x"])
        turbineY.append(turbine["location"]["y"])
        turbineYaw.append(turbine["yaw"])

    nTurbines = len(turbines)

    myFloris = floris_assembly_opt_AEP(nTurbines= nTurbines,
                                        nDirections=1,
                                        optimize_yaw=False,
                                        optimize_position=False,
                                        datasize=datasize,
                                        nSamples = resolution*resolution)

    # use default FLORIS parameters
    myFloris.parameters = FLORISParameters()

    # Properties of the air and wind
    windDirection                   = wind["angle"]
    windSpeed                       = wind["speed"] # in m/s
    myFloris.windrose_directions    = np.array([windDirection])
    myFloris.windrose_speeds        = windSpeed
    myFloris.air_density            = 1.1716

    # Infrastructure parameters
    myFloris.turbineX               = turbineX
    myFloris.turbineY               = turbineY
    myFloris.yaw                    = turbineYaw
    myFloris.curve_wind_speed       = NREL5MWCPCT.wind_speed
    myFloris.curve_CP               = NREL5MWCPCT.CP
    myFloris.curve_CT               = NREL5MWCPCT.CT
    myFloris.axialInduction         = np.ones(nTurbines)*axialInduction
    myFloris.hubHeight              = np.ones(nTurbines)*hub_height
    myFloris.rotorDiameter          = np.ones(nTurbines)*rotorDiameter
    myFloris.rotorArea              = np.ones(nTurbines)*rotorArea
    myFloris.generator_efficiency   = np.ones(nTurbines)*generator_efficiency

    # Define site measurements

    myFloris.run()
    baselinePower = np.sum(myFloris.floris_power_0.wt_power)
    return baselinePower

#calcProduction(wind, [a, b, c, d])
