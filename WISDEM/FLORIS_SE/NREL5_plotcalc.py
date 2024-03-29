# This example script compares FLORIS predictions with steady-state SOWFA data as obtained
# throught the simulations described in:
#

import numpy as np

import simplejson

#import matplotlib as mpl
#from matplotlib import pyplot as plt

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
#NREL5MWCPCT = pickle.load(open('WISDEM/FLORIS_SE/NREL5MWCPCT.p'))
NREL5MWCPCT = pickle.load(open('./NREL5MWCPCT.p'))
datasize = NREL5MWCPCT.CP.size

#DEBUG
#wind = {"angle": 0, "speed": 8}
#a = {"location": {"x": 1000, "y": 20}, "yaw": 0}
#b = {"location": {"x": 55, "y": 20}, "yaw": 0}
#c = {"location": {"x": 55, "y": 20}, "yaw": 50}
#d = {"location": {"x": 550, "y": 20}, "yaw": 20}
#wind = {"angle": 0, "speed": 8.1}

wind = {"angle": 180, "speed": 8.1}
turs = [
  {
    "model": "NREL 5MW",
    "location":
    {
      "x": 0,
      "y": 0
    },
    "yaw": 0
  },
  {
    "model": "NREL 5MW",
    "location":
    {
      "x": 400,
      "y": 0
    },
    "yaw": 0
  },
  {
    "model": "NREL 5MW",
    "location":
    {
      "x": 800,
      "y": 0
    },
    "yaw": 0
  }
]

def calcProduction(wind, par):



    turbineX = [665, 590, 520, 516, 452, 250]
    turbineY = [24, 120, 232, 343, 479, 619]
    turbineYaw = par


    nTurbines = len(turbineX)

    myFloris = floris_assembly_opt_AEP(nTurbines= nTurbines,
                                        nDirections=1,
                                        optimize_yaw=False,
                                        optimize_position=False,
                                        datasize=datasize,
                                        nSamples = resolution*resolution)

    # use default FLORIS parameters
    myFloris.parameters = FLORISParameters()

    # Normal distributed noise for wind diection and wind speed
    angleNoise = np.random.normal(0, 0.01)
    speedNoise = np.random.normal(0, 0.01)

    # Properties of the air and wind
    windDirection                   = wind["angle"] #+ angleNoise
    windSpeed                       = wind["speed"] #+ speedNoise # in m/s
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
    #return myFloris.floris_power_0.wt_power
    return baselinePower

#print calcProduction(wind, [a, b, c, d])
#print calcProduction(wind, turs)
wind = {"angle": 0, "speed": 8.1}

res = []

actions = [-30, -25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30]
actions = [1, 2]

#print calcProduction(wind, [0, 0, 0])

for action1 in actions:
    first = []
    for action2 in actions:
        second = []
        for action3 in actions:
            third = []
            for action4 in actions:
                fourth = []
                for action5 in actions:
                    fifth = []
                    for action6 in actions:
                        result = calcProduction(wind, [action1, action2, action3, action4, action5, action6]).tolist()
                        print ([action1, action2, action3, action4, action5, action6], result)
                        fifth.append(result)
                    fourth.append(fifth)
                third.append(fourth)
            second.append(third)
        first.append(second)
    res.append(first)

print res
f = open('output.txt', 'w')
simplejson.dump(res, f)
f.close()
