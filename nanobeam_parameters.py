# Nanobeam Geometric Parameters Generator
# Author: Ruchir Tullu

# This program generates a set of nanobeam geometry parameters to be used in numerical simulations (e.g. COMSOL Multiphysics)
# There are a set of tunable parameters one may change such that the resulting nanobeam geometry changes accordingly
# The parameters are then returned in a .txt file for easy viewing and accessing
# To run the program, simple type the desired parameters below and compile as usual
# Can be used in conjunction with an Excel spreadsheet to visualize and organize the data in a way the numerical simulation program understands

# Instructions for running program and using the generated data in Excel & COMSOL Multiphysics:
# 1) Choose appropriate parameters below
# 2) Run program (compile)
# 3) Copy-paste data lists from generated text file to an Excel spreadsheet
# 4) Use "Text to Columns" option under "Data" tab in Excel to convert data into columns
# 5) In the pop-up wizard, choose "Delimited", with the delimiters being "Tab", "Comma". Choose the format as "General".
# 6) Copy the generated columns; choose a location to paste, and do: "paste special" -> "transpose"
# 7) In COMSOL, under the "Parameters" section, choose "Load from file" and select the Excel spreadsheet
# 8) Choose the appropriate columns/rows. Note that the format COMSOL prefers in adjacent columns is: [name][value[units]][description]
# 9) Note that the column next to the data chosen from the spreadsheet is the description of the parameter (data chosen) if left unselected


import math
import datetime


# Tunable parameters:

beam_length = 4 * 10**(-3)  #Scale of 10^0 [mm], this is the total nanobeam length
beam_width_narrowest = 400 * 10**(-9)  #Scale of 10^2 [nm], this is the minimum beam width near the central defect
beam_thickness = 20 * 10**(-9)  #Scale of 10^1 [nm], this parameter is not explicitly used in this program, just for reference
N_unit_cells = 50  #This is the number of unit cells in the nanobeam, typically less than 100, must be an even number
alpha_width = 0.15  #Parameter used in the calculation of the beam width, ranges from 0.15 to 0.2
i_0 = 8  #Parameter used in the calculation of the beam width, ranges from 8 to 10
L_d = 50 * 10**(-6)  #Scale of 10^1 [um], Central defect length, this typically ranges from the 10s to 100 um
length_units = ' [m] '   #Unit of meters, this is used in a function to generate numbers easily recognizable by COMSOL
file_name = "nanobeam_geometry_parameters" + "_" + str(N_unit_cells) + "_unit_cells.txt"    #File name generated based on unit cell numbers



# Generating width:
def nanobeam_unitcell_widths(N_unit_cells, beam_width_narrowest):
    width_list = []
    for i in range(0, int(N_unit_cells/2)): #Generates an empty list for storage of widths
        width_list.append([None, None])  #Creates a list of lists with the indices i,j denoting the unit cell # and whether it is a local max or min, respectively

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

    return width_list   #Half of the beam widths, because it is symmetric across the central defect



# Sum elements of a list:
def sum_list(L):    #Testing function
    accum = 0
    for element in L:
        accum += element
    return accum



# Generating lengths:
def nanobeam_unitcell_lengths(N_unit_cells, beam_length):
    length_list = [None] * int(N_unit_cells/2)  #Initialize length list
    width = nanobeam_unitcell_widths(N_unit_cells, beam_width_narrowest)  #List of lists of half of the nanobeam unit cell widths, from before
    m = 0.5 * 10**(-6)   #initialize multiplicative factor for scaling length parameters
    optimization_factor = 0 #initialize quantity to help determine m
    allowed_half_length_total = (beam_length - L_d)/2    # Allowed length for one half of the unit cells on the nanobeam

    for i in range(0, int(N_unit_cells/2)):
        optimization_factor += 1/(math.sqrt(width[i][0]))

    m = allowed_half_length_total/optimization_factor

    for i in range(0, int(N_unit_cells/2)):     #Scale the lengths accordingly as per the respective width of the unit cell
        length_list[i] = 1/(math.sqrt(width[i][0])) * m     # Lc(i) ~ 1/(sqrt(w_max(i)), the multiplicative factor of m is chosen such that the allowed_helf_length_total matches the length_list total

    return length_list  #Half of the beam length, because it only used half of the beam widths



# List splitting function:
def return_two_lists(L):    #takes in a list of lists in the form [ [,], [,], [,],...] and returns two lists depending on which index the item is in in the inner list
    L_index_0 = []
    L_index_1 = []  #initiate lists to store data

    for i in range(0, len(L)):
        L_index_0.append(L[i][0])
        L_index_1.append(L[i][1])

    return L_index_0, L_index_1



# Add units to values in a list:
def add_units_to_parameter_list(parameter_list, unit):     #Function for adding units (e.g.: [m]) to each index of a list. Unit must be a string, pre-declared
    index_list = [None] * (len(parameter_list))     #One less comma than the number of elements in a list
    index = 0   #Initialize index
    updating_index = 0  #Initialize index to be updated in loop
    str_parameter_list = str(parameter_list)    #Easier to work with it in string form

    for i in range(0, len(index_list)):
        if(i==0):
            index = str_parameter_list.find(",")    #Look for index of comma that separates the numbers
            index_list[i] = index   #Add to index list
            str_parameter_list = str_parameter_list[:index] + unit + str_parameter_list[index:]     #Slicing notation, adds unit after the number
        else:
            updating_index = str_parameter_list.find(",", index_list[i-1] + 6 )   #Shifts index in string such that next comma can be considered without repetition
            index_list[i] = updating_index  #Update index list
            str_parameter_list = str_parameter_list[:updating_index] + unit + str_parameter_list[updating_index:]     #Slicing notation, adds unit after the number

    return str_parameter_list



# Helper function to sum a list till a certain index:
def sum_list_till_particular_index(lst, start_index, stop_index):
    accumulator = 0

    if (stop_index < start_index):  # Edge case, this is the intended functionality; for the first unit cell
        return 0

    if (stop_index == start_index): # For the second unit cell
        return lst[0]

    for i in range(start_index, stop_index+1):  #changed to +1 because range discards last index
        accumulator += lst[i]

    return accumulator



# Generating positions of half unit cells (maximum and minimum widths within a unit cell)(center):
def generate_positions_of_half_unit_cells(N_unit_cells, L_d, length_list):      # Works for the origin centered at the center of the central defect in the nanobeam
    position_list_max = [None] * int(N_unit_cells/2)    # Max positions of w_max(i)
    position_list_min = [None] * int(N_unit_cells/2)    # Min positions of w_min(i)
    counter = 1     # To remember if the half-unit cell is max or min width; start is always from max (immediately after the central defect)
    max_index_counter = 0   #To index the max position list
    min_index_counter = 0   #To index the max position list
    length_counter = 0      #To index the length_list

    for i in range(0, N_unit_cells):
        if (counter%2 != 0):    #max width
            position_list_max[max_index_counter] = (L_d/2) + sum_list_till_particular_index(length_list, 0, length_counter-1) + (length_list[length_counter]/2) + (length_list[length_counter]/4)
            max_index_counter += 1  #Update index counter

        if (counter%2 == 0):     #min width
            position_list_min[min_index_counter] = (L_d/2) + sum_list_till_particular_index(length_list, 0, length_counter-1) + (length_list[length_counter]/2) - (length_list[length_counter]/4)
            min_index_counter += 1  #Update index counter
            length_counter += 1     #Update length_counter only if a min pair to the max has been reached (since both use same length Lc(i) value)

        counter += 1    #Update counter once a loop has been done so that the appropriate sub-loop triggers next iteration (max/min)

    return position_list_max, position_list_min   # position of ith unit cell, max or min, i = 0, i, 2, ... N_unit_cell/2



# Generating positions of unit cells (center):
def generate_positions_of_unit_cells(N_unit_cells, L_d, length_list):  # Works for the origin centered at the center of the central defect in the nanobeam
    position_list = [None] * int(N_unit_cells/2)    #Generate half of the lengths, symmetric about the central defect

    for i in range(0, int(N_unit_cells/2)):
        position_list[i] = (L_d/2) + sum_list_till_particular_index(length_list, 0, i-1) +(length_list[i]/2)

    return position_list    # position of ith unit cell, i = 0, i, 2, ... N_unit_cell/2





# Generate data:

length_parameters = nanobeam_unitcell_lengths(N_unit_cells, beam_length)
print("Length Parameters:\n")
print(length_parameters)


width_parameters = nanobeam_unitcell_widths(N_unit_cells, beam_width_narrowest)
print("\n Width Parameters:\n")
print(width_parameters)


length_sum = sum_list(length_parameters)
print("\n Length sum:", length_sum)       # We expect this to be around 2mm, or half of the total beam width
print("0.5*(Beam length - L_d) - Length sum:", 0.5* (beam_length - L_d) - length_sum)   # If the lengths are correctly computed, then this should be zero, or very small due to floating point error


w_max, w_min = return_two_lists(width_parameters)   #Seperates the max and min width parameters into two lists


unit_cell_positions = generate_positions_of_unit_cells(N_unit_cells, L_d, length_parameters)
half_unit_cell_position_max, half_unit_cell_position_min = generate_positions_of_half_unit_cells(N_unit_cells, L_d, length_parameters)

print("\n Unit cell positions: \n")
print(unit_cell_positions)
print("\n Half unit cell positions max: \n")
print(half_unit_cell_position_max)
print("\n Half unit cell positions min: \n")
print(half_unit_cell_position_min)


# Write data generated to a .txt file:
file1 = open(file_name, "w")

# String format of lists that hold the generated data to be printed to the text file. Function adds units and converts to string format to be printed.
L_width_parameters = add_units_to_parameter_list(width_parameters, length_units)  #str(width_parameters)
L_length_parameters = add_units_to_parameter_list(length_parameters, length_units)  #str(length_parameters)
L_w_max = add_units_to_parameter_list(w_max,length_units)  #str(w_max)
L_w_min = add_units_to_parameter_list(w_min, length_units)  #str(w_min)
L_unit_cell_positions = add_units_to_parameter_list(unit_cell_positions, length_units)  #str(unit_cell_positions)
L_half_unit_cell_position_max = add_units_to_parameter_list(half_unit_cell_position_max, length_units)  #str(half_unit_cell_position_max)
L_half_unit_cell_position_min = add_units_to_parameter_list(half_unit_cell_position_min, length_units)  #str(half_unit_cell_position_min)

date = datetime.date.today()
print(date)


# \n is placed to indicate EOL (End of Line)
file1.writelines("The generated parameters for the nanobeam include: unit cell widths, unit cell lengths, unit cell positions, and relevant program parameters used. \n \n")
file1.writelines("\n \n Date Modified: ")
file1.writelines(str(date))
file1.writelines('\n \n \n \n Width list [[w_max(i,j), w_min(i,j)]]: \n \n')
file1.writelines(L_width_parameters)
file1.writelines('\n \n \n Length list [L_c(i)]: \n \n')
file1.writelines(L_length_parameters)
file1.writelines("\n \n \n Length sum (should be very close to beam length): ")
file1.writelines(str(length_sum)+ '[m]')
file1.writelines("\n \n 0.5*(Beam length - L_d) - Length sum (should be <<1):")
file1.writelines(str(0.5* (beam_length - L_d) - length_sum)+ '[m]')
file1.writelines("\n \n \n \n Unit cell width maximums (w_max(i)): \n \n")
file1.writelines(L_w_max)
file1.writelines("\n \n \n Unit cell width minimums (w_min(i)): \n \n")
file1.writelines(L_w_min)
file1.writelines("\n \n \n Unit cell positions: \n \n")
file1.writelines(L_unit_cell_positions)
file1.writelines("\n \n \n Unit cell half cell positions (max widths): \n \n")
file1.writelines(L_half_unit_cell_position_max)
file1.writelines("\n \n \n Unit cell half cell positions (min widths): \n \n")
file1.writelines(L_half_unit_cell_position_min)
file1.writelines("\n \n \n \n \n Parameters used: ")
file1.writelines("\n \n Central defect length: ")
file1.writelines(str(L_d)+ '[m]')
file1.writelines("\n \n Beam length: ")
file1.writelines(str(beam_length) + '[m]')
file1.writelines("\n \n Minimum beam width: ")
file1.writelines(str(beam_width_narrowest)+ '[m]')
file1.writelines("\n \n Beam thickness: ")
file1.writelines(str(beam_thickness)+ '[m]')
file1.writelines("\n \n Number of unit cells: ")
file1.writelines(str(N_unit_cells))
file1.writelines("\n \n Parameters used for tapering the width of the beam: ")
file1.writelines("\n \n alpha_width: ")
file1.writelines(str(alpha_width))
file1.writelines("\n \n i_0: ")
file1.writelines(str(i_0))


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

# print(L_width_parameters[4])
#  OUT: 2

# l = [[1,2],[3,4],[5,6]]
#
# l1, l2 = return_two_lists(l)
# print(l1)
# print(l2)

# lst1 = [1, 2,3, 4, 5]
#
# print("lstsum ", sum_list_till_particular_index(lst1, 2, len(lst1)))
# OUT: 12


# Precursor/ideas to add_units_to_parameter_list() function:

# print(L_w_max)
# index = L_w_max.find(',')
# L_w_max = L_w_max[:index] + ' [m] ' + L_w_max[index:]
# index1 = L_w_max.find(',', index+6)
# L_w_max = L_w_max[:index1] + ' [m] ' + L_w_max[index1:]
# index2 = L_w_max.find(",", index1+6)
# L_w_max = L_w_max[:index2] + ' [m] ' + L_w_max[index2:]
#
# print(index)
# print(index1)
# print(index2)
# print(L_w_max)
# print(len(w_max))

# new_string = add_units_to_parameter_list(w_max, length_units)
# print("\n\nnew\n", new_string)

# Checking file name:
# tst = 40
# print("nanobeam" + "_" + str(tst))