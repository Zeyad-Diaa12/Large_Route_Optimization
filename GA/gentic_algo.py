import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .genome import Chromosome
from .fitness import Fitness
from .individual import Individual
from .truck import Truck
from .crossover import order_crossover, edge_crossover
from .mutation import swap_mutation, scramble_mutation, insertion_mutation, inversion_mutation
from .selection import  tournament_selection, exponential_rank_selection
from .elitism import elitism_survivor_selection
from .load_data import distance_matrix, mapped_orders, list_mapped_orders

def run_ga_order_crossover(population_size, candidate_len, generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism):
    population = []
    fitness_values = []
    generation = []
    average_fitness_in_each_generation = []

    def initialize_population(population_size, candidate_len):
        for i in range(population_size):
            truck = Truck()
            candidate = Individual(candidate_len).individual
            fit = Fitness(candidate, truck)
            fit.get_fitness()
            genome = Chromosome(candidate, fit.fitness, truck.truck_id)
            population.append(genome.cand)
            fitness_values.append(genome.fitness)

    def crossover(parent1, parent2, crossover_rate, crossover_fn):
        if random.random() < crossover_rate:
            child1, child2 = crossover_fn(parent1, parent2)
        else:
            child1 = parent1
            child2 = parent2
        return child1, child2

    def mutation(child, mutation_rate, mutation_fn):
        if random.random() < mutation_rate:
            child = mutation_fn(child)
        return child

    def selection(population, fitness_values, selection_fn):
        return selection_fn(population, fitness_values)

    initialize_population(population_size, candidate_len)

    def update_plot(frame):
        nonlocal population, fitness_values, generation, average_fitness_in_each_generation
        nonlocal crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism

        next_generation = []
        next_generation_fitness = []
        for _ in range(population_size // 2):
            # Parent Selection
            parent1 = selection(population, fitness_values, selection_fn)
            parent2 = selection(population, fitness_values, selection_fn)

            # Crossover
            child1, child2 = crossover(parent1, parent2, crossover_rate, crossover_fn)

            # Mutation
            child1 = mutation(child1, mutation_rate, mutation_fn)
            child2 = mutation(child2, mutation_rate, mutation_fn)

            next_generation.append(child1)
            next_generation.append(child2)

            next_generation_fitness.append(Fitness(child1, Truck()).get_fitness())
            next_generation_fitness.append(Fitness(child2, Truck()).get_fitness())

        # Survivor Selection
        elites = survivor_mechanism(population, next_generation, fitness_values, next_generation_fitness)

        # Convert lists to tuples
        population_set = set(map(tuple, population))
        elites_set = set(map(tuple, elites))
        next_generation_set = set(map(tuple, next_generation))

        # Update population with elites and remaining individuals from next generation
        population_set = elites_set.union(next_generation_set)

        # Convert sets back to lists
        population = [list(individual) for individual in population_set]

        # Check if the population size matches the specified size
        if len(population) < population_size:
            # Add random individuals to fill the population to the specified size
            while len(population) < population_size:
                random_individual = random.choice(list(next_generation_set - elites_set))
                population.append(list(random_individual))

        # Truncate the population to the specified size
        population = population[:population_size]

        # Recalculate fitness values for the entire population
        fitness_values = [Fitness(candidate, Truck()).get_fitness() for candidate in population]

        # Record statistics
        generation.append(frame)
        average_fitness = sum(fitness_values) / len(fitness_values)
        average_fitness_in_each_generation.append(average_fitness)
        print(f"Generation {frame}: Average Fitness = {average_fitness}")

        # Clear previous plots and draw new ones
        plt.cla()
        plt.plot(generation, average_fitness_in_each_generation, marker='o', linestyle='-', color='b')
        plt.title('Average Fitness Across Generations')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.grid(True)

    # Create animation
    ani = FuncAnimation(plt.gcf(), update_plot, frames=range(generations), repeat=False)
    plt.show()
    return population,generations,average_fitness_in_each_generation
def run_ga_edge_crossover(population_size, candidate_len, generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism):
    population = []
    fitness_values = []
    generation = []
    average_fitness_in_each_generation = []

    def initialize_population(population_size, candidate_len):
        for i in range(population_size):
            truck = Truck()
            candidate = Individual(candidate_len).individual
            fit = Fitness(candidate, truck)
            fit.get_fitness()
            genome = Chromosome(candidate, fit.fitness, truck.truck_id)
            population.append(genome.cand)
            fitness_values.append(genome.fitness)

    def crossover(parent1, parent2, crossover_rate, crossover_fn):
        if random.random() < crossover_rate:
            child = crossover_fn(parent1, parent2)
        else:
            child = random.choice([parent1, parent2])
        return child

    def mutation(child, mutation_rate, mutation_fn):
        if random.random() < mutation_rate:
            child = mutation_fn(child)
        return child

    def selection(population, fitness_values, selection_fn):
        return selection_fn(population, fitness_values)

    initialize_population(population_size, candidate_len)

    def update_plot(frame):
        nonlocal population, fitness_values, generation, average_fitness_in_each_generation
        nonlocal crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism

        next_generation = []
        next_generation_fitness = []
        for _ in range(population_size):
            # Parent Selection
            parent1 = selection(population, fitness_values, selection_fn)
            parent2 = selection(population, fitness_values, selection_fn)

            # Crossover
            child = crossover(parent1, parent2, crossover_rate, crossover_fn)

            # Mutation
            child = mutation(child, mutation_rate, mutation_fn)

            next_generation.append(child)

            next_generation_fitness.append(Fitness(child, Truck()).get_fitness())

        # Survivor Selection
        elites = survivor_mechanism(population, next_generation, fitness_values, next_generation_fitness)

        # Convert lists to tuples
        population_set = set(map(tuple, population))
        elites_set = set(map(tuple, elites))
        next_generation_set = set(map(tuple, next_generation))

        # Update population with elites and remaining individuals from next generation
        population_set = elites_set.union(next_generation_set)

        # Convert sets back to lists
        population = [list(individual) for individual in population_set]

        # Check if the population size matches the specified size
        if len(population) < population_size:
            # Add random individuals to fill the population to the specified size
            while len(population) < population_size:
                random_individual = random.choice(list(next_generation_set - elites_set))
                population.append(list(random_individual))

        # Truncate the population to the specified size
        population = population[:population_size]

        # Recalculate fitness values for the entire population
        fitness_values = [Fitness(candidate, Truck()).get_fitness() for candidate in population]

        # Record statistics
        generation.append(frame)
        average_fitness = sum(fitness_values) / len(fitness_values)
        average_fitness_in_each_generation.append(average_fitness)
        print(f"Generation {frame}: Average Fitness = {average_fitness}")

        # Clear previous plots and draw new ones
        plt.cla()
        plt.plot(generation, average_fitness_in_each_generation, marker='o', linestyle='-', color='b')
        plt.title('Average Fitness Across Generations')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.grid(True)

    # Create animation
    ani = FuncAnimation(plt.gcf(), update_plot, frames=range(generations), repeat=False)
    plt.show()
    return population,generations,average_fitness_in_each_generation