import random

import numpy as np

def exponential_rank_selection(population, fitness_values, selection_pressure=1.2):
    # Sort individuals by fitness values
    sorted_population = sorted(zip(population, fitness_values), key=lambda x: x[1])
    ranks = range(1, len(sorted_population) + 1)
    selection_probs = [1 / (rank ** selection_pressure) for rank in ranks]
    
    selected = random.choices(sorted_population, weights=selection_probs)[0]
    return selected[0]  # Return the selected individual

def tournament_selection(population, fitness_values, tournament_size=4):
    """Perform Tournament Selection on a population."""
    selected = None
    # Perform multiple tournaments
    for _ in range(tournament_size):
        # Randomly select individuals for the tournament
        tournament = random.sample(list(zip(population, fitness_values)), tournament_size)
        # Find the individual with the min fitness in the tournament
        winner = min(tournament, key=lambda x: x[1])[0]
        # Update the selected individual if it has lower fitness
        if selected is None or fitness_values[population.index(winner)] < fitness_values[population.index(selected)]:
            selected = winner
    return selected

