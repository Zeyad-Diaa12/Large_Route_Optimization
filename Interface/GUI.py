import streamlit as st
import matplotlib.pyplot as plt  # For plotting the loss graph (optional)
# Import your GA core functionality (likely from separate files)
# from chromosome import Chromosome
# from ga_functions import evaluate_chromosome, run_ga 

# Pre-defined data (replace with your actual data loading logic)
distances = {'A': {'B': 10, 'C': 20}, 'B': {'C': 15, 'D': 30}, 'C': {'D': 25}}
item_weights = {'A': 2, 'B': 4, 'C': 1, 'D': 3}
truck_capacity = 5
time_windows = {'A': (9, 11), 'B': (10, 12), 'C': (11, 13), 'D': (12, 14)}
depot = 'A'
destination = 'D'

# User-defined hyperparameters (default values)
population_size = st.sidebar.number_input("Population Size", min_value=10, max_value=100, value=50)
mutation_rate = st.sidebar.number_input("Mutation Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.1)
crossover_rate = st.sidebar.number_input("Crossover Rate", min_value=0.0, max_value=1.0, step=0.01, value=0.7)
num_generations = st.sidebar.number_input("Number of Generations", min_value=10, max_value=100, value=50)

# Title and Introduction
st.title("GA Delivery Route Optimization")
st.write("This interactive tool allows you to visualize delivery routes and adjust hyperparameters for your GA optimization process.")

# Route Visualization (placeholder for your visualization function)
def visualize_route(route):
    # Implement your route visualization logic here (e.g., map or list with connections)
    st.write("Route Visualization Placeholder")

# Run GA Button and Logic
if st.button("Run GA"):
    best_chromosome, fitness_history = run_ga(
        population_size, mutation_rate, crossover_rate, num_generations,
        distances, item_weights, truck_capacity, time_windows, depot, destination
    )
    visualize_route(best_chromosome.get_stop_sequence())  # Call your visualization function

    # Plot Loss Graph (optional)
    plt.figure(figsize=(8, 5))
    plt.plot(fitness_history)
    plt.xlabel("Generation")
    plt.ylabel("Fitness Score")
    plt.title("Fitness Score Over Generations")
    st.pyplot()

# Display Current Best Route (if GA has run)
if 'best_chromosome' in st.session_state:
    best_route = st.session_state['best_chromosome'].get_stop_sequence()
    st.write("Current Best Route:", best_route)
