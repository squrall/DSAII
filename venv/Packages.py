#John Lemire 001043932
"""
This file contains classes, data structures and modules pertaining to packages, their import and manipulation:

class Package_list - Linked Hash list for storing Package objects

class Package - Takes package data and creates package object

method add_all_packages() - Imports packages from Excel file

method get_package_list() - Returns Package_list
"""

import xlrd

path = ".\WGUPS Package File.xlsx"

# Class - Package_List
#
# __init__
# takes as a variable an int and creates an array of arrays with length(capacity)
#
# insert
# takes package object, hashes key and inserts into hash list
#
# search
# retreives object at index(key) with key(key)
#
# remove
# removes object at index(key) with key(key)

class Package_List:
    def __init__(self, capacity):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    def insert(self, key, package):
        index = hash(key) % len(self.table)
        key_pack = [key,package]

        hashed_index = self.table[index]
        #print(index, self.table[index])
        hashed_index.append(key_pack)

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        index = hash(key) % len(self.table)
        hashed_index = self.table[index]

        for set in hashed_index:
            if set[0] == key:
                return set[1]


    # Removes an item with matching key from the hash table.
    def remove(self, key):

        # get the bucket list where this item will be removed from.
        index = hash(key) % len(self.table)
        hashed_index = self.table[bucket]

        # remove the item from the bucket list if it is present.
        if key in hashed_index:
            hashed_index.remove(key)

# Container for Package_List object

p_list = Package_List(10)

# Class - Package
#
# __init__
# takes package variables, assigns them to self.variable
#
# update_address
# takes new address and updates package
#
# update_status
# sets package.status to new status
#
# get_id
# returns package.id
#
# set_time_delivered
# sets package.delivery_time to given time

class Package:
    def __init__(self, id, address, city, state, zip, delivery_deadline, weight, notes,status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.delivery_time = ''
        self.time_left_hub = ''
        self.weight = weight
        self.notes = notes
        self.status = status

        deliver_with_container = []
        if id == 14:
            deliver_with_container.append(15)
            deliver_with_container.append(19)
        if id == 16:
            deliver_with_container.append(13)
            deliver_with_container.append(19)
        if id == 20:
            deliver_with_container.append(13)
            deliver_with_container.append(15)

        self.deliver_with = deliver_with_container
        self.time_delivered = "0.0"
        if id == 3 or id == 18 or id == 36 or id == 38:
            self.load_on_truck = 2

    def update_address(package,new_address,new_city,new_state,new_zip):
        if new_addres != NULL:
            package.address = new_address
        if new_city != NULL:
            package.city = new_city
        if new_state != NULL:
            package.state = new_state
        if new_zip != NULL:
            package.zip = new_zip

    def update_status(package,new_status):
        package.status = new_status

    def get_id(self):
        return self.id

    def set_time_delivered(self, time):
        self.delivery_time = time
    def get_time_delivered(self):
        return self.delivery_time
    def set_time_left_hub(self, time):
        self.time_left_hub = time

# Method - add_all_packages() O(n)
# opens excel workbot at path
# iterates through list of packages and inserts them into the Package_List hash table

def add_all_packages():
    workbook = xlrd.open_workbook(path)
    package_sheet = workbook.sheet_by_index(0)
    package_sheet.cell_value(0,0)
    num_rows = package_sheet.nrows
    x = 8

    package_id = []
    package_address = []
    package_city = []
    package_state = []
    package_zip = []
    package_delivery_deadline = []
    package_weight = []
    package_notes = []

    #iterate through excel doc O(n)
    #adds packages to package list

    while x < num_rows:
        package_id = package_sheet.cell_value(x,0)
        package_address = package_sheet.cell_value(x,1)
        package_city = package_sheet.cell_value(x,2)
        package_state = package_sheet.cell_value(x,3)
        package_zip = package_sheet.cell_value(x,4)
        package_delivery_deadline = package_sheet.cell_value(x,5)
        package_weight = package_sheet.cell_value(x,6)
        package_notes = package_sheet.cell_value(x,7)

        if package_address == '3575 W Valley Central Station bus Loop':
            package_address = '3575 W Valley Central Sta bus Loop'

        if package_id == 9:
            package_address = '410 SsState St'
            package_zip = '84111'

        if package_delivery_deadline == 'EOD':
            package_delivery_deadline = package_delivery_deadline.strip()

        #insert package to list
        p_list.insert(package_id, Package(package_id,package_address,package_city,package_state,package_zip,package_delivery_deadline,package_weight,package_notes,"Unloaded"))

        #iterate counter for package list
        x=x+1

# Method - get_package_list() O(1)
# returns Package List

def get_package_list():
    return p_list