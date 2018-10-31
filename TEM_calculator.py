# author: Ben Stordy
# python based TEM image calculator

# imports sys module allowing for error handling
# imports the argparse module, allowing for command line input.
# imports pandas module allowing for excel sheet handling
import sys
import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt

print("running TEM sizing calculator ... \n")

# define parse to be the funtion ArgumentParser from the argparse module
parse = argparse.ArgumentParser()

# use the add_argument function to specify which command line options the
# calculator will accept.
parse.add_argument("filename", type=str, help="the filename of your excel "
                    "sheet. This cannot contain spaces.")
parse.add_argument("sheetname", type=str, nargs="?", default="Sheet1", help=
                    "The name of the sheet in the excel file that contains the "
                    "data to be analysed. By default this is 'Sheet1'.")
parse.add_argument("-p", "--plot", action="store_true", help="plot histogram of"
                    " the data.")
# parse the arguments passed in the command line
args = parse.parse_args()

# check that sensible input values have been given
# if(args.filename ):
#     sys.exit("Error: You must provide an excel file as your input! \nUse the"
#         " help flag '-h' if you need help using the calculator.\n")

# get the path to the file (will vary for different users)
# path =("~/Documents/Academic/OneDrive/OneDrive\ -\ University\ of\ Toronto/"
#    "Data/"+args.filename)

# load the spreadsheet
xl = pd.ExcelFile(args.filename)
TEM_df = xl.parse(args.sheetname)

# get the conversion factor from pixels to nanometres
factors = TEM_df.scale/TEM_df.length
# create a new column called factor, and fill it with the conversion factors for
# each scale bar measurement (skip nanoparticle measurement rows)
TEM_df['factor'] = factors.where(TEM_df.img.notnull())
# fill the nanoparticle measurement rows with its own scale factor determined
# above
TEM_df['factor'] = TEM_df['factor'].fillna(method='ffill')
# use the scale factor to convert from a pixel length to the size in nanometres
TEM_df['size'] = TEM_df.length*TEM_df.factor
# get the rows of the 'size' column that do not contain scalebar measurements
TEM_df = TEM_df['size'][TEM_df['scale'].isnull()]
# separate the odd and even elements of the size
TEM_df = pd.DataFrame({ 'nm_length' : TEM_df.iloc[::2], 'nm_width' :
                            TEM_df.iloc[1::2]})
# create a new dataframe to hold the lengths of the nanorods
nm_measured_df = TEM_df.dropna(subset = ['nm_length']).reset_index(drop=True)
# create a new dataframe to hold the widths of the nanorods
nm_width = TEM_df.dropna(subset = ['nm_width']).reset_index(drop=True)
# combine the widths and lengths side-by-side for each measured nanorod
nm_measured_df['nm_width'] = nm_width['nm_width']
# calculate the aspect ratio of each nanorod
nm_measured_df['nm_AR'] = nm_measured_df.nm_length/nm_measured_df.nm_width

means = nm_measured_df.mean()
stdDev = nm_measured_df.std()
results = pd.DataFrame({'parameter':means.index, 'mean':means.values, 'std dev':
                        stdDev.values})
n = nm_measured_df.count()
print(results, '\nnumber of observations: ', n[1])

if args.plot:
    nm_measured_df.hist()
    plt.show()
