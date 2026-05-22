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
        
if __name__ == "__main__":
    arquivo = 'teste15.txt'

    if arquivo == 'instancia.txt':
        with open(arquivo, 'r') as file:
            n_cities = int(file.readline().strip())
            
            coordenadas = {}
            for i, linha in enumerate(file):
                x, y = map(float, linha.split())
                coordenadas[i] = (x, y)
            Gn = nx.complete_graph(n_cities)
            nx.set_node_attributes(Gn, coordenadas, "pos")

            for u, v in Gn.edges():
                pos_u = coordenadas[u]
                pos_v = coordenadas[v]

                distancia = math.dist(pos_u, pos_v)

                Gn[u][v]['weight'] = distancia
    else:
        matriz = np.loadtxt(arquivo)

        Gn = nx.from_numpy_array(matriz)
    
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    
    n_testes = 10
    max_iter = 500
    results = []
    best_result_path = []
    best_result_fitness = float('inf')

    history = np.zeros((n_testes, max_iter))

    start = datetime.datetime.now()

    for i in range(n_testes):
        abc = ArtificialBeeColony(Gn, num_bees = 53, max_iterations=max_iter, seed=seed+i)

        best_path, best_fitness = abc.run()

        if best_fitness < best_result_fitness:
            best_result_fitness = best_fitness
            best_result_path = best_path

        i_cost = [passo[1] for passo in abc.test_data]
        history[i, :] = i_cost
        
        results.append(best_fitness)

    end = datetime.datetime.now()

    abc_time = end - start

    performance_average = np.mean(results)

    iteration_average = np.mean(history, axis=0)
    best_iteration = np.min(history, axis=0)
    worst_iteration = np.max(history, axis=0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(iteration_average, label='Custo Médio', color='blue', linewidth=2)
    ax1.plot(best_iteration, label='Melhor Rodada', color='green', linestyle='--')
    ax1.plot(worst_iteration, label='Pior Rodada', color='red', linestyle=':')

    ax1.fill_between(range(max_iter), best_iteration, worst_iteration, color='blue', alpha=0.1)

    ax1.set_title('Curva de Convergência')
    ax1.set_xlabel('Iterações')
    ax1.set_ylabel('Custo do Caminho')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()

    ax2.boxplot(results, patch_artist=True, showfliers=False,
                boxprops=dict(facecolor='lightblue', color='blue'),
                medianprops=dict(color='red', linewidth=2))

    posicao_x = np.random.normal(1, 0.03, size=len(results))

    ax2.scatter(posicao_x, results, 
                color='darkblue', 
                alpha=0.7, 
                s=60,                 
                edgecolors='black',     
                label='Tentativas Individuais ' + str(n_testes),
                zorder=3)

    ax2.set_title('Dispersão dos Resultados Finais')
    ax2.set_ylabel('Custo Final')
    ax2.set_xticks([1])

    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.legend()
    plt.tight_layout()
    plt.savefig(f'analise_resultados_{arquivo}.png', dpi=300)
    plt.show()

    print("Performance average: ", performance_average, "in", n_testes, "epochs")
    print("Best optimal path: ", best_result_path)
    print("Best optimal path cost: ", best_result_fitness)
    print("ABC total Exec time => ", abc_time.total_seconds())