import random
import pandas as pd 
import json

def load_distance_matrix_from_json(file_path):
    with open(file_path, 'r') as json_file:
        distance_matrix = json.load(json_file)
    return distance_matrix

# Example usage:
file_path = './Data/distance_matrix.json'
distance_matrix = load_distance_matrix_from_json(file_path)

class Chromosome:
    def __init__(self,items,destination,max_stops=10):
        cities = ["24","30","26","20","32","25","56","2","5","50","6","7","12","41","35","13","44","9","19","36","17","60","14","1","47","8","27","51","43","38","58","46","28","53","10","34","61","52","48","16","40","29","11","31","22","49","45","23","18","4","55","21","15","3","37","54","57","42","39","59","0","33"]
        self.routes = [city for city in cities if city != destination and city !='61']
        self.max_stops = max_stops
        self.items = items
        self.destination = destination 
        self.fitness = 0.0
        self.total_distance = 0.0
        self.total_weight = 0.0
        self.total_time = 0.0
        self.truck_capacity = 10000
        self.truck_area = 16.1*2.5
        self.cost_per_km = 0.0
        self.generated_route = []
        self._generate_route()
        self.evaluate_fitness()

    def _generate_route(self):
        route = ['61'] + random.sample(self.routes, self.max_stops - 2) + [self.destination]

        self.generated_route = route

    def evaluate_fitness(self):
        total_distance = 0
        # total_weight = 0
        route = self.generated_route
        time_taken = 0
        total_cost = 0

        # Calculate total distance traveled along the route and total weight
        for i in range(len(route) - 1):
            current_city = route[i]
            next_city = route[i + 1]
            total_distance += distance_matrix[current_city][next_city]['distance']
            total_cost += distance_matrix[current_city][next_city]['cost']
            time_taken += distance_matrix[current_city][next_city]['time']

        # Calculate total weight of items in the route
        # for item in items:
        #     if item.destination in route:
        #         total_weight += item.weight

        # Calculate total cost
        # total_cost = total_distance * self.cost_per_km

        # # Check weight capacity constraint
        # if total_weight > self.truck_capacity:
        #     total_cost += float('inf')  # Penalize if weight capacity is exceeded

        # Check time constraints, compatibility, and other constraints here
        # Update total_cost accordingly based on these constraints

        # Update chromosome's fitness, total distance, and total weight attributes
        self.total_distance = total_distance
        self.cost_per_km = total_cost
        self.total_time = time_taken
        # chromosome.total_weight = total_weight
        self.fitness = total_cost+time_taken+total_distance



test = Chromosome([1,2,3,4,5],'5')

print(test.fitness)
print(test.total_distance)
print(test.total_time)
print(test.cost_per_km)
print(test.generated_route)