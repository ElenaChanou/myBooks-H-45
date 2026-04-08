import tkinter as tk
from tkinter import messagebox

class BookDetailsScreen(tk.Frame):
    '''Η κλάση BookDetailsScreen είναι ενα Tkinter Frame...'''
    def __init__(self, parent, manager):
        super().__init__(parent)
        #ΑΠΟΘΗΚΕΥΟΜΕ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ (Manager) ΓΙΑ ΝΑ ΤΟΝ ΕΧΕΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΣΤΗ ΜΝΗΜΗ ΤΟΥ ΚΑΙ ΝΑ ΤΟΥ ΔΙΝΕΙ ΕΝΤΟΛΕΣ ΑΡΓΟΤΕΡΑ
        self.manager = manager 
        BookDetailsButton = tk.Label(self, text="Book Details", font=("Arial", 20), bg="lightcoral").pack(pady=30)
        MainButton = tk.Button(self, text = "Back to main", command = manager.show_main)
        MainButton.pack()

        