import random

class GeneticAlgorithm:
    def __init__(self, G, population_size, max_generation, crossover_rate=0.8, mutation_rate=0.1, seed=None):
        """
        Inicializa o Algoritmo Genético para resolver o PCV.
        G: Grafo do NetworkX com as cidades e as distâncias.
        population_size: Quantidade de rotas (indivíduos) por geração.
        max_generation: Número máximo de gerações (iterações de evolução).
        crossover_rate: Chance de ocorrer o cruzamento entre dois pais (0.0 a 1.0).
        mutation_rate: Chance de ocorrer mutação em um filho (0.0 a 1.0).
        seed: Semente para fins de reprodutibilidade dos testes aleatórios.
        """
        self.G = G
        self.population_size = population_size
        self.max_generation = max_generation
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.seed = seed
        self.num_nodes = len(G.nodes)

        # Configura a semente aleatória, caso informada
        if seed is not None:
            random.seed(seed)
        
        # Cria a primeira geração de indivíduos com rotas completamente aleatórias
        self.population = [self.generate_possible_solution() for i in range(self.population_size)]
        
        # Define o primeiro indivíduo gerado como a melhor solução inicial
        self.current_best_solution = self.population[0]
        self.best_cost = self.evaluate_distance(self.current_best_solution)

        # Armazena o histórico do custo da melhor rota ao longo das gerações
        self.test_data = []

    def generate_possible_solution(self):
        """
        Gera um indivíduo aleatório (um caminho válido embaralhando a lista de cidades).
        """
        nodes = list(self.G.nodes)
        random.shuffle(nodes)
        return nodes
    
    def evaluate_distance(self, path):
        """
        Função de custo: calcula o peso (distância) total do circuito fechado.
        """
        distance = 0.0
        n = len(path)
        for i in range(n):
            curr_node = path[i]
            next_node = path[(i+1) % n]  # Retorna à cidade inicial no fim do circuito
            distance += self.G[curr_node][next_node]['weight']
        return distance
    
    def selection_tournament(self, k=3):
        """
        Seleção por Torneio: Sorteia 'k' indivíduos aleatórios da população e 
        retorna aquele que tiver o menor custo de rota (o mais apto do subgrupo).
        """
        tournament = random.sample(self.population, k)
        return min(tournament, key=self.evaluate_distance)
    
    def crossover_order(self, parent1, parent2):
        """
        Crossover: Combina dois pais para gerar dois filhos.
        Preserva a ordem relativa das cidades sem gerar duplicatas.
        """
        # Se o sorteio for maior que a taxa estabelecida, não há cruzamento
        if random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
            
        size = self.num_nodes

        # Sorteia dois pontos de corte aleatórios mantendo a ordem correta
        idx1, idx2 = sorted(random.sample(range(size), 2))

        # Inicializa as rotas filhas com espaços vazios (-1)
        child1 = [-1] * size
        child2 = [-1] * size

        # Copia o segmento central dos pais originais
        child1[idx1:idx2] = parent1[idx1:idx2]
        child2[idx1:idx2] = parent2[idx1:idx2]

        def fill_child(child, parent):
            """Preenche os espaços restantes (-1) usando a ordem das cidades do outro pai"""
            current_pos = idx2 % size
            for item in parent:
                # Se a cidade ainda não foi inserida na rota do filho
                if item not in child:
                    child[current_pos] = item
                    current_pos = (current_pos + 1) % size
            return child
        
        # Preenche os vazios do Filho 1 usando o Pai 2, e do Filho 2 usando o Pai 1
        child1 = fill_child(child1, parent2)
        child2 = fill_child(child2, parent1)

        return child1, child2
    
    def mutate_inversion(self, individual):
        """
        Mutação por Inversão: Se o sorteio cair dentro da taxa de mutação,
        escolhe dois pontos da rota aleatoriamente e inverte a ordem das cidades ali dentro.
        """
        if random.random() < self.mutation_rate:
            idx1, idx2 = sorted(random.sample(range(self.num_nodes), 2))
            individual[idx1:idx2] = reversed(individual[idx1:idx2])
        return individual
    
    def run(self):
        """
        Laço evolucionário principal que comanda a transição entre gerações.
        """
        for generation in range(self.max_generation):
            new_population = []

            # Identifica a melhor rota da geração atual e a envia para a próxima geração sem alterações. Isso impede a perda de boas soluções.
            current_best = min(self.population, key=self.evaluate_distance)
            new_population.append(current_best.copy())
            
            # Continua gerando filhos até preencher o tamanho completo de indivíduos
            while len(new_population) < self.population_size:
                # Seleciona os pais usando o mecanismo de torneio
                p1 = self.selection_tournament()
                p2 = self.selection_tournament()

                # Cruza os pais gerando novos caminhos filhos
                c1, c2 = self.crossover_order(p1, p2)

                # Aplica o operador de mutação aleatória nos filhos gerados
                c1 = self.mutate_inversion(c1)
                c2 = self.mutate_inversion(c2)

                # Insere os novos indivíduos na próxima geração
                new_population.append(c1)
                if len(new_population) < self.population_size:
                    new_population.append(c2)
            

            self.population = new_population

            # Atualiza o melhor indivíduo histórico
            for i in self.population:
                cost = self.evaluate_distance(i)
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_solution = i.copy()
                    
            # Guarda o registro histórico do custo dessa geração para gerar os gráficos
            self.test_data.append([generation, self.best_cost])
            
        # Retorna a melhor rota encontrada pelo algoritmo e seu respectivo custo
        return self.best_solution, self.best_cost