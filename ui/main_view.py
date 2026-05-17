import tkinter as tk
from tkinter import messagebox


class MainScreen(tk.Frame):

    def __init__(self, parent, manager):
        super().__init__(parent)
        #ΑΠΟΘΗΚΕΥΟΜΕ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ (Manager) ΓΙΑ ΝΑ ΤΟΝ ΕΧΕΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΣΤΗ ΜΝΗΜΗ ΤΟΥ ΚΑΙ ΝΑ ΤΟΥ ΔΙΝΕΙ ΕΝΤΟΛΕΣ ΑΡΓΟΤΕΡΑ
        self.manager = manager 
        
        self.const = tk.Label(self, text = "", font=("Courier", 16, "bold")).pack(pady=20)

        Logout_button = tk.Button(self, text = "Logout", command=manager.show_login, bg='blue', fg='white').pack(side="bottom",pady=20)
        Add_book_button = tk.Button(self, text="Add book", command=manager.show_add, bg='purple', fg='white').pack(side="top",pady=20)