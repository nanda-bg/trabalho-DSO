from datetime import datetime
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from exception.camposVaziosException import CampoVaziosException
from exception.chipInvalidoException import ChipInvalidoException
from exception.cpfInvalidoException import CPFInvalidoException
from exception.dataFinalInvalidaException import DataFinalInvalida
from exception.motivo_invalido_exception import MotivoInvalidoException
from exception.nomeInvalidoException import NomeInvalidoException
from exception.raca_invalida_exception import RacaInvalidaException
from view.abstract_tela import AbstractTela

class TelaDoacao(AbstractTela):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.opcao_selecionada = None
        self.root.title("Gerenciamento de Doações")
        self.root.geometry("500x700")
        self.root.configure(bg="#fdd9b9")

    def limpar_tela(self):
        """Remove todos os widgets da janela."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_widgets(self):
        tk.Label(self.root, text="Gerenciamento de Doações", font=("Times New Roman", 16), bg="#fdd9b9").pack(pady=10)
        tk.Label(self.root, text="Escolha uma operação:", font=("Times New Roman", 12), bg="#fdd9b9").pack(pady=5)

        opcoes = [
            ("Doar", 1),
            ("Emitir Relatório", 2),
            ("Excluir Doação", 3),
            ("Alterar Doação", 4),
            ("Retornar ao Menu Principal", 5)
        ]

        for i, (texto, valor) in enumerate(opcoes, start=1):  # 'i' é o número da opção
            botao = tk.Button(
                self.root,
                text=texto,
                command=lambda v=valor, num=i: self.set_opcao(num),  # Passa o valor e o número
                font=("Times New Roman", 12),
                bg="#ff7e0e",
                fg="white",
                width=30
            )
            botao.bind("<Enter>", lambda event, b=botao: b.config(bg="#eb6c00"))
            botao.bind("<Leave>", lambda event, b=botao: b.config(bg="#ff7e0e"))
            botao.pack(pady=5)

    def set_opcao(self, opcao):
        self.opcao_selecionada = opcao
        self.root.quit()

    def mostrar_tela(self):
        self.limpar_tela()
        self.criar_widgets()
        self.opcao_selecionada = None
        self.root.mainloop()
        return self.opcao_selecionada

    def mostrar_mensagem(self, mensagem):
        messagebox.showinfo("Informação", mensagem)

    def pega_dados_doacao(self):
        self.limpar_tela()
        dados = {}

        # Configurar canvas e scroll
        canvas = tk.Canvas(self.root, bg="#fdd9b9")
        scroll_y = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg="#fdd9b9")

        # Configurar canvas e ligação com a rolagem
        canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        central_frame = tk.Frame(container, bg="#fdd9b9")
        central_frame.pack(expand=True)

        tk.Label(central_frame, text="Cadastro do Animal", font=("Times New Roman", 16), bg="#fdd9b9").pack(pady=10)

        labels = ["CPF do doador:", "Chip do Animal:", "Nome do Animal:", "Raça do Animal:", "Vacinas do Animal:", "Tipo do Animal:", "Motivo da Doação:"]
        campos = ["cpf_doador", "chip_animal", "nome_animal", "raca_animal", "vacinas_animal", "tipo_animal", "motivo_doacao"]

        vacinas = ["Raiva", "Leptospirose", "Hepatite Infecciosa", "Cinomose", "Parvovirose", "Coronavirose"]
        vacinas_selecionadas = []

        def configurar_opcao(opcao):
            opcao.config(
                font=("Times New Roman", 12),
                bg="white",
                fg="black",
                relief="solid",
                width=15
            )

        # Variáveis para armazenar o menu e seu estado
        porte_label = None
        porte_menu = None
        porte_menu_var = tk.StringVar(value="Escolha...")  # Variável global para o valor do Porte

        # Função para exibir o campo de porte apenas após a seleção de "Cachorro"
        def exibir_campo_porte(*args):
            nonlocal porte_label, porte_menu
            if opcao_animal.get() == "Cachorro":
                if not porte_label:  # Apenas cria o campo se ainda não existir
                    porte_label = tk.Label(central_frame, text="Porte do Animal:", font=("Times New Roman", 12), bg="#fdd9b9")
                    porte_label.pack(pady=5)

                    porte_menu = tk.OptionMenu(central_frame, porte_menu_var, "Grande", "Médio", "Pequeno")
                    configurar_opcao(porte_menu)
                    porte_menu.pack(pady=5)
            else:
                if porte_label:
                    porte_label.destroy()
                    porte_menu.destroy()
                    porte_label = None
                    porte_menu = None
                    porte_menu_var.set("Escolha...")  # Resetando o valor

        # Loop para criar os elementos da interface
        for label, campo in zip(labels, campos):
            tk.Label(central_frame, text=label, font=("Times New Roman", 12), bg="#fdd9b9").pack(pady=5)
            if campo == "tipo_animal":
                opcao_animal = tk.StringVar()
                opcao_animal.set("Escolha...")
                tipo_animal = tk.OptionMenu(central_frame, opcao_animal, "Gato", "Cachorro")
                configurar_opcao(tipo_animal)
                tipo_animal.pack(pady=5)

                dados[campo] = opcao_animal
                opcao_animal.trace("w", exibir_campo_porte)  # Monitora mudanças na seleção
            elif campo == "vacinas_animal":
                vacinas_frame = tk.Frame(central_frame, bg="#fdd9b9")
                vacinas_frame.pack(pady=5)
                for vacina in vacinas:
                    var = tk.BooleanVar()
                    vacinas_selecionadas.append((vacina, var))
                    tk.Checkbutton(vacinas_frame, text=vacina, variable=var, bg="#fdd9b9", font=("Times New Roman", 12)).pack(anchor="w")
                dados[campo] = vacinas_selecionadas
            else:
                entrada = tk.Entry(central_frame, font=("Times New Roman", 12))
                entrada.pack(pady=5)
                dados[campo] = entrada

        def confirmar():
            try:    
                campos_vazios = []

                for key, campo in dados.items():
                    if not campo:
                        campos_vazios.append(key)
                    elif key == "vacinas_animal":
                        dados[key] = [vacina for vacina, var in campo if var.get()]
                    dados[key] = campo

                if campos_vazios:
                    raise CampoVaziosException(campos_vazios)
                
                if not dados["cpf"].isDigit() or dados["cpf"].length() != 11 or not self.validar_numeros_cpf(dados["cpf"].get()):
                    raise CPFInvalidoException()
                
                if not dados["chip"].isDigit() or dados["chip"].length() != 7:
                    raise ChipInvalidoException()
                
                if dados["nome_animal"].length < 3:
                    raise NomeInvalidoException()
                
                if dados["raca_animal"].length < 3:
                    raise RacaInvalidaException()
                
                if dados["motivo_doacao"].length < 3:
                    raise MotivoInvalidoException()
        
                for key, campo in dados.items():
                    if key == "vacinas_animal":
                        dados[key] = [vacina for vacina, var in campo if var.get()]
                    else:    
                        dados[key] = campo.get()

                self.opcao_selecionada = dados
                self.root.quit()
            except Exception as e:
                self.mostrar_mensagem(e)    

        def voltar():
            for key in dados:
                dados[key] = None
            self.opcao_selecionada = None
            self.root.quit()

        # Botões Confirmar e Voltar
        tk.Button(
            central_frame,
            text="Confirmar",
            command=confirmar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white"
        ).pack(pady=20)

        tk.Button(
            central_frame,
            text="Voltar",
            command=voltar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white",
            width=30
        ).pack(pady=20)

        self.root.mainloop()
        return dados


    def pega_datas_relatorio(self):
        def abrir_calendario(entry):
            def confirmar_data():
                data_selecionada = calendario.get_date()
                entry.delete(0, tk.END)
                entry.insert(0, data_selecionada)
                janela_calendario.destroy()

            janela_calendario = tk.Toplevel()
            janela_calendario.title("Selecionar Data")
            calendario = Calendar(janela_calendario, date_pattern="yyyy-mm-dd")
            calendario.pack(pady=10)
            tk.Button(janela_calendario, text="Confirmar", command=confirmar_data).pack(pady=10)

        def confirmar():
            try:
                campos_vazios = []

                data_inicio = entrada_inicio.get()
                data_fim = entrada_fim.get()

                if not data_inicio:
                    campos_vazios.append("Data de Início")

                if not data_fim:
                    campos_vazios.append("Data de Fim")

                if campos_vazios:
                    raise CampoVaziosException(campos_vazios)

                data_inicio_obj = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                data_fim_obj = datetime.strptime(data_fim, "%Y-%m-%d").date()

                if data_inicio_obj > data_fim_obj:      
                    raise DataFinalInvalida()
                    
                datas["inicio"] = data_inicio
                datas["fim"] = data_fim

                janela_relatorio.destroy()

            except Exception as e:
                self.mostrar_mensagem(e)

        datas = {}

        # Janela de seleção
        janela_relatorio = tk.Toplevel()
        janela_relatorio.title("Selecionar Datas")
        janela_relatorio.geometry("300x200")
        janela_relatorio.configure(bg="#fdd9b9")

        tk.Label(janela_relatorio, text="Data de Início:", bg="#fdd9b9").pack(pady=5)
        entrada_inicio = tk.Entry(janela_relatorio, font=("Arial", 12))
        entrada_inicio.pack(pady=5)
        entrada_inicio.bind("<Button-1>", lambda e: abrir_calendario(entrada_inicio))

        tk.Label(janela_relatorio, text="Data de Fim:", bg="#fdd9b9").pack(pady=5)
        entrada_fim = tk.Entry(janela_relatorio, font=("Arial", 12))
        entrada_fim.pack(pady=5)
        entrada_fim.bind("<Button-1>", lambda e: abrir_calendario(entrada_fim))

        tk.Button(janela_relatorio, text="Confirmar", command=confirmar, bg="#ff7e0e", fg="white").pack(pady=20)

        self.root.wait_window(janela_relatorio)  # Aguarda o fechamento da janela_relatorio
        return datas


    def seleciona_animal(self):
        self.limpar_tela()

        tk.Label(self.root, text="Digite o chip do animal envolvido na doação:", font=("Times New Roman", 14), bg="#fdd9b9").pack(pady=10)
        entrada_chip = tk.Entry(self.root, font=("Times New Roman", 12))
        entrada_chip.pack(pady=10)

        def confirmar():
            try:
                chip = entrada_chip.get()

                if not chip.isdigit() or len(chip) != 7:
                    raise ChipInvalidoException()
                
                self.opcao_selecionada = int(entrada_chip.get())
                self.root.quit()
                
            except ChipInvalidoException as e:
                self.mostrar_mensagem(e)

        def voltar():
            self.opcao_selecionada = None
            self.root.quit()    

        tk.Button(
            self.root,
            text="Confirmar",
            command=confirmar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white"
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Voltar",
            command=voltar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white",
            width=30
        ).pack(pady=20)

        self.root.mainloop()
        return self.opcao_selecionada
    
    def confirmar_exclusão(self, dados_doacao):
        resposta = messagebox.askquestion("Confirme a exclusão", f"Tem certeza que deseja excluir a doação do animal {dados_doacao['nome_animal']}?", icon="warning")
        if resposta == "yes":
            return "s"
        else:
            return "n"

    def deseja_cadastrar_doador(self):
        resposta = messagebox.askquestion("Doador não encontrado", "O doador não existe, deseja cadastrar?")
        if resposta == "yes":
            return "s"
        else:
            return "n"

    def pega_dados_alteracao(self):     
        self.limpar_tela()
        dados = {}

        tk.Label(self.root, text=f"Alteração de Doação", font=("Times New Roman", 16), bg="#fdd9b9").pack(pady=10)

        labels = ["Alterar doador (CPF): ", "Alterar animal (chip): ", "Alterar motivo da doação: "]
        campos = ["cpf", "animal", "motivo_doacao"]

        for label, campo in zip(labels, campos):
            tk.Label(self.root, text=label, font=("Times New Roman", 12), bg="#fdd9b9").pack(pady=5)
            entrada = tk.Entry(self.root, font=("Times New Roman", 12))
            entrada.pack(pady=5)
            dados[campo] = entrada 

        def confirmar():
            for key, campo in dados.items():
                valor = campo.get() if campo else None
                dados[key] = valor

            self.opcao_selecionada = dados
            self.root.quit()

        def voltar():
            self.opcao_selecionada = None
            self.root.quit()

        tk.Button(
            self.root,
            text="Confirmar",
            command=confirmar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white"
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="Voltar",
            command=voltar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white",
            width=30
        ).pack(pady=20)


        self.root.mainloop()
        return dados
    
    def exibir_dados_doacoes(self, lista_doacoes):
        self.limpar_tela()
        titulo = "Relatório de Doações"
        tk.Label(self.root, text=titulo, font=("Times New Roman", 16), bg="#fdd9b9").pack(pady=10)

        # Criação do Treeview
        colunas = ("Data", "Animal", "Doador", "Motivo")
        tabela = ttk.Treeview(self.root, columns=colunas, show="headings", height=10)

        # Configurar cabeçalhos
        for coluna in colunas:
            tabela.heading(coluna, text=coluna)
            tabela.column(coluna, anchor="center", width=200)

        # Adicionar os dados à tabela
        for doacao in lista_doacoes:
            tabela.insert("", "end", values=(
                doacao["Data"], 
                doacao["Animal"], 
                doacao["Doador"], 
                doacao["Motivo"]
                ))

        tabela.pack(pady=10, padx=10)

        def voltar():
            self.root.quit()

        # Botão voltar
        tk.Button(
            self.root,
            text="Voltar",
            command= voltar,
            font=("Times New Roman", 12),
            bg="#ff7e0e",
            fg="white",
            width=30
        ).pack(pady=20)

        

        self.root.mainloop()
