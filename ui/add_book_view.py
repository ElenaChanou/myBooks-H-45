import tkinter as tk
from tkinter import messagebox

class AddBookScreen(tk.Frame):
    '''Η κλάση AddBookScreen είναι ενα Tkinter Frame...'''
    def __init__(self, parent, manager):
        super().__init__(parent)
        #ΑΠΟΘΗΚΕΥΟΜΕ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ (Manager) ΓΙΑ ΝΑ ΤΟΝ ΕΧΕΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΣΤΗ ΜΝΗΜΗ ΤΟΥ ΚΑΙ ΝΑ ΤΟΥ ΔΙΝΕΙ ΕΝΤΟΛΕΣ ΑΡΓΟΤΕΡΑ
        self.manager = manager 
        AddButton = tk.Button(self, text="Add book", font= ("Courier", 10), bg = "yellow").place(x=600 , y=200)
        MainButton = tk.Button(self, text = "Back to main", command = manager.show_main)
        MainButton.pack()