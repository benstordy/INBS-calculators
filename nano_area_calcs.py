# author: Ben Stordy
# python based nano colloid calculator function library

# import scipy module for its constants and mathematical function.
from scipy import constants

# create a function to calculate the area of a sphere in square centimetres,
# taking diameter in nanometres as an argument.
def area_NP(diameter):
    # get the surface area of a sphere from its diameter.
    area = constants.pi*diameter**2*1e-14
    return area

# create a function to calculate the number of nanoparticles of a given area
# required to acheive the target area. Both arguments are to be given in square
# centimetres.
def number_NP(area, target_area):
    # get the number of nanoparticles required by taking the ratio of the target
    # area to the area per nanoparticle.
    num = target_area/area
    return num

# create a function to convert to the moles of nanoparticles from a number.
def mols_NP(num):
    # use avogadro's constant to get moles from a number.
    mol = num/constants.Avogadro
    return mol

# create a function to calculate the required volume of nanoparticles required
# to acheive the target area. Concentration is to be given in nanomolar, while
# mol (required moles) is given in moles.
def volume_NP(concentration, mol):
    # take the ratio of the desired number of moles over the solution
    # concentration to get solution volume required
    vol = (mol/(concentration*1e-9))*1e6
    return vol

# create a function to calculate the area of a rod in square centimetres,
# taking length and width in nanometres as arguments.
def area_NR(length, width):
    # calculate area of a sphere with diameter = width of NR (in cm^2).
    caps_area = constants.pi*width**2*1e-14
    # calculate area of the side of a cylinder with cylinder length =
    # length of NR - width of NR, and diameter = width of NR (in cm^2).
    side_area = constants.pi*width*(length-width)*1e-14
    # sum to get total area.
    area = side_area+caps_area
    return area
