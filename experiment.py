import networkx as nx
import random
import datetime
import numpy as np
import math
import matplotlib.pyplot as plt

from genetic_algorithm import GeneticAlgorithm
from artificial_bee_colony import ArtificialBeeColony

class experiment:
    def __init__(self, arquivo='teste/instancia.txt', n_testes=10, max_iter=100, num_bees=53, limit=20, population_size=53, crossover_rate=0.9, mutation_rate=0.15, seed=None):
        self.arquivo = arquivo
        self.n_testes = n_testes                    #Número de vezes que o algoritmo será executado.
        self.max_iter = max_iter                    #Número de épocas do algoritmo. O algoritmo busca minimizar o valor obtido durante o passar das épocas.
        self.num_bees = num_bees
        self.limit = limit
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.seed = seed                            #Semente para ser passadas para funções aleatórias. Serve para manter os testes reproduzíveis

    def execute_experiment(self, algorithm):
        #O arquivo instancia.txt vem em um formato de coordenadas, por isso é preciso um tratamento diferente
        #para transformá-lo em uma matriz com as distâncias.
        if self.arquivo == 'tests/instancia.txt':                    
            with open(self.arquivo, 'r') as file:
                n_cities = int(file.readline().strip())             #Pega o número de cidades
                
                #Pega todas as coordenadas no arquivo instancia
                coordenadas = {}
                for i, linha in enumerate(file):
                    x, y = map(float, linha.split())
                    coordenadas[i] = (x, y)
                Gn = nx.complete_graph(n_cities)                    #Inicializa um grafo em que todos os nós possuem uma aresta conectando com cada um dos outros nós
                nx.set_node_attributes(Gn, coordenadas, "pos")      #Associa as coordenadas x e y lidas como atributos de posição dos nós do grafo

                #Percorre todas as arestas possíveis do grafo para calcular a distância Euclidiana entre as cidades
                for u, v in Gn.edges():
                    pos_u = coordenadas[u]
                    pos_v = coordenadas[v]

                    distancia = math.dist(pos_u, pos_v)

                    Gn[u][v]['weight'] = distancia
        else:                                               #Caso a entrada não seja o 'instância.txt' o processo é bem mais simples
            matriz = np.loadtxt(self.arquivo)                    #Lê a matriz com as distâncias

            Gn = nx.from_numpy_array(matriz)                #Transforma a matriz com as distâncias para um grafo do networkx

        random.seed(self.seed)                   #Define a semente aleatória para a biblioteca padrão random do Python
        np.random.seed(self.seed)                #Define a semente aleatória para as operações globais da biblioteca numpy
        results = []                        #Lista para armazenar o resultado do algoritmo em cada teste executado. Usado para criar gráficos depois
        best_result_path = []               #Armazena o caminho que mais minimiza a distância percorrida pelo algoritmo
        best_result_fitness = float('inf')  #Armazena o custo de percorrer o melhor caminho encontrado
        history = np.zeros((self.n_testes, self.max_iter))        #Matriz para armazenar o histórico do custo de cada iteração para todas as rodadas executadas

        start = datetime.datetime.now()

        for i in range(self.n_testes):
            if algorithm == 1:
                algoritmo = ArtificialBeeColony(Gn, num_bees = self.num_bees, max_iterations=self.max_iter, limit=self.limit, seed=self.seed+i)       #Algoritmo de colônia artificial de abelhas
            else:
                algoritmo = GeneticAlgorithm(Gn, self.population_size, self.max_iter, self.crossover_rate, self.mutation_rate, seed=self.seed+i)                                     #Algoritmo Genético

            best_path, best_fitness = algoritmo.run()   #Executa a metaheurística escolhida retornando o melhor caminho encontrado junto com seu custo

            if best_fitness < best_result_fitness:
                best_result_fitness = best_fitness
                best_result_path = best_path

            i_cost = [passo[1] for passo in algoritmo.test_data]    #Extrai apenas os valores de custo obtidos em cada iteração da rodada atual
            history[i, :] = i_cost                                  #Armazena o vetor de evolução da rodada atual na linha correspondente da matriz histórica
            
            results.append(best_fitness)                            #Adiciona o melhor custo alcançado na rodada na lista de resultados

        end = datetime.datetime.now()

        algoritmo_time = end - start

        algorithm_name = 'Genetic Algorithm' if isinstance(algoritmo, GeneticAlgorithm) else 'Artificial Bee Colony'            #Separa tag dependendo do algoritmo escolhido para ser colocado no nome da imagem na saída
        tag = 'ga' if algorithm_name == 'Genetic Algorithm' else 'abc'

        performance_average = np.mean(results)                      #Calcula a média aritmética dos custos finais obtidos em todas as execuções do algoritmo

        iteration_average = np.mean(history, axis=0)                #Calcula a média de custos combinando todas as rodadas por iteração
        best_iteration = np.min(history, axis=0)                    #Filtra o menor custo obtido a cada iteração
        worst_iteration = np.max(history, axis=0)                   #Filtra o maior custo obtido a cada iteração 

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))       #Inicializa uma figura com duas telas de gráficos dispostas lado a lado

        arquivo = self.arquivo[6:]                                       #Remove os primeiros 6 caracteres ('tests/') para limpar o nome exibido no título

        fig.suptitle(f"Resultados {self.arquivo} {algorithm_name}")                 #Define o título geral unificado localizado no topo da imagem gerada

        #Configurações de plotagem do primeiro subplot (Gráfico de Linhas)
        ax1.plot(iteration_average, label='Custo Médio', color='blue', linewidth=2)
        ax1.plot(best_iteration, label='Melhor Rodada', color='green', linestyle='--')
        ax1.plot(worst_iteration, label='Pior Rodada', color='red', linestyle=':')
        ax1.fill_between(range(self.max_iter), best_iteration, worst_iteration, color='blue', alpha=0.1)     #Preenche a área de desvio entre o melhor e pior caso
        ax1.set_title('Curva de Convergência')                      #Define o título do primeiro gráfico
        ax1.set_xlabel('Iterações')                                 #Define o rótulo do eixo horizontal do primeiro gráfico
        ax1.set_ylabel('Custo do Caminho')                          #Define o rótulo do eixo vertical do primeiro gráfico
        ax1.grid(True, linestyle='--', alpha=0.6)                   #Ativa as linhas de grade tracejadas no fundo do gráfico de linhas
        ax1.legend()                                                #Insere a legenda contendo os rótulos de cada linha plotada

        #Configurações de plotagem do segundo subplot (Boxplot)
        ax2.boxplot(results, patch_artist=True, showfliers=False,
                    boxprops=dict(facecolor='lightblue', color='blue'),
                    medianprops=dict(color='red', linewidth=2))

        posicao_x = np.random.normal(1, 0.03, size=len(results))    #Muda a posição horizontal dos pontos para evitar sobreposição

        #Plota os pontos das rodadas individuais
        ax2.scatter(posicao_x, results, 
                    color='darkblue', 
                    alpha=0.7, 
                    s=60,                 
                    edgecolors='black',     
                    label='Tentativas Individuais: ' + str(self.n_testes),
                    zorder=3)                                       

        ax2.set_title('Dispersão dos Resultados Finais')            #Define o título do segundo gráfico
        ax2.set_ylabel('Custo Final')                               #Define o rótulo do eixo vertical do segundo gráfico
        ax2.set_xticks([1])                                         #Fixa uma única marcação no eixo horizontal do Boxplot

        ax2.grid(True, linestyle='--', alpha=0.3)                   #Ativa as linhas de grade no fundo do gráfico
        ax2.legend()                                                
        plt.tight_layout()                                          #Ajusta as margens automaticamente para evitar sobreposição de textos e eixos
        save_name = arquivo.replace('.txt', '')
        plt.savefig(f'results/analise_resultados_{save_name}_{tag}.png', dpi=300)     #Salva os gráficos em uma imagem
        plt.show()                                                  #Renderiza os gráficos na tela do usuário

        print("Performance average: ", performance_average, "in", self.n_testes, "epochs")
        print("Best optimal path: ", best_result_path)
        print("Best optimal path cost: ", best_result_fitness)
        print("Total Exec time => ", algoritmo_time.total_seconds())