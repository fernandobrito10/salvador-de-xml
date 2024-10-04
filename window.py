import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

def selecionar_pasta():
    caminho_selecionado = filedialog.askdirectory()
    if caminho_selecionado:
        caminho_txt = os.path.join(os.path.expanduser('~'), 'caminho.txt')
        with open(caminho_txt, "w") as f:
            f.write(caminho_selecionado)
        
        # Ocultar o arquivo no Windows
        os.system(f'attrib +h "{caminho_txt}"')
        
        messagebox.showinfo("Sucesso", f"Caminho salvo!")
    else:
        messagebox.showwarning("Aviso", "Nenhuma pasta selecionada!")

# Criação da janela principal
root = tk.Tk()
root.title("Seleção de Pasta")
root.geometry("400x200")

# Botão para abrir o diálogo de seleção de pasta
botao = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
botao.pack(pady=20)

# Inicia o loop da aplicação
root.mainloop()
