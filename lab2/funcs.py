import random

from itertools import compress




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


def get_elites(population, number_of_elites, items, knapsack_max_capacity):
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


def mutation(population):
      mutated_population = []
      for individual in population:
            mutated_individual = individual.copy()

            index = random.randint(0, len(individual)-1)

            mutated_individual[index] = 1 - mutated_individual[index]

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