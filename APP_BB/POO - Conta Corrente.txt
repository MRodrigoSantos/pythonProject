import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ContaBancaria:
    def __init__(self, nome_cliente):
        self._nome_cliente = nome_cliente
        self.__saldo = 0.0
        self._ultima_data = None
        self._ultimo_tipo = "Nenhuma"
        self._ultimo_valor = 0.0

    @property
    def saldo(self):
        return self.__saldo

    def _alterar_saldo(self, valor):
        if self.__saldo + valor < 0:
            raise ValueError("Saldo insuficiente.")
        self.__saldo += valor

    def _registrar_movimentacao(self, tipo, valor):
        self._ultima_data = datetime.datetime.now()
        self._ultimo_tipo = tipo
        self._ultimo_valor = valor

    def consultar_saldo(self):
        return self.saldo

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de depósito inválido.")
        self._alterar_saldo(valor)
        self._registrar_movimentacao("Depositou", valor)

    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor de saque inválido.")
        self._alterar_saldo(-valor)
        self._registrar_movimentacao("Sacou", valor)

class ContaCorrente(ContaBancaria):
    contas_cadastradas = []

    def __init__(self, nome_cliente, chave_pix, carregando=False, saldo_carregado=0.0, ultima_data=None, ultimo_tipo="Criado", ultimo_valor=0.0):
        super().__init__(nome_cliente)
        if not carregando:
            if any(conta.chave_pix == chave_pix for conta in ContaCorrente.contas_cadastradas):
                raise ValueError("Chave Pix já existe.")
            self._registrar_movimentacao("Conta criada", 0)
            salvar_movimentacao(chave_pix, datetime.datetime.now(), "Conta criada", 0.0, "")
        else:
            self._ultima_data = ultima_data
            self._ultimo_tipo = ultimo_tipo
            self._ultimo_valor = ultimo_valor
            self._alterar_saldo(saldo_carregado)
        self._chave_pix = chave_pix
        ContaCorrente.contas_cadastradas.append(self)

    @property
    def chave_pix(self):
        return self._chave_pix

    def pagar(self, chave_destino, valor):
        if valor <= 0:
            raise ValueError("Valor de Pix inválido.")
        destino = next((c for c in ContaCorrente.contas_cadastradas if c.chave_pix == chave_destino), None)
        if not destino:
            raise ValueError("Chave Pix não encontrada.")
        self.sacar(valor)
        destino.receber_pix(valor)
        self._registrar_movimentacao(f"Transferiu para {chave_destino}", valor)
        salvar_movimentacao(self.chave_pix, datetime.datetime.now(), f"Transferiu para {chave_destino}", valor, "")
        destino._registrar_movimentacao(f"Recebeu de {self.chave_pix}", valor)
        salvar_movimentacao(destino.chave_pix, datetime.datetime.now(), f"Recebeu de {self.chave_pix}", valor, "")

    def receber_pix(self, valor):
        if valor <= 0:
            raise ValueError("Valor de Pix inválido.")
        self.depositar(valor)

def salvar_dados():
    with open("contas.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("Nome,Chave Pix,Saldo,Última Movimentação,Valor\n")
        for conta in ContaCorrente.contas_cadastradas:
            data_formatada = conta._ultima_data.strftime("%d/%m/%Y %H:%M") if conta._ultima_data else "Nenhuma"
            valor_br = f"R$ {conta._ultimo_valor:.2f}" if conta._ultimo_valor > 0 else "-"
            linha = f"{conta._nome_cliente},{conta.chave_pix},{conta.saldo:.2f},{data_formatada} {conta._ultimo_tipo},{valor_br}\n"
            arquivo.write(linha)

def carregar_dados():
    ultima_data_global = None
    if os.path.exists("contas.txt"):
        try:
            with open("contas.txt", "r", encoding="utf-8") as arquivo:
                next(arquivo)
                for linha in arquivo:
                    linha = linha.strip()
                    if not linha:
                        continue
                    partes = linha.split(",", 4)
                    if len(partes) != 5:
                        continue
                    nome, chave_pix, saldo_str, movimento, valor_str = partes
                    try:
                        saldo_carregado = float(saldo_str)
                        valor = float(valor_str.replace("R$ ", "")) if "R$" in valor_str else 0.0
                        if movimento != "Nenhuma":
                            partes_mov = movimento.split(" ", 2)
                            if len(partes_mov) == 3:
                                data_str = partes_mov[0] + " " + partes_mov[1]
                                ultimo_tipo = partes_mov[2]
                                ultima_data = datetime.datetime.strptime(data_str, "%d/%m/%Y %H:%M")
                                if (ultima_data_global is None) or (ultima_data > ultima_data_global):
                                    ultima_data_global = ultima_data
                                ContaCorrente(nome, chave_pix, carregando=True, saldo_carregado=saldo_carregado, ultima_data=ultima_data, ultimo_tipo=ultimo_tipo, ultimo_valor=valor)
                            else:
                                ContaCorrente(nome, chave_pix, carregando=True, saldo_carregado=saldo_carregado)
                        else:
                            ContaCorrente(nome, chave_pix, carregando=True, saldo_carregado=saldo_carregado)
                    except:
                        pass
        except:
            pass
    return ultima_data_global.strftime("%d/%m/%Y %H:%M") if ultima_data_global else None

def salvar_movimentacao(chave_pix, data, movimentacao, valor, extra):
    with open("movimentacoes.txt", "a", encoding="utf-8") as arq:
        data_str = data.strftime("%d/%m/%Y %H:%M")
        linha = f"{chave_pix},{data_str},{movimentacao},{valor:.2f},{extra}\n"
        arq.write(linha)

def carregar_movimentacoes():
    movimentos = []
    if os.path.exists("movimentacoes.txt"):
        with open("movimentacoes.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split(",", 4)
                if len(partes) != 5:
                    continue
                chave, data_str, mov, valor_str, extra = partes
                try:
                    valor_f = float(valor_str)
                    data_dt = datetime.datetime.strptime(data_str, "%d/%m/%Y %H:%M")
                    movimentos.append({
                        "chave": chave,
                        "data": data_dt,
                        "movimentacao": mov,
                        "valor": valor_f,
                        "extra": extra
                    })
                except:
                    pass
    return movimentos

def remover_movimentacoes(chave):
    """Remove do arquivo movimentacoes.txt todas as linhas que contenham a chave informada."""
    if os.path.exists("movimentacoes.txt"):
        try:
            with open("movimentacoes.txt", "r", encoding="utf-8") as arq:
                linhas = arq.readlines()
            with open("movimentacoes.txt", "w", encoding="utf-8") as arq:
                for linha in linhas:
                    if not linha.startswith(chave + ","):
                        arq.write(linha)
        except Exception as e:
            print(f"Erro ao remover movimentações: {e}")

class AppTk:
    def __init__(self, root):
        self.root = root
        self.root.title("Eletrobank - Tkinter")
        self.root.geometry("360x600")
        self.root.resizable(False, False)
        self.top_frame = tk.Frame(root, bg="#6A0DAD", height=60)
        self.top_frame.pack(fill="x")
        self.top_label = tk.Label(self.top_frame, text="Olá, Usuário", bg="#6A0DAD", fg="white", font=("Arial", 14, "bold"))
        self.top_label.pack(side="left", padx=20, pady=15)
        self.profile_btn = tk.Button(self.top_frame, text="Eletrobank", bg="white", fg="#6A0DAD", relief="flat", font=("Montserrat", 10))
        self.profile_btn.pack(side="right", padx=20, pady=15)
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)
        self.account_var = tk.StringVar()
        self.account_combo = ttk.Combobox(self.main_frame, textvariable=self.account_var, state="readonly")
        self.account_combo.pack(pady=5, fill="x")
        self.account_combo.bind("<<ComboboxSelected>>", lambda e: self.atualiza_info_conta())
        self.saldo_label = tk.Label(self.main_frame, text="Saldo: R$ 0.00", font=("Arial", 18, "bold"))
        self.saldo_label.pack(pady=10, anchor="w")
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=10, fill="x")
        self.pix_btn = tk.Button(btn_frame, text="Pix", command=self.fazer_pix)
        self.pix_btn.pack(side="left", expand=True, fill="x", padx=5)
        self.deposit_btn = tk.Button(btn_frame, text="Depositar", command=self.depositar)
        self.deposit_btn.pack(side="left", expand=True, fill="x", padx=5)
        self.sacar_btn = tk.Button(btn_frame, text="Sacar", command=self.sacar)
        self.sacar_btn.pack(side="left", expand=True, fill="x", padx=5)
        self.nova_conta_btn = tk.Button(self.main_frame, text="Criar Conta", command=self.criar_conta)
        self.nova_conta_btn.pack(pady=5, fill="x")
        self.apagar_conta_btn = tk.Button(self.main_frame, text="Apagar Conta", command=self.apagar_conta)
        self.apagar_conta_btn.pack(pady=5, fill="x")
        self.todos_saldos_btn = tk.Button(self.main_frame, text="Consultar Todos [Adm] - Senha: 123", command=self.consultar_todos_saldos)
        self.todos_saldos_btn.pack(pady=5, fill="x")
        self.mov_frame = tk.Frame(self.main_frame)
        self.mov_frame.pack(pady=5, fill="both", expand=True)
        self.mov_label = tk.Label(self.mov_frame, text="Movimentações da Conta:", font=("Arial", 12, "bold"))
        self.mov_label.pack(anchor="w")
        cols = ("Data", "Movimentação", "Valor")
        self.mov_tree = ttk.Treeview(self.mov_frame, columns=cols, show="headings", height=6)
        self.mov_tree.heading("Data", text="Data")
        self.mov_tree.heading("Movimentação", text="Movimentação")
        self.mov_tree.heading("Valor", text="Valor")
        self.mov_tree.column("Data", width=100)
        self.mov_tree.column("Movimentação", width=180)
        self.mov_tree.column("Valor", width=100)
        self.mov_tree.pack(fill="both", expand=True)
        self.mov_tree.bind("<Configure>", self.ajustar_colunas)
        self.sair_btn = tk.Button(self.main_frame, text="Sair", command=self.sair)
        self.sair_btn.pack(pady=5, fill="x")
        self.update_label = tk.Label(self.main_frame, text="", justify="right", anchor="e", fg="gray", font=("Arial", 9))
        self.update_label.pack(side="bottom", anchor="e", pady=5)
        self.data_atualizacao = carregar_dados()
        self.movimentacoes = carregar_movimentacoes()
        self.atualiza_combo_contas()
        if ContaCorrente.contas_cadastradas:
            self.account_combo.current(0)
            self.atualiza_info_conta()
        self.atualiza_label_rodape()

    def ajustar_colunas(self, event):
        largura = event.width
        self.mov_tree.column("Data", width=int(largura * 0.30))
        self.mov_tree.column("Movimentação", width=int(largura * 0.45))
        self.mov_tree.column("Valor", width=int(largura * 0.25))

    def atualiza_combo_contas(self):
        contas_lista = [f"{conta._nome_cliente} ({conta.chave_pix})" for conta in ContaCorrente.contas_cadastradas]
        self.account_combo["values"] = contas_lista

    def get_conta_selecionada(self):
        idx = self.account_combo.current()
        if idx == -1:
            return None
        return ContaCorrente.contas_cadastradas[idx]

    def atualiza_info_conta(self):
        conta = self.get_conta_selecionada()
        if conta:
            self.top_label.config(text=f"Olá, {conta._nome_cliente}")
            self.saldo_label.config(text=f"Saldo: R$ {conta.saldo:.2f}")
            self.atualiza_lista_movimentacoes(conta.chave_pix)
        else:
            self.top_label.config(text="Olá, Usuário(a)")
            self.saldo_label.config(text="Saldo: R$ 0.00")
            self.mov_tree.delete(*self.mov_tree.get_children())

    def atualiza_lista_movimentacoes(self, chave_pix):
        self.mov_tree.delete(*self.mov_tree.get_children())
        for mov in self.movimentacoes:
            if mov["chave"] == chave_pix:
                data_str = mov["data"].strftime("%d/%m/%Y %H:%M")
                mov_str = mov["movimentacao"]
                val_str = f"R$ {mov['valor']:.2f}"
                self.mov_tree.insert("", "end", values=(data_str, mov_str, val_str))

    def atualiza_label_rodape(self):
        if self.data_atualizacao:
            self.update_label.config(text=f"Atualizado em {self.data_atualizacao}")
        else:
            self.update_label.config(text="Banco de dados não criado ou não compatível.\nSerá criado após o primeiro cadastro de conta.")

    def fazer_pix(self):
        conta_origem = self.get_conta_selecionada()
        if not conta_origem:
            messagebox.showerror("Erro", "Nenhuma conta selecionada.")
            return
        chave_destino = simpledialog.askstring("Fazer Pix", "Chave Pix de destino:")
        if not chave_destino:
            return
        valor_str = simpledialog.askstring("Fazer Pix", "Valor do Pix:")
        if not valor_str:
            return
        try:
            valor = float(valor_str)
            conta_origem.pagar(chave_destino, valor)
            salvar_dados()
            self.movimentacoes = carregar_movimentacoes()
            self.atualiza_info_conta()
            messagebox.showinfo("Pix", "Pix realizado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", f"Não foi possível realizar Pix:\n{e}")

    def depositar(self):
        conta = self.get_conta_selecionada()
        if not conta:
            messagebox.showerror("Erro", "Nenhuma conta selecionada.")
            return
        valor_str = simpledialog.askstring("Depositar", "Valor do depósito:")
        if not valor_str:
            return
        try:
            valor = float(valor_str)
            conta.depositar(valor)
            salvar_movimentacao(conta.chave_pix, datetime.datetime.now(), "Depositou", valor, "")
            salvar_dados()
            self.movimentacoes = carregar_movimentacoes()
            self.atualiza_info_conta()
            messagebox.showinfo("Depósito", "Depósito realizado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", f"Não foi possível depositar:\n{e}")

    def sacar(self):
        conta = self.get_conta_selecionada()
        if not conta:
            messagebox.showerror("Erro", "Nenhuma conta selecionada.")
            return
        valor_str = simpledialog.askstring("Sacar", "Valor do saque:")
        if not valor_str:
            return
        try:
            valor = float(valor_str)
            conta.sacar(valor)
            salvar_movimentacao(conta.chave_pix, datetime.datetime.now(), "Sacou", valor, "")
            salvar_dados()
            self.movimentacoes = carregar_movimentacoes()
            self.atualiza_info_conta()
            messagebox.showinfo("Saque", "Saque realizado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", f"Não foi possível sacar:\n{e}")

    def criar_conta(self):
        nome = simpledialog.askstring("Criar Conta", "Nome do cliente:")
        if not nome:
            return
        chave = simpledialog.askstring("Criar Conta", "Chave Pix:")
        if not chave:
            return
        try:
            nova = ContaCorrente(nome, chave)
            salvar_dados()
            self.movimentacoes = carregar_movimentacoes()
            self.atualiza_combo_contas()
            idx = self.account_combo["values"].index(f"{nova._nome_cliente} ({nova.chave_pix})")
            self.account_combo.current(idx)
            self.atualiza_info_conta()
            messagebox.showinfo("Conta", "Conta criada com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", f"Não foi possível criar conta:\n{e}")

    def apagar_conta(self):
        conta = self.get_conta_selecionada()
        if not conta:
            messagebox.showerror("Erro", "Nenhuma conta selecionada.")
            return
        resp = messagebox.askyesno("Apagar Conta", f"Confirma apagar a conta de {conta._nome_cliente}?")
        if resp:
            ContaCorrente.contas_cadastradas.remove(conta)
            remover_movimentacoes(conta.chave_pix)
            salvar_dados()
            self.movimentacoes = carregar_movimentacoes()
            self.atualiza_combo_contas()
            self.atualiza_info_conta()
            messagebox.showinfo("Conta", "Conta apagada com sucesso!")

    def consultar_todos_saldos(self):
        senha = simpledialog.askstring("Modo Adm", "Digite a senha:", show="*")
        if senha != "123":
            messagebox.showerror("Erro", "Senha incorreta.")
            return
        if not ContaCorrente.contas_cadastradas:
            messagebox.showinfo("Contas", "Nenhuma conta cadastrada.")
            return
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Contas Cadastradas")
        nova_janela.geometry("1000x350")
        colunas = ("Nome", "Chave Pix", "Saldo", "Última Movimentação")
        tabela = ttk.Treeview(nova_janela, columns=colunas, show="headings")
        tabela.heading("Nome", text="Nome")
        tabela.heading("Chave Pix", text="Chave Pix")
        tabela.heading("Saldo", text="Saldo")
        tabela.heading("Última Movimentação", text="Última Movimentação")
        tabela.column("Nome", width=175)
        tabela.column("Chave Pix", width=175)
        tabela.column("Saldo", width=100)
        tabela.column("Última Movimentação", width=250)
        tabela.pack(fill="both", expand=True)
        for c in ContaCorrente.contas_cadastradas:
            data_formatada = c._ultima_data.strftime("%d/%m/%Y %H:%M") if c._ultima_data else "Nenhuma"
            if c._ultima_data:
                mov = f"{data_formatada} {c._ultimo_tipo} R$ {c._ultimo_valor:.2f}"
            else:
                mov = "Criado - R$ 0.00"
            tabela.insert("", "end", values=(c._nome_cliente, c.chave_pix, f"R$ {c.saldo:.2f}", mov))

    def sair(self):
        self.root.destroy()

def exibir_janela_login():
    login_root = tk.Tk()
    login_root.title("Login")
    login_root.geometry("300x220")
    login_root.resizable(False, False)
    label_usuario = tk.Label(login_root, text="Usuário:")
    label_usuario.pack(pady=(10, 0))
    entry_usuario = tk.Entry(login_root)
    entry_usuario.pack()
    entry_usuario.focus_set()
    label_senha = tk.Label(login_root, text="Senha:")
    label_senha.pack(pady=(10, 0))
    entry_senha = tk.Entry(login_root, show="*")
    entry_senha.pack()
    btn_entrar = tk.Button(login_root, text="Entrar", command=lambda: verificar(entry_usuario, entry_senha, login_root))
    btn_entrar.pack(pady=5)
    credenciais = tk.Label(login_root, text="(Usuário: Márcio / Senha: 123)", fg="gray", font=("Arial", 9))
    credenciais.pack(pady=(0, 10))
    entry_usuario.bind("<Return>", lambda e: entry_senha.focus_set())
    entry_senha.bind("<Return>", lambda e: btn_entrar.invoke())
    def verificar(entry_usuario, entry_senha, login_root):
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        if usuario == "Márcio" and senha == "123":
            login_root.destroy()
            iniciar_app()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
    login_root.mainloop()

def iniciar_app():
    root = tk.Tk()
    app = AppTk(root)
    root.mainloop()

if __name__ == "__main__":
    exibir_janela_login()
    sys.exit(0)