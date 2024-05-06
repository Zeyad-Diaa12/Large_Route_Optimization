import random

class Truck():
    def __init__(self,source='61',max_stops=10):
        self.truck_id = random.randint(1,1000000)
        self.truck_weight = 10000
        self.truck_area = 16.1*2.5
        self.source = source
        self.max_stops = max_stops