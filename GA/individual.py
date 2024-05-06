import random
from .load_data import list_mapped_orders

class Individual():
    def __init__(self,individual_len):
        self.individual = random.sample(list_mapped_orders, individual_len)