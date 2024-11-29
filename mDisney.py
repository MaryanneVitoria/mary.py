import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Função para buscar dados do personagem da API
def buscar_personagem():
    url = "https://api.disneyapi.dev/character/18"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta exceção para status codes de erro
        
        data = response.json()
        
        # Extrair nome e filmes do personagem
        name = data['data']['name']
        films = data['data']['films']
        image_url = data['data']['imageUrl']
        
        # Atualizar os rótulos na janela
        label_nome.config(text=f"Personagem: {name}")
        
        # Exibir a lista de filmes
        if films:
            filmes_text = "\n".join(films)
        else:
            filmes_text = "Este personagem não aparece em nenhum filme."
        
        label_filmes.config(text=f"Filmes:\n{filmes_text}")
        
        # Exibir a imagem
        carregar_imagem(image_url)
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao acessar a API: {e}")

# Função para carregar e exibir a imagem do personagem
def carregar_imagem(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Carregar a imagem da URL
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        
        # Redimensionar a imagem para caber na interface
        image = image.resize((200, 200))  # Sem usar o Image.ANTIALIAS, que foi removido
        
        # Converter para um formato compatível com Tkinter
        img_tk = ImageTk.PhotoImage(image)
        
        # Atualizar o rótulo da imagem
        label_imagem.config(image=img_tk)
        label_imagem.image = img_tk  # Necessário manter a referência para não perder a imagem
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao carregar a imagem: {e}")

# Criar a janela principal
root = tk.Tk()
root.title("Disney Personagens")
root.geometry("400x500")

# Criar rótulos para exibir os dados
label_nome = tk.Label(root, text="Personagem: ", font=("Arial", 14))
label_nome.pack(pady=10)

label_filmes = tk.Label(root, text="Filmes:", font=("Arial", 12), justify=tk.LEFT)
label_filmes.pack(pady=10)

# Rótulo para exibir a imagem
label_imagem = tk.Label(root)
label_imagem.pack(pady=20)

# Botão para buscar os dados do personagem
btn_buscar = tk.Button(root, text="Buscar Personagem", command=buscar_personagem)
btn_buscar.pack(pady=20)

# Iniciar o loop da janela
root.mainloop()
