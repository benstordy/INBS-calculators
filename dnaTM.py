# Python based oligo analyzer
# Get command line arguments
import sys
print("Running", sys.argv[0])

# checks to make sure BioPython is installed
try:
    import Bio
except ImportError:
    sys.exit("BioPython module must be installed")

# Parsing the arguments
# initializing parsing
import argparse
#instantiate the parser
parser = argparse.ArgumentParser()
parser.add_argument("Sequence", type=str, help="Enter the DNA sequence here")
parser.add_argument("Na", type=float, nargs='?', default=50, help="Enter the sodium ion concentration (mM) here, the default is 50 mM")
parser.add_argument("K", type=float, nargs='?', default=0, help="Enter the potassium ion concentration(mM) here, the default is 0 mM")
parser.add_argument("Tris", type=float, nargs='?', default=0, help="Enter the Tris ion concentration(mM) here, the default is 0 mM")
parser.add_argument("Mg", type=float, nargs='?', default=0, help="Enter the magnesium ion concentration(mM) here, the default is 0 mM")
parser.add_argument("dNTPs", type=float, nargs='?', default=0, help="Enter the nucleotide concentration (mM) here, the default is 0 mM")
parser.add_argument("dnac1", type=float, nargs='?', default=250, help="Enter the DNA strand concentration (nM) here, the default is 250 nM")
args = parser.parse_args()

#Checks that a DNA sequence is given
#defining a set of allowed characters
allowed_chars = set('ATGCatgc')
if set(args.Sequence).issubset(allowed_chars):
    #assigns sequence information as mystring
    mystring = args.Sequence
    print("My DNA sequence is", mystring)
else :
    sys.exit("A valid DNA sequence is not given.")

#Print sodium concentration
print("The sodium ion concentration is", args.Na, "mM.")
#print potassium concentration
print("The potassium ion concentration is", args.K, "mM.")
#print Tris concentration
print("The tris ion concentration is", args.Tris, "mM.")
#print Mg concentration
print("The magnesium ion concentration is", args.Mg, "mM.")
#print dNTPs concentration as nucleotide if prsent, otherwise it is 0 mM
print("The nucleotide concentration is", args.dNTPs, "mM.")
#print dnac1 concentration as dna
print("The dna concentration is", args.dnac1, "nM.")

# imports utility functions for meltingtemperature
from Bio.SeqUtils import MeltingTemp as mt
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna
myseq = Seq(mystring, generic_dna)
print("The melting temperature is", '%0.3f'% mt.Tm_NN(myseq, Na=args.Na, K=args.K, Tris=args.Tris, Mg=args.Mg, dNTPs=args.dNTPs, dnac1=args.dnac1), "C based on nearest neighbor dynamics using SantaLucia (1997) parameters.")
print("The melting temperature is", '%0.3f'% mt.Tm_NN(myseq, nn_table=mt.DNA_NN4, Na=args.Na, K=args.K, Tris=args.Tris, Mg=args.Mg, dNTPs=args.dNTPs, dnac1=args.dnac1), "C based on nearest neighbor dynamics using SantaLucia (2004) parameters.")

# prints out the reverse complement of the DNA
print("The reverse complement of the DNA is", myseq.reverse_complement())
