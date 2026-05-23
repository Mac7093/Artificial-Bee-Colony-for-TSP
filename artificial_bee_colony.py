import random

class ArtificialBeeColony:
    def __init__(self, G, num_bees, max_iterations, limit=200, seed=None):
        """
        Inicializa a Colônia de Abelhas Artificial para resolver o PCV
        G: Grafo do NetworkX representando as cidades e as distâncias
        num_bees: Tamanho total da população de abelhas
        max_iterations: Quantidade de iterações/épocas que o algoritmo vai rodar
        limit: Limite de tentativas sem melhora antes de abandonar uma rota
        seed: Semente para garantir a reprodutibilidade dos resultados aleatórios
        """
        self.G = G
        self.num_bees = num_bees
        self.max_iterations = max_iterations
        self.limit = limit

        #Define a semente aleatória se ela for fornecida
        if seed is not None:
            random.seed(seed)

        self.current_population = [self.generate_possible_solution() for i in range(self.num_bees)]     #Gera a população inicial
        self.population_cost = [self.evaluate_distance(sol) for sol in self.current_population]         #Calcula o custo do caminho de cada abelha
        self.trials = [0] * self.num_bees       # Histórico de falhas: conta quantas vezes cada rota tentou mudar e não melhorou

        #Define a primeira rota da população como a melhor encontrada até o momento
        self.current_best_solution = self.current_population[0]
        self.current_best_cost = self.evaluate_distance(self.current_best_solution)

        #Divide as abelhas: metade operárias (employed) e metade observadoras (onlooker)
        self.num_employeed_bees = self.num_bees // 2
        self.num_onlooker_bees = self.num_bees - self.num_employeed_bees

        #Variáveis para armazenar o histórico de dados e estatísticas do experimento
        self.test_data = []
        self.test_cases = 0

    def evaluate_distance(self, path):
        """
        Função de custo: calcula a distância total percorrida em um circuito completo
        """
        distance = 0.0
        n = len(path)
        for i in range(n):
            curr_node = path[i]
            next_node = path[(i+1) % n]
            distance += self.G[curr_node][next_node]['weight']

        return distance
    
    def apply_random_neighborhood_structure(self, path):
        """
        Exploração local
        Seleciona dois pontos da rota aleatoriamente e inverte o trecho entre eles
        """
        new_path = path.copy()
        idx1, idx2 = sorted(random.sample(range(len(path)), 2))
        new_path[idx1:idx2] = reversed(new_path[idx1:idx2])
        return new_path
    
    def generate_possible_solution(self):
        """
        Gera uma rota inicial válida embaralhando a lista de nós (todas as cidades).
        """
        nodes = list(self.G.nodes)
        random.shuffle(nodes)
        return nodes
    
    def run(self):
        """
        Executa o ciclo completo do algoritmo pelas iterações definidas
        """
        for iteration in range(self.max_iterations):
            # Employed Bee phase
            # Cada operária avalia sua fonte de alimento atual e tenta melhorá-la
            for i in range(self.num_employeed_bees):
                current_solution = self.current_population[i]
                current_solution_cost = self.population_cost[i]

                # Propõe uma nova rota modificando a rota atual
                new_solution = self.apply_random_neighborhood_structure(current_solution)
                new_solution_cost = self.evaluate_distance(new_solution)

                # Se a nova rota for mais curta, substitui a antiga
                if new_solution_cost < current_solution_cost:
                    self.current_population[i] = new_solution
                    self.population_cost[i] = new_solution_cost
                    self.trials[i] = 0          # Reseta o contador de falhas da rota
                    self.test_cases += 1
                else:
                    self.trials[i] += 1         # Incrementa o contador de falhas

            #Onlooker Bee phase
            # Calcula o fitness (aptidão) de cada rota. Quanto menor a distância, maior o fitness.
            # O valor 1e-6 evita divisões por zero caso o custo seja nulo.
            fitness = [1.0 / (c + 1e-6) for c in self.population_cost]
            sum_fitness = sum(fitness)
            probability_list = [f / sum_fitness for f in fitness]       # Cria a roleta de probabilidades baseada na qualidade de cada fonte de alimento

            # Cada observadora escolhe uma rota para tentar refinar usando a roleta de probabilidades
            for _ in range(self.num_onlooker_bees):
                i = random.choices(range(self.num_bees), weights=probability_list, k=1)[0]      # Sorteia o índice de uma rota baseado nos pesos de probabilidade

                current_solution = self.current_population[i]
                current_cost = self.population_cost[i]

                # Tenta otimizar localmente a rota que ela escolheu observar
                new_solution = self.apply_random_neighborhood_structure(current_solution)
                new_cost = self.evaluate_distance(new_solution)

                # Se a modificação funcionou, salva a melhoria
                if new_cost < current_cost:
                    self.current_population[i] = new_solution
                    self.population_cost[i] = new_cost
                    self.trials[i] = 0
                    self.test_cases += 1
                else:
                    self.trials[i] += 1

            # Varre toda a população para verificar se alguma abelha achou a melhor rota histórica
            for i in range(self.num_bees):
                cost = self.population_cost[i]
                if cost < self.current_best_cost:
                    self.current_best_cost = cost
                    self.current_best_solution = self.current_population[i]

            # Scout Bee phase
            # Se uma rota estagnou e passou do limite de tentativas sem melhora, ela é descartada
            for i in range(self.num_bees):
                if self.trials[i] > self.limit:
                    # A abelha abandona a rota antiga e gera uma completamente nova do zero
                    self.current_population[i] = self.generate_possible_solution()
                    self.population_cost[i] = self.evaluate_distance(self.current_population[i])
                    self.trials[i] = 0
            
            self.test_data.append([iteration, self.current_best_cost, self.test_cases])     # Registra o histórico da iteração atual para plotagem
        return self.current_best_solution, self.current_best_cost       # Retorna a melhor rota global e o seu menor custo de distância