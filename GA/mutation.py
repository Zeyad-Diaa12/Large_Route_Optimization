import random

def swap_mutation(chromosome):
  """
  This function performs Swap Mutation on a chromosome, a common technique in Genetic Algorithms (GAs) 
  to introduce variation into the population. Swap mutation randomly selects two positions within the 
  chromosome and swaps the elements at those positions. This can potentially disrupt existing good 
  combinations of genes (sub-parts of the chromosome) and create new combinations that might be 
  beneficial for the fitness of the individual.

  Args:
      chromosome (list): A list representing the chromosome (individual) to be mutated.

  Returns:
      list: The mutated chromosome with the swapped elements.
  """
  size = len(chromosome)
  # Select two distinct positions randomly (using random.sample to avoid duplicates)
  pos1, pos2 = random.sample(range(size), 2)
  # Swap the elements at the selected positions
  chromosome[pos1], chromosome[pos2] = chromosome[pos2], chromosome[pos1]
  return chromosome

def scramble_mutation(chromosome):
  """
  This function performs Scramble Mutation on a chromosome. Scramble mutation randomly selects a 
  subset of the chromosome and shuffles the order of the elements within that subset. This mutation 
  can be particularly useful for problems where the relative order of genes within a chromosome 
  might be less crucial compared to the presence or absence of specific genes. Shuffling elements 
  within a subset can disrupt existing combinations while potentially creating new beneficial arrangements.

  Args:
      chromosome (list): A list representing the chromosome (individual) to be mutated.

  Returns:
      list: The mutated chromosome with the scrambled elements.
  """
  size = len(chromosome)
  # Select a random starting and ending position for the subset (sorted to ensure start < end)
  start, end = sorted(random.sample(range(size), 2))
  # Scramble the elements within the selected subset
  subset = chromosome[start:end]
  random.shuffle(subset)
  # Replace the original subset with the scrambled elements
  chromosome[start:end] = subset
  return chromosome

def inversion_mutation(chromosome):
  """
  This function performs Inversion Mutation on a chromosome. Inversion mutation randomly selects a 
  subset of the chromosome and reverses the order of the elements within that subset. Similar to 
  scramble mutation, this can be useful for problems where the relative order is not as important 
  as the presence/absence of specific genes. However, inversion mutation might be more likely to 
  preserve existing good combinations within the subset compared to scrambling, as it essentially flips 
  a section of the chromosome while maintaining the relative order within that section.

  Args:
      chromosome (list): A list representing the chromosome (individual) to be mutated.

  Returns:
      list: The mutated chromosome with the inverted elements.
  """
  size = len(chromosome)
  # Select a random starting and ending position for the subset (sorted to ensure start < end)
  start, end = sorted(random.sample(range(size), 2))
  # Reverse the order of elements within the selected subset using slicing with a step of -1
  chromosome[start:end] = chromosome[start:end][::-1]
  return chromosome

def insertion_mutation(chromosome):
  """
  This function performs Insertion Mutation on a chromosome. Insertion mutation randomly selects two 
  positions within the chromosome. It removes the element at the first position and inserts it at the 
  second position, shifting other elements in the chromosome as necessary to accommodate the insertion. 
  This mutation can be particularly useful for problems where the absolute position of a gene 
  within the chromosome might be important for its functionality. By inserting a gene at a new 
  position, it can potentially disrupt existing interactions with nearby genes while introducing it to 
  potentially beneficial interactions at the new location.

  Args:
      chromosome (list): A list representing the chromosome (individual) to be mutated.

  Returns:
      list: The mutated chromosome with the element inserted at a new position.
  """
  size = len(chromosome)
  # Select two distinct positions randomly (using random.sample to avoid duplicates)
  pos1, pos2 = random.sample(range(size), 2)
  # Remove the element at the first position
  element = chromosome.pop(pos1)
  # Insert the removed element at the second position, shifting elements to the right if necessary
  chromosome.insert(pos2, element)
  return chromosome

def random_resetting_mutation(chromosome):
    """
    This function performs Random Resetting Mutation on a chromosome. Random resetting mutation
    randomly selects a gene (element) within the chromosome and replaces it with a randomly chosen
    value that is not already present in the chromosome. This mutation introduces variation by
    potentially replacing existing genes with new ones, which can help explore different regions
    of the search space.

    Args:
        chromosome (list): A list representing the chromosome (individual) to be mutated.

    Returns:
        list: The mutated chromosome with a randomly chosen gene reset.
    """
    size = len(chromosome)
    
    # Convert string values to integers for comparison
    chromosome = [int(gene) for gene in chromosome]
    
    # Select a random position within the chromosome
    pos = random.randint(0, size - 1)
    
    # Choose a new value that is not already present in the chromosome
    new_value = random.choice([val for val in range(size) if val not in chromosome])
    
    # Reset the gene at the selected position with the new value
    chromosome[pos] = new_value
    
    # Convert integers back to string representation
    chromosome = [str(gene) for gene in chromosome]
    
    return chromosome


