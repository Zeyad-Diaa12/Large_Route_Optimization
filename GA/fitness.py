import json
from chromosome import Chromosome
import random

def load_distance_matrix_from_json(file_path):
    with open(file_path, 'r') as json_file:
        distance_matrix = json.load(json_file)
    return distance_matrix

def load_orders(file_path):
    with open(file_path, 'r') as json_file:
        orders_items = json.load(json_file)
    return orders_items

file_path_distance = './Data/distance_matrix.json'
file_path_orders = './Data/all_items_in_order.json'

distance_matrix = load_distance_matrix_from_json(file_path_distance)
all_orders = load_orders(file_path_orders)
all_orders_list = [order for order in all_orders]

class Truck():
    def __init__(self):
        self.truck_id = random.randint(1,1000000)
        self.items = None
        self.available_weight = 10000
        self.area = 16.1*2.5
        self._add_item()

    def _add_item(self):
        self.items=random.sample(all_orders_list, 5)

class Fitness():
    def __init__(self,chromosome,truck):
        self.chromosme = chromosome
        self.truck = truck
        self.fitness = 0.0
        self._assign_route_to_chromosome()
    def _assign_route_to_chromosome(self):
        self.chromosme.route = [all_orders[route]['Destination'] for route in self.truck.items]

    def _evaluate_fitness(self):
        finalFitness = 0.0 
        # DISTANCE_PENALTY = 0
        # COST_PENALTY = 0
        CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT = 2.0
        # TIME_PENALTY = 0
        # AVAILABILTY_PENALTY = 0
        # DEADLINE_PENALTY = 0
        # MAX_STOPS_PENALTY = 0


        # total_distance = 0.0
        total_weight = 0.0
        total_area = 0.0
        route = self.chromosme.route
        orders = self.truck.items
        time_taken = 0
        total_cost = 0

        # Calculate total distance traveled along the route and total weight
        for i in range(len(route) - 1):
            current_city = route[i]
            next_city = route[i + 1]
            total_cost += distance_matrix[current_city][next_city]['cost']
            time_taken += distance_matrix[current_city][next_city]['time']

        # Calculate total weight of items in the route
        for order in orders:
            total_weight += all_orders[order]['Items'][0]['Weight']
            total_area += all_orders[order]['Items'][0]['Area']

        if total_weight > self.truck.available_weight:
            finalFitness += max(0,total_weight-self.truck.available_weight)*CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT
        if total_area > self.truck.area:
            finalFitness += max(0,total_area-self.truck.area)*CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT

        # Check time constraints, compatibility, and other constraints here
        # Update total_cost accordingly based on these constraints

        # Update chromosome's fitness, total distance, and total weight attributes
        # self.total_distance = total_distance
        # self.cost_per_km = total_cost
        # self.total_time = time_taken
        # # chromosome.total_weight = total_weight
        # self.fitness = total_cost+time_taken+total_distance

truck1 = Truck()
print("Truck ID:",truck1.truck_id)
print("Items in truck:",truck1.items)
