# Nanobeam Geometric Parameters Generator
# Author: Ruchir Tullu

# This program generates a set of nanobeam geometry paremeters to be used in numerical simulations (e.g. COMSOL Multiphysics)
# There are a set of tunable parameters one may change such that the resulting nanobeam geometry changes accordingly
# The parameters are then returned in a .txt file for easy viewing and accessing
# To run the program, simple type the desired parameters below and compile as usual

import math


# Tunable parameters:

beam_length = 4 * 10**(-3)  #[mm]
beam_width_narrowest = 400 * 10**(-9)  #[nm], this is the minimum beam width near the central defect
beam_thickness = 20 * 10**(-9)  #[nm], this parameter is not explicitly used in this program, just for reference
N_unit_cells = 38  #This is the number of unit cells in the nanobeam, typically less than 100, must be an even number
alpha_width = 0.15  #Parameter used in the calculation of the beam width, ranges from 0.15 to 0.2
i_0 = 8  #Parameter used in the calculation of the beam width, ranges from 8 to 10



# Generating width:

def nanobeam_unitcell_widths(N_unit_cells, beam_length, beam_width_narrowest):
    width_list = []
    for i in range(0, int(N_unit_cells/2)):
        width_list.append([[None, None]])  #Creates a list of lists with the indices i,j denoting the unit cell # and whether it is a local max or min, respectively
        # width_list = [[None, None] * int(N_unit_cells/2)]    #Generates an empty list for storage of widths

    for i in range(0, int(N_unit_cells/2)):  #/2 because the beam widths are symmetric across the central defect

        if((i%2) == 0):   #even index, local maximum
            if(i == 0):   #first maximum
                width_list[i][0] = beam_width_narrowest * 2.3
            else:
                width_list[i][0] = ((1 - (1-alpha_width)*(math.exp(-((i**2)/(i_0**2)))))/(1 - (1-alpha_width)*(math.exp(-(((i-1)**2)/(i_0**2)))))) * width_list[i-1][0]

        if((i%2) !=0):   #odd index, local minimum
            if(i==1):   #first minimum
                width_list[i][1] = beam_width_narrowest
            else:
                width_list[i][1] = (width_list[i-1][0])/2.3

    # width_list += width_list
    return width_list


test = nanobeam_unitcell_widths(N_unit_cells, beam_length, beam_width_narrowest)
print(test)










list = str([1,2,3])
# Program to show various ways to read and
# write data in a file.
file1 = open("nanobeam_geometry_parameters.txt", "w")

L_test = str(test)
# \n is placed to indicate EOL (End of Line)
file1.writelines('Width list: \n')
file1.writelines(L_test)
file1.writelines("\n\ntest\n")
file1.writelines(list)
file1.close()  # to change file access modes






# Test code:

# for i in range(0, N_unit_cells):
#     print(1 - (1-alpha_width)*(math.exp(-((i**2)/(i_0**2)))))

# width_list = []
# for i in range(0, int(38 / 2)):
#     width_list.append([None, None])
# print(width_list)








