import random
from matplotlib.animation import FuncAnimation
import streamlit as st
import matplotlib.pyplot as plt
import GA
import GA.gentic_algo
from GA.genome import Chromosome
from GA.fitness import Fitness
from GA.individual import Individual
from GA.truck import Truck
from GA.crossover import order_crossover, edge_crossover
from GA.mutation import swap_mutation, scramble_mutation, insertion_mutation, inversion_mutation
from GA.selection import tournament_selection, exponential_rank_selection
from GA.elitism import elitism_survivor_selection
from GA.load_data import distance_matrix, mapped_orders, list_mapped_orders

def run_ga_order_crossover(population_size, candidate_len, generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism):
    population = []
    fitness_values = []
    generation = []
    average_fitness_in_each_generation = []

    def initialize_population(population_size, candidate_len):
        for i in range(population_size):
            truck = Truck()
            candidate = [random.randint(0, 1) for _ in range(candidate_len)]
            fit = Fitness(candidate, truck)
            fit.get_fitness()
            genome = Chromosome(candidate, fit.fitness, truck.truck_id)
            population.append(genome)
            fitness_values.append(genome.fitness)

    def crossover(parent1, parent2, crossover_rate, crossover_fn):
        if random.random() < crossover_rate:
            child1, child2 = crossover_fn(parent1.cand, parent2.cand)
            child1 = Chromosome(child1, Fitness(child1, Truck()).get_fitness(), parent1.truck_id)
            child2 = Chromosome(child2, Fitness(child2, Truck()).get_fitness(), parent2.truck_id)
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

            next_generation_fitness.append(child1.fitness)
            next_generation_fitness.append(child2.fitness)

        # Survivor Selection
        elites = survivor_mechanism(population, next_generation, fitness_values, next_generation_fitness)

        # Update population with elites and remaining individuals from next generation
        population[:] = elites + random.sample(next_generation, population_size - len(elites))

        # Recalculate fitness values for the entire population
        fitness_values[:] = [individual.fitness for individual in population]

        # Record statistics
        generation.append(frame)
        average_fitness = sum(fitness_values) / len(fitness_values)
        average_fitness_in_each_generation.append(average_fitness)
        print(f"Generation {frame}: Average Fitness = {average_fitness}")

    # Display real-time graph
    fig, ax = plt.subplots()
    def update(frame):
        ax.clear()
        update_plot(frame)
        ax.plot(generation, average_fitness_in_each_generation, marker='o', linestyle='-', color='b')
        ax.set_title('Average Fitness Across Generations')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Average Fitness')
        ax.grid(True)

    ani = FuncAnimation(fig, update, frames=range(generations), repeat=False)
    st.pyplot(fig)
    return population, generations, average_fitness_in_each_generation

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

    # Display real-time graph
    fig, ax = plt.subplots()  # Create figure and axis objects
    chart, = ax.plot([], [], marker='o', linestyle='-', color='b')  # Initialize an empty plot

    def update_plot(frame):
        ax.clear()  # Clear the previous plot
        ax.plot(range(frame + 1), average_fitness[:frame + 1], marker='o', linestyle='-', color='b')  # Plot the average fitness
        ax.set_title('Average Fitness Across Generations')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Average Fitness')
        ax.grid(True)

    # Create animation
    ani = FuncAnimation(fig, update_plot, frames=range(generations), repeat=False)
    st.pyplot(fig)  # Display the animation
    return population, generations, average_fitness_in_each_generation

# User-defined hyperparameters (default values)
population_size = st.sidebar.number_input("Population Size", min_value=10, max_value=100, value=50)
mutation_rate = st.sidebar.number_input("Mutation Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
crossover_rate = st.sidebar.number_input("Crossover Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
num_generations = st.sidebar.number_input("Number of Generations", min_value=30, max_value=1000, value=50)
candidate_len = st.sidebar.number_input("Candidate Length", min_value=5, max_value=20,step=1,value=10)

# Mapping between selection options and functions
crossover_functions = {
    "Order Crossover": order_crossover,
    "Edge Crossover": edge_crossover
}

mutation_functions = {
    "Swap": swap_mutation,
    "Insertion": insertion_mutation,
    "Scramble": scramble_mutation,
    "Inversion": inversion_mutation
}

selection_functions = {
    "Exponential": exponential_rank_selection,
    "Tournament": tournament_selection
}

survivor_strategies = {
    "Elitism": elitism_survivor_selection
}

# User selection from the sidebar
crossover_option = st.sidebar.selectbox("Crossover Function", list(crossover_functions.keys()))
mutation_option = st.sidebar.selectbox("Mutation Function", list(mutation_functions.keys()))
selection_option = st.sidebar.selectbox("Selection Function", list(selection_functions.keys()))
survivor_option = st.sidebar.selectbox("Survivor Strategy", list(survivor_strategies.keys()))

# Assign selected functions based on user choice
crossover_fn = crossover_functions[crossover_option]
mutation_fn = mutation_functions[mutation_option]
selection_fn = selection_functions[selection_option]
survivor_mechanism = survivor_strategies[survivor_option]

# Title and Introduction
st.title("GA Large Route Optimization")
st.write("This interactive tool allows you to visualize delivery routes and adjust hyperparameters for your GA optimization process.")

# Route Visualization (placeholder for your visualization function)
def visualize_route(route):
    # Implement your route visualization logic here (e.g., map or list with connections)
    st.write("Route Visualization Placeholder")

# Run GA Button and Logic
if st.button("Run GA"):
    if(crossover_fn == "Edge Crossover"):
        population, generations, average_fitness = run_ga_edge_crossover(population_size, candidate_len, num_generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism)
    else:
        population, generations, average_fitness = run_ga_order_crossover(population_size, candidate_len, num_generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism)
