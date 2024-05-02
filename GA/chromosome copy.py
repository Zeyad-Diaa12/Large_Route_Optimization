import random
import json
import time
from datetime import datetime

def load_distance_matrix_from_json(file_path):
    with open(file_path, 'r') as json_file:
        distance_matrix = json.load(json_file)
    return distance_matrix

def load_orders(file_path):
    with open(file_path, 'r') as json_file:
        orders_items = json.load(json_file)
    return orders_items

def load_mapped_orders(file_path):
    with open(file_path, 'r') as json_file:
        orders_items = json.load(json_file)
    return orders_items


file_path_distance = './Data/distance_matrix.json'
file_path_orders = './Data/modified_orders.json'
file_path_mapped_orders = './Data/mapped_orders.json'

distance_matrix = load_distance_matrix_from_json(file_path_distance)
all_orders = load_orders(file_path_orders)
mapped_orders = load_mapped_orders(file_path_mapped_orders)
all_orders_list = [order for order in all_orders]
list_mapped_orders = [order for order in mapped_orders]


class Chromosome:

    def __init__(self, source='61', max_stops=3):
        self.truck_id = random.randint(1,1000000)
        self.representation = None
        self.truck_weight = 10000
        self.truck_area = 16.1*2.5
        self.max_stops = max_stops
        self.source = source
        self.weight = 0.0
        self.area = 0.0
        self.cost_per_km = 0.0
        self.time_taken = 0.0
        self.moving_time = None
        self.fitness = 0.0
        self.unload_time = 3.0
        self.cost_per_stop = 10000.0
        self.load_time = 48.0
        self.diff_time = None

    def _calculate_moving_time_of_truck(self):
        datetime_objects = []
        for item in self.items:
            order_time = all_orders[item]['Available_Time']
            datetime_objects.append(datetime.strptime(order_time, '%Y-%m-%d %H:%M:%S'))
        # Use max with key to find the datetime object with the highest value (latest)
        self.moving_time = max(datetime_objects, key=lambda x: x)

    def _calculate_time_diff(self):
        datetime_objects = []
        for rep in self.representation:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][2],'%Y-%m-%d %H:%M:%S'))
        min_time = min(datetime_objects,key=lambda x:x)
        max_time = max(datetime_objects,key=lambda x:x)
        self.diff_time = (max_time-min_time).total_seconds()/3600

    def _get_representation(self):
        self.representation = random.sample(list_mapped_orders, self.max_stops - 1)

    def _evaluate_fitness(self):
        DISTANCE_PENALTY = 1000
        CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT = 1000
        TIME_PENALTY = 500
        # AVAILABILTY_PENALTY = 0
        # DEADLINE_PENALTY = 0
        # MAX_STOPS_PENALTY = 0


        # total_distance = 0.0
        # total_weight = 0.0
        # total_area = 0.0
        # route = self.route
        # orders = self.items
        # time_taken = 0
        # total_cost = 0

        # Calculate total distance traveled along the route and total weight
        for i in range(len(self.representation) - 1):
            current_city = all_orders[mapped_orders[self.representation[i]][0]]['Destination']
            next_city = all_orders[mapped_orders[self.representation[i+1]][0]]['Destination']
            self.cost_per_km += distance_matrix[current_city][next_city]['cost']
            self.time_taken += distance_matrix[current_city][next_city]['time']

        # Calculate total weight of items in the route
        for rep in self.representation:
            order = all_orders[mapped_orders[rep][0]]
            self.weight += order['Items'][0]['Weight']
            self.area += order['Items'][0]['Area']

        if self.weight > self.truck_weight:
            self.fitness += max(0,self.weight-self.truck_weight)

        if self.area > self.truck_area:
            self.fitness += max(0,self.area-self.truck_area)
        
        if self.diff_time > self.load_time:
            self.fitness += (self.diff_time-self.load_time)

        self.fitness = self.time_taken + self.weight + self.area + self.cost_per_km

test = Chromosome()

test._get_representation()
test._calculate_time_diff()
print(test.representation)
print(test.diff_time)
# print(test.truck_id)
# print(test.source)
# print(test.area)
# print(test.weight)
# print(test.fitness)
# print(test.representation)
# print(test.moving_time)


