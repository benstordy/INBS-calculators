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
parse.add_argument("filename", type=str, help="The filename of your excel "
                    "sheet. This cannot contain spaces.")
parse.add_argument("sheetname", type=str, nargs="?", default="Sheet1", help=
                    "(Optional) The name of the sheet in the excel file that "
                    "contains the data to be analysed. By default this is "
                    "'Sheet1'.")
parse.add_argument("output", type=str, nargs="?", default="output.xlsx", help=
                    "(Optional) The desired name of the output excel file. By "
                    "default this is 'ouput.xlsx'.")
parse.add_argument("-p", "--plot", action="store_true", help="Plot histogram of"
                    " the data.")
parse.add_argument("-s", "--save", action="store_true", help="Save data to an "
                    " excel file.")
# parse the arguments passed in the command line
args = parse.parse_args()

# get the path to the file (will vary for different users)
# path =("~/Documents/Academic/OneDrive/OneDrive\ -\ University\ of\ Toronto/"
#    "Data/"+args.filename)

# load the spreadsheet
xl = pd.ExcelFile(args.filename)
TEM_df = xl.parse(args.sheetname)
writer = pd.ExcelWriter(args.output)

# check that each image has a corresponding scale factor
if (sum(TEM_df.img.notnull()) != sum(TEM_df.scale.notnull())):
    sys.exit("Some of your images do not have corresponding scale factors. "
            "Please add the missing scale factors. \n")

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
size_df = TEM_df['size'][TEM_df['scale'].isnull()]
# separate the odd and even elements of the size
size_df = pd.DataFrame({ 'length_nm' : size_df.iloc[::2], 'width_nm' :
                            size_df.iloc[1::2]})

# create a new dataframe to hold the lengths of the nanorods
measured_nm_df = size_df.dropna(subset = ['length_nm']).reset_index(drop=True)
# create a new dataframe to hold the widths of the nanorods
width_nm = size_df.dropna(subset = ['width_nm']).reset_index(drop=True)
# combine the widths and lengths side-by-side for each measured nanorod
measured_nm_df['width_nm'] = width_nm['width_nm']
# calculate the aspect ratio of each nanorod
measured_nm_df['AR_nm'] = measured_nm_df.length_nm/measured_nm_df.width_nm

# apply some statistics
means = measured_nm_df.mean()
stdDev = measured_nm_df.std()
n = measured_nm_df.count()

# create a results dataframe
results = pd.DataFrame({'parameter':means.index, 'mean':means.values, 'std dev':
                        stdDev.values, 'N':n.values})
# output the results
print(results)

# save the data if desired
if args.save:
    results.to_excel(writer, sheet_name='results')
    measured_nm_df.to_excel(writer, sheet_name='measurements')
    TEM_df.to_excel(writer, sheet_name='data')

    writer.save()

# plot a histogram if desired
if args.plot:
    measured_nm_df.hist()
    plt.show()
