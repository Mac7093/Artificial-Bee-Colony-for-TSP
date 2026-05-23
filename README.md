# Artificial-Bee-Colony-for-TSP
Comparação do desempenho do algoritmo Artificial Bee Colony com o Algoritmo Genético no problema do Caixeiro Viajante
# Algoritmo de Colônia de Abelhas Artificial (ABC) para o PCV

O módulo "artificial_bee_colony.py' implementa a meta-heurística baseada na Inteligência de Enxame chamada Artificial Bee Colony (ABC), aplicada para resolver o Problema do Caixeiro Viajante (TSP). O objetivo principal do algoritmo é encontrar a rota mais curta possível que visite todas as cidades (nós do grafo) exatamente uma vez e retorne à cidade de origem.
O algoritmo simula o comportamento de busca por alimento de uma colônia de abelhas real. O código divide a população total de abelhas (num_bees) em três funções diferentes:

### 1. Abelhas Operárias (Employed Bees)
*   Cada abelha operária cuida de uma fonte de alimento específica (uma rota atual). Elas tentam melhorar essa rota fazendo pequenas alterações nela (exploração local).
*   **No código:** Controlado pelo método `apply_random_neighborhood_structure()`, que inverte um trecho aleatório do caminho. Se a nova rota modificada for melhor (tiver custo menor), a abelha descarta a rota atual e memoriza a nova rota.

### 2. Abelhas Observadoras (Onlooker Bees)
*   Onlooker bees ficam na colmeia esperando as operárias voltarem para compartilhar informações sobre a qualidade das rotas. Fontes de alimento mais ricas (rotas com menor distância acumulada) atraem mais atenção.
*   **No código:** O algoritmo calcula o `fitness` (que é o inverso do custo da distância). Usando `random.choices` com pesos baseados em probabilidade, as observadoras escolhem em quais rotas vale a pena investir tempo para tentar fazer refinamentos locais.

### 3. Abelhas Escoteiras (Scout Bees)
*   Se uma fonte de alimento é explorada repetidas vezes e não melhora mais a abelha operária daquela rota vira uma escoteira, abandona o caminho antigo e escolhe um caminho completamente aleatório para descobrir uma nova rota do zero.
*   **No código:** Cada abelha da população possui um contador de falhas na lista `self.trials`. Se esse contador passar do valor estipulado em `self.limit`, a rota é descartada e resetada com `generate_possible_solution()`. Isso busca evitar que o código fique preso em ótimos locais.

---

## Estrutura das Funções em 'artificia_bee_colony.py'

*   `__init__`: Inicializa os parâmetros da colônia, gera a população inicial de rotas aleatórias e define os limites de escoteiras.
*   `evaluate_distance(path)`: **Função de custo**. Calcula o custo de percorrer o caminho passado em `path`.
*   `apply_random_neighborhood_structure(path)`: Aplica a alteração na rota. Ela escolhe dois pontos aleatórios do caminho e inverte o pedaço do meio.
*   `generate_possible_solution()`: Retorna um caminho aleatório contendo todas as cidades do grafo.
*   `run()`: O laço principal que executa as fases das operárias, observadoras e escoteiras sequencialmente até atingir `max_iterations`. Ela coleta dados de convergência a cada época em `self.test_data`.

---

## Hiperparâmetros

| Parâmetro | O que afeta no algoritmo |
| :--- | :--- |
| `num_bees` | O tamanho total da colônia. Mais abelhas significam mais rotas sendo olhadas simultaneamente (maior diversidade), mas deixam o código mais lento por iteração. |
| `max_iterations` | O tempo total de convergência. É o número de épocas que o algoritmo terá para otimizar os caminhos. |
| `limit` | A paciência do algoritmo. Um limite muito baixo faz as abelhas abandonarem caminhos promissores cedo demais. Um limite muito alto faz o algoritmo perder tempo insistindo em caminhos ruins. |

# Algoritmo Genético (GA) para o PCV

O módulo `genetic_algorithm.py` implementa a meta-heurística chamada **Algoritmo Genético (GA)**, para resolver o Problema do Caixeiro Viajante (TSP).

O algoritmo simula a seleção natural, onde as melhores soluções têm maior chance de sobreviver, gerar descendentes e transmitir suas características para as próximas gerações.

### 1. Seleção (Selection)
*   Para gerar uma nova geração de rotas, o algoritmo precisa escolher quais rotas da população atual serão os "pais". Rotas mais curtas possuem maior aptidão (*fitness*) e, portanto, têm maior probabilidade de serem selecionadas para a reprodução.
*   **No código:** O método de seleção (torneio) escolhe os indivíduos da população baseando-se no valor de *fitness*. Isso garante que as rotas mais promissoras sejam preservadas e passadas adiante.

### 2. Cruzamento (Crossover)
*   Duas rotas escolhidas como pais combinam suas estruturas para gerar filhos (novas rotas).
*   **No código:** Controlado pela taxa `crossover_rate`. O operador de cruzamento pega um pedaço do caminho do Pai 1 e preenche o restante com as cidades do Pai 2 na ordem em que aparecem, gerando uma rota filha que herda as boas sequências de caminhos de ambos os pais.

### 3. Mutação (Mutation)
*   Para evitar que a população se torne idêntica muito rápido (convergência prematura) e fique presa em um resultado, ocorrem pequenas alterações genéticas aleatórias nos filhos.
*   **No código:** Controlado pela taxa `mutation_rate`. O algoritmo escolhe duas cidades aleatórias dentro de uma rota e altera sua ordem (inversão de trecho). Isso introduz novos caminhos no mapa que não existiam nos pais, forçando a exploração de novas possibilidades.

---

## Estrutura das Funções em `genetic_algorithm.py`

*   `__init__`: Inicializa os parâmetros do algoritmo, gera a população inicial de indivíduos (rotas aleatórias) e configura o tamanho da população e as taxas evolutivas.
*   `evaluate_distance(path)` / `calculate_fitness(path)`: **Função de Aptidão**. Mede o comprimento total da rota. Quanto menor a distância, maior é o *fitness* (aptidão) desse indivíduo na população.
*   `crossover(parent1, parent2)`: Realiza a combinação genética entre duas rotas para gerar descendentes, respeitando a regra de não duplicar cidades.
*   `mutate(path)`: Aplica uma alteração aleatória na rota do indivíduo baseado na probabilidade de mutação.
*   `run()`: O laço principal que comanda a evolução por várias gerações até atingir `max_generation`. A cada geração, os indivíduos são selecionados, cruzados, mutados e a população antiga é substituída pela nova, salvando o histórico em `self.test_data`.

---

## Hiperparâmetros

| Parâmetro | O que afeta no algoritmo |
| :--- | :--- |
| `population_size` | O tamanho da população (número de rotas por geração). Uma população maior explora mais caminhos ao mesmo tempo, reduzindo a chance de erro, mas torna o processamento de cada geração mais lento. |
| `max_generation` | O tempo total de evolução. É o número de gerações que o algoritmo terá para cruzar e refinar as rotas em busca do melhor circuito. |
| `crossover_rate` | A intensidade de recombinação (geralmente entre 0.7 e 0.95). Define a chance de dois pais gerarem filhos misturados. Se for muito baixa, o algoritmo vira uma busca quase estagnada que apenas repete os pais. |
| `mutation_rate` | A taxa de inovação (geralmente entre 0.01 e 0.2). Controla a frequência com que novas rotas aleatórias surgem. Se for muito alta, o algoritmo vira uma busca puramente aleatória; se for muito baixa, a população se torna homogênea e para de evoluir. |
