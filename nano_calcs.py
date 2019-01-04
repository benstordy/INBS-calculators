# author: Ben Stordy
# python based nano colloid calculator function library

# import scipy module for its constants and mathematical function.
from scipy import constants

# create a function to calculate the area of a sphere in square centimetres,
# taking diameter in nanometres as an argument. Returns area in cm^2
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
# taking length and width in nanometres as arguments. Returns area in cm^2
def area_NR(length, width):
    # calculate area of a sphere with diameter = width of NR (in cm^2).
    caps_area = constants.pi*width**2*1e-14
    # calculate area of the side of a cylinder with cylinder length =
    # length of NR - width of NR, and diameter = width of NR (in cm^2).
    side_area = constants.pi*width*(length-width)*1e-14
    # sum to get total area.
    area = side_area+caps_area
    return area

# create a function to calculate the number of streptavidin tetramers required,
# taking conjugated NP area (cm^2) as an argument.
def number_SA(conj_area, num_NP):
    # assuming streptavidin hydrodynamic diameter ~5nm, get projected area of
    # streptavidin, treating it as a sphere (in cm^2)
    projected_area = constants.pi*2.5**2*1e-14
    # using the area of the nanoparticle with DNA conjugated to the surface,
    # get number of streptavidin that would fit on surface (in cm^2)
    num_SA_NP = (conj_area/projected_area)
    # get total number of streptavidin to add using total number of NP in
    # solution
    num_SA = num_SA_NP*num_NP
    return num_SA

# create a function to calculate the microlitres of 5mg/mL streptavidin required
# taking conjugated NP area (cm^2) as an argument. Assumes 55kDA MW
def volume_SA(conj_area, num_NP):
    # get the number of SA molecules required in total
    num_SA = number_SA(conj_area, num_NP)
    # calculates volume of SA solution to add to get the target concentration
    # vol_SA=((num_SA/constants.Avogadro)[mol]*(55000[g/mol]/5[g/L]))[L]*1e6
    vol_SA = (num_SA/constants.Avogadro)*(55000/5)*1e6
    return vol_SA

def volume_xlink(conj_area, num_NP):
    # get the number of SA molecules required in total
    num_SA = number_SA(conj_area, num_NP)
    # 16 amine sites per streptavidin tetramer
    num_xlink = num_SA*16
    # 574g/L
    vol_xlink = (num_xlink/constants.Avogadro)*(574/5)*1e6
    return vol_xlink

# create a function to calculate the microlitres of DNA solution required,
# taking total NP area (cm^2) as an argument. Assumes DNA concentration = 10uM
def volume_DNA(area):
    # calculates the number of DNA to add to get one DNA strand per 7nm^2
    # converting area in cm^2 to nm^2
    num_DNA = area*(1e14)/7
    # calculates volume of DNA solution to add to get the target concentration
    # vol_DNA=((num_DNA/constants.Avogadro)[mol]/(DNA_conc*1e-6[mol/L]))[L]*1e6
    vol_DNA = ((num_DNA/constants.Avogadro)/(10*1e-6))*1e6
    return vol_DNA

# create a function to calculate the microlitres of 5mg/mL PEG required,
# taking total NP area (cm^2) as an argument. Assumes 5000g/mol (using PEG5k)
def volume_PEG(area):
    # calculates the number of PEG to add to get 10 PEG strands per 1nm^2
    # converting area in cm^2 to nm^2
    num_PEG = area*(1e14)*10
    # calculates volume of PEG solution to add to get the target concentration
    # vol_PEG=((num_PEG/constants.Avogadro)[mol]*(5000[g/mol]/5[g/L]))[L]*1e6
    vol_PEG = (num_PEG/constants.Avogadro)*(5000/5)*1e6
    return vol_PEG
