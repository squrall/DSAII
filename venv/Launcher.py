#John Lemire 001043932
"""
Main file
Prompts UI

Program uses a greedy algorithm to calculate distances, sorting by delivery deadlines first, then closest distance
If all packages with delivery deadlines have been delivered, then closest distance is prioritiesed

I use a chaining hash table to solve any collisions. Default size of hash table is 10 to guarantee collisions and prove
implementation of said hash table performs correctly. Size of hash table can be any integer from 1 - x, I used 10
Hash table stores package objects that are then referenced in Truck.package manifest list. This is how we "pack" our trucks

Packages.py has Hash Table and Package object
Locations.py contains data structures for locations (35x35 matrix object for lookups)
Trucks.py contains Truck containers and the delivery algorithm
Time.py contains neseccary time functions/methods
Launcher.py contains calls to all main methods and UI interface logic

"""

#imports

import Packages
import Locations
import Trucks
import datetime
import time
#import deliver_packages

Packages.add_all_packages()
Package_List = Packages.get_package_list()

Locations.add_all_locations()
Location_List = Locations.get_loc_list()

Truck_List = Trucks.init_trucks()
Packed_Trucks = Trucks.pack_trucks(Truck_List, Package_List)

Trucks.deliver_packages(Packed_Trucks, Truck_List)

# Interface for user to look up package status.

start = input("Welcome to the WGU UPS Program!\n"
              "Type 'track' to look up details on a specific package\n"
              "Type 'status' to look up the delivery status for all packages at a specific time\n"
              "Type 'quit' to exit the program!\n")
while start != 'quit':
    if start == 'track':
        try:
            package_input_id = input("Please enter a package ID from 1-40 to look up its details\n")
            try:
                if int(package_input_id) not in range(1, 41):
                    print("Package ID invalid")
                    quit()

            except ValueError:
                pass

            package = Package_List.search(int(package_input_id))
            print('Package ID:\t\t', package.id, '\nPackage Status:\t', package.status,'\nTime Delivered:\t', package.delivery_time)
        except ValueError:
            pass
        start = input("Type 'track' to look up details on a specific package\n"
                      "Type 'status' to look up the delivery status for all packages at a specific time\n"
                      "Type 'quit' to exit the program!\n")
    if start == 'status':
        try:
            time_of_status = input("Please enter a time of day in HH:MM:SS format \n")
            try:
                time.strptime(time_of_status, '%H:%M:%S')
            except ValueError:
                pass
            (hours, minutes, seconds) = time_of_status.split(':')
            timestamp_of_status = (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=0, minute=00)) + datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))).time()
            package_counter = 1
            print("Timestamp: ", timestamp_of_status)
            while package_counter <= 40:
                package = Package_List.search(package_counter)
                if package.time_left_hub > timestamp_of_status:
                    print('Package ID:\t\t', package.id, 'Package left hub: ', package.time_left_hub, '\tPackage Status:\t At Hub')
                elif package.get_time_delivered() < timestamp_of_status:
                    print('Package ID:\t\t', package.id, 'Package left hub: ', package.time_left_hub, '\tPackage Status:\t Delivered')
                else:
                    print('Package ID:\t\t', package.id, 'Package left hub: ', package.time_left_hub, '\tPackage Status:\t Enroute')
                package_counter += 1
        except ValueError:
            pass

        start = input("Type 'track' to look up details on a specific package\n"
                      "Type 'status' to look up the delivery status for all packages at a specific time\n"
                      "Type 'quit' to exit the program!\n")

    elif start =='quit':
        exit()
    else:
        start = input("Please try again\n"
              "Type 'track' to look up details on a specific package\n"
              "Type 'status' to look up the delivery status for all packages at a specific time\n"
              "Type 'quit' to exit the program!\n"
              )



