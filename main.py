import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime


def criar_banco():
    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT NOT NULL,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        nota_max REAL NOT NULL,
        nota_min REAL NOT NULL,
        media REAL NOT NULL
    )
    """)
    conexao.commit()
    conexao.close()


def calcular_media(nota_max, nota_min):
    return (nota_max + nota_min) / 2


def validar_data(data_texto):
    try:
        data_formatada = datetime.strptime(data_texto, "%d/%m/%Y")
        return data_formatada.strftime("%d/%m/%Y")
    except ValueError:
        messagebox.showwarning("Erro", "Data de nascimento inválida! Use o formato DD/MM/AAAA.")
        return None


def limitar_caracteres(entry_texto, limite):
    if len(entry_texto.get()) > limite:
        entry_texto.set(entry_texto.get()[:limite])


def adicionar_aluno():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    data_nascimento = validar_data(entry_data_nascimento.get())
    nota_max = entry_nota_max.get()
    nota_min = entry_nota_min.get()


    try:
        nota_max = float(nota_max)
        nota_min = float(nota_min)
        media = calcular_media(nota_max, nota_min)
    except ValueError:
        messagebox.showwarning("Erro", "As notas devem ser numéricas.")
        return


    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO alunos (matricula, nome, cpf, data_nascimento, nota_max, nota_min, media)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (matricula, nome, cpf, data_nascimento, nota_max, nota_min, media))
    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Aluno adicionado!")
    limpar_campos()
    exibir_alunos()


def exibir_alunos():
    conexao = sqlite3.connect("alunos.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    conexao.close()

    listbox_alunos.delete(0, END)

    for aluno in alunos:
        listbox_alunos.insert(END, f"ID: {aluno[0]} | Matrícula: {aluno[1]} | Nome: {aluno[2]} | CPF: {aluno[3]} | Nascimento: {aluno[4]} | Nota Máx: {aluno[5]} | Nota Mín: {aluno[6]} | Média: {aluno[7]:.2f}")


def limpar_campos():
    entry_matricula.delete(0, END)
    entry_nome.delete(0, END)
    entry_cpf.delete(0, END)
    entry_data_nascimento.delete(0, END)
    entry_nota_max.delete(0, END)
    entry_nota_min.delete(0, END)


app = Tk()
app.title("Sistema de Cadastro de Notas")
app.geometry("500x500")


matricula_var = StringVar()
cpf_var = StringVar()

matricula_var.trace("w", lambda *args: limitar_caracteres(matricula_var, 12))
cpf_var.trace("w", lambda *args: limitar_caracteres(cpf_var, 11))


Label(app, text="Matrícula:").pack(pady=5)
entry_matricula = Entry(app, textvariable=matricula_var)
entry_matricula.pack(pady=5)

Label(app, text="Nome do Aluno:").pack(pady=5)
entry_nome = Entry(app)
entry_nome.pack(pady=5)

Label(app, text="CPF:").pack(pady=5)
entry_cpf = Entry(app, textvariable=cpf_var)
entry_cpf.pack(pady=5)

Label(app, text="Data de Nascimento (DD/MM/AAAA):").pack(pady=5)
entry_data_nascimento = Entry(app)
entry_data_nascimento.pack(pady=5)

Label(app, text="Nota Máxima:").pack(pady=5)
entry_nota_max = Entry(app)
entry_nota_max.pack(pady=5)

Label(app, text="Nota Mínima:").pack(pady=5)
entry_nota_min = Entry(app)
entry_nota_min.pack(pady=5)



btn_adicionar = Button(app, text="Adicionar Aluno", command=adicionar_aluno)
btn_adicionar.pack(pady=10)

Label(app, text="Alunos Cadastrados:").pack()

frame_lista = Frame(app)
frame_lista.pack(pady=5)


scrollbar = Scrollbar(frame_lista, orient=VERTICAL)
listbox_alunos = Listbox(frame_lista, width=70, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_alunos.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox_alunos.pack(side=LEFT, fill=BOTH)




criar_banco()
exibir_alunos()


app.mainloop()