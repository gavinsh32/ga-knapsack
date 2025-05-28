# main.py
# Gavin Haynes
# CS4731 Evolutionary Computation
# Project 1 - GA Knapsack 

import random
import matplotlib.pyplot as plt

# Item Constants
NUM_ITEMS = 20
MAX_WEIGHT = 10000
INITIAL_ITEM_THRESH = 1.5

# Individual Constants
MUTATION_NUM = NUM_ITEMS // 20

# Popuation Constants
POP_SIZE = 20
MAX_PARENTS = 10
TOURN_SIZE = 3

# Scoring Constants
SCORE_SCALE = 1.3

# Simulation Constants
NUM_TRIALS = 3
NUM_GENERATIONS = 50

# Item Generation
items = []
for i in range(NUM_ITEMS):
    weight = random.randint(1, 10000)
    value = weight + 1000 + random.randint(0, 100)
    items.append((value, weight))

# Simulation Results
all_best_fit = [0.0 for _ in range(NUM_GENERATIONS)]
all_avg_fit = [0.0 for _ in range(NUM_GENERATIONS)]
all_best_value = [0.0 for _ in range(NUM_GENERATIONS)]

# Simulation Loop
def main():
    for trial in range(NUM_TRIALS):
        pop = Population()

        for gen in range(NUM_GENERATIONS):
            print(f'Gen: {gen}, Avg Fit: {pop.avg_fit}, Best: {pop.members[pop.best_ind].fitness}, ${pop.members[pop.best_ind].value}, avg weight: {pop.avg_weight} oz')
            #pop.display()
            pop.generation()
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
    plt.savefig(f'result.png')

class Individual:
    """
    Represents an individual solution to the knapsack problem.
    """
    def __init__(self):
        self.fitness = 0
        self.value = 0
        self.weight = 0
        self.genome = [0 for _ in range(NUM_ITEMS)]
        
        for _ in range(NUM_ITEMS):
            if abs(self.weight - MAX_WEIGHT) < 5000:
                break
            self.genome[random.randrange(NUM_ITEMS)] = 1
            self.update()

    def mutate(self):
        """
        Mutates the individual by flipping a random bit in the genome.
        """
        for i in range(MUTATION_NUM):
            index = random.randrange(NUM_ITEMS)
            self.genome[index] = 1 - self.genome[index]
            
        self.update()

    def update(self):
        """
        Update the fitness, value, and weight difference of the individual.
        """
        self.value = 0
        self.weight = 0
        self.fitness = 0
        
        for i in range(NUM_ITEMS):
            if self.genome[i] == 1:
                self.value += items[i][0]
                self.weight += items[i][1]
        
        # Weight does not exceed
        if self.weight <= MAX_WEIGHT:
            self.fitness = self.value
        # Weight exceeds, apply penalty
        else:
            self.fitness = int(self.value - (self.weight - MAX_WEIGHT) * 1.5)

    def copy(self) -> 'Individual':
        """
        Returns a copy of the individual.
        """
        clone = Individual()
        clone.genome = self.genome[:]
        clone.update()
        return clone

    def __str__(self):
        return f'${self.value}, {self.weight}oz, {self.fitness} fit {self.genome}'
    
    def __repr__(self):
        return str(self.genome)
    
class Population:
    def __init__(self):
        """
        Initializes the population with a list of individuals.
        """
        self.members = [Individual() for _ in range(POP_SIZE)]
        self.avg_fit = 0
        self.best_fit = -9999
        self.best_ind = -1
        self.avg_weight = 0
        self.update()

    def generation(self, max_parents=MAX_PARENTS) -> None:
        """
        Perform reproduction via tournament selectiona and one-point crossover.
        """
        # Keep the best individual
        elite = self.members[self.best_ind].copy()
        new_members = [elite]

        for _ in range(random.randint(1, max_parents)):
            # Select two parents
            a = self.select()
            b = self.select()
            
            # Perform one-point crossover
            p = random.randrange(NUM_ITEMS)
            c = Individual()
            c.genome = a.genome[:p] + b.genome[p:]
            c.mutate()
            c.update()

            # Replace random member in the population with the new child
            new_members.append(c)

        while len(new_members) < POP_SIZE:
            new_members.append(Individual())

        self.members = new_members[:POP_SIZE]
        self.update()

    def select(self) -> Individual:
        """
        Tournament selection of k individuals. Returns a copy.
        """
        best = 0
        best_fit = self.members[best].fitness

        for i in range(TOURN_SIZE):
            ind = random.randint(0, POP_SIZE - 1)
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
    
if __name__ == "__main__":
    main()