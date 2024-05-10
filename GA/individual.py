import random
from .load_data import list_mapped_orders,list_part_1,list_part_2,list_part_3,list_part_4

random.seed(42)
class Individual():
    def __init__(self,individual_len):
        self.individual = random.sample(list_part_1, int(individual_len/4)) + random.sample(list_part_2, int(individual_len/4)) + random.sample(list_part_3, int(individual_len/4)) + random.sample(list_part_4, int(individual_len/4))

