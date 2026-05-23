import networkx as nx
import numpy as np
import random
import datetime
import math

class GeneticAlgorithm:
    def __init__(self, G, population_size, max_generation, crossover_rate=0.8, mutation_rate=0.1, seed=None):
        self.G = G
        self.population_size = population_size
        self.max_generation = max_generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.seed = seed
        self.num_nodes = len(G.nodes)

        if seed is not None:
            random.seed(seed)
        
        self.population = [self.generate_possible_solution() for i in range(self.population_size)]
        self.current_best_solution = self.population[0]
        self.best_cost = self.evaluate_distance(self.current_best_solution)

        self.test_data = []

    def generate_possible_solution(self):
        nodes = list(self.G.nodes)
        random.shuffle(nodes)
        return nodes
    
    def evaluate_distance(self, path):
        distance = 0.0
        n = len(path)
        for i in range(n):
            curr_node = path[i]
            next_node = path[(i+1) % n]
            distance += self.G[curr_node][next_node]['weight']
        return distance
    
    def selection_tournament(self, k=3):
        tournament = random.sample(self.population, k)
        return min(tournament, key=self.evaluate_distance)
    
    def crossover_order(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        size = self.num_nodes

        idx1, idx2 = sorted(random.sample(range(size), 2))

        child1 = [-1] * size
        child2 = [-1] * size

        child1[idx1:idx2] = parent1[idx1:idx2]
        child2[idx1:idx2] = parent2[idx1:idx2]

        def fill_child(child, parent):
            current_pos = idx2 % size
            for item in parent:
                if item not in child:
                    child[current_pos] = item
                    current_pos = (current_pos + 1) % size
            return child
        
        child1 = fill_child(child1, parent2)
        child2 = fill_child(child2, parent1)

        return child1, child2
    
    def mutate_inversion(self, individual):
        if random.random() < self.mutation_rate:
            idx1, idx2 = sorted(random.sample(range(self.num_nodes), 2))
            individual[idx1:idx2] = reversed(individual[idx1:idx2])
        return individual
    
    def run(self):
        for generation in range(self.max_generation):
            new_population = []

            current_best = min(self.population, key=self.evaluate_distance)
            new_population.append(current_best.copy())
            
            while len(new_population) < self.population_size:
                p1 = self.selection_tournament()
                p2 = self.selection_tournament()

                c1, c2 = self.crossover_order(p1, p2)

                c1 = self.mutate_inversion(c1)
                c2 = self.mutate_inversion(c2)

                new_population.append(c1)
                if len(new_population) < self.population_size:
                    new_population.append(c2)
            self.population = new_population

            for i in self.population:
                cost = self.evaluate_distance(i)
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_solution = i.copy()
            self.test_data.append([generation, self.best_cost])
        return self.best_solution, self.best_cost