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
        self.back_button = tk.Button(self, text="Αρχική", command=self.manager.show_main, 
                                     font=("Arial", 10, "bold"), bg="blue", fg='white', width=20)
        self.back_button.pack(pady=10)

        # 2. Labels τίτλου και συγγραφέα
        self.label_title = tk.Label(self, text="", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=10)

        self.label_authors = tk.Label(self, text="", font=("Arial", 12))
        self.label_authors.pack(pady=5)

        # 3. Εξώφυλλο βιβλίου
        self.label_cover = tk.Label(self)
        self.label_cover.pack(pady=10)

        # 4. Πλαίσιο Σχολίων (Αντικατάσταση Treeview με tk.Text)
        self.comments_frame = tk.Frame(self)
        self.comments_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Label για τίτλο πάνω από τα σχόλια
        tk.Label(self.comments_frame, text="Σχόλια Χρηστών", font=("Arial", 12, "bold")).pack(pady = 15)

        # Το Text widget με wrap="word" ώστε να κόβει το κείμενο στις λέξεις και όχι στα γράμματα
        self.text_comments = tk.Text(self.comments_frame, height=8, wrap="word", font=("Arial", 10), state="disabled")
        
        # Scrollbar για το Text widget
        self.scrollbar = ttk.Scrollbar(self.comments_frame, orient="vertical", command=self.text_comments.yview)
        self.text_comments.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.text_comments.pack(side="left", fill="both", expand=True)

    def load_book_info(self, book_id):
        book = self.manager.db_manager.get_book(book_id)
        ratings = self.manager.db_manager.get_ratings(book_id)
            
        self.label_title.config(text=book["title"])
        self.label_authors.config(text=f"Συγγραφέας: {book['authors']}")

        # Φόρτωση εικόνας
        path = book.get("cover_path")
        if path and os.path.exists(path):
            try:
                img = Image.open(path)
                img = img.resize((150, 220))
                self.photo = ImageTk.PhotoImage(img) # Αποθήκευση στο self.photo
                self.label_cover.config(image=self.photo, text="")
            except Exception:
                self.label_cover.config(image="", text="Σφάλμα φόρτωσης εικόνας", fg="red")
        else:
            self.label_cover.config(image="", text="Το εξώφυλλο δεν βρέθηκε\n(No Image)", font=("Arial", 10, "italic"), bg="lightgrey", width=20, height=10)


        # Κάνουμε ένα read-only Text widget για να εμφανίσουμε τα σχόλια
        self.text_comments.delete("1.0", tk.END)
        self.text_comments.config(state="normal")
        
        if not ratings:
            self.text_comments.insert(tk.END, "Δεν υπάρχουν σχόλια γιά το βιβλίο ακόμη.\n")
        else:
            for rating_data in ratings:
                # rating_data είναι λεξικό με τα κλειδιά: rating, comments, username
            
                rate_user = f"Βαθμολογία {rating_data['rating']}/5  από  {rating_data['username']}\n"
                user_comment = f"{rating_data['comments']}\n"
                
                self.text_comments.insert(tk.END, rate_user)
                self.text_comments.insert(tk.END, user_comment)
        #Disable το Text widget για να μην μπορεί ο χρήστης να πειράξει τα σχόλια
        self.text_comments.config(state="disabled")
        