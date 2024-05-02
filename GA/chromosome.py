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

file_path_distance = './Data/distance_matrix.json'
file_path_orders = './Data/modified_orders.json'

distance_matrix = load_distance_matrix_from_json(file_path_distance)
all_orders = load_orders(file_path_orders)
all_orders_list = [order for order in all_orders]

class Chromosome:

    def __init__(self, source='61', max_stops=4):
        self.truck_id = random.randint(1,1000000)
        self.items = None
        self.truck_weight = 10000
        self.truck_area = 16.1*2.5
        self.max_stops = max_stops
        self.source = source
        self.weight = 0.0
        self.area = 0.0
        self.cost_per_km = 0.0
        self.time_taken = 0.0
        self.moving_time = None
        self.route = None
        self.fitness = 0.0
        self._add_item()        
        self._assign_route_to_chromosome()
        self._evaluate_fitness()
        self._calculate_moving_time_of_truck()

    def _assign_route_to_chromosome(self):
        self.route = [self.source]+[all_orders[route]['Destination'] for route in self.items]
        
    def _add_item(self):
        # candidate_items = random.sample(all_orders_list, self.max_stops - 1)
        # seen_destinations = set()
        # final_items = []
        # for item in candidate_items:
        #     destination = all_orders[item]["Destination"]
        #     if destination not in seen_destinations:
        #         final_items.append(item)
        #         seen_destinations.add(destination)

        # # If not enough items found due to duplicates, randomly pick from remaining items
        # if len(final_items) < self.max_stops - 1:
        #     remaining_items = list(set(all_orders_list) - seen_destinations)
        #     final_items.extend(random.sample(list(set(all_orders_list) - seen_destinations), self.max_stops - 1 - len(final_items)))

        self.items = random.sample(all_orders_list, self.max_stops - 1)

    def _calculate_moving_time_of_truck(self):
        datetime_objects = []
        for item in self.items:
            order_time = all_orders[item]['Available_Time']
            datetime_objects.append(datetime.strptime(order_time, '%Y-%m-%d %H:%M:%S'))
        # Use max with key to find the datetime object with the highest value (latest)
        self.moving_time = max(datetime_objects, key=lambda x: x)

    def _evaluate_fitness(self):
        # DISTANCE_PENALTY = 0
        # COST_PENALTY = 0
        # CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT = 2.0
        # TIME_PENALTY = 0
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
        for i in range(len(self.route) - 1):
            current_city = self.route[i]
            next_city = self.route[i + 1]
            self.cost_per_km += distance_matrix[current_city][next_city]['cost']
            self.time_taken += distance_matrix[current_city][next_city]['time']

        # Calculate total weight of items in the route
        for order in self.items:
            self.weight += all_orders[order]['Items'][0]['Weight']
            self.area += all_orders[order]['Items'][0]['Area']

        if self.weight > self.truck_weight:
            self.fitness += max(0,self.weight-self.truck_weight)
        if self.area > self.truck_area:
            self.fitness += max(0,self.area-self.truck_area)

        self.fitness = self.time_taken + self.weight + self.area + self.cost_per_km

test = Chromosome()
print(test.truck_id)
print(test.source)
print(test.area)
print(test.weight)
print(test.fitness)
print(test.route)
print(test.items)
print(test.moving_time)