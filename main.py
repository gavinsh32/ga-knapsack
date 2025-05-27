# main.py
# Gavin Haynes
# CS 4731 Evolutionary Computation
# Project 1 - GA Knapsack 

import random
import matplotlib.pyplot as plt

# Item Constants
NUM_ITEMS = 20
MAX_WEIGHT = 10000

# Individual Constants
MUTATION_NUM = 1

# Scoring Constants
SCORE_SCALE = 1.3

# Popuation Constants
INITIAL_POP_SIZE = 16
MAX_PARENTS = 4
TOURN_SIZE = 5

# Simulation Constants
NUM_TRIALS = 3
NUM_GENERATIONS = 50

# Item Generation
items = []
for i in range(NUM_ITEMS):
    weight = random.randint(1, 10000)
    value = weight + 1000 + random.randint(0, 100)
    items.append((value, weight))

class Individual:
    """
    Represents an individual solution to the knapsack problem.
    """
    def __init__(self):
        self.genome = [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        self.fitness = 0
        self.value = 0
        self.weight = 0
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
        self.weight = 0
        self.fitness = 0
        
        for i in range(NUM_ITEMS):
            if self.genome[i] == 1:
                self.value += items[i][0]
                self.weight += items[i][1]
        
        if self.weight <= MAX_WEIGHT:
            self.fitness = self.value
        else:
            self.fitness = int(self.value - (self.weight - MAX_WEIGHT) * SCORE_SCALE)

    def copy(self) -> 'Individual':
        """
        Returns a copy of the individual.
        """
        clone = Individual()
        clone.genome = self.genome[:]
        clone.update()
        return clone

    def __str__(self):
        return f'${self.value}, {self.weight}oz, {self.fitness} fit'
    
    def __repr__(self):
        return str(self.genome)
    
class Population:
    def __init__(self):
        """
        Initializes the population with a list of individuals.
        """
        self.members = [Individual() for _ in range(INITIAL_POP_SIZE)]
        self.avg_fit = 0
        self.best_fit = -9999
        self.best_ind = -1
        self.avg_weight = 0
        self.update()

    def reproduce(self, max_parents=MAX_PARENTS) -> None:
        """
        Perform reproduction by tournament selection and replication with mutation.
        """
        elite = self.members[self.best_ind].copy()
        elite.mutate()
        self.members.append(elite)

        for _ in range(random.randint(1, max_parents)):
            parent = self.select()
            child = parent.copy()
            child.mutate()
            self.members.append(child)

        self.update()

    def select(self) -> Individual:
        """
        Tournament selection of k individuals. Returns the index of the best individual.
        """
        best = 0
        best_fit = self.members[best].fitness

        for i in range(TOURN_SIZE):
            ind = random.randint(0, INITIAL_POP_SIZE - 1)
            if self.members[ind].fitness > best_fit:
                best_fit = self.members[ind].fitness
                best = ind

        return self.members[best].copy()

    def update(self) -> None:
        """
        Calculates the average weight, average fitness, best individual, and fitness of the population. 
        """
        self.avg_weight = sum(ind.weight for ind in self.members) / len(self.members)
        self.avg_fit = sum(ind.fitness for ind in self.members) / len(self.members)
        self.best_fit = -999999
        self.best_ind = -1

        for i, indiv in enumerate(self.members):
            if indiv.fitness > self.best_fit:
                self.best_fit = indiv.fitness
                self.best_ind = i

    def display(self):
        for member in self.members:
            print(member)

    def __len__(self):
        return len(self.members)

all_best_fit = [0 for _ in range(NUM_GENERATIONS)]
all_avg_fit = [0 for _ in range(NUM_GENERATIONS)]
all_best_value = [0 for _ in range(NUM_GENERATIONS)]

# Simulation Loop
for trial in range(NUM_TRIALS):
    pop = Population()
    
    for gen in range(NUM_GENERATIONS):
        print(f'Gen: {gen}, Avg Fit: {pop.avg_fit}, Best: {pop.members[pop.best_ind].fitness}, ${pop.members[pop.best_ind].value}')
        #pop.display()
        pop.reproduce()
        all_best_fit[gen] += pop.best_fit
        all_avg_fit[gen] += pop.avg_fit
        all_best_value[gen] = pop.members[pop.best_ind].value

# Average the results over all trials
for i in range(NUM_GENERATIONS):
    all_best_fit[i] /= NUM_TRIALS
    all_avg_fit[i] /= NUM_TRIALS

# Plot Results
plt.figure(figsize=(8, 6))
plt.plot(all_best_fit, label='Best Fit')
plt.plot(all_avg_fit, label='Average Fit')
plt.xlabel('Generation')
plt.ylabel('Value / Fitness ($)')
plt.title(f'Value Over Generations')
plt.legend()
plt.savefig(f'./results/result-{NUM_ITEMS}-items.png')
plt.show()