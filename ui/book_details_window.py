import tkinter as tk
from tkinter import ttk
from PIL import Image  # Κρατάμε μόνο το Image, σβήσαμε το ImageTk (Lint Fix)
import os
from tkinter import messagebox
import customtkinter as ctk
from services.rating_service import save_rating
from api.covers import download_cover

class BookDetailsWindow(ctk.CTkFrame):
    def __init__(self, master, book_data, on_save):
        super().__init__(master, fg_color="transparent")
        self.book = book_data.get("book", {})
        self.ratings = book_data.get("ratings", [])
        self.on_save = on_save
        
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)

        # Κουμπί επιστροφής
        self.btn_back = ctk.CTkButton(self, text="< Επιστροφή", width=100, command=self.go_back, fg_color="gray40", hover_color="gray30")
        self.btn_back.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Τίτλος και Συγγραφέας
        self.label_title = ctk.CTkLabel(self, text=self.book.get("title", "Άγνωστος Τίτλος"), font=("arial", 18, "bold"))
        self.label_title.grid(row=1, column=0, pady=(10, 15))

        self.label_authors = ctk.CTkLabel(self, text=f"Συγγραφέας: {self.book.get('authors', 'Άγνωστος')}", font=("Arial", 12))
        self.label_authors.grid(row=2, column=0, pady=5)

        print("--- ΔΕΔΟΜΕΝΑ ΠΟΥ ΕΦΤΑΣΑΝ ΣΤΙΣ ΛΕΠΤΟΜΕΡΕΙΕΣ ---")
        print(self.book)
        
        # --- ΦΟΡΤΩΣΗ ΕΙΚΟΝΑΣ ΕΞΩΦΥΛΛΟΥ (Απόλυτο Μονοπάτι) ---
        cover_path = self.book.get("cover_img")
        image_loaded = False

        if cover_path:
            absolute_cover_path = os.path.abspath(cover_path)
            if os.path.exists(absolute_cover_path):
                try:
                    pil_img = Image.open(absolute_cover_path)
                    # CTkImage με τις σωστές διαστάσεις του cover.py (128x192)
                    self.cover_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(128, 192))
                    
                    self.label_cover = ctk.CTkLabel(self, text="", image=self.cover_image)
                    image_loaded = True
                except Exception as e:
                    print(f"Σφάλμα φόρτωσης τοπικής εικόνας: {e}")

        if not image_loaded:
            # Καλαίσθητο placeholder αν δεν βρεθεί η εικόνα
            self.label_cover = ctk.CTkLabel(
                self, 
                text="📘\nΔεν βρέθηκε\nεξώφυλλο", 
                font=("arial", 12, "italic"), 
                width=128, 
                height=192, 
                fg_color="#2b2b2b", 
                corner_radius=10
            )

        self.label_cover.grid(row=3, column=0, pady=10)

        # Container για τα σχόλια
        self.comments_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.comments_frame.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)
        self.comments_frame.grid_columnconfigure(0, weight=1)

        # Ρύθμιση χρωμάτων για το Treeview (Dark Mode Fix)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2a2a",
                        foreground="white",
                        fieldbackground="#2a2a2a",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#333333",
                        foreground="white",
                        font=("arial", 11, "bold"))

        # Λίστα σχολίων Treeview
        self.tree_comments = ttk.Treeview(self.comments_frame, columns="comment", show="headings", height=5)
        self.tree_comments.heading("comment", text="Σχόλια Χρηστών")
        self.tree_comments.column("comment", width=400, anchor="w")

        self.scrollbar = ttk.Scrollbar(self.comments_frame, orient="vertical", command=self.tree_comments.yview)
        self.tree_comments.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_comments.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        # Σωστά widgets αξιολόγησης με GRID
        self.lbl_your_rating = ctk.CTkLabel(self, text="Η αξιολόγησή σου:", font=("arial", 12, "bold"))
        self.lbl_your_rating.grid(row=5, column=0, pady=(20, 5))

        self.combo_rating = ttk.Combobox(self, values=["1", "2", "3", "4", "5"], state="readonly")
        self.combo_rating.grid(row=6, column=0, pady=5)

        self.lbl_comment = ctk.CTkLabel(self, text="Σχόλιο:", font=("arial", 11))
        self.lbl_comment.grid(row=7, column=0, pady=(10, 0))

        self.text_comment = ctk.CTkTextbox(self, height=80, width=400)
        self.text_comment.grid(row=8, column=0, pady=5, padx=10)

        self.save_button = ctk.CTkButton(self, text="Αποθήκευση", command=self.handle_save, fg_color="#4CAF50", hover_color="#45a049", text_color="white")
        self.save_button.grid(row=9, column=0, pady=15)

        # Φόρτωση σχολίων με υποστήριξη για Dict (με/χωρίς s) και Tuple
        print("--- DEBUG RATINGS DATA ---")
        for r in self.ratings:
            print("DATA TYPE CHECK:", type(r), "->", r)
            
            if isinstance(r, dict):
                rating_val = r.get('rating', 0)
                username = r.get('username', 'Άγνωστος')
                comment_text = r.get('comments', r.get('comment', ''))
            
            elif isinstance(r, (list, tuple)):
                rating_val = r[2] if len(r) > 2 else 0
                username = f"Χρήστης #{r[1]}" if len(r) > 1 else "Άγνωστος"
                comment_text = r[3] if len(r) > 3 else ''
            
            else:
                continue

            display_text = f"⭐ {rating_val}/5 - {username}: {comment_text}"
            self.tree_comments.insert("", "end", values=(display_text,))

    def handle_save(self):
        rating = self.combo_rating.get()
        comment = self.text_comment.get("1.0", "end").strip()

        if not rating:
            messagebox.showwarning("Προσοχή", "Παρακαλώ επιλέξτε βαθμολογία!")
            return
            
        book_id = self.book.get('book_id')
        
        # Έλεγχος Συνεδρίας Χρήστη (High Severity Copilot Fix)
        if not hasattr(self.master, 'current_user') or not self.master.current_user:
            messagebox.showerror("Σφάλμα", "Δεν βρέθηκε ενεργή συνεδρία χρήστη. Παρακαλώ συνδεθείτε ξανά.")
            return
            
        user_id = self.master.current_user.get('id')
        if not user_id:
            messagebox.showerror("Σφάλμα", "Το ID του χρήστη δεν είναι έγκυρο. Η αποθήκευση ακυρώθηκε.")
            return
        
        try:
            save_rating(user_id, book_id, int(rating), comment)
            messagebox.showinfo("Επιτυχία", "Η αξιολόγησή σου αποθηκεύτηκε!")
            self.text_comment.delete("1.0", "end")
            
            if self.on_save:
                self.on_save()

        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Δεν μπόρεσε να αποθηκευτεί: {e}")

    def go_back(self):
        print("Επιστροφή στην αρχική οθόνη!")
        self.destroy()
        if hasattr(self.master, 'show_main_screen'):
            self.master.show_main_screen()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    test_book = {"book": {"book_id": 1, "title": "Test Book", "authors": "Test Author"}}
    def test_refresh(): print("Refresh callback triggered!")
    app = BookDetailsWindow(root, book_data=test_book, on_save=test_refresh)
    root.mainloop()