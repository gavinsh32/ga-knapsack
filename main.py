# main.py
# Gavin Haynes
# CS 4731 Evolutionary Computation
# Project 1 - GA Knapsack 

import math
import random

# Individual Constants
NUM_ITEMS = 32
MAX_WEIGHT = 64
MAX_VALUE = 16
MUTATION_NUM = 1
WEIGHT_THRESH = 50

# Popuation Constants
POP_SIZE = 32
MAX_PARENTS = 8
TOURN_SIZE = 3

ITEMS = [
    (random.randint(1, MAX_VALUE),
     random.randint(1, MAX_WEIGHT))
    for _ in range(NUM_ITEMS)
]

print('\nItems:\n', ITEMS)

def main():
    pass

class individual:
    
    def __init__(self):
        
        self.genome = [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        self.fitness = 0
        self.value = 0
        self.weight_diff = 0
        self.calc()

    def mutate(self):
        
        for i in range(MUTATION_NUM):
            
            index = random.randrange(NUM_ITEMS)
            self.genome[index] = 1 - self.genome[index]
            self.calc()
            
            # If the weight difference is too high, revert the mutation
            # and try again.
            if self.weight_diff > WEIGHT_THRESH:
                self.genome[index] = 1 - self.genome[index]
                self.calc()
                i -= 1

    def calc(self):

        self.value = 0
        self.weight_diff = 0
        
        for i in range(NUM_ITEMS):
            if self.genome[i] == 1:
                self.value += ITEMS[i][0]
                self.weight_diff += ITEMS[i][1]
        
        self.weight_diff = MAX_WEIGHT - self.weight_diff

        if self.weight_diff > 0:
            self.fitness = 0
        else:
            self.fitness = self.value

    def copy(self):
        dst = individual()
        dst.genome = self.genome.copy()
        dst.calc()
        return dst

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

        self.calc()
    
    def reproduce(self):
        for _ in range(random.randint(1, MAX_PARENTS)):
            child = self.select()
            child.mutate()
            self.members.append(child)
        
        self.calc()

    def select(self):
        """
        Selects a random individual from the population via a tournament.
        """

        return self.members[self.tourn()].copy()

    def tourn(self):
        """
        Tournament selection of k individuals.
        """

        best = -1
        best_fit = -9999

        for i in range(TOURN_SIZE):
            ind = random.randint(0, POP_SIZE - 1)
            if self.members[ind].fitness > best_fit:
                best_fit = self.members[ind].fitness
                best = ind

        return best

    def calc(self):
        """
        Calculates the average fitness and best fitness of the population.
        """

        self.avg_fit = 0
        self.best_fit = -9999
        self.best_ind = -1

        for i in range(POP_SIZE):
            self.avg_fit += self.members[i].fitness
            if self.members[i].fitness > self.best_fit:
                self.best_fit = self.members[i].fitness
                self.best_ind = i

        self.avg_fit //= POP_SIZE

    def __str__(self):
        return f'Avg: {self.avg_fit} Best: {self.best_fit} Best Ind: {self.best_ind}'
    
print('\nTest Individual:')
test_ind = individual()
print(test_ind)
print('\nTest Population:')
test_pop = population()
print(test_pop)
print()
print('Best tourn:', str(test_pop.members[test_pop.tourn()]))
print()
test_pop.reproduce()
print('After Reproduce:')
print(test_pop)
    
if __name__ == "__main__":
    main()