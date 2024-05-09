
def elitism_survivor_selection(population, offspring, fitness_values, offspring_fitness, num_elites=30):
    """
    Perform Elitism Survivor Selection.

    Args:
        population (list): List of individuals in the current population.
        offspring (list): List of individuals generated as offspring.
        fitness_values (list): List of fitness values corresponding to the population.
        offspring_fitness (list): List of fitness values corresponding to the offspring.
        num_elites (int): Number of top individuals (elites) to be preserved for the next generation.

    Returns:
        list: Elites selected to pass to the next generation.

    Elitism survivor selection is a strategy used in evolutionary algorithms to preserve the best-performing individuals 
    (elites) from the current population and offspring to the next generation without any alteration. This approach helps 
    maintain diversity and prevent loss of good solutions over generations.

    The function takes the following steps:
    1. Combine the current population and offspring lists into a single list.
    2. Combine the fitness values of the population and offspring into a single list.
    3. Zip the combined population and fitness lists to pair each individual with its corresponding fitness value.
    4. Sort the paired list based on fitness values in ascending order.
    5. Select the top 'num_elites' individuals (elites) from the sorted list.
    6. Return the list of elites selected to pass to the next generation.
    """
    # Combine the current population and offspring
    combined_population = population + offspring
    combined_fitness = fitness_values + offspring_fitness
    
    # Zip the combined population and fitness lists to pair each individual with its corresponding fitness value
    combined_individuals_fitness = zip(combined_population, combined_fitness)
    
    # Sort the combined population by fitness values in ascending order
    sorted_combined = sorted(combined_individuals_fitness, key=lambda x: x[1])
    
    # Select the top individuals (elites) to pass to the next generation
    elites = [individual for individual, _ in sorted_combined[:num_elites]]
    
    return elites


