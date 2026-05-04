import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class BookDetailsScreen(tk.Frame): 
    def __init__(self, parent, manager): 
        super().__init__(parent)
        self.manager = manager 
        
        # Καλούμε τα γραφικά στοιχεία ΜΙΑ φορά στην αρχή
        self.create_widgets()

    def create_widgets(self):
        # 1. Κουμπί επιστροφής στην αρχική οθόνη
        self.back_button = tk.Button(self, text="⬅ Πίσω", command=self.manager.show_main, font=("Arial", 10, "bold"), bg="lightgray")
        self.back_button.pack(anchor="nw", pady=5, padx=5)

        # 2. Labels τίτλου και συγγραφέα (αρχικά κενά, θα γεμίζουν δυναμικά)
        self.label_title = tk.Label(self, text="", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=10)

        self.label_authors = tk.Label(self, text="", font=("Arial", 12))
        self.label_authors.pack(pady=5)

        # 3. Εξώφυλλο βιβλίου
        self.label_cover = tk.Label(self)
        self.label_cover.pack(pady=10)

        # 4. Λίστα σχολίων (Σε δικό του Frame για να μπει σωστά το Scrollbar)
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree_comments = ttk.Treeview(self.tree_frame, columns="comment", show="headings", height=5)
        self.tree_comments.heading("comment", text="Σχόλια Χρηστών")
        self.tree_comments.column("comment", width=400, anchor="w")

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree_comments.yview)
        self.tree_comments.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.tree_comments.pack(side="left", fill="both", expand=True)

    def load_book_info(self, book_id):
        """Αυτή η μέθοδος καλείται από τον Manager και φορτώνει τα δεδομένα του συγκεκριμένου βιβλίου"""
        
        # ---- ΠΡΟΣΩΡΙΝΑ DEMO DATA (Αργότερα θα έρχονται από τη βάση π.χ. self.manager.db.get_book(book_id) ) ----
        book = {
            "title": "Η μεγάλη χίμαιρα",
            "authors": "Μ.Καραγάτσης",
            "cover_path": None
        }
        
        ratings = [
            {"username": "Giannis", "rating": 5, "comment": "Εξαιρετικό!"},
            {"username": "Vasilis", "rating": 4, "comment": "Αρκετά καλό"}
        ]
        # ---------------------------------------------------------------------------------------------------

        # Ενημέρωση των κειμένων με τα νέα δεδομένα
        self.label_title.config(text=book["title"])
        self.label_authors.config(text=f"Συγγραφέας: {book['authors']}")

        # Φόρτωση εικόνας
        path = book.get("cover_path")
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                img = img.resize((150, 220))
                self.photo = ImageTk.PhotoImage(img) # Η μεταβλητή πρέπει να είναι στο self.photo για να μην διαγραφεί!
                self.label_cover.config(image=self.photo, text="")
            except Exception:
                self.label_cover.config(image="", text="Σφάλμα φόρτωσης εικόνας", fg="red")
        else:
            self.label_cover.config(image="", text="Το εξώφυλλο δεν βρέθηκε\n(No Image)", font=("Arial", 10, "italic"), bg="lightgrey", width=20, height=10)

        # Καθαρισμός του πίνακα από παλιά σχόλια (αν υπήρχαν) πριν βάλουμε τα νέα
        for item in self.tree_comments.get_children():
            self.tree_comments.delete(item)

        # Φόρτωση νέων σχολίων στο Treeview
        for r in ratings:
            display_text = f"⭐ {r['rating']}/5 - {r['username']}: {r['comment']}"
            self.tree_comments.insert("", "end", values=(display_text,))

        