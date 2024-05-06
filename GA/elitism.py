import random

def elitism_survivor_selection(population, offspring, fitness_values,offspring_fitness, num_elites=10):
    """Perform Elitism Survivor Selection."""
    # Combine population and offspring
    combined_population = population + offspring
    combined_fitness = fitness_values + offspring_fitness
    # Sort individuals by fitness values
    sorted_combined = sorted(zip(combined_population, combined_fitness), key=lambda x: x[1], reverse=False)
    # Select the top individuals (elites) to pass to the next generation
    elites = [individual for individual, _ in sorted_combined[:num_elites]]
    return elites

def mu_lambda_selection_strategy(parents, offspring, parent_fitness, offspring_fitness, number_of_parents = 5, number_to_keep = 7):
    # Combine parents and offspring
    combined_population = parents + offspring
    combined_fitness = parent_fitness + offspring_fitness
    
    # Sort individuals by fitness values
    sorted_combined = sorted(zip(combined_population, combined_fitness), key=lambda x: x[1])
    
    # Select the top mu individuals (parents) from the combined population
    selected_parents = [individual for individual, _ in sorted_combined[:number_of_parents]]
    
    # Truncate the combined population to keep only the top lambda individuals
    truncated_combined_population = [individual for individual, _ in sorted_combined[:number_to_keep]]
    
    return selected_parents, truncated_combined_population
