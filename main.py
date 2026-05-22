import networkx as nx
import pandas as pd
import random
import datetime
import numpy as np
import math
import matplotlib.pyplot as plt

from genetic_algorithm import GeneticAlgorithm
from artificial_bee_colony import ArtificialBeeColony

arquivo = 'tests/teste15.txt'

if arquivo == 'teste/instancia.txt':
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
max_iter = 100
results = []
best_result_path = []
best_result_fitness = float('inf')

history = np.zeros((n_testes, max_iter))

start = datetime.datetime.now()

for i in range(n_testes):
    algoritmo = ArtificialBeeColony(Gn, num_bees = 53, max_iterations=max_iter, limit=200, seed=seed+i)
    #algoritmo = GeneticAlgorithm(Gn, 53, max_iter, 0.9, 0.15, seed=seed+i)

    best_path, best_fitness = algoritmo.run()

    if best_fitness < best_result_fitness:
        best_result_fitness = best_fitness
        best_result_path = best_path

    i_cost = [passo[1] for passo in algoritmo.test_data]
    history[i, :] = i_cost
    
    results.append(best_fitness)

end = datetime.datetime.now()

algoritmo_time = end - start

tag = 'ga' if isinstance(algoritmo, GeneticAlgorithm) else 'abs'

performance_average = np.mean(results)

iteration_average = np.mean(history, axis=0)
best_iteration = np.min(history, axis=0)
worst_iteration = np.max(history, axis=0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

arquivo = arquivo[6:]

fig.suptitle(f"Resultados {arquivo} {tag}")

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
plt.savefig(f'results/analise_resultados_{arquivo}_{tag}.png', dpi=300)
plt.show()

print("Performance average: ", performance_average, "in", n_testes, "epochs")
print("Best optimal path: ", best_result_path)
print("Best optimal path cost: ", best_result_fitness)
print("Total Exec time => ", algoritmo_time.total_seconds())