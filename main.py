import experiment
import time

while True:
    print("\n[ MENU PRINCIPAL ]")
    print("1 - Colônia Artificial de Abelhas (ABC)")
    print("2 - Algoritmo Genético (GA)")
    print("3 - Sair do Programa")

    try:
        op = int(input("Escolha uma opção: "))
        if op == 3:
            break
        if op not in [1, 2]:
            print("Opção Inválida")
            continue
    except ValueError:
        print("Digite apenas números inteiros")
        continue

    while True:
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
                inp = input("Número de abelhas / num_bees (Padrão: 53): ").strip()
                if inp.lower() == 'v': break
                num_bees = int(inp) if inp else 53

                inp = input("Limite de tentativas / limit (Padrão: 20): ").strip()
                if inp.lower() == 'v': break
                limit = int(inp) if inp else 20
                
                # Instancia a classe passando as variáveis lidas
                exp = experiment.experiment(arquivo=arq, n_testes=n_testes, max_iter=max_iter, 
                                    num_bees=num_bees, limit=limit, seed=seed_val)
            except ValueError:
                print("\n[ERRO] Parâmetros numéricos da Colônia inválidos. Reiniciando...")
                continue

        else:
            # Hiperparâmetros do Algoritmo Genético
            try:
                inp = input("Tamanho da população / population_size (Padrão: 53): ").strip()
                if inp.lower() == 'v': break
                population_size = int(inp) if inp else 53

                inp = input("Taxa de Crossover [0.0 a 1.0] (Padrão: 0.9): ").strip()
                if inp.lower() == 'v': break
                crossover = float(inp) if inp else 0.9

                inp = input("Taxa de Mutação [0.0 a 1.0] (Padrão: 0.15): ").strip()
                if inp.lower() == 'v': break
                mutation = float(inp) if inp else 0.15
                
                # Instancia a classe passando as variáveis lidas
                exp = experiment.experiment(arquivo=arq, n_testes=n_testes, max_iter=max_iter, 
                                    population_size=population_size, crossover_rate=crossover, 
                                    mutation_rate=mutation, seed=seed_val)
            except ValueError:
                print("\n[ERRO] Parâmetros numéricos do AG inválidos. Reiniciando...")
                continue

        exp.execute_experiment(algorithm)
        time.sleep(3)
        break