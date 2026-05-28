import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import os


class BookDetailsWindow(tk.Toplevel):
    def __init__(self,master,):#αλλαγή στο μέλλον θα μπει μια παράμετρος book_data που θα λαβάνει από το main_window
        super().__init__(master)

       
        self.title("Λεπτομέρειες")  
        self.geometry("500x600")

        #----ΠΡΟΣΩΡΙΝΑ DEMO DATA----
        #To self.book θα παίρνει από το book_data
        self.book = {"title": "Η μεγάλη χίμαιρα",
                     "authors": "Μ.Καραγάτσης",
                     "cover_path": None}
        #τα ratings θα έρχονται από το api
        self.ratings = [
            {"username": "Giannis", "rating": 5, "comment": "Εξαιρετικό!"},
            {"username": "Vasilis", "rating": 4, "comment": "Αρκετά καλό"}
        ]
        self.create_widgets()

    def create_widgets(self):

        #Δημιουργία widgets τίτλος και συγγραφέας
        self.label_title=tk.Label(self, text=self.book["title"], font=("arial", 18,"bold"))
        self.label_title.pack(pady=15)

        self.label_authors=tk.Label(self.master, text=f"Συγγραφέας:{self.book['authors']}", font= ("Arial", 12))
        self.label_authors.pack(pady=5)

        #Το cover_path θα περιέχει την πλήρη διαδρομή τοπικά ή URL
        path = self.book.get("cover_path")

        #Έλγχος αν υπάρχει διαδρομή  και αρχείο για να μην κρασάρει
        if path and os.path.exists(path):
            try:
                img= Image.open(path)
                img= img.resize((150, 220))
                self.photo = ImageTk.PhotoImage(img)
                self.label_cover = tk.Label(self, image=self.photo)
            except Exception:#έλεγχος αν η εικονα υπάρχει αλλά είναι κατεσταμμέν
                self.label_cover = tk.Label(self, text="Σφάλμα δόρτωσης εικόνας", fg="red")

        else: #Αν το αρχείο δεν υπάρχει
            self.label_cover = tk.Label(self, text = "Το εξώφυλλο δεν βρέθηκε", font=("arial", 10, "italic"), bg="lightgrey", width=20, height=10)
        
        self.label_cover.pack(pady=10)

      
        #Λίστα σχολίων Treeview
        self.tree_comments= ttk.Treeview(self,columns="comment", show="headings", height=5 )
        self.tree_comments.heading("comment", text="Σχόλια Χρηστών")
        self.tree_comments.column("comment", width=400, anchor="w")

        self.scrollbar=ttk.Scrollbar(self, orient="vertical", command=self.tree_comments.yview)
        self.tree_comments.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree_comments.pack(pady=10, padx=10, fill="both", expand=True)

        #Φόρτωση σχολίων από Demo Data
        for r in self.ratings:
            display_text = f"⭐ {r['rating']}/5 - {r['username']}: {r['comment']}"
            self.tree_comments.insert("", "end", values=(display_text,))


if __name__ == "__main__":
    root = tk.Tk()    
    root.withdraw()       
    app= BookDetailsWindow(root)
    root.mainloop()        