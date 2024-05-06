from datetime import datetime, timedelta
import json
import random
from .load_data import distance_matrix, mapped_orders

class Fitness():
    def __init__(self,individual,truck):
        self.genome = individual

        self.truck = truck
        self.source = self.truck.source
        self.max_stops = self.truck.max_stops
        self.truck_id = self.truck.truck_id

        self.count_stops = 0
        self.weight = 0.0
        self.area = 0.0
        self.cost_per_km = 0.0
        self.time_violation = 0.0
        self.stops_violation = 0.0
        self.current_time = None
        self.load_time = 48.0
        self.diff_time = None
        self.fitness = 0.0
        
    def _calculate_moving_time_of_truck(self):
        datetime_objects = []
        for rep in self.genome:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4], '%Y-%m-%d %H:%M:%S'))
        self.current_time = max(datetime_objects, key=lambda x: x)

    def _calculate_time_diff(self):
        datetime_objects = []
        for rep in self.genome:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4],'%Y-%m-%d %H:%M:%S'))
        min_time = min(datetime_objects,key=lambda x:x)
        max_time = max(datetime_objects,key=lambda x:x)
        self.diff_time = (max_time-min_time).total_seconds()/3600
    
    def get_fitness(self):

        self._calculate_moving_time_of_truck()
        self._calculate_time_diff()

        for i in range(len(self.genome)-1):
            if i == 0:
                self.count_stops+=1
                current_city = self.source
                next_city = mapped_orders[self.genome[i]][1]

                self.cost_per_km += distance_matrix[current_city][next_city]['cost']

                time_taken = distance_matrix[current_city][next_city]['time']
                modified_time = self.current_time + timedelta(hours=time_taken)
                self.current_time = modified_time

                if self.count_stops>self.max_stops:
                    self.stops_violation += 100
                if modified_time > datetime.strptime(mapped_orders[self.genome[i]][5],'%Y-%m-%d %H:%M:%S'):
                    self.time_violation += 100
            else:
                current_city = mapped_orders[self.genome[i]][1]
                next_city = mapped_orders[self.genome[i+1]][1]

                if current_city==next_city:
                    self.cost_per_km += 0.0
                    self.time_violation += 0
                else:
                    self.count_stops+=1
                    self.cost_per_km += distance_matrix[current_city][next_city]['cost']

                    time_taken = distance_matrix[current_city][next_city]['time']
                    modified_time = self.current_time + timedelta(hours=time_taken)
                    self.current_time = modified_time

                    if self.count_stops>self.max_stops:
                        self.stops_violation += 100
                    if modified_time > datetime.strptime(mapped_orders[self.genome[i]][5],'%Y-%m-%d %H:%M:%S'):
                        self.time_violation += 100


        for rep in self.genome:
            self.weight += mapped_orders[rep][3]
            self.area += mapped_orders[rep][2]

        if self.weight > self.truck.truck_weight:
            self.fitness += (self.weight-self.truck.truck_weight)*0.2

        if self.area > self.truck.truck_area:
            self.fitness += (self.area-self.truck.truck_area)*0.2
        
        if self.diff_time > self.load_time:
            self.fitness += self.diff_time-self.load_time

        self.fitness = (self.time_violation*0.6) + (self.cost_per_km*0.1) + (self.stops_violation*0.1)

        return self.fitness


