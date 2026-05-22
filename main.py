import networkx as nx
import pandas as pd
import numpy as np
import random
import datetime
import math

from genetic_algorithm import GeneticAlgorithm
from artificial_bee_colony import ArtificialBeeColony

arquivo = 'teste48.txt'

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
results = []
best_result_path = []
best_result_fitness = float('inf')

start = datetime.datetime.now()

for i in range(n_testes):
    #algoritmo = ArtificialBeeColony(Gn, num_bees = 103, max_iterations=1000, limit=200, seed=seed+i)
    algoritmo = GeneticAlgorithm(Gn, 103, 1000, 0.9, 0.15, seed=seed+i)
    
    best_path, best_fitness = algoritmo.run()

    if best_fitness < best_result_fitness:
        best_result_fitness = best_fitness
        best_result_path = best_path
    
    results.append(best_fitness)

end = datetime.datetime.now()

algoritmo_time = end - start

performance_average = np.mean(results)

print("Performance average: ", performance_average, "in", n_testes, "epochs")
print("Best optimal path: ", best_result_path)
print("Best optimal path cost: ", best_result_fitness)
print("Total exec time => ", algoritmo_time.total_seconds())