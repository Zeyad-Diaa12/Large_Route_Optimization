import random
import numpy as np

random.seed(42)

def exponential_rank_selection(population, fitness_values, selection_pressure=1.1):
  """
  This function implements Exponential Rank Selection, an algorithm used in Evolutionary Algorithms (EA) 
  to select individuals for reproduction based on their fitness.

  Args:
      population (list): A list containing the individuals (potential solutions) in the current population.
      fitness_values (list): A list containing the corresponding fitness values for each individual in the population.
          Higher fitness values represent better solutions.
      selection_pressure (float, optional): Controls the selection intensity towards fitter individuals. Defaults to 1.2.
          - Values closer to 1 lead to weaker selection pressure, meaning all individuals have a more equal chance 
            of being selected.
          - Values further from 1 (like 2 or higher) lead to stronger selection pressure, where fitter individuals 
            have a significantly higher chance of being selected.

  Returns:
      individual: A single individual (solution) selected from the population for reproduction.
  """
  # Sort together individuals and their corresponding fitness values based on fitness (ascending order)
  sorted_population = sorted(zip(population, fitness_values), key=lambda x: x[1])
  ranks = range(1, len(sorted_population) + 1)  # Assign ranks (from 1 to population size) to each individual based on its position in the sorted list (better fitness -> lower rank)

  # Calculate selection probability for each individual based on its rank and the selection pressure
  # - Higher ranks (lower fitness) will have lower selection probabilities.
  # - The selection pressure parameter controls the shape of this probability distribution. Higher pressure 
  #   concentrates probability mass towards fitter individuals with lower ranks.
  selection_probs = [1 / (rank ** selection_pressure) for rank in ranks]

  # Use weighted random selection to choose an individual for reproduction.
  # - Individuals with higher selection probabilities are more likely to be chosen.
  selected = random.choices(sorted_population, weights=selection_probs)[0]
  return selected[0]  # Return only the individual (not the fitness value)

def tournament_selection(population, fitness_values, tournament_size=20):
  """
  This function performs Tournament Selection, another common selection method in EAs. 

  Args:
      population (list): A list containing the individuals (potential solutions) in the current population.
      fitness_values (list): A list containing the corresponding fitness values for each individual in the population.
          Lower fitness values represent better solutions (assuming a minimization problem).
      tournament_size (int, optional): The number of individuals competing in each mini-tournament. Defaults to 4.
          Larger tournament sizes tend to provide a more balanced selection pressure 
          compared to smaller sizes that might be more prone to selecting random "lucky" individuals.

  Returns:
      individual: The fittest individual selected through the tournaments.
  """
  selected = None
  # Perform multiple mini-tournaments (number of tournaments = tournament_size)
  for _ in range(tournament_size):
    # Randomly sample individuals to participate in the current tournament
    tournament = random.sample(list(zip(population, fitness_values)), tournament_size)

    # Find the individual with the LOWEST (Best) fitness value in the tournament
    winner = min(tournament, key=lambda x: x[1])[0]

    # Update the selected individual if the current winner has a lower (better) fitness value
    if selected is None or fitness_values[population.index(winner)] > fitness_values[population.index(selected)]:
      selected = winner

  return selected
