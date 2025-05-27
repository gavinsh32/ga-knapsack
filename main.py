# main.py
# Gavin Haynes
# CS 4731 Evolutionary Computation
# Project 1 - GA Knapsack 

import math
import random
import numpy as np
import matplotlib.pyplot as plt

# Individual Constants
NUM_ITEMS = 16
MAX_WEIGHT = 32
MAX_VALUE = 16
MUTATION_NUM = 1
WEIGHT_THRESH = 70

# Popuation Constants
POP_SIZE = 16
MAX_PARENTS = 4
TOURN_SIZE = 3

# Simulation Constants
NUM_TRIALS = 1
NUM_GENERATIONS = 5

ITEMS = [
    (random.randint(1, MAX_VALUE),
     random.randint(1, MAX_WEIGHT))
    for _ in range(NUM_ITEMS)
]

def main():

    print('\n', ITEMS)
    print('\nKnapsack with', NUM_ITEMS, 'items and a maximum weight of', MAX_WEIGHT, '\n')

    all_avg_fit = []
    all_best_fit = []

    for trial in range(NUM_TRIALS):

        avg_fit = []
        best_fit = []
        pop = population()

        for gen in range(NUM_GENERATIONS):
            
            print(f'Gen: {gen}, Size: {len(pop)}, Avg: ${pop.avg_fit}, Best: ${pop.best_fit}, Diff: {pop.avg_weight_diff} oz')

            pop.display()

            pop.reproduce()
            
            avg_fit.append(pop.avg_fit)
            best_fit.append(pop.best_fit)

    plt.figure(figsize=(6, 4))
    plt.plot(avg_fit, label='Average')
    plt.plot(best_fit, label='Best')
    plt.xlabel('Generation')
    plt.ylabel('Value ($)')
    plt.title('Average and Best Value Over Generations')
    plt.legend()
    plt.show()

class individual:
    
    def __init__(self):
        
        self.genome = [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        self.fitness = 0
        self.value = 0
        self.weight_diff = 0
        self.update()

    def mutate(self, num_mutations=1):
        """
        Mutates the individual by flipping a random bit in the genome.
        """
        for i in range(MUTATION_NUM):
            
            index = random.randrange(NUM_ITEMS)
            self.genome[index] = 1 - self.genome[index]
            
        self.update()

    def update(self):
        """
        Calculates the fitness, value, and weight difference of the individual.
        """
        self.value = 0
        self.weight_diff = 0
        
        for i in range(NUM_ITEMS):
            if self.genome[i] == 1:
                self.value += ITEMS[i][0]
                self.weight_diff += ITEMS[i][1]
        
        # Difference from the maximum weight.
        # Positive is overweight and negative is underweight.
        self.weight_diff = self.weight_diff - MAX_WEIGHT

        # Set the fitness based on the weight difference.
        # If the weight difference is too large, the fitness is 0.
        if abs(self.weight_diff) < WEIGHT_THRESH:
            self.fitness = self.value
        else:
            self.fitness = 0

    def copy(self):
        """
        Returns a copy of the individual.
        """
        clone = individual()
        clone.genome = self.genome.copy()
        clone.update()
        return clone

    def __str__(self):
        return f'${self.value}, {self.weight_diff}oz, {self.fitness} fit'
    
    def __repr__(self):
        return str(self.genome)
    
class population:

    def __init__(self):
        """
        Initializes the population with a list of individuals.
        """
        
        self.members = [individual() for _ in range(POP_SIZE)]
        self.avg_fit = 0
        self.best_fit = -9999
        self.best_ind = -1
        self.avg_weight_diff = 0

        self.update()

    def reproduce(self, max_parents=MAX_PARENTS) -> None:
        """
        Perform reproduction by tournament selection and replication with mutation.
        """

        for _ in range(random.randint(1, max_parents)):
            
            parent = self.select()
            child = parent.copy()
            child.mutate()
            self.members.append(child)

        self.update()

    def select(self) -> individual:
        """
        Tournament selection of k individuals. Returns the index of the best individual.
        """

        best = -1
        best_fit = -9999

        for i in range(TOURN_SIZE):
            ind = random.randint(0, POP_SIZE - 1)
            if self.members[ind].fitness > best_fit:
                best_fit = self.members[ind].fitness
                best = ind

        return self.members[best].copy()

    def update(self) -> None:
        """
        Calculates the average fitness and best fitness of the population.
        """

        self.avg_fit = 0
        self.best_fit = -9999
        self.best_ind = -1
        self.avg_weight_diff = sum(ind.weight_diff for ind in self.members) // len(self.members)

        for i, indiv in enumerate(self.members):
            
            self.avg_fit += indiv.fitness
            
            if indiv.fitness > self.best_fit:
                
                self.best_fit = indiv.fitness
                self.best_ind = i

        self.avg_fit //= len(self.members)

    def display(self):
        """
        Displays the population.
        """
        print(self)
        for member in self.members:
            print(member)

    def __len__(self):
        """
        Returns the size of the population.
        """
        return len(self.members)
    
if __name__ == "__main__":
    main()