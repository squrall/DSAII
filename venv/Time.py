# John Lemire 001043932
'''
This contains methods pertaining to time and its calculation
'''

import datetime

# Method - int_to_hours O(1)
# returns time interval based on distance traveled

def int_to_hours(distance):
    hours_traveled = distance/18
    return datetime.timedelta(hours=hours_traveled)

# Method - get_time O(1)
# returns start time plus the time it took the truck to drive the distance

def get_time(starting_time,distance):
    hours_traveled = distance /18
    time_traveled = datetime.timedelta(hours = hours_traveled)
    tmp_time_finished = (datetime.datetime.combine(datetime.date.today(), starting_time) + time_traveled).time()
    return tmp_time_finished
