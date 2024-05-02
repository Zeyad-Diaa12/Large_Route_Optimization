import random
import json

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

class Chromosome:
    """
    Represents a potential travel route (chromosome) in an optimization algorithm.

    This class encapsulates information about a route, including:
        - Source city (starting point)
        - Destination city (ending point)
        - Available intermediate cities (excluding source and destination)
        - Maximum number of allowed stops
        - The actual route (list of city IDs)

    The `_generate_route` method constructs a random route within the specified
    constraints.
    """

    def __init__(self, source='61', max_stops=5):
        """
        Initializes a Chromosome object with the given parameters.

        Args:
            destination (str): ID of the destination city.
            source (str, optional): ID of the source city. Defaults to '61'.
            max_stops (int, optional): Maximum number of intermediate stops. Defaults to 10.
        """

        # # Predefined list of all city IDs
        # self.cities = ["24", "30", "26", "20", "32", "25", "56", "2", "5", "50", "6", "7",
        #                "12", "41", "35", "13", "44", "9", "19", "36", "17", "60", "14", "1",
        #                "47", "8", "27", "51", "43", "38", "58", "46", "28", "53", "10", "34",
        #                "61", "52", "48", "16", "40", "29", "11", "31", "22", "49", "45", "23",
        #                "18", "4", "55", "21", "15", "3", "37", "54", "57", "42", "39", "59",
        #                "0", "33"]

        # Filter available cities to exclude source and destination
        # self.routes = [city for city in self.cities if city != destination and city != source]
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
        # self.destination = None
        self.route = None
        self.fitness = 0.0
        self._add_item()        
        self._assign_route_to_chromosome()
        self._evaluate_fitness()

    def _assign_route_to_chromosome(self):
        self.route = [self.source]+[all_orders[route]['Destination'] for route in self.items]
    def _add_item(self):
        self.items=random.sample(all_orders_list, self.max_stops-1)
    
    def _evaluate_fitness(self):
        # DISTANCE_PENALTY = 0
        # COST_PENALTY = 0
        CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT = 2.0
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
            self.fitness += max(0,self.weight-self.truck_weight)*CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT
        if self.area > self.truck_area:
            self.fitness += max(0,self.area-self.truck_area)*CAPACITY_VIOLATION_PENALTY_AREA_WEIGHT

        self.fitness = self.time_taken + self.weight + self.area + self.cost_per_km

test = Chromosome()
print(test.truck_id)
print(test.source)
print(test.area)
print(test.weight)
print(test.fitness)
print(test.route)
print(test.items)
