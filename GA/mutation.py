import random

def swap_mutation(chromosome):
    """Perform Swap Mutation on a chromosome."""
    size = len(chromosome)
    # Select two distinct positions randomly
    pos1, pos2 = random.sample(range(size), 2)
    # Swap the elements at the selected positions
    chromosome[pos1], chromosome[pos2] = chromosome[pos2], chromosome[pos1]
    return chromosome

def scramble_mutation(chromosome):
    """Perform Scramble Mutation on a chromosome."""
    size = len(chromosome)
    # Select a random subset of positions
    start, end = sorted(random.sample(range(size), 2))
    # Scramble the elements within the selected subset
    subset = chromosome[start:end]
    random.shuffle(subset)
    chromosome[start:end] = subset
    return chromosome

def inversion_mutation(chromosome):
    """Perform Inversion Mutation on a chromosome."""
    size = len(chromosome)
    # Select a random subset of positions
    start, end = sorted(random.sample(range(size), 2))
    # Reverse the order of elements within the selected subset
    chromosome[start:end] = chromosome[start:end][::-1]
    return chromosome

def insertion_mutation(chromosome):
    """Perform Insertion Mutation on a chromosome."""
    size = len(chromosome)
    # Select two distinct positions randomly
    pos1, pos2 = random.sample(range(size), 2)
    # Remove the element at pos1 and insert it at pos2, shifting elements as necessary
    element = chromosome.pop(pos1)
    chromosome.insert(pos2, element)
    return chromosome

