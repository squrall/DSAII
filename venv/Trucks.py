#John Lemire 001043932
"""
This file contains methods and classes for trucks and packing those trucks

"""

import math
import datetime
import Locations
import Packages
import Time

# Container for Truck objects

Trucks = []

# Class Truck
#
# __init__
# takes truck id and creates object
#
# set_current_loc
# takes new addres and sets current location
#
# set_next_location
# takes addres and sets next location
#
# add_package
# adds package to package manifest
#
# remove_package
# removes package from package manifest

class Truck:

    def __init__(self, truck_id):
        self.id = truck_id
        self.package_manifest = []
        self.departing_time = ''
        self.current_loc = ''
        self.next_loc = ''
        #self.package_count = 0
        self.distance_traveled = 0

    def set_current_loc(self, current_location):
        self.current_loc = current_location

    def set_next_loc(self, next_location):
        self.next_loc = next_location

    def add_package(self, package):
        self.package_manifest.append(package)

    def remove_package(self,package):
        self.package_manifest.remove(package)

# Method - init_trucks O(n)
# inits truck object with number of trucks and assigns number to each truck

def init_trucks():

    truck_number = 0
    while truck_number < 3:
        Trucks.append(Truck(truck_number))
        truck_number = truck_number + 1

    return Trucks

# Method - pack_trucks O(n)
# goes through each package and sorts it into a truck
# there are multiple if statements with qualifiers (such as deliver deadline etc)
# if the package doesn't qualify for any of the statements then its sorted into a random truck unless that truck is full

def pack_trucks(Truck_List, Package_List):
    truck_counter = 0
    deadline_counter = 0
    package_counter = 1
    Package_Listt = Packages.get_package_list()
    while package_counter < 41:

        package = Package_List.search(package_counter)
        truck_counter = truck_counter % 3
        deadline_counter = deadline_counter % 2

        if package.delivery_deadline != 'EOD':
            #print(package.delivery_deadline)
            if 'Must' in package.notes or 'None' in package.notes:
                Truck_List[0].add_package(package)
            elif package.id == 15:
                Truck_List[0].add_package(package)
            else:
                Truck_List[deadline_counter].add_package(package)
                deadline_counter +=1

        elif 'Can only be' in package.notes:
            Truck_List[1].add_package(package)

        elif 'Delayed' in package.notes:
            Truck_List[1].add_package(package)

        elif 'Wrong' in package.notes:
            package.address = '410 S State St'
            package.zip = '84111'
            Truck_List[2].add_package(package)

        if package not in Truck_List[0].package_manifest and package not in Truck_List[1].package_manifest and package not in Truck_List[2].package_manifest:
            if(len(Truck_List[2].package_manifest) >= 10):
                Truck_List[truck_counter].add_package(package)
            else:
                Truck_List[2].add_package(package)
        #Truck_List[truck_counter].package_count += 1
        #print("Truck", truck_counter, "Package Count", Truck_List[truck_counter].package_count, Truck_List[truck_counter].id)
        package.update_status('Loaded')
        truck_counter += 1
        package_counter += 1

    #print(Locations.get_address(0).address)
    Truck_List[0].set_current_loc("4001 South 700 East,")
    Truck_List[1].set_current_loc("4001 South 700 East,")
    Truck_List[2].set_current_loc("4001 South 700 East,")
    Truck_List[0].departing_time = datetime.time(hour=8,minute=00)
    Truck_List[1].departing_time = datetime.time(hour=9, minute=5)
    Truck_List[2].departing_time = datetime.time(hour=10, minute=00)
    return Truck_List

# Method - deliver_packages O(n^2) nested loops
# takes each truck and cycles through their package manifest, delivering the closest one via delivery date first then distance

def deliver_packages(Packed_Trucks, Truck_List):
    Package_List = Packages.get_package_list()
    truck_counter = 1;

    for truck in Packed_Trucks:

        #first truck gets fed in, we have find nerest package. now we need to run through until all packages are delivered'

        while truck.package_manifest:
            delivered_package = find_nearest_package(truck.package_manifest, truck.current_loc,truck)
            truck.set_current_loc(delivered_package.address)
            Package_List.search(delivered_package.id).set_time_left_hub(truck.departing_time)
            Package_List.search(delivered_package.id).update_status('Delivered')
            Package_List.search(delivered_package.id).set_time_delivered(Time.get_time(truck.departing_time, truck.distance_traveled))

            #print("Package delivered id and time: ", delivered_package.id, delivered_package.delivery_time, len(truck.package_manifest))
            truck.remove_package(delivered_package)

        if truck_counter == 1:
            Truck_List[2].departing_time = Time.get_time(truck.departing_time, truck.distance_traveled)
            truck_counter += 1

        print('Truck: ', truck.id, truck.departing_time)
        print('Total Distance Traveled: ',truck.distance_traveled, 'Time taken: ', Time.int_to_hours(truck.distance_traveled))
        print('Time finished = ', Time.get_time(truck.departing_time, truck.distance_traveled))
        print('************ \n')

# Method find_nearest_package O(n)
# finds nearest package based on location (factoring in the delivery deadline)

def find_nearest_package(package_manifest, current_location,truck):
    lowest_distance = 50
    lowest_soonest_distance = 50
    return_package = []
    soonest_deadline = 999

    for package in package_manifest:
        distance = Locations.get_distance_address(current_location, package.address)
        deadline = package.delivery_deadline

        if (package.delivery_deadline != 'EOD'):
            if (deadline <= soonest_deadline) and (distance < lowest_soonest_distance):
                soonest_deadline = deadline
                lowest_soonest_distance = distance
                lowest_distance = distance
                package_addy = package.address
                return_package = package

        elif distance < lowest_distance and lowest_soonest_distance == 50:
            lowest_distance = distance
            package_addy = package.address
            return_package = package

    truck.distance_traveled += lowest_distance
    return return_package

# Method - travel_to_hub O(1)
# sets current location to hub

def travel_to_hub (current_location, truck):
    return None