from datetime import datetime, timedelta  # Import necessary modules for date and time operations
from .load_data import distance_matrix, mapped_orders  # Import data from local module

class Fitness():
    """
    Class to evaluate the fitness of a truck routing solution.

    Attributes:
        genome (list): The individual solution representing the route.
        truck (object): The truck object with related attributes.
        source (str): The starting location of the truck.
        max_stops (int): Maximum allowed stops for the truck.
        truck_id (int): Identifier for the truck.
        count_stops (int): Counter for the number of stops.
        weight (float): Total weight of the cargo on the truck.
        area (float): Total area occupied by cargo on the truck.
        cost_per_km (float): Total cost per kilometer traveled.
        time_violation (float): Penalty for violating time constraints.
        stops_violation (float): Penalty for exceeding stop limits.
        current_time (datetime): Current time during route evaluation.
        load_time (float): Maximum allowed time for loading.
        diff_time (float): Difference between earliest and latest stop times.
        fitness (float): Overall fitness score of the solution.
    """
    def __init__(self, individual, truck):
        """
        Initializes the Fitness object with individual solution and truck details.

        Args:
            individual (list): The individual solution representing the route.
            truck (object): The truck object with related attributes.
        """
        self.genome = individual
        self.truck = truck
        self.source = self.truck.source
        self.max_stops = self.truck.max_stops
        self.truck_id = self.truck.truck_id

        self.count_stops = 1
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
        """
        Calculates the moving time of the truck based on scheduled stops.
        """
        datetime_objects = []
        for rep in self.genome:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4], '%Y-%m-%d %H:%M:%S'))
        self.current_time = max(datetime_objects, key=lambda x: x)

    def _calculate_time_diff(self):
        """
        Calculates the time difference between earliest and latest stop times.
        """
        datetime_objects = []
        for rep in self.genome:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4],'%Y-%m-%d %H:%M:%S'))
        min_time = min(datetime_objects, key=lambda x:x)
        max_time = max(datetime_objects, key=lambda x:x)
        self.diff_time = (max_time - min_time).total_seconds() / 3600
    def _calculate_arrival_time(self,chromosome):
        """
        Calculates the arrival time of the truck based on scheduled stops.
        """
        arrival_time = {}
        datetime_objects = []
        for rep in chromosome:
            datetime_objects.append(datetime.strptime(mapped_orders[rep][4], '%Y-%m-%d %H:%M:%S'))
        moving_time = max(datetime_objects, key=lambda x: x)
        total_time = moving_time
        for i in range(len(chromosome)):
            if i==len(chromosome)-1:
                arrival_time[mapped_orders[chromosome[i]][0]] = total_time
            else:
                if i == 0:
                    current_city = self.source
                    next_city = mapped_orders[chromosome[i]][1]

                    time_taken = distance_matrix[current_city][next_city]['time']
                    
                    arrival_time[mapped_orders[chromosome[i]][0]] = total_time + timedelta(hours=time_taken)
                else:
                    current_city = mapped_orders[chromosome[i]][1]
                    next_city = mapped_orders[chromosome[i+1]][1]
                    if current_city == next_city:
                        arrival_time[mapped_orders[chromosome[i]][0]] = total_time
                    else:
                        time_taken = distance_matrix[current_city][next_city]['time']
                        
                        arrival_time[mapped_orders[chromosome[i]][0]] = total_time + timedelta(hours=time_taken)
        return arrival_time
    def get_fitness(self):
        """
        Evaluates the fitness of the solution based on various criteria.

        Returns:
            float: The fitness score of the solution.
        """
        self._calculate_moving_time_of_truck()
        self._calculate_time_diff()

        for i in range(len(self.genome) - 1):
            if i == 0:
                self.count_stops += 1
                current_city = self.source
                next_city = mapped_orders[self.genome[i]][1]

                self.cost_per_km += distance_matrix[current_city][next_city]['cost']

                time_taken = distance_matrix[current_city][next_city]['time']
                modified_time = self.current_time + timedelta(hours=time_taken)
                self.current_time = modified_time

                if self.count_stops > self.max_stops:
                    self.stops_violation += 100
                if modified_time > datetime.strptime(mapped_orders[self.genome[i]][5],'%Y-%m-%d %H:%M:%S'):
                    self.time_violation += 100
            else:
                current_city = mapped_orders[self.genome[i]][1]
                next_city = mapped_orders[self.genome[i + 1]][1]

                if current_city == next_city:
                    self.cost_per_km += 0.0
                    self.time_violation += 0
                else:
                    self.count_stops += 1
                    self.cost_per_km += distance_matrix[current_city][next_city]['cost']

                    time_taken = distance_matrix[current_city][next_city]['time']
                    modified_time = self.current_time + timedelta(hours=time_taken)
                    self.current_time = modified_time

                    if self.count_stops > self.max_stops:
                        self.stops_violation += 100
                    if modified_time > datetime.strptime(mapped_orders[self.genome[i]][5],'%Y-%m-%d %H:%M:%S'):
                        self.time_violation += 100

        for rep in self.genome:
            self.weight += mapped_orders[rep][3]
            self.area += mapped_orders[rep][2]

        if self.weight > self.truck.truck_weight:
            self.fitness += (self.weight - self.truck.truck_weight) * 0.4

        if self.area > self.truck.truck_area:
            self.fitness += (self.area - self.truck.truck_area) * 0.4
        
        if self.diff_time > self.load_time:
            self.fitness += self.diff_time - self.load_time

        self.fitness = (self.time_violation * 0.4) + (self.cost_per_km * 0.1) + (self.stops_violation * 0.1)

        return self.fitness
