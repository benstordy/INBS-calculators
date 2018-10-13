# author: Ben Stordy
# python based NR concentration calculator
# assumes a hemispherical-capped cylinder rod
# takes command line inputs

# imports the sys module, and the argparse module, allowing for command line
# input.
import sys
import argparse

import nano_area_calcs as calcs

# tell the user that the script is running
print("running", sys.argv[0], "\n")

# define parse to be the funtion ArgumentParser from the argparse module
parse = argparse.ArgumentParser()
# use the add_argument function to specify which command line options the
# calculator will accept. We need four inputs, the length, width, concentration,
# and target area.
parse.add_argument("length", type=float, help="the length of the NR (in nm)")
parse.add_argument("width", type=float, help="the width of the NR (in nm)")
parse.add_argument("concentration", type=float, help="the concentration of the"
                    " NP solution (in nM)")
parse.add_argument("target_area", type=float, help="the target area of the NP"
                    " (in cm^2)")
parse.add_argument("DNA_conc", type=float, nargs="?", default=10, help="the "
                    "concentration of the DNA solution (in uM). This is set to "
                    "10uM by default")
parse.add_argument("-v", "--verbose", action="store_true", help="increase "
                    "detail of output")
# parse the arguments passed in the command line
args = parse.parse_args()

# check that sensible input values have been given
if(args.width <= 0 or args.length <= 0 or args.concentration <= 0
    or args.target_area <= 0):
    sys.exit("Error: You must provide positive values for each input! \n")

# use the nano_area_calcs formulae to calculate the area, number, mols, volume
# of the nanorods, and volume of DNA to be added (in 10x excess)
area = calcs.area_NR(args.length, args.width)
number = calcs.number_NP(area, args.target_area)
mols = calcs.mols_NP(number)
volume = calcs.volume_NP(args.concentration, mols)
vol_DNA = 10*calcs.volume_DNA(args.target_area, args.DNA_conc)
vol_PEG = calcs.volume_PEG(args.target_area)

# decide how much of this info to output, depending whether the user wants
# verbosity
if args.verbose:
    print("For", args.target_area, "cm^2: \n")
    print("The area of a single nanorod is", "%.4E" % area, "cm^2 \n")
    print("The number of nanorods required is", "%.4E" % number, "\n")
    print("The number of moles is", "%.4E" % mols, "\n")
    print("The volume of", args.concentration, "nM nanorod solution required"
        "is", "%.1f" % volume, "uL \n")
    print("The volume of", args.DNA_conc, "uM DNA solution required is", "%.1f"
        % vol_DNA, "uL \n")
    print("The volume of 5mg/mL sulfo-NHS-PEG5k-diazirine solution required is",
        "%.1f" % vol_PEG, "uL \n")

else:
    print("Use", "%.1f" % volume, "uL GNR,", "%.1f" % vol_DNA, "uL DNA, and "
        "%.1f" % vol_PEG, "uL PEG for", args.target_area, "cm^2 \n \nFor more "
        "details, try including the optional verbosity flag '-v' in your input"
         "\n")
