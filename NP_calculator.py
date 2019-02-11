# author: Ben Stordy
# python based NP and NR calculator
# outputs required DNA, PEG and GNP or GNR for a given size, concentration,
# and surface area of particles

# imports sys module allowing for error handling
import sys

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
parse.add_argument("length", type=float, nargs="?", default=0, help="the length"
                    " of the NR (in nm). This must be defined for nanorod "
                    "calculations.")
parse.add_argument("-NR", "--nanorods", action="store_true", help="perform "
                    "nanorod calculations. Th")
parse.add_argument("-v", "--verbose", action="store_true", help="increase "
                    "detail of output")
# parse the arguments passed in the command line
args = parse.parse_args()

# check that sensible input values have been given
if(args.diameter <= 0 or args.concentration <= 0 or args.target_area <= 0):
    sys.exit("Error: You must provide positive values for each input! \nUse the"
        " help flag '-h' if you need help using the calculator.\n")

# run nanorod calculations if the optional nanorods flag has been used
if args.nanorods:
    # check that sensible input values have been given
    if(args.length <= 0):
        sys.exit("Error: You must provide positive values for each input! \nUse"
            " the help flag '-h' if you need help using the calculator. \n")

    print("Nanorods calculator selected. Particle width = " "%.1f" %
        args.diameter, "nm, particle length =" "%.1f" % args.length ,"nm. \n")
    # use the nano_calcs formulae to calculate the area of a nanorod
    area = calcs.area_NR(args.length, args.diameter)
    # use the nano_calcs formulae to calculate the area of a nanorod with DNA
    # conjugated to its surface (DNA length is 25bp which is ~8nm on each side)
    conj_area = calcs.area_NR(args.length+8*2, args.diameter+8*2)
else:
    print("Spherical NP calculator selected. Particle diameter = ", "%.1f" %
        args.diameter, "nm. \n")
    if(args.length != 0):
        sys.exit("Error: you provided a length argument, but are running a "
        "spherical nanoparticle calculator!\nUse the help flag -h if you need "
        "help using the calculator.\n")
    # use the nano_calcs formulae to calculate the area of a nanoparticle
    area = calcs.area_NP(args.diameter)
    # use the area_NP formula to calculate the area of a nanoparticle with
    # DNA & PEG conjugated to its surface (~10 nm increase on each side)
    conj_area = calcs.area_NP(args.diameter+10*2)

# use the nano_calcs formulae to calculate the required number, mols, and volume
# of the nanoparticles, and volumes of DNA and PEG to be added
num_NP = calcs.number_NP(area, args.target_area)
mols = calcs.mols_NP(num_NP)
volume = calcs.volume_NP(args.concentration, mols)
num_SA = calcs.number_SA(conj_area, num_NP)
vol_SA = calcs.volume_SA(conj_area, num_NP)
vol_xlink = calcs.volume_xlink(conj_area, num_NP)
vol_DNA = calcs.volume_DNA(args.target_area)
vol_DNA_XS = vol_DNA*1.6
vol_PEG = calcs.volume_PEG(args.target_area)

# decide how much of this info to output, depending whether the user wants
# verbosity
if args.verbose:
    print("For", args.target_area, "cm^2: \n")
    print("The area of a single nanoparticle is", "%.4E" % area, "cm^2 \n")
    print("The required number of nanoparticles is", "%.4E" % num_NP, "\n")
    print("The required nanomoles of nanoparticles is", "%.4E" % (mols*1e9),
        "\n")
    print("The required volume of", args.concentration, "nM nanoparticle "
        "solution is", "%.1f" % volume, "uL \n")
    print("The required volume of 10uM DNA solution (60% excess) is", "%.1f"
        % vol_DNA_XS, "uL \n")
    print("The required volume of 5g/L SH-PEG5k-biotin solution is",
        "%.1f" % vol_PEG, "uL \n")
    print("The required number of streptavidins is", "%.4E" % (num_SA), "\n")
    print("The required volume of 5g/L streptavidin solution with 30x excess is"
        , "%.1f" % (30*vol_SA), "uL \n")
    print("The required volume of 5g/L Sulfo-NHS-PEG4-diazirine solution with "
        "125x excess is", "%.1f" % (125*vol_xlink), "uL \n")

else:
    print("Use", "%.1f" % volume, "uL GNP,", "%.1f" % vol_DNA, "uL DNA,", "%.1f"
        % vol_PEG, "uL PEG, " "%.1f"% (25*vol_SA), "uL streptavidin,", "%.1f" %
        (125*vol_xlink), "uL crosslinker for", args.target_area, "cm^2 \n \n"
        "For more details, try including the optional verbosity flag '-v' in"
        "your input \n")
