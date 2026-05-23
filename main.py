import experiment
import pandas as pd

while True:
    print("\n[ MENU PRINCIPAL ]")
    print("1 - Colônia Artificial de Abelhas (ABC)")
    print("2 - Algoritmo Genético (GA)")
    print("3 - Buscar experimentos")
    print("4 - Sair")

    try:
        op = int(input("Escolha uma opção: "))
        if op == 4:
            break
        if op not in [1, 2, 3]:
            continue
    except ValueError:
        print("Digite apenas números inteiros")
        continue

    while True:
        if op in [1, 2]:
            algorithm = "Artificial Bee Colony" if op == 1 else "Genetic Algorithm"
            print(f"\n--- Configurações para: {algorithm} ---")
            print("Digite os parâmetros ou digite 'v' para voltar ao menu anterior.")
            
            #Hiperparâmetros do Algoritmo de Colônia de Abelhas
            #Número de testes
            arquivos = ['tests/instancia.txt', 'tests/teste15.txt', 'tests/teste17.txt', 'tests/teste26.txt', 'tests/teste42.txt', 'tests/teste48.txt']
            print("\nArquivos de teste disponíveis:")
            for idx, arquivo_opcao in enumerate(arquivos, start=1):
                print(f"{idx} - {arquivo_opcao}")
            inp_arq = input("Escolha o número do arquivo (Padrão: 1 - tests/instancia.txt): ").strip()
            if inp_arq.lower() == 'v': break
            if not inp_arq:
                arq = 'tests/instancia.txt'
            else:
                try:
                    num_arq = int(inp_arq)
                    if 1 <= num_arq <= len(arquivos):
                        arq = arquivos[num_arq - 1]  # -1 porque listas em Python começam em 0
                    else:
                        print(f"[Aviso] Opção inválida. Usando o padrão: tests/instancia.txt")
                        arq = 'tests/instancia.txt'
                except ValueError:
                    print(f"[Aviso] Entrada inválida. Usando o padrão: tests/instancia.txt")
                    arq = 'tests/instancia.txt'

            try:
                # Número de testes
                inp = input("Número de testes independentes (Default: 10): ").strip()
                if inp.lower() == 'v': break
                n_testes = int(inp) if inp else 10

                #Max Iterações
                inp = input("Número máximo de iterações/épocas (Default: 100): ").strip()
                if inp.lower() == 'v': break
                max_iter = int(inp) if inp else 100

                # Semente (Seed)
                inp = input("Seed (Padrão: 42): ").strip()
                if inp.lower() == 'v': break
                seed_val = int(inp) if inp else 42 
                
            except ValueError:
                print("\n[ERRO] Tipo de dado incorreto inserido")
                continue

            if op == 1:
                # Hiperparâmetros da Colônia de Abelhas
                try:
                    inp = input("Número de abelhas / num_bees (Default: 53): ").strip()
                    if inp.lower() == 'v': break
                    num_bees = int(inp) if inp else 53

                    inp = input("Limite de tentativas / limit (Default: 20): ").strip()
                    if inp.lower() == 'v': break
                    limit = int(inp) if inp else 20
                    
                    # Instancia a classe passando as variáveis lidas
                    exp = experiment.experiment(arquivo=arq, n_testes=n_testes, max_iter=max_iter, 
                                        num_bees=num_bees, limit=limit, seed=seed_val)
                except ValueError:
                    print("\n[ERRO] Parâmetros numéricos da Colônia inválidos.")
                    continue

            elif op == 2:
                # Hiperparâmetros do Algoritmo Genético
                try:
                    inp = input("Tamanho da população / population_size (Default: 53): ").strip()
                    if inp.lower() == 'v': break
                    population_size = int(inp) if inp else 53

                    inp = input("Taxa de Crossover [0.0 a 1.0] (Default: 0.9): ").strip()
                    if inp.lower() == 'v': break
                    crossover = float(inp) if inp else 0.9

                    inp = input("Taxa de Mutação [0.0 a 1.0] (Default: 0.15): ").strip()
                    if inp.lower() == 'v': break
                    mutation = float(inp) if inp else 0.15
                    
                    # Instancia a classe passando as variáveis lidas
                    exp = experiment.experiment(arquivo=arq, n_testes=n_testes, max_iter=max_iter, 
                                        population_size=population_size, crossover_rate=crossover, 
                                        mutation_rate=mutation, seed=seed_val)
                except ValueError:
                    print("\n[ERRO] Parâmetros numéricos do AG inválidos.")
                    continue

            exp.execute_experiment(op)
            while True:
                op = input("Aperte 'v' para voltar: ").strip()
                if op.lower() == 'v': break

        elif op == 3:
            #Seleção do arquivo para filtragem
            arquivos = ['instancia.txt', 'teste15.txt', 'teste17.txt', 'teste26.txt', 'teste42.txt', 'teste48.txt']
            
            print("\nArquivos de teste disponíveis para histórico:")
            for idx, arquivo_opcao in enumerate(arquivos, start=1):
                print(f"{idx} - {arquivo_opcao}")
                
            inp_arq = input("Escolha o número do arquivo para filtrar os resultados: ").strip()
            
            if inp_arq.lower() == 'v': 
                continue  # Volta para o menu principal
                
            if not inp_arq:
                arq_selecionado = 'tests/instancia.txt'
            else:
                try:
                    num_arq = int(inp_arq)
                    if 1 <= num_arq <= len(arquivos):
                        arq_selecionado = arquivos[num_arq - 1]
                    else:
                        print("Opção inválida. Usando o padrão: tests/instancia.txt")
                        arq_selecionado = 'tests/instancia.txt'
                except ValueError:
                    print("Entrada inválida. Usando o padrão: tests/instancia.txt")
                    arq_selecionado = 'tests/instancia.txt'

            # Leitura e Filtragem do arquivo CSV
            csv_abc = 'results/historico_experimentos_abc.csv' 
            csv_ga = 'results/historico_experimentos_ga.csv'

            dfs = []

            try:
                df_abc = pd.read_csv(csv_abc)
                dfs.append(df_abc)
            except FileNotFoundError:
                pass

            try:
                df_ga = pd.read_csv(csv_ga)
                dfs.append(df_ga)
            except FileNotFoundError:
                pass

            try:
                # Junta os DataFrames encontrados (faz o merge/empilhamento das tabelas)
                df_total = pd.concat(dfs, ignore_index=True, sort=False)
                
                # Filtra apenas as linhas referentes ao arquivo que o usuário escolheu
                df_filtrado = df_total[df_total['Caso_Teste'] == arq_selecionado].copy()

                df_ordenado = df_filtrado.sort_values(by='Custo_Medio', ascending=True)

                colunas_gerais = ['Caso_Teste', 'Algoritmo', 'Custo_Medio', 'Melhor_Custo_Encontrado', 'Tempo_Exec_Segundos']
                outras_colunas = [col for col in df_ordenado.columns if col not in colunas_gerais]
                df_ordenado = df_ordenado[colunas_gerais + outras_colunas]

                print(f"\n=======================================================================================================================")
                print(f"RANKING GLOBAL DE RESULTADOS COMPARTILHADOS - {arq_selecionado}")
                print(f"=======================================================================================================================")
                
                # Mostra a tabela formatada substituindo os valores vazios (NaN) por '-' para ficar mais limpo
                print(df_ordenado.fillna('-').to_string(index=False))
                print(f"=======================================================================================================================\n")
                
            except KeyError as e:
                print(f"\n[Erro de Coluna] Não encontrei a coluna {e} nos arquivos CSV.")
            
            input("\nPressione Enter para voltar ao menu")
            break
        break
