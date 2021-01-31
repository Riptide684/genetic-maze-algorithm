import random
import sys
import time

directions = ["R", "L", "D", "U"]
moves = {
    "R": [0, 1],
    "L": [0, -1],
    "U": [-1, 0],
    "D": [1, 0]
}
maze = []
maze_size = 0


class DNA:
    def __init__(self):
        self.genes = []
        self.fitness = 0

    def create_genes(self, number):
        for i in range(number):
            self.genes.append(directions[random.randint(0, 3)])

    def update_fitness(self):
        best_score = 0
        position = [0, 0]

        for a in range(maze_size):
            for b in range(maze_size):
                if maze[a][b] == "S":
                    position = [a, b]
                    break

        goal = [0, 0]

        for a in range(maze_size):
            for b in range(maze_size):
                if maze[a][b] == "F":
                    goal = [a, b]
                    break

        for gene in self.genes:
            position[0] += moves[gene][0]
            position[1] += moves[gene][1]
            if position[0] < 0 or position[0] >= maze_size or position[1] < 0 or position[1] >= maze_size:
                position[0] -= moves[gene][0]
                position[1] -= moves[gene][1]
            elif maze[position[0]][position[1]] == "X":
                position[0] -= moves[gene][0]
                position[1] -= moves[gene][1]

            if maze[position[0]][position[1]] == "F":
                best_score = 2*maze_size
                break

            score = 2 * maze_size - (abs(goal[0] - position[0]) + abs(goal[1] - position[1]))

            if score > best_score:
                best_score = score

        self.fitness = best_score**2

    def crossover(self, data):
        parent1 = data[0]
        parent2 = data[1]

        midpoint = random.randint(1, len(parent1.genes)-1)

        self.genes = list(parent1.genes[:midpoint] + parent2.genes[midpoint:])

    def mutate(self, chance):
        for k in range(len(self.genes)):
            num = random.randint(1, 100)
            if num <= chance:
                self.genes[k] = directions[random.randint(0, 3)]


class Population:
    def __init__(self, data):
        self.population_size = data[0]
        self.mutation_rate = data[1]
        self.generations = 0
        self.population = []
        self.pool = []
        self.done = False
        self.best = 0
        self.complete = []

    def populate(self):
        for n in range(self.population_size):
            chromosome = DNA()
            chromosome.create_genes(maze_size**2)
            self.population.append(chromosome)

    def calculate_fitness(self):
        for solution in self.population:
            solution.update_fitness()
            if solution.fitness > self.best:
                self.best = solution.fitness
                self.complete = solution.genes.copy()

            if solution.fitness == (2*maze_size)**2:
                self.done = True

    def generate(self):
        self.generations += 1
        self.pool = self.population.copy()

        maximum = 0

        for sequence in self.pool:
            maximum += sequence.fitness

        if maximum == 0:
            self.population = []
            self.populate()

        else:
            for m in range(self.population_size):
                number1 = random.randint(1, maximum)
                number2 = random.randint(1, maximum)
                current = 0

                while number1 > 0:
                    number1 -= self.pool[current].fitness
                    current += 1

                parent1 = self.pool[current-1]

                current = 0

                while number2 > 0:
                    number2 -= self.pool[current].fitness
                    current += 1

                parent2 = self.pool[current-1]

                self.population[m].crossover([parent1, parent2])
                self.population[m].mutate(self.mutation_rate)


def solve(board, size_of_population, rate_of_mutation):
    global maze
    maze = board.copy()
    global maze_size
    maze_size = len(maze)

    test = Population([size_of_population, rate_of_mutation])
    test.populate()
    achieved = 0
    starting_time = time.time()

    while not test.done:
        new_time = time.time()
        if new_time >= starting_time + 10:
            print("Halting program execution, time limit exceeded")
            print("Try increasing mutation rate to 5%")
            sys.exit()

        test.calculate_fitness()
        if test.best > achieved:
            achieved = test.best
            print("Best: " + str(test.best))
        test.generate()

    print("Solved after " + str(test.generations) + " generations")
    print("".join(test.complete))

    return
