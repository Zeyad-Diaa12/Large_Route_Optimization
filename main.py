import time
import random
import streamlit as st
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
import networkx as nx
import datetime as dt

import GA
from GA.genome import Chromosome
from GA.fitness import Fitness
from GA.individual import Individual
from GA.truck import Truck
from GA.crossover import order_crossover, edge_crossover
from GA.mutation import swap_mutation, scramble_mutation, insertion_mutation, inversion_mutation,random_resetting_mutation
from GA.selection import tournament_selection, exponential_rank_selection
from GA.elitism import elitism_survivor_selection
from GA.load_data import mapped_orders


def run_ga_order_crossover(population_size, candidate_len, generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism,max_stops):
    population = []
    fitness_values = []
    generation = []
    average_fitness_in_each_generation = []
    best_population = []
    best_population_avg_fitness = float('inf')
    best_solution = []
    best_solution_fitness = 0.0

    def initialize_population(population_size, candidate_len):
        for _ in range(population_size):
            truck = Truck(max_stops=max_stops)
            candidate = Individual(candidate_len).individual
            fit = Fitness(candidate, truck)
            fit.get_fitness()
            population.append(candidate)
            fitness_values.append(fit.fitness)

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
        # Create a Plotly figure
    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(title="Average Fitness Across Generations", xaxis_title="Generation", yaxis_title="Average Fitness")

    chart = st.plotly_chart(fig)
    start_time = dt.datetime.now()
    for gen in range(generations):
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

            next_generation_fitness.append(Fitness(child1, Truck(max_stops=max_stops)).get_fitness())
            next_generation_fitness.append(Fitness(child2, Truck(max_stops=max_stops)).get_fitness())

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
        fitness_values = [Fitness(candidate, Truck(max_stops=max_stops)).get_fitness() for candidate in population]
        
        # Record statistics
        generation.append(gen+1)
        average_fitness = sum(fitness_values) / len(fitness_values)
        average_fitness_in_each_generation.append(average_fitness)
        if average_fitness < best_population_avg_fitness:
            best_solution_fitness = min(fitness_values)
            best_solution = population[fitness_values.index(best_solution_fitness)]
            best_population = population
            best_population_avg_fitness = average_fitness
        print(f"Generation {gen+1}: Average Fitness = {average_fitness}")

        fig.add_trace(go.Scatter(x=generation, y=average_fitness_in_each_generation, mode='lines+markers'), row=1, col=1)
        chart.plotly_chart(fig)
    st.write(f"Time taken to find best solution: {dt.datetime.now() - start_time}")
    return best_solution,best_solution_fitness,best_population,best_population_avg_fitness,generations,average_fitness_in_each_generation

def run_ga_edge_crossover(population_size, candidate_len, generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism,max_stops):
    population = []
    fitness_values = []
    generation = []
    average_fitness_in_each_generation = []
    best_population = []
    best_population_avg_fitness = float('inf')
    best_solution = []
    best_solution_fitness = 0.0

    def initialize_population(population_size, candidate_len):
        for _ in range(population_size):
            truck = Truck(max_stops=max_stops)
            candidate = Individual(candidate_len).individual
            fit = Fitness(candidate, truck)
            fit.get_fitness()
            population.append(candidate)
            fitness_values.append(fit.fitness)

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

    # Create a Plotly figure
    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(title="Average Fitness Across Generations", xaxis_title="Generation", yaxis_title="Average Fitness")

    chart = st.plotly_chart(fig)

    start_time = dt.datetime.now()
    for gen in range(generations):
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

            next_generation_fitness.append(Fitness(child, Truck(max_stops=max_stops)).get_fitness())

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
        fitness_values = [Fitness(candidate, Truck(max_stops=max_stops)).get_fitness() for candidate in population]

        # Record statistics
        generation.append(gen+1)
        average_fitness = sum(fitness_values) / len(fitness_values)
        average_fitness_in_each_generation.append(average_fitness)
        if average_fitness < best_population_avg_fitness:
            best_solution_fitness = min(fitness_values)
            best_solution = population[fitness_values.index(best_solution_fitness)]
            best_population = population
            best_population_avg_fitness = average_fitness
        print(f"Generation {gen+1}: Average Fitness = {average_fitness}")

        fig.add_trace(go.Scatter(x=generation, y=average_fitness_in_each_generation, mode='lines+markers'), row=1, col=1)
        chart.plotly_chart(fig)
    st.write(f"Time taken to find best solution: {dt.datetime.now() - start_time}")
    return best_solution,best_solution_fitness,best_population,best_population_avg_fitness,generations,average_fitness_in_each_generation

# User-defined hyperparameters (default values)
population_size = st.sidebar.number_input("Population Size", min_value=50, max_value=1000, value=50)
mutation_rate = st.sidebar.number_input("Mutation Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
crossover_rate = st.sidebar.number_input("Crossover Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.8)
num_generations = st.sidebar.number_input("Number of Generations", min_value=30, max_value=1000, value=50)
candidate_len = st.sidebar.number_input("Candidate Length", min_value=5, max_value=20, step=1, value=10)
max_stops = st.sidebar.number_input("Max Stops", min_value=5, max_value=20, step=1, value=10)

# Mapping between selection options and functions
crossover_functions = {
    "Order Crossover": order_crossover,
    "Edge Crossover": edge_crossover
}

mutation_functions = {
    "Swap": swap_mutation,
    "Insertion": insertion_mutation,
    "Scramble": scramble_mutation,
    "Inversion": inversion_mutation,
    "Random Resetting": random_resetting_mutation,
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

# Function to visualize the best solution as connected cities with a main point city
def visualize_best_solution(best_solution, main_point_city='61'):
    plt.figure()

    # Create a directed graph
    G = nx.DiGraph()
    cities = []

    # Add edges between cities in the best solution
    for individual in best_solution:
        city = mapped_orders[individual][1]
        cities.append(city)

    for i in range(len(cities)-1):
        G.add_edge(cities[i], cities[i + 1])

    # Add main point city as the starting point
    G.add_node(main_point_city)

    # Add edges from the main point city to the first city in the best solution
    G.add_edge(main_point_city, cities[0])

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=10, font_weight='bold', width=2, arrowsize=20)
    
    # Color the main city differently
    nx.draw_networkx_nodes(G, pos, nodelist=[main_point_city], node_color='green', node_size=700)

    plt.title('Best Solution')
    plt.axis('off')  # Disable axis
    st.pyplot(plt)  # Display the plot in Streamlit

def printData():
    st.write(f"Population size :{len(best_population)}")
    st.write(f"Best Average Fitness :{best_population_avg_fitness}")
    st.write(f"Best Solution :{best_sol}")
    st.write(f"Best Solution Fitness :{best_sol_fit}")

# def outputTable(best_solution):
    

best_population = []
best_population_avg_fitness=[]
genrations= []
average_fitness = []
# Run GA Button and Logic
if st.button("Run GA"):
    if crossover_option == "Edge Crossover":
        best_sol,best_sol_fit,best_population,best_population_avg_fitness,genrations,average_fitness = run_ga_edge_crossover(population_size, candidate_len, num_generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism,max_stops)
        printData()
        visualize_best_solution(best_sol)
    else:
        best_sol,best_sol_fit,best_population,best_population_avg_fitness,genrations,average_fitness = run_ga_order_crossover(population_size, candidate_len, num_generations, crossover_rate, mutation_rate, crossover_fn, mutation_fn, selection_fn, survivor_mechanism,max_stops)
        printData()
        visualize_best_solution(best_sol)
