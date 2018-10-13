# author: Ben Stordy
# python based NP and NR calculator
# outputs required DNA, PEG and GNP or GNR for a given size, concentration,
# and surface area of particles

# imports the argparse module, allowing for command line input.
import argparse

import nano_calcs as calcs

# tell the user that the script is running
print("Running nanoparticle calculator...\n")

# define parse to be the funtion ArgumentParser from the argparse module
parse = argparse.ArgumentParser()
# use the add_argument function to specify which command line options the
# calculator will accept. We need four inputs, the length, width, concentration,
# and target area.
parse.add_argument("concentration", type=float, help="the concentration of the"
                    " NP solution (in nM)")
parse.add_argument("target_area", type=float, help="the target area of the NP"
                    " (in cm^2)")
parse.add_argument("diameter", type=float, help="the diameter of the NP (in "
                    "nm)")
parse.add_argument("length", type=float, nargs="?", help="the length of the NR "
                    "(in nm). This must be defined for nanorod calculations.")
parse.add_argument("-NR", "--nanorods", action="store_true", help="perform "
                    "nanorod calculations. Th")
parse.add_argument("-v", "--verbose", action="store_true", help="increase "
                    "detail of output")
# parse the arguments passed in the command line
args = parse.parse_args()

# check that sensible input values have been given
if(args.diameter <= 0 or args.concentration <= 0 or args.target_area <= 0):
    sys.exit("Error: You must provide positive values for each input! \n")

# run nanorod calculations if the optional nanorods flag has been used
if args.nanorods:
    # check that sensible input values have been given
    if(args.length <= 0):
        sys.exit("Error: You must provide positive values for each input! \n")

    print("Nanorods calculator selected \n")
    # use the nano_calcs formulae to calculate the area of a nanorod
    area = calcs.area_NR(args.length, args.diameter)

else:
    # use the nano_calcs formulae to calculate the area of a nanoparticle
    area = calcs.area_NP(args.diameter)

# use the nano_calcs formulae to calculate the required number, mols, and volume
# of the nanoparticles, and volumes of DNA and PEG to be added
number = calcs.number_NP(area, args.target_area)
mols = calcs.mols_NP(number)
volume = calcs.volume_NP(args.concentration, mols)
vol_DNA = calcs.volume_DNA(args.target_area)
vol_PEG = calcs.volume_PEG(args.target_area)

# decide how much of this info to output, depending whether the user wants
# verbosity
if args.verbose:
    print("For", args.target_area, "cm^2: \n")
    print("The area of a single nanoparticle is", "%.4E" % area, "cm^2 \n")
    print("The required number of nanoparticles is", "%.4E" % number, "\n")
    print("The required nanomoles of nanoparticles is", "%.4E" % (mols*1e9), "\n")
    print("The required volume of", args.concentration, "nM nanoparticle "
        "solution is", "%.1f" % volume, "uL \n")
    print("The required volume of 10uM DNA solution is", "%.1f"
        % vol_DNA, "uL \n")
    print("The required volume of 5mg/mL sulfo-NHS-PEG5k-diazirine solution is",
        "%.1f" % vol_PEG, "uL \n")

else:
    print("Use", "%.1f" % volume, "uL GNP,", "%.1f" % vol_DNA, "uL DNA, and "
        "%.1f" % vol_PEG, "uL PEG for", args.target_area, "cm^2 \n \nFor more "
        "details, try including the optional verbosity flag '-v' in your input"
         "\n")
