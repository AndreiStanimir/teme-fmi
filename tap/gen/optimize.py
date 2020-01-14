"""
Algoritm genetic care optimizează o funcție obiectiv
"""

import copy
import math
import random

# Parametrii configurabili
POPULATION_SIZE = 10
FUNCTION_RANGE = (-1, 2)

PRECISION = 5

RECOMBINATION_PROBA = 0.5
MUTATION_PROBA = 0.25

STEPS = 15


DECIMAL_RANGE = 10 ** PRECISION

left, right = FUNCTION_RANGE
RANGE_LEN = right - left

GENOME_LENGTH = math.ceil(math.log2(RANGE_LEN * DECIMAL_RANGE))


def objective(x):
    return -x ** 2 + x + 2


class Chromosome:
    def __init__(self):
        self.bits = [False] * GENOME_LENGTH

    def to_float(self):
        value = 0
        for bit in self.bits:
            value = (value << 1) | bit
        return RANGE_LEN * value / (2 ** GENOME_LENGTH - 1)

    def fitness(self):
        return objective(self.to_float())

    def flip(self, index):
        self.bits[index] = not self.bits[index]

    @staticmethod
    def random():
        chromo = Chromosome()

        bits = random.getrandbits(GENOME_LENGTH)
        for i in range(GENOME_LENGTH):
            chromo.bits[i] = bool(bits % 2)
            bits //= 2

        return chromo

    def __repr__(self):
        return f'Chromo(x={self.to_float():.4f})'


def selection(population):
    fitnesses = [chromo.fitness() for chromo in population]
    selected = random.choices(population, weights=fitnesses, k=len(population))
    return selected


def split_population(population, proba):
    selected = []
    not_selected = []

    for chromo in population:
        if random.random() < proba:
            selected.append(chromo)
        else:
            not_selected.append(chromo)

    return selected, not_selected


def crossover(a, b):
    split_point = random.randint(0, GENOME_LENGTH - 1)
    a.bits[:split_point], b.bits[:split_point] = b.bits[:split_point], a.bits[:split_point]


population = [Chromosome.random() for _ in range(POPULATION_SIZE)]

for step in range(STEPS):
    population = selection(population)

    selected, population = split_population(population, RECOMBINATION_PROBA)

    if len(selected) >= 2:
        if len(selected) % 2 == 1:
            a = selected.pop()
            b = copy.deepcopy(selected[-1])
            crossover(a, b)
            population.append(b)

        for i in range(0, len(selected) - 1, 2):
            crossover(selected[i], selected[i + 1])
            population += [selected[i], selected[i + 1]]
    else:
        population += selected

    selected, population = split_population(population, MUTATION_PROBA)
    for chromo in selected:
        index = random.randint(0, GENOME_LENGTH - 1)
        chromo.flip(index)
        population.append(chromo)


    best = max(population, key=Chromosome.fitness)
    print(f"Step #{step + 1} = {best.fitness():.4f} for x = {best.to_float():.4f}")
