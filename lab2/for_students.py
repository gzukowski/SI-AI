from itertools import compress
import random
import time
import matplotlib.pyplot as plt

import sys

from data import *



POPULATION_SIZE = 100
GENERATIONS = 200
N_SELECTION = 30
N_ELITE = 6


def initial_population(individual_size, population_size):
    return [[random.choice([1, 0]) for _ in range(individual_size)] for _ in range(population_size)]

def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))

def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


def get_elites(population, number_of_elites):
    population_fitnesses = [(fitness(items, knapsack_max_capacity, individual), individual) for individual in population]

    population_fitnesses.sort(reverse=True)

    elites = [individual for _, individual in population_fitnesses[:number_of_elites]]

    rest_population = [individual for _, individual in population_fitnesses[number_of_elites:]]
    return elites, rest_population




def roulette_wheel_selection(items, knapsack_max_capacity, population, selection_quantity):
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    total_fitness = sum(population_fitnesses)
    probabilities = [fitness / total_fitness for fitness in population_fitnesses]

    selected = []

    for _ in range(selection_quantity):

        spinned = random.random()
        current_prob = 0

        for index, prob in enumerate(probabilities):
            current_prob = current_prob + prob

            if spinned <= current_prob:
                selected.append(population[index])
                break

    return selected


def mutation(population, mutation_rate):
    mutated_population = []
    for individual in population:
        mutated_individual = []
        for gene in individual:
            if random.random() < mutation_rate:
                mutated_individual.append(1 - gene)
            else:
                mutated_individual.append(gene)
        mutated_population.append(mutated_individual)
    return mutated_population



def crossover(parents):
    new_generation = []
    quantity_needed = (POPULATION_SIZE-N_ELITE) // 2

    for _ in range(quantity_needed):
        parent_a = random.choice(parents)
        parent_b = random.choice(parents)

        midpoint = len(parent_a) // 2

        descendant = parent_a[:midpoint] + parent_b[midpoint:]
        new_generation.append(descendant)

        descendant = parent_b[:midpoint] + parent_a[midpoint:]
        new_generation.append(descendant)

    return new_generation
     


items, knapsack_max_capacity = get_big()




start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), POPULATION_SIZE)


#print(population)


for _ in range(GENERATIONS):
    population_history.append(population)

    # TODO: implement genetic algorithm

    print("----")
    elites, rest_population = get_elites(population, N_ELITE)
    print(  )
    print("----")

    parents = roulette_wheel_selection(items, knapsack_max_capacity, population, N_SELECTION)

    new_generation = crossover(parents)

    mutation_rate = 0.7  

    new_generation = mutation(new_generation, mutation_rate)

    population = elites + new_generation

    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    #print(best_fitness)
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
