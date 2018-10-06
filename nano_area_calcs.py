# author: Ben Stordy
# python based nano colloid calculator function library

# import scipy module for its constants and mathematical function.
from scipy import constants

# create a function to calculate the area of a sphere in square centimetres,
# taking diameter in nanometres as an argument.
def sphere_area(diameter):
    area = constants.pi*diameter**2*1e-14
    return area

# create a function to calculate the number of nanoparticles of a given area
# required to acheive the target area. Both arguments are to be given in square
# centimetres.
def number_NP(area, target_area):
    num = target_area/area
    return num

# create a function to convert to the moles of nanoparticles from a number.
def mols_NP(num):
    mol = num/constants.Avogadro
    return mol

# create a function to calculate the required volume of nanoparticles required
# to acheive the target area. Concentration is to be given in nanomolar, while
# mol (required moles) is given in moles.
def volume_NP(concentration, mol):
    vol = (mol/(concentration*1e-9))*1e6
    return vol
