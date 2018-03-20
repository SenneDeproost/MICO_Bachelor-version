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
ICOWESdata = loadmat('YawPosResults.mat')

# visualization: define resolution
resolution = 75

# Define turbine characteristics
rotorDiameter = 126.4
rotorArea = np.pi*rotorDiameter*rotorDiameter/4.0
axialInduction = 1.0/3.0 # used only for initialization
generator_efficiency = 0.944
hub_height = 90.0
NREL5MWCPCT = pickle.load(open('NREL5MWCPCT.p'))
datasize = NREL5MWCPCeT.CP.size



def calcProduction(turbine_a, turbine_b, wind):

    turbineXinit = np.array([turbine_a["location"]["x"], turbine_b["location"]["x"])
    turbineYinit = np.array([turbine_a["location"]["y"], turbine_b["location"]["y"])

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
    myFloris.turbineX = turbineXinit
    myFloris.turbineY = turbineYinit

    # Define site measurements
    windDirection = wind["angle"]
    myFloris.windrose_directions = np.array([windDirection])
    wind_speed = wind["speed"]    # m/s
    myFloris.windrose_speeds = wind_speed
    myFloris.air_density = 1.1716
