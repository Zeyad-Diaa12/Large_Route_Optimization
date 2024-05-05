from chromosome import Chromosome


initial_population = []

def initialize_population(number_of_candidates,candidate_len):
    for i in range(number_of_candidates):
        gene = Chromosome(candidate_len)
        gene._get_representation()
        gene._get_fitness()
        initial_population.append(gene)

initialize_population(1000,6)
lowest = [cand.fitness for cand in initial_population]
print(min(lowest))
