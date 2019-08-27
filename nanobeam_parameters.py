# Nanobeam Geometric Parameters Generator
# Author: Ruchir Tullu

# This program generates a set of nanobeam geometry parameters to be used in numerical simulations (e.g. COMSOL Multiphysics)
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
L_d = 50 * 10**(-6)  #[um], Central defect length, this typically ranges from the 10s to 100 um



# Generating width:

def nanobeam_unitcell_widths(N_unit_cells, beam_width_narrowest):
    width_list = []
    for i in range(0, int(N_unit_cells/2)):
        width_list.append([None, None])  #Creates a list of lists with the indices i,j denoting the unit cell # and whether it is a local max or min, respectively
        # width_list = [[None, None] * int(N_unit_cells/2)]    #Generates an empty list for storage of widths

    for i in range(0, int(N_unit_cells / 2)):  # /2 because the beam widths are symmetric across the central defect
        for j in range(0, 2):  #Iterate across inner indices

            if((j%2) == 0):   #even index, local maximum
                if(i == 0):   #first maximum
                    width_list[i][0] = beam_width_narrowest * 2.3
                else:   #Scale the width of the subsequent unit cell based on the Gaussian envelope:
                    width_list[i][0] = ((1 - (1-alpha_width)*(math.exp(-((i**2)/(i_0**2)))))/(1 - (1-alpha_width)*(math.exp(-(((i-1)**2)/(i_0**2)))))) * width_list[i-1][0]

            if((j%2) != 0):   #odd index, local minimum
                if(i == 0):   #first minimum
                    width_list[i][1] = beam_width_narrowest
                else:
                    width_list[i][1] = (width_list[i-1][0])/2.3

    # width_list += width_list
    return width_list   #Half of the beam widths, because it is symmetric across the central defect


def sum_list(L):    #Testing function
    accum = 0
    for element in L:
        accum += element
    return accum


# Generating lengths:
def nanobeam_unitcell_lengths(N_unit_cells, beam_length):
    length_list = [None] * int(N_unit_cells/2)  #Initialize length list
    width = nanobeam_unitcell_widths(N_unit_cells, beam_width_narrowest)  #List of lists of half of the nanobeam unit cell widths, from before
    m = 0.5 * 10**(-6)   #initialize multiplicative factor for convergence loop of length parameters
    optimization_factor = 0 #initialize quantity to help determine m
    allowed_half_length_total = (beam_length - L_d)/2    # Allowed length for one half of the unit cells on the nanobeam

    for i in range(0, int(N_unit_cells/2)):
        optimization_factor += 1/(math.sqrt(width[i][0]))

    m = allowed_half_length_total/optimization_factor

    for i in range(0, int(N_unit_cells/2)):     #Scale the lengths accordingly as per the respective width of the unit cell
        length_list[i] = 1/(math.sqrt(width[i][0])) * m     # Lc(i) ~ 1/(sqrt(w_max(i)), the multiplicative factor of m is chosen such that the allowed_helf_length_total matches the length_list total

    return length_list  #Half of the beam length, because it only used half of the beam widths





# Testing:

length_parameters = nanobeam_unitcell_lengths(N_unit_cells, beam_length)
print("Length Parameters:\n")
print(length_parameters)


width_parameters = nanobeam_unitcell_widths(N_unit_cells, beam_width_narrowest)
print("\n Width Parameters:\n")
print(width_parameters)


length_sum = sum_list(length_parameters)
print("\n Length sum:", length_sum)       # We expect this to be around 2mm, or half of the total beam width
print("0.5*(Beam length - L_d) - Length sum:", 0.5* (beam_length - L_d) - length_sum)   # If the lengths are correctly computed, then this should be zero, or very small due to floating point error


# Write data generated to a .txt file:
file1 = open("nanobeam_geometry_parameters.txt", "w")

L_width_parameters = str(width_parameters)
L_length_parameters = str(length_parameters)

# \n is placed to indicate EOL (End of Line)
file1.writelines('Width list [[w_max(i,j), w_min(i,j)]]: \n \n')
file1.writelines(L_width_parameters)
file1.writelines('\n \n Length list [L_c(i)]: \n \n')
file1.writelines(L_length_parameters)

file1.close()  # to change file access modes






# Test code:

# for i in range(0, N_unit_cells):
#     print(1 - (1-alpha_width)*(math.exp(-((i**2)/(i_0**2)))))


# width_list = []
# for i in range(0, int(38 / 2)):
#     width_list.append([None, None])
# print(width_list)


# for i in range(0,2):
#     print(i)

#     OUT: 0,1


# for i in range(0, int(N_unit_cells/2)):
#     print(i)

#     OUT: 0-18




