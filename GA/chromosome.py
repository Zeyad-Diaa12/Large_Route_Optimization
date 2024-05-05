import random
import json
import time
from datetime import datetime,timedelta

def load_data_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data


file_path_distance = './Data/distance_matrix.json'
# file_path_orders = './Data/modified_orders.json'
file_path_mapped_orders = './Data/all_mapped_orders.json'

distance_matrix = load_data_json(file_path_distance)
# all_orders = load_orders(file_path_orders)
mapped_orders = load_data_json(file_path_mapped_orders)
# all_orders_list = [order for order in all_orders]
list_mapped_orders = [order for order in mapped_orders]


class Chromosome:

    def __init__(self, candidate_len,source='61', max_stops=10):

        self.truck_id = random.randint(1,1000000)
        self.truck_weight = 10000
        self.truck_area = 16.1*2.5
        self.max_stops = max_stops
        self.source = source
        self.candidates_len = candidate_len

        self.representation = None
        self.weight = 0.0
        self.area = 0.0
        self.cost_per_km = 0.0
        self.time_violation = 0.0
        self.current_time = None
        self.load_time = 48.0
        self.diff_time = None
        self.fitness = 0.0

    def _calculate_moving_time_of_truck(self):
        datetime_objects = []
        for rep in self.representation:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4], '%Y-%m-%d %H:%M:%S'))
        self.current_time = max(datetime_objects, key=lambda x: x)

    def _calculate_time_diff(self):
        datetime_objects = []
        for rep in self.representation:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4],'%Y-%m-%d %H:%M:%S'))
        min_time = min(datetime_objects,key=lambda x:x)
        max_time = max(datetime_objects,key=lambda x:x)
        self.diff_time = (max_time-min_time).total_seconds()/3600

    def _get_representation(self):
        self.representation = random.sample(list_mapped_orders, self.candidates_len)

    def _get_fitness(self):
        
        self._calculate_moving_time_of_truck()
        self._calculate_time_diff()

        for i in range(len(self.representation) - 1):
            if i == 0:
                current_city = self.source
                next_city = mapped_orders[self.representation[i]][1]

                self.cost_per_km += distance_matrix[current_city][next_city]['cost']

                time_taken = distance_matrix[current_city][next_city]['time']
                modified_time = self.current_time + timedelta(hours=time_taken)
                self.current_time = modified_time

                if modified_time > datetime.strptime(mapped_orders[self.representation[i]][5],'%Y-%m-%d %H:%M:%S'):
                    self.time_violation += 100
                else:
                    self.time_violation += 0.0
            else:
                current_city = mapped_orders[self.representation[i]][1]
                next_city = mapped_orders[self.representation[i+1]][1]

                if current_city==next_city:
                    self.cost_per_km += 0.0
                    self.time_violation += 0
                else:
                    self.cost_per_km += distance_matrix[current_city][next_city]['cost']

                    time_taken = distance_matrix[current_city][next_city]['time']
                    modified_time = self.current_time + timedelta(hours=time_taken)
                    self.current_time = modified_time

                    if modified_time > datetime.strptime(mapped_orders[self.representation[i]][5],'%Y-%m-%d %H:%M:%S'):
                        self.time_violation += 100
                    else:
                        self.time_violation += 0.0


        for rep in self.representation:
            self.weight += mapped_orders[rep][3]
            self.area += mapped_orders[rep][2]

        if self.weight > self.truck_weight:
            self.fitness += (self.weight-self.truck_weight)*0.3

        if self.area > self.truck_area:
            self.fitness += (self.area-self.truck_area)*0.3
        
        if self.diff_time > self.load_time:
            self.fitness += self.diff_time-self.load_time

        self.fitness = (self.time_violation*0.6) + (self.cost_per_km*0.1)

        # Max stops to be implemented


# test = Chromosome(candidate_len=5)
# test._get_representation()
# test._calculate_moving_time_of_truck()
# test._calculate_time_diff()
# test._get_fitness()
# print(test.representation)
# print(test.time_violation)
# print(test.area)
# print(test.cost_per_km)
# print(test.current_time)
# print(test.diff_time)
# print(test.load_time)
# print(test.weight)
# print(test.fitness)
