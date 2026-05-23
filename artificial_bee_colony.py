import networkx as nx
import pandas as pd
import random
import datetime
import numpy as np
import math
import matplotlib.pyplot as plt

class ArtificialBeeColony:
    def __init__(self, G, num_bees, max_iterations, limit=200, seed=None):
        self.G = G
        self.num_bees = num_bees
        self.max_iterations = max_iterations
        self.limit = limit

        if seed is not None:
            random.seed(seed)

        self.current_population = [self.generate_possible_solution() for i in range(self.num_bees)]
        self.population_cost = [self.evaluate_distance(sol) for sol in self.current_population]
        self.trials = [0] * self.num_bees

        self.current_best_solution = self.current_population[0]
        self.current_best_cost = self.evaluate_distance(self.current_best_solution)

        self.num_employeed_bees = self.num_bees // 2
        self.num_onlooker_bees = self.num_bees - self.num_employeed_bees
        self.test_data = []
        self.test_cases = 0

    def evaluate_distance(self, path):
        distance = 0.0

        n = len(path)
        for i in range(n):
            curr_node = path[i]
            next_node = path[(i+1) % n]
            distance += self.G[curr_node][next_node]['weight']

        return distance
    
    def apply_random_neighborhood_structure(self, path):
        new_path = path.copy()
        idx1, idx2 = sorted(random.sample(range(len(path)), 2))
        new_path[idx1:idx2] = reversed(new_path[idx1:idx2])
        return new_path
    
    def generate_possible_solution(self):
        nodes = list(self.G.nodes)
        random.shuffle(nodes)
        return nodes
    
    def run(self):
        for iteration in range(self.max_iterations):
            # Employed Bee phase
            for i in range(self.num_employeed_bees):
                current_solution = self.current_population[i]
                current_solution_cost = self.population_cost[i]
                new_solution = self.apply_random_neighborhood_structure(current_solution)
                new_solution_cost = self.evaluate_distance(new_solution)

                if new_solution_cost < current_solution_cost:
                    self.current_population[i] = new_solution
                    self.population_cost[i] = new_solution_cost
                    self.trials[i] = 0
                    self.test_cases += 1
                else:
                    self.trials[i] += 1

            #Onlooker Bee phase
            fitness = [1.0 / (c + 1e-6) for c in self.population_cost]
            sum_fitness = sum(fitness)
            probability_list = [f / sum_fitness for f in fitness]

            for _ in range(self.num_onlooker_bees):
                i = random.choices(range(self.num_bees), weights=probability_list, k=1)[0]

                current_solution = self.current_population[i]
                current_cost = self.population_cost[i]

                new_solution = self.apply_random_neighborhood_structure(current_solution)
                new_cost = self.evaluate_distance(new_solution)

                if new_cost < current_cost:
                    self.current_population[i] = new_solution
                    self.population_cost[i] = new_cost
                    self.trials[i] = 0
                    self.test_cases += 1
                else:
                    self.trials[i] += 1

            for i in range(self.num_bees):
                cost = self.population_cost[i]
                if cost < self.current_best_cost:
                    self.current_best_cost = cost
                    self.current_best_solution = self.current_population[i]

            # Scout Bee phase
            for i in range(self.num_bees):
                if self.trials[i] > self.limit:
                    self.current_population[i] = self.generate_possible_solution()
                    self.population_cost[i] = self.evaluate_distance(self.current_population[i])
                    self.trials[i] = 0
            
            self.test_data.append([iteration, self.current_best_cost, self.test_cases])
        return self.current_best_solution, self.current_best_cost
        