from collections import defaultdict
import random

def order_crossover(parent1, parent2):
    """Perform Order Crossover (OX) on two parent chromosomes."""
    size = len(parent1)
    # Choose two random points for crossover
    cxpoint1 = random.randint(0, size - 1)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint2 < cxpoint1:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Initialize the offspring with the genetic material of the parents
    offspring1 = [''] * size
    offspring2 = [''] * size

    # Copy a segment from parent1 to offspring1 and from parent2 to offspring2
    offspring1[cxpoint1:cxpoint2 + 1] = parent1[cxpoint1:cxpoint2 + 1]
    offspring2[cxpoint1:cxpoint2 + 1] = parent2[cxpoint1:cxpoint2 + 1]

    # Create a list of elements not copied from parent1 for offspring2
    remaining1 = [x for x in parent1 if x not in offspring2[cxpoint1:cxpoint2 + 1]]

    # Create a list of elements not copied from parent2 for offspring1
    remaining2 = [x for x in parent2 if x not in offspring1[cxpoint1:cxpoint2 + 1]]

    # Fill in the remaining positions in the offspring with the remaining elements
    index1 = 0
    index2 = 0
    for i in range(size):
        if offspring1[i] == '':
            if index2 < len(remaining2):
                offspring1[i] = remaining2[index2]
                index2 += 1
            else:
                offspring1[i] = remaining1[index1]
                index1 += 1
        if offspring2[i] == '':
            if index1 < len(remaining1):
                offspring2[i] = remaining1[index1]
                index1 += 1
            else:
                offspring2[i] = remaining2[index2]
                index2 += 1

    return offspring1, offspring2


def edge_crossover(parent1, parent2):
    """Perform Edge Recombination Crossover (ERX) on two parent chromosomes."""
    size = len(parent1)
    # Create adjacency lists for both parents
    adj_list1 = defaultdict(list)
    adj_list2 = defaultdict(list)
    for i in range(size):
        adj_list1[parent1[i]].append(parent1[(i + 1) % size])
        adj_list1[parent1[i]].append(parent1[(i - 1) % size])
        adj_list2[parent2[i]].append(parent2[(i + 1) % size])
        adj_list2[parent2[i]].append(parent2[(i - 1) % size])
    
    # Create offspring list
    offspring = []
    # Initialize current node to a random starting point
    current_node = random.choice(list(parent1))
    while len(offspring) < size:
        # Add current node to offspring if it's not already present
        if current_node not in offspring:
            offspring.append(current_node)
        # Remove current node from adjacency lists
        for key in adj_list1:
            if current_node in adj_list1[key]:
                adj_list1[key].remove(current_node)
        for key in adj_list2:
            if current_node in adj_list2[key]:
                adj_list2[key].remove(current_node)
        # Remove current node from neighbors' lists
        neighbors = adj_list1[current_node] + adj_list2[current_node]
        for neighbor in neighbors:
            if current_node in adj_list1[neighbor]:
                adj_list1[neighbor].remove(current_node)
            if current_node in adj_list2[neighbor]:
                adj_list2[neighbor].remove(current_node)
        # Find the neighbor with the fewest edges
        available_neighbors = adj_list1[current_node] + adj_list2[current_node]
        if available_neighbors:
            min_neighbors = min(available_neighbors, key=lambda x: len(adj_list1[x]) + len(adj_list2[x]))
            # If multiple neighbors have the same number of edges, choose randomly
            if len(adj_list1[min_neighbors]) + len(adj_list2[min_neighbors]) > 0:
                current_node = random.choice([min_neighbors] + [x for x in available_neighbors if x != min_neighbors])
            else:
                current_node = random.choice(list(parent1))
        else:
            # If there are no neighbors available, choose randomly from remaining nodes
            remaining_nodes = [node for node in parent1 if node not in offspring]
            if remaining_nodes:
                current_node = random.choice(remaining_nodes)
            else:
                break  # No remaining nodes, terminate loop and return offspring
    return offspring
