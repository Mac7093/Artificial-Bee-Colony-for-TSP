import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
from PIL import Image, ImageTk  # IMPORTANTE: Requer 'pip install Pillow'
import experiment

class ExperimentInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Experimentos ABC X GA")
        self.root.geometry("850x600")
        
        # Lista padrão de instâncias/arquivos
        self.arquivos_disponiveis = ['instancia.txt', 'teste15.txt', 'teste17.txt', 'teste26.txt', 'teste42.txt', 'teste48.txt']
        
        # Criar o controlador de Abas (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Inicializar as 3 abas principais
        self.tab_abc = ttk.Frame(self.notebook)
        self.tab_ga = ttk.Frame(self.notebook)
        self.tab_ranking = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_abc, text="Artificial Bee Colony (ABC)")
        self.notebook.add(self.tab_ga, text="Genetic Algorithm (GA)")
        self.notebook.add(self.tab_ranking, text="Ranking & Histórico")
        
        # Construir a interface de cada aba
        self.setup_abc_ui()
        self.setup_ga_ui()
        self.setup_ranking_ui()

    def criar_campos_comuns(self, container):
        """Cria os campos de texto compartilhados por ambos os algoritmos"""
        campos = {}
        
        ttk.Label(container, text="Arquivo de Instância:").grid(row=0, column=0, sticky='w', pady=5)
        campos['arquivo'] = ttk.Combobox(container, values=self.arquivos_disponiveis, state="readonly")
        campos['arquivo'].current(0)
        campos['arquivo'].grid(row=0, column=1, sticky='ew', pady=5)
        
        ttk.Label(container, text="Número de Testes (Default: 10):").grid(row=1, column=0, sticky='w', pady=5)
        campos['n_testes'] = ttk.Entry(container)
        campos['n_testes'].insert(0, "10")
        campos['n_testes'].grid(row=1, column=1, sticky='ew', pady=5)
        
        ttk.Label(container, text="Iterações Máximas (Default: 100):").grid(row=2, column=0, sticky='w', pady=5)
        campos['max_iter'] = ttk.Entry(container)
        campos['max_iter'].insert(0, "100")
        campos['max_iter'].grid(row=2, column=1, sticky='ew', pady=5)
        
        ttk.Label(container, text="Seed/Semente (Default: 42):").grid(row=3, column=0, sticky='w', pady=5)
        campos['seed'] = ttk.Entry(container)
        campos['seed'].insert(0, "42")
        campos['seed'].grid(row=3, column=1, sticky='ew', pady=5)
        
        return campos

    def setup_abc_ui(self):
        """Layout da aba do algoritmo ABC"""
        frame = ttk.LabelFrame(self.tab_abc, text=" Documento de Configuração - ABC ", padding=15)
        frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Renderiza os parâmetros gerais
        self.abc_inputs = self.criar_campos_comuns(frame)
        
        # Separador visual interno
        ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)
        
        # Parâmetros exclusivos do ABC
        ttk.Label(frame, text="Número de Abelhas / num_bees (Default: 53):").grid(row=5, column=0, sticky='w', pady=5)
        self.abc_inputs['num_bees'] = ttk.Entry(frame)
        self.abc_inputs['num_bees'].insert(0, "53")
        self.abc_inputs['num_bees'].grid(row=5, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame, text="Limite de Tentativas / limit (Default: 20):").grid(row=6, column=0, sticky='w', pady=5)
        self.abc_inputs['limit'] = ttk.Entry(frame)
        self.abc_inputs['limit'].insert(0, "20")
        self.abc_inputs['limit'].grid(row=6, column=1, sticky='ew', pady=5)
        
        # Botão Executar
        btn_rodar = ttk.Button(frame, text="Executar Experimento ABC", command=self.rodar_abc)
        btn_rodar.grid(row=7, column=0, columnspan=2, pady=20, ipady=5)
        
        frame.columnconfigure(1, weight=1)

    def setup_ga_ui(self):
        """Layout da aba do algoritmo GA"""
        frame = ttk.LabelFrame(self.tab_ga, text=" Documento de Configuração - GA ", padding=15)
        frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Renderiza os parâmetros gerais
        self.ga_inputs = self.criar_campos_comuns(frame)
        
        ttk.Separator(frame, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)
        
        # Parâmetros exclusivos do GA
        ttk.Label(frame, text="Tamanho da População (Default: 53):").grid(row=5, column=0, sticky='w', pady=5)
        self.ga_inputs['population_size'] = ttk.Entry(frame)
        self.ga_inputs['population_size'].insert(0, "53")
        self.ga_inputs['population_size'].grid(row=5, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame, text="Taxa de Crossover [0.0 a 1.0] (Default: 0.9):").grid(row=6, column=0, sticky='w', pady=5)
        self.ga_inputs['crossover_rate'] = ttk.Entry(frame)
        self.ga_inputs['crossover_rate'].insert(0, "0.9")
        self.ga_inputs['crossover_rate'].grid(row=6, column=1, sticky='ew', pady=5)
        
        ttk.Label(frame, text="Taxa de Mutação [0.0 a 1.0] (Default: 0.15):").grid(row=7, column=0, sticky='w', pady=5)
        self.ga_inputs['mutation_rate'] = ttk.Entry(frame)
        self.ga_inputs['mutation_rate'].insert(0, "0.15")
        self.ga_inputs['mutation_rate'].grid(row=7, column=1, sticky='ew', pady=5)
        
        # Botão Executar
        btn_rodar = ttk.Button(frame, text="Executar Experimento GA", command=self.rodar_ga)
        btn_rodar.grid(row=8, column=0, columnspan=2, pady=20, ipady=5)
        
        frame.columnconfigure(1, weight=1)

    def setup_ranking_ui(self):
        """Layout da aba de Ranking e histórico usando uma Treeview real"""
        frame_top = ttk.Frame(self.tab_ranking, padding=10)
        frame_top.pack(fill='x')
        
        ttk.Label(frame_top, text="Filtrar por Instância:").pack(side='left', padx=5)
        self.combo_filtro = ttk.Combobox(frame_top, values=self.arquivos_disponiveis, state="readonly")
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side='left', padx=5)
        
        btn_atualizar = ttk.Button(frame_top, text="Buscar & Atualizar Ranking", command=self.carregar_ranking)
        btn_atualizar.pack(side='left', padx=10)
        
        # Mensagem informativa para o usuário saber que dá para clicar
        ttk.Label(self.tab_ranking, text="* Dica: Dê um duplo clique em uma linha para visualizar o gráfico do resultado.", 
                  font=("Arial", 9, "italic"), foreground="gray").pack(anchor='w', padx=15)

        # Frame da Tabela com Scrollbar
        frame_tabela = ttk.Frame(self.tab_ranking, padding=10)
        frame_tabela.pack(fill='both', expand=True)
        
        self.tree = ttk.Treeview(frame_tabela, show='headings')
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side='right', fill='y')
        scrollbar_x.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)

        # Vincula o evento de duplo clique na tabela à função de exibição de imagens
        self.tree.bind("<Double-1>", self.exibir_grafico_selecionado)

    def coletar_dados_base(self, inputs):
        """Valida e extrai os parâmetros comuns do formulário"""
        arquivo_puro = inputs['arquivo'].get()
        caminho_instancia = f"tests/{arquivo_puro}"
        
        return {
            'arquivo': caminho_instancia,
            'n_testes': int(inputs['n_testes'].get() or 10),
            'max_iter': int(inputs['max_iter'].get() or 100),
            'seed': int(inputs['seed'].get() or 42)
        }

    def rodar_abc(self):
        try:
            base = self.coletar_dados_base(self.abc_inputs)
            num_bees = int(self.abc_inputs['num_bees'].get() or 53)
            limit = int(self.abc_inputs['limit'].get() or 20)
            
            exp = experiment.experiment(
                arquivo=base['arquivo'], n_testes=base['n_testes'], max_iter=base['max_iter'],
                num_bees=num_bees, limit=limit, seed=base['seed']
            )
            exp.execute_experiment(1) # Opção 1 = ABC
            
            messagebox.showinfo("Sucesso", f"Experimento ABC finalizado!\nResultado salvo em seu respectivo CSV.")
            self.carregar_ranking() 
        except ValueError:
            messagebox.showerror("Erro de Tipo", "Certifique-se de que todos os parâmetros inseridos sejam numéricos.")

    def rodar_ga(self):
        try:
            base = self.coletar_dados_base(self.ga_inputs)
            pop_size = int(self.ga_inputs['population_size'].get() or 53)
            crossover = float(self.ga_inputs['crossover_rate'].get() or 0.9)
            mutation = float(self.ga_inputs['mutation_rate'].get() or 0.15)
            
            exp = experiment.experiment(
                arquivo=base['arquivo'], n_testes=base['n_testes'], max_iter=base['max_iter'],
                population_size=pop_size, crossover_rate=crossover, mutation_rate=mutation, seed=base['seed']
            )
            exp.execute_experiment(2) # Opção 2 = GA
            
            messagebox.showinfo("Sucesso", f"Experimento GA finalizado!\nResultado salvo em seu respectivo CSV.")
            self.carregar_ranking() 
        except ValueError:
            messagebox.showerror("Erro de Tipo", "Verifique as taxas de Crossover/Mutação (Decimais) e tamanho da população (Inteiro).")

    def carregar_ranking(self):
        """Lê os dois CSVs, unifica, filtra e exibe na tabela do Tkinter"""
        csv_abc = 'results/historico_experimentos_abc.csv' 
        csv_ga = 'results/historico_experimentos_ga.csv'
        
        dfs = []
        if os.path.exists(csv_abc):
            try: dfs.append(pd.read_csv(csv_abc))
            except Exception: pass
        if os.path.exists(csv_ga):
            try: dfs.append(pd.read_csv(csv_ga))
            except Exception: pass
            
        if not dfs:
            messagebox.showwarning("Aviso", "Nenhum arquivo de histórico encontrado em 'results/'.")
            return
            
        try:
            df_total = pd.concat(dfs, ignore_index=True, sort=False)
            
            filtro_selecionado = self.combo_filtro.get()
            df_filtrado = df_total[
                (df_total['Caso_Teste'] == filtro_selecionado) | 
                (df_total['Caso_Teste'] == f"tests/{filtro_selecionado}")
            ].copy()
            
            if df_filtrado.empty:
                self.tree.delete(*self.tree.get_children())
                messagebox.showinfo("Informação", f"Nenhum registro encontrado para {filtro_selecionado}")
                return
                
            df_ordenado = df_filtrado.sort_values(by='Custo_Medio', ascending=True)
            
            colunas_gerais = ['Caso_Teste', 'Algoritmo', 'Custo_Medio', 'Melhor_Custo_Encontrado', 'Tempo_Exec_Segundos']
            outras_colunas = [col for col in df_ordenado.columns if col not in colunas_gerais]
            colunas_finais = colunas_gerais + outras_colunas
            
            df_ordenado = df_ordenado[colunas_finais].fillna('-')
            
            self.tree["columns"] = colunas_finais
            for col in colunas_finais:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=110, anchor='center')
                
            self.tree.delete(*self.tree.get_children())
            
            for _, row in df_ordenado.iterrows():
                self.tree.insert("", "end", values=list(row))
                
        except Exception as e:
            messagebox.showerror("Erro de Processamento", f"Falha ao gerar ranking:\n{str(e)}")

    def exibir_grafico_selecionado(self, event):
        """Detecta qual linha foi clicada e abre a imagem correspondente em um pop-up"""
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            return
            
        # Pega os valores das colunas da linha clicada
        valores_linha = self.tree.item(item_selecionado[0], 'values')
        
        # Mapeia as colunas baseado no arranjo do 'colunas_gerais' do seu método carregar_ranking
        caso_teste = valores_linha[0].replace("tests/", "") # Limpa o caminho para obter ex: 'teste15.txt'
        algoritmo = valores_linha[1].lower()               # Obtém 'abc' ou 'ga'
        tempo = valores_linha[10]

        tag = 'abc' if algoritmo == 'artificial bee colony' else 'ga'
        
        caminho_imagem = f'results/analise_resultados_{caso_teste.replace('.txt', '')}_{tag}_{tempo}.png'
        #caminho_imagem = os.path.join("results", nome_imagem)
        
        # Verifica se a imagem realmente existe na pasta de resultados antes de tentar carregar
        if not os.path.exists(caminho_imagem):
            messagebox.showwarning("Imagem não encontrada", f"Não foi possível localizar o gráfico para este resultado:\n{caminho_imagem}")
            return
            
        try:
            # Cria uma janela pop-up separada
            janela_imagem = tk.Toplevel(self.root)
            janela_imagem.title(f"Gráfico de Convergência - {algoritmo.upper()} ({caso_teste})")
            
            # Carrega e converte a imagem usando o Pillow
            img_original = Image.open(caminho_imagem)
            
            # Redimensiona a imagem caso ela seja gigantesca (ajusta bem em 600x450 mantendo qualidade)
            img_redimensionada = img_original.resize((600, 450), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_redimensionada)
            
            label_img = ttk.Label(janela_imagem, image=img_tk)
            label_img.image = img_tk 
            label_img.pack(padx=15, pady=15)
            
            # Botão fechar em formato ttk
            btn_fechar = ttk.Button(janela_imagem, text="Fechar Visualização", command=janela_imagem.destroy)
            btn_fechar.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Erro ao abrir imagem", f"Ocorreu um problema ao renderizar o gráfico:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentInterface(root)
    root.mainloop()