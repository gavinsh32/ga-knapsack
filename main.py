# main.py
# Gavin Haynes
# CS 4731 Evolutionary Computation
# Project 1 - GA Knapsack 

import math
import random

# Individual Constants
NUM_ITEMS = 16
MAX_WEIGHT = 64
MAX_VALUE = 16
MUTATION_NUM = 1
WEIGHT_THRESH = 200

# Popuation Constants
POP_SIZE = 16
MAX_PARENTS = 4
TOURN_SIZE = 3

# Simulation Constants
NUM_TRIALS = 10
NUM_GENERATIONS = 100

ITEMS = [
    (random.randint(1, MAX_VALUE),
     random.randint(1, MAX_WEIGHT // 2))
    for _ in range(NUM_ITEMS)
]

def main():

    total_item_weight = sum(item[1] + MAX_WEIGHT for item in ITEMS)

    print('\nKnapsack with', NUM_ITEMS, 'items and a maximum weight of', MAX_WEIGHT, 'and items totaling a weight of', total_item_weight, 'and an average weight of', total_item_weight // NUM_ITEMS, '\n')

    for trial in range(1):

        pop = population()

        for gen in range(10):
            print('Generation:', gen, 'size:', len(pop))
            print(pop)

            for _ in range(random.randint(1, 4)):
                child = pop.select().copy()
                child.mutate()
                print('Adding', child)
            
            pop.members.append(child)
            pop.calc()

class individual:
    
    def __init__(self):
        
        self.genome = [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        self.fitness = 0
        self.value = 0
        self.weight_diff = 0
        self.calc()

    def mutate(self):
        """
        Mutates the individual by flipping a random bit in the genome.
        """
        for i in range(MUTATION_NUM):
            
            index = random.randrange(NUM_ITEMS)
            self.genome[index] = 1 - self.genome[index]
            
        self.calc()

    def calc(self):
        """
        Calculates the fitness, value, and weight difference of the individual.
        """
        self.value = 0
        self.weight_diff = 0
        
        for i in range(NUM_ITEMS):
            if self.genome[i] == 1:
                self.value += ITEMS[i][0]
                self.weight_diff += ITEMS[i][1]
        
        self.weight_diff = MAX_WEIGHT - self.weight_diff

        self.fitness = self.value

    def copy(self):
        """
        Returns a copy of the individual.
        """
        clone = individual()
        clone.genome = self.genome.copy()
        clone.calc()
        return clone

    def __str__(self):
        return f'{self.value} {self.weight_diff} {self.fitness} {self.genome}'
    
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
        self.size = POP_SIZE

        self.calc()
    
    def reproduce(self):
        for _ in range(random.randint(1, MAX_PARENTS)):
            parent = self.select()
            child = parent.copy()
            child.mutate()
            print('Child', child)
            self.members.append(child)

        self.calc()

    def select(self):
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

    def calc(self):
        """
        Calculates the average fitness and best fitness of the population.
        """

        self.avg_fit = 0
        self.best_fit = -9999
        self.best_ind = -1

        for i in range(len(self.members)):
            self.avg_fit += self.members[i].fitness
            if self.members[i].fitness > self.best_fit:
                self.best_fit = self.members[i].fitness
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
        return len(self.members)

    def __str__(self):
        return f'Avg: {self.avg_fit} Best: {self.best_fit} Best Ind: {self.best_ind}'
    
if __name__ == "__main__":
    main()