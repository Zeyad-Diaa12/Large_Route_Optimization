import json

def load_data_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data


file_path_distance = './Data/distance_matrix.json'
file_path_mapped_orders = './Data/all_mapped_orders.json'
file_path_all_orders = './Data/all_items_in_order.json'

distance_matrix = load_data_json(file_path_distance)
mapped_orders = load_data_json(file_path_mapped_orders)
all_orders = load_data_json(file_path_all_orders)

list_mapped_orders = [order for order in mapped_orders]
