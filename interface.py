import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, ttk, filedialog

candidatos = []
votacao_ativa = False

COR_FUNDO = "#505050"
COR_TEXTO = "white"
FONTE_PADRAO = ("Helvetica", 12)

janela = tk.Tk()
style = ttk.Style()


style.theme_use("vista") 

# Criando um estilo personalizado chamado "Custom.TButton"
style.configure("Custom.TButton",
    background = COR_FUNDO,
    foreground = "#901010",
    font = ("Helvetica", 10),
    padding = 5
)

# Para corrigir o hover e o click (porque ttk sobrescreve)
style.map("Custom.TButton",
    background = [("active", "#707070"), ("pressed", "#404040")]
)

style.configure("TLabel", background = COR_FUNDO, foreground = COR_TEXTO, font = ("Helvetica", 12))

style.configure("TFrame", background="#8F8F8F")



def mostrar_menu():

    janela.title("Sistema de Votação")
    janela.geometry("400x350")
    janela.configure(padx = 20, pady = 20, bg = COR_FUNDO)

    label_menu = ttk.Label(janela, text = "Escolha Uma Opção:")
    label_menu.pack(pady = 20)

    ttk.Button(janela, text = "📝 Cadastro de Candidato", style = "Custom.TButton", command = cadastra_candidato).pack(pady = 5)
    ttk.Button(janela, text = "📝 Lista de Candidatos", style = "Custom.TButton", command = lista_candidatos).pack(pady = 5)
    ttk.Button(janela, text = "🗳️ Iniciar Votação", style = "Custom.TButton", command = iniciar_votacao).pack(pady = 5)
    ttk.Button(janela, text = "📊 Encerrar Votação", style = "Custom.TButton", command = encerrar_votacao).pack(pady = 5)

    status_bar = ttk.Label(janela, text="Sistema de votação - desenvolvido em Python", anchor="center")
    status_bar.pack(side="bottom", fill="x", pady=5)

def cadastra_candidato():
    janela_cadastro = tk.Toplevel(janela)
    janela_cadastro.title("Cadastro de Candidato")
    janela_cadastro.geometry("400x400")
    janela_cadastro.configure(padx = 20, pady = 20, bg=COR_FUNDO)
    
    imagem_caminho = tk.StringVar()

    ttk.Label(janela_cadastro, text = "Número do Candidato:").pack(pady = 5)
    entrada_numero = ttk.Entry(janela_cadastro)
    entrada_numero.pack(pady = 5)

    ttk.Label(janela_cadastro, text = "Nome do Candidato").pack(pady = 5)
    entrada_nome = ttk.Entry(janela_cadastro)
    entrada_nome.pack(pady = 5)

    ttk.Label(janela_cadastro, text = "Partido do Candidato").pack(pady = 5)
    entrada_partido = ttk.Entry(janela_cadastro)
    entrada_partido.pack(pady = 5)

    def selecionar_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png *.jpg *.jpeg *.gif")]
        )
        if caminho:
            imagem_caminho.set(caminho)
            ttk.Label(janela_cadastro, text="Imagem selecionada").pack()

    ttk.Button(janela_cadastro, text="Selecionar Imagem", style="Custom.TButton", command=selecionar_imagem).pack(pady=5)

    def salvar_candidato():
        numero = entrada_numero.get()
        nome = entrada_nome.get()
        partido = entrada_partido.get()
        imagem = imagem_caminho.get()

        if not numero.isdigit() or not nome or not partido or not imagem:
            messagebox.showwarning("Erro", "Preencha todos os campos corretamente.")
            return
        elif any(c["numero"] == numero for c in candidatos):
            messagebox.showwarning("Erro", "Número de candidato já cadastrado.")
            return
        
        candidatos.append({
            "numero": numero,
            "nome": nome,
            "partido": partido,
            "imagem": imagem,
            "votos": 0
        })
        messagebox.showinfo("Sucesso", "Candidato cadastrado com sucesso!")

    ttk.Button(janela_cadastro, text = "Fechar", style = "Custom.TButton", command =  janela_cadastro.destroy ).pack(side="bottom", pady = 5)
    ttk.Button(janela_cadastro, text = "Salvar", style = "Custom.TButton", command = salvar_candidato).pack(side="bottom", pady = 5)



def iniciar_votacao():
    global votacao_ativa
    votacao_ativa = True
    registrar_voto()

def registrar_voto():
    if votacao_ativa:
        janela_votacao = tk.Toplevel(janela)
        janela_votacao.title("Votação")
        janela_votacao.geometry("400x300")
        janela_votacao.configure(padx = 20, pady = 20, bg = COR_FUNDO)
        
        ttk.Label(janela_votacao, text = "Digite sua matricula:").pack(pady = 5)
        entrada_matricula = ttk.Entry(janela_votacao)
        entrada_matricula.pack(pady = 5)

        ttk.Label(janela_votacao, text = "Digite o número do candidato:").pack(pady = 5)
        entrada_voto = ttk.Entry(janela_votacao)
        entrada_voto.pack(pady = 5)

        def confirmar_voto():
            matricula = entrada_matricula.get()
            voto = entrada_voto.get()
            matriculas_votaram = set()

            if not matricula:
                messagebox.showwarning("Erro", "Matricula não pode ser vazia.")
                return
            
            elif matricula in matriculas_votaram:
                messagebox.showwarning("Erro", "Esta matrícula já votou.")
                return
            
            matriculas_votaram.add(matricula)
            
            candidato_escolhido = next((c for c in candidatos if c["numero"] == voto), None)
            if candidato_escolhido:
                confirmar = messagebox.askyesno("Confirmação", f"Confirmar voto para {candidato_escolhido['nome']} ({candidato_escolhido['partido']})?")
                if confirmar:
                    candidato_escolhido["votos"] += 1
                    messagebox.showinfo("Sucesso", "Voto registrado com sucesso")
                    janela_votacao.destroy()
                    registrar_voto()

            else:
                confirmar = messagebox.askyesno("Confirmação", "Candidato inexistente. Confirmar voto nulo?")
                if confirmar:
                    messagebox.showinfo("Sucesso", "Voto nulo registrado!")
                    janela_votacao.destroy()
                    registrar_voto()

        
        botao_retornar = ttk.Button(janela_votacao, text = "Fechar", style="Custom.TButton", command =janela_votacao.destroy )
        botao_retornar.pack(side="bottom", pady = 5)

        botao_votar = ttk.Button(janela_votacao, text = "Votar ", style="Custom.TButton", command = confirmar_voto)
        botao_votar.pack(side="bottom", pady = 5)


def lista_candidatos():
    janela_lista = tk.Toplevel(janela)
    janela_lista.title("Resultados")
    janela_lista.geometry("400x400")
    janela_lista.configure(padx = 20, pady = 20, bg = COR_FUNDO)

    frame_menu = ttk.Frame(janela_lista)
    frame_menu.pack(expand=True)

    if candidatos:
        imagens_referencias = []  # Para evitar que o garbage collector remova as imagens

        for candidato in sorted(candidatos, key=lambda c: c["votos"], reverse=True):
            # Carregar a imagem
            try:
                imagem_original = Image.open(candidato["imagem"])
            except:
                imagem_original = Image.open("imagem_exemplo.png")

            imagem_redimensionada = imagem_original.resize((100, 80))
            imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
            imagens_referencias.append(imagem_tk)  # Manter referência

            label_imagem = tk.Label(frame_menu, image=imagem_tk, background=COR_FUNDO)
            label_imagem.pack(pady=5)

            ttk.Label(frame_menu, text=f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos").pack(pady=5)

        janela_lista.imagens = imagens_referencias  # Armazena a lista na janela para manter viva

    else:
        ttk.Label(frame_menu, text="Não há Candidatos cadastrados no momento.").pack(pady=5)

def imprime_relatorio():
    janela_relatorio = tk.Toplevel(janela)
    janela_relatorio.title("Resultados")
    janela_relatorio.geometry("400x300")
    janela_relatorio.configure(padx = 20, pady = 20, bg = COR_FUNDO)

    frame_menu = ttk.Frame(janela_relatorio)
    frame_menu.pack(expand=True)

    total_votos = sum(c["votos"] for c in candidatos)
    

    if total_votos > 0:
        for candidato in sorted(candidatos, key = lambda c: c["votos"], reverse = True):
            ttk.Label(frame_menu, text=f"{candidato['nome']} ({candidato['partido']}):{candidato['votos']} votos").pack(pady=5)
            

    else:
        ttk.Label(frame_menu, text="Não houve votos válidos.").pack(pady=5)

    def importar():
        linhas_relatorio = []

        if total_votos > 0:
            for candidato in sorted(candidatos, key = lambda c: c["votos"], reverse = True):
                texto = f"{candidato['nome']} ({candidato['partido']}): {candidato['votos']} votos"
                linhas_relatorio.append(texto)
        try:
            with open("relatorio.txt", "w", encoding="utf-8") as arquivo:
                for linha in linhas_relatorio:
                    arquivo.write(linha + "\n")
            ttk.Label(janela_relatorio, text="Relatório salvo como 'relatorio.txt'").pack(pady=10)
        except Exception as e:
            ttk.Label(janela_relatorio, text=f"Erro ao salvar arquivo: {e}").pack(pady=10)

    botao_fechar = ttk.Button(janela_relatorio, text = "Fechar", style = "Custom.TButton", command = janela_relatorio.destroy)
    botao_fechar.pack(side="bottom", pady = 5)

    botao_importar = ttk.Button(janela_relatorio, text = "Importar arquivos", style = "Custom.TButton", command = importar)
    botao_importar.pack(side="bottom", pady = 5)

def encerrar_votacao():
    global votacao_ativa
    votacao_ativa = False
    imprime_relatorio()

mostrar_menu()
janela.mainloop()