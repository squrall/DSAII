#John Lemire 001043932
"""
This files contains modules to gather and calculate distances from locations

class Location - Object containing pertinant information about locations
"""

import math
import xlrd

path = ".\WGUPS Distance Table.xlsx"

# Containers to hold inported location data
# location_matrix generations O(n^2)

Location_Matrix = [[0 for x in range(35)] for y in range(35)]
Location_List = []

# Class - Location
#
# __init__
# takes name address and index and creates object
#
# get_index
# returns location index
#
# get_address
# returns location address

class Location:
    def __init__(self, name, address, index):
        if name == '3575 W Valley Central Sta bus Loop':
            self.name == '3575 W Valley Central Station bus Loop'
        else:
            self.name = name
        self.address = address
        self.index = index

    def get_index(self):
        return self.index
    def get_address(self):
        return self.address

# Method - add_all_locations() O(n^2)
# opens Excel file and imports all location data into Location_Matrix

def add_all_locations():
    workbook = xlrd.open_workbook(path)
    location_sheet = workbook.sheet_by_index(0)
    location_sheet.cell_value(0, 0)
    num_rows = location_sheet.nrows
    scanning_x = 8 # set to 8 because that's the row when pertinent location data starts

    name = []
    address = []
    city = []
    state = []
    zip = []
    contents = []

    #this is the part that makes this methods complexity O(n^2)

    while scanning_x < num_rows:
        contents = location_sheet.cell_value(scanning_x,0).splitlines()
        Location_List.append(Location(contents[0],contents[1],scanning_x))

        scanning_y = 2 # set to 2 because that's the column in which pertinent data starts appearing

        while location_sheet.cell_value(scanning_x,scanning_y) != 0:
            Location_Matrix[scanning_x][scanning_y+6] = location_sheet.cell_value(scanning_x,scanning_y)
            scanning_y = scanning_y + 1

        scanning_x = scanning_x + 1

# Method - get_loc_list() O(1)
# returns location_list

def get_loc_list():
    return Location_List

# Method - get_one_loc() O(1)
# returns location at index(int)

def get_one_loc(int):
    return Location_List[int]

# Method - get_distance_address() O(1)
# returns distance between two address
# uses next method to simplify things

def get_distance_address(address1, address2):
    distance = get_distance_index(get_index(address1),get_index(address2))
    return distance

# Method - get_distance_index() O(1)
# returns distance

def get_distance_index(index1, index2):
    if index1 > index2:
        return Location_Matrix[index1][index2]
    else:
        return Location_Matrix[index2][index1]

# Medthod - get_index() O(1)
# returns the index of the location via address

def get_index(address):
    addy_trimmed = address.strip()

    for location in Location_List:
        if (location.address).strip() == addy_trimmed:
            return location.index

# Method - get_address() O(1)
# returns address based on index

def get_address(index):
    address = Location_List[index]
    return address
