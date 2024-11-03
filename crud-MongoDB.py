import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['Jannos']
collection = db['enderecos']  # Altere para a coleção que deseja realizar o crud

class CrudApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo CRUD")

        # Campo de entrada para ID
        tk.Label(root, text="ID").grid(row=0, column=0)
        self.entry_id = tk.Entry(root)
        self.entry_id.grid(row=0, column=1)

        # Campo de entrada para nome
        tk.Label(root, text="Nome").grid(row=1, column=0)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=1, column=1)

        # Botões
        tk.Button(root, text="Criar", command=self.create).grid(row=2, column=0)
        tk.Button(root, text="Ler", command=self.read).grid(row=2, column=1)
        tk.Button(root, text="Atualizar", command=self.update).grid(row=3, column=0)
        tk.Button(root, text="Deletar", command=self.delete).grid(row=3, column=1)

        # Campo de resultado
        self.result = tk.Text(root, height=10, width=50)
        self.result.grid(row=4, column=0, columnspan=2)

    def create(self):
        name = self.entry_name.get()
        if name:
            new_entry = {"_id": self.entry_id.get(), "name": name}
            collection.insert_one(new_entry)
            messagebox.showinfo("Info", "Documento criado com sucesso!")
            self.clear_entries()
        else:
            messagebox.showerror("Erro", "O nome não pode estar vazio!")

    def read(self):
        id_value = self.entry_id.get()
        if id_value:
            document = collection.find_one({"_id": id_value})
            if document:
                self.result.delete(1.0, tk.END)
                self.result.insert(tk.END, str(document))
            else:
                messagebox.showerror("Erro", "Documento não encontrado!")
        else:
            messagebox.showerror("Erro", "Informe um ID!")

    def update(self):
        id_value = self.entry_id.get()
        name = self.entry_name.get()
        if id_value and name:
            result = collection.update_one({"_id": id_value}, {"$set": {"name": name}})
            if result.matched_count > 0:
                messagebox.showinfo("Info", "Documento atualizado com sucesso!")
                self.clear_entries()
            else:
                messagebox.showerror("Erro", "Documento não encontrado!")
        else:
            messagebox.showerror("Erro", "ID e Nome não podem estar vazios!")

    def delete(self):
        id_value = self.entry_id.get()
        if id_value:
            result = collection.delete_one({"_id": id_value})
            if result.deleted_count > 0:
                messagebox.showinfo("Info", "Documento deletado com sucesso!")
                self.clear_entries()
            else:
                messagebox.showerror("Erro", "Documento não encontrado!")
        else:
            messagebox.showerror("Erro", "Informe um ID!")

    def clear_entries(self):
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.result.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudApp(root)
    root.mainloop()
