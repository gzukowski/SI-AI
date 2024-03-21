from itertools import compress
import random
import time
import matplotlib.pyplot as plt


from funcs import *

import sys

from data import *



POPULATION_SIZE = 100
GENERATIONS = 200
N_SELECTION = 40
N_ELITE = 6


items, knapsack_max_capacity = get_big()


start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), POPULATION_SIZE)




for _ in range(GENERATIONS):
    population_history.append(population)


    elites, rest_population = get_elites(population, N_ELITE, items, knapsack_max_capacity)
    parents = roulette_wheel_selection(items, knapsack_max_capacity, population, N_SELECTION)

    new_generation = crossover(parents)

    new_generation = mutation(new_generation)

    population = elites + new_generation

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)

    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)



end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', f"{best_fitness:,}")
print('Time: ', total_time)

#sys.exit(0)
# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
