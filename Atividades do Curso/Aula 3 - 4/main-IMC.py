# =================================================================================================
# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
# =================================================================================================

import tkinter as tk         # Biblioteca base para as janelas e rótulos
import Cálculos_IMC as cl    # Sua biblioteca com as funções matemáticas
from tkinter import ttk      # Componentes avançados (Abas, Inputs e Tabela)
import sqlite3               # Banco de dados nativo do Python

# =================================================================================================
# CONFIGURANDO O BANCO DE DADOS (SQLite3)
# =================================================================================================

def init_db():
    # Conecta ou cria o arquivo do banco de dados local
    conn = sqlite3.connect("sistema_calculos.db")
    cursor = conn.cursor()

    # Cria a tabela de pessoas e guarda todas as colunas necessárias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            peso REAL,
            altura REAL,
            carga_horaria REAL,
            salario REAL,
            horas_extras INTEGER
        )
    """)
    conn.commit()
    conn.close()

def salvar_no_banco(dados_dict):
    """Guarda ou atualiza os dados do usuário com base no nome digitado"""
    nome_val = nome_cadastro.get().strip()
    if not nome_val:
        return # Se o campo Nome estiver em branco, o cálculo roda mas não salva
        
    conn = sqlite3.connect("sistema_calculos.db")
    cursor = conn.cursor()
    
    # Procura se o nome inserido já existe no banco
    cursor.execute("SELECT id FROM pessoas WHERE nome = ?", (nome_val,))
    existe = cursor.fetchone()
    
    if existe:
        # Se a pessoa já existe, atualiza apenas o dado que foi calculado agora
        for campo, valor in dados_dict.items():
            if valor is not None:
                cursor.execute(f"UPDATE pessoas SET {campo} = ? WHERE nome = ?", (valor, nome_val))
    else:
        # Se for um nome novo, cria um novo registro do zero
        cursor.execute("""
            INSERT INTO pessoas (nome, peso, altura, carga_horaria, salario, horas_extras)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nome_val, 
            dados_dict.get('peso'), 
            dados_dict.get('altura'), 
            dados_dict.get('carga_horaria'), 
            dados_dict.get('salario'), 
            dados_dict.get('horas_extras')
        ))
        
    conn.commit()
    conn.close()
    atualizar_tabela() # Atualiza a tabela na tela imediatamente

def atualizar_tabela():
    """Busca os dados do banco e redesenha a tabela de histórico na tela"""
    for row in tabela.get_children():
        tabela.delete(row) # Limpa a tabela antes de recarregar
        
    conn = sqlite3.connect("sistema_calculos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, peso, altura, carga_horaria, salario, horas_extras FROM pessoas")
    
    for linha in cursor.fetchall():
        tabela.insert("", "end", values=linha) # Adiciona cada linha encontrada
    conn.close()

# ========================================================================================================================================================
# FUNÇÕES VINCULADAS AOS BOTÕES (LÓGICA)
# ========================================================================================================================================================

def run_imc():
    peso_ = float(peso.get())
    altura_ = float(altura.get())
    resultado = cl.imc(peso_, altura_)
    r = round(resultado, 2)
    
    # Envia os dados para salvar na tabela do banco
    salvar_no_banco({'peso': peso_, 'altura': altura_})
    return mostrar_imc.config(text=f"IMC: {r}") 

def run_calculo_h():
    carga_ = float(carga.get())
    salario_ = float(salario.get())
    resultado = cl.calculo_sal_hora(carga_, salario_)
    r = round(resultado, 2)
    
    # Envia os dados trabalhistas para salvar no banco
    salvar_no_banco({'carga_horaria': carga_, 'salario': salario_})
    return mostrar_sal.config(text=f"Valor por Hora: R$ {r}")

def run_extra():
    q = int(quantidade.get())
    carga_ = float(carga.get())
    salario_ = float(salario.get())
    resultado = cl.calculo_sal_hora(carga_, salario_)
    r = round(resultado, 2)
    rs = cl.calculo_quantidade_extra50(q, r)
    
    # Envia o pacote completo de informações trabalhistas incluindo as horas extras
    salvar_no_banco({'carga_horaria': carga_, 'salario': salario_, 'horas_extras': q})
    return mostrar_extra.config(text=f"Total Horas Extras: R$ {rs}")


# =========== Inicializando o Banco de Dados antes da Tela abrir =========
init_db()

# =================================================================================================
# CONFIGURAÇÃO DA JANELA DE USO
# =================================================================================================

janela = tk.Tk()
janela.title("Painel Integrado de Cálculos")
janela.geometry("600x500")
janela.configure(bg="#f8f9fa")

# Criando o gerenciador de abas (Notebook)
notebook = ttk.Notebook(janela)
notebook.pack(pady=15, padx=15, fill="both", expand=True)

# Instanciando os frames das 3 abas principais
aba_cadastro = ttk.Frame(notebook)
aba_imc = ttk.Frame(notebook)
aba_trabalho = ttk.Frame(notebook)

# Vinculando as abas criadas dentro do componente de abas
notebook.add(aba_cadastro, text="  Identificação / Histórico  ")
notebook.add(aba_imc, text="  Índice de Massa Corporal (IMC)  ")
notebook.add(aba_trabalho, text="  Cálculos Trabalhistas  ")

# ========================================================================================================================================================
# ABA 1: HISTÓRICO E IDENTIFICAÇÃO DO USUÁRIO
# ========================================================================================================================================================

aba_cadastro.grid_columnconfigure(1, weight=1) # Faz a coluna de inputs expandir

tk.Label(aba_cadastro, text="Identificação do Usuário", font=("Arial", 14, "bold"), fg="#212529").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 5))
tk.Label(aba_cadastro, text="Insira o nome para salvar ou atualizar os cálculos no banco de dados:", font=("Arial", 9, "italic"), fg="#6c757d").grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 15))

tk.Label(aba_cadastro, text="Nome Completo:", font=("Arial", 10, "bold"), fg="#495057").grid(row=2, column=0, sticky="w", padx=20, pady=5)
nome_cadastro = ttk.Entry(aba_cadastro, font=("Arial", 11))
nome_cadastro.grid(row=2, column=1, sticky="we", padx=(0, 20), pady=5)

# Configurando a Tabela de Visualização (Treeview)
colunas = ("nome", "peso", "altura", "carga", "salario", "extras")
tabela = ttk.Treeview(aba_cadastro, columns=colunas, show="headings", height=8)

tabela.heading("nome", text="Nome")
tabela.heading("peso", text="Peso (kg)")
tabela.heading("altura", text="Alt (m)")
tabela.heading("carga", text="Carga H.")
tabela.heading("salario", text="Salário")
tabela.heading("extras", text="H. Extras")

tabela.column("nome", width=140, anchor="w")
tabela.column("peso", width=60, anchor="center")
tabela.column("altura", width=60, anchor="center")
tabela.column("carga", width=70, anchor="center")
tabela.column("salario", width=80, anchor="e")
tabela.column("extras", width=60, anchor="center")

tabela.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
aba_cadastro.grid_rowconfigure(3, weight=1) # Faz a tabela usar o espaço vertical restante

# ========================================================================================================================================================
# ABA 2: CÁLCULO DO IMC
# ========================================================================================================================================================

aba_imc.grid_columnconfigure(1, weight=1)

tk.Label(aba_imc, text="Cálculo de IMC", font=("Arial", 14, "bold"), fg="#212529").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

tk.Label(aba_imc, text="Peso Atual (kg)", font=("Arial", 10), fg="#495057").grid(row=1, column=0, sticky="w", padx=20, pady=5)
peso = ttk.Entry(aba_imc, font=("Arial", 11))
peso.grid(row=1, column=1, sticky="we", padx=(0, 20), pady=5)

tk.Label(aba_imc, text="Altura (metros)", font=("Arial", 10), fg="#495057").grid(row=2, column=0, sticky="w", padx=20, pady=5)
altura = ttk.Entry(aba_imc, font=("Arial", 11))
altura.grid(row=2, column=1, sticky="we", padx=(0, 20), pady=5)

bt_imc = ttk.Button(aba_imc, text="Calcular e Salvar IMC", command=run_imc)
bt_imc.grid(row=3, column=0, columnspan=2, sticky="we", padx=20, pady=20)

mostrar_imc = tk.Label(aba_imc, text="", font=("Arial", 12, "bold"), fg="#2b8a3e")
mostrar_imc.grid(row=4, column=0, columnspan=2, pady=5)

# ========================================================================================================================================================
# ABA 3: CÁLCULOS TRABALHISTAS
# ========================================================================================================================================================

aba_trabalho.grid_columnconfigure(1, weight=1)

tk.Label(aba_trabalho, text="Análise de Horas e Salário", font=("Arial", 14, "bold"), fg="#212529").grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

tk.Label(aba_trabalho, text="Carga Mensal (Horas)", font=("Arial", 10), fg="#495057").grid(row=1, column=0, sticky="w", padx=20, pady=5)
carga = ttk.Entry(aba_trabalho, font=("Arial", 11))
carga.grid(row=1, column=1, sticky="we", padx=(0, 20), pady=5)

tk.Label(aba_trabalho, text="Salário Base (R$)", font=("Arial", 10), fg="#495057").grid(row=2, column=0, sticky="w", padx=20, pady=5)
salario = ttk.Entry(aba_trabalho, font=("Arial", 11))
salario.grid(row=2, column=1, sticky="we", padx=(0, 20), pady=5)

tk.Label(aba_trabalho, text="Qtd. Horas Extras", font=("Arial", 10), fg="#495057").grid(row=3, column=0, sticky="w", padx=20, pady=5)
quantidade = ttk.Entry(aba_trabalho, font=("Arial", 11))
quantidade.grid(row=3, column=1, sticky="we", padx=(0, 20), pady=5)

# Sub-container interno para alinhar os botões lado a lado
frame_botoes = ttk.Frame(aba_trabalho)
frame_botoes.grid(row=4, column=0, columnspan=2, sticky="we", padx=20, pady=15)
frame_botoes.columnconfigure(0, weight=1)
frame_botoes.columnconfigure(1, weight=1)

bt_sal = ttk.Button(frame_botoes, text="Calcular Salário/Hora", command=run_calculo_h)
bt_sal.grid(row=0, column=0, padx=(0, 5), sticky="we")

bt_ex = ttk.Button(frame_botoes, text="Calcular e Salvar Extra", command=run_extra)
bt_ex.grid(row=0, column=1, padx=(5, 0), sticky="we")

mostrar_sal = tk.Label(aba_trabalho, text="", font=("Arial", 10, "bold"), fg="#1864ab")
mostrar_sal.grid(row=5, column=0, columnspan=2, pady=2, sticky="w", padx=20)

mostrar_extra = tk.Label(aba_trabalho, text="", font=("Arial", 10, "bold"), fg="#e03131")
mostrar_extra.grid(row=6, column=0, columnspan=2, pady=2, sticky="w", padx=20)

# Executa a listagem da tabela pela primeira vez ao iniciar o aplicativo
atualizar_tabela()

# Mantém o aplicativo aberto
janela.mainloop()