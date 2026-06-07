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
        # Αρχικοποιούμε το Frame και το κάνουμε διάφανο για να ταιριάζει με το κεντρικό παράθυρο
        super().__init__(master, fg_color="transparent")

        # Εξάγουμε τα δεδομένα του βιβλίου και τις αξιολογήσεις από το λεξικό που μας ήρθε
        # Χρησιμοποιούμε get() με default τιμές ({} και []) για να μην κρασάρει αν λείπουν τα κλειδιά.
        self.book = book_data.get("book", {})
        self.ratings = book_data.get("ratings", [])
        # Αποθηκεύουμε τη συνάρτηση (callback) που θα κληθεί όταν ο χρήστης σώσει μια νέα αξιολόγηση, 
        # ώστε να ανανεωθεί ο κεντρικός πίνακας αν χρειάζεται.
        self.on_save = on_save
        
        self.create_widgets()

    def create_widgets(self):
        # Δίνουμε βάρος  στη στήλη 0, ώστε τα στοιχεία να στοιχίζονται στο κέντρο ομοιόμορφα
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
        
        # φόρτωση εικόνας εξωφύλλου
        cover_path = self.book.get("cover_img")
        image_loaded = False# Μεταβλητή ελέγχου για το αν βρέθηκε και φορτώθηκε η εικόνα επιτυχώς

        if cover_path:
            # Μετατρέπουμε το μονοπάτι σε απόλυτο για να είμαστε σίγουροι ότι η Python θα το βρει
            absolute_cover_path = os.path.abspath(cover_path)
            if os.path.exists(absolute_cover_path):
                try:
                    # Ανοίγουμε την εικόνα με τη βιβλιοθήκη PIL
                    pil_img = Image.open(absolute_cover_path)
                   # Δημιουργούμε το CTkImage βάζοντας ακριβώς τις διαστάσεις (128x192) που χρησιμοποιεί το api
                    self.cover_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(128, 192))
                    
                    self.label_cover = ctk.CTkLabel(self, text="", image=self.cover_image)
                    image_loaded = True
                except Exception as e:
                    print(f"Σφάλμα φόρτωσης τοπικής εικόνας: {e}")
        # Αν δεν υπήρχε cover_path ή αν έγινε σφάλμα στη φόρτωση, δημιουργούμε ένα όμορφο Placeholder
        if not image_loaded:
            
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

        # Περιγραφή Βιβλίου
        # Φτιάχνουμε ένα Textbox για να χωράει πολλές γραμμές
        self.desc_textbox = ctk.CTkTextbox(self, height=80, width=600, wrap="word", fg_color="transparent")
        self.desc_textbox.grid(row=4, column=0, pady=(10, 10), padx=20)
        
        # Διαβάζουμε την περιγραφή (με get() για να μην κρασάρει αν δεν υπάρχει)
        description_text = self.book.get("description", "")
        if not description_text:  # Αν είναι None ή κενό
            description_text = "Δεν υπάρχει διαθέσιμη περιγραφή για αυτό το βιβλίο."
            
        # Βάζουμε το κείμενο μέσα
        self.desc_textbox.insert("0.0", description_text)
        
        # Το κλειδώνουμε(disabled) για να μην μπορεί ο χρήστης να το σβήσει!
        self.desc_textbox.configure(state="disabled")

        # Container για τα σχόλια
        self.comments_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.comments_frame.grid(row=5, column=0, sticky="nsew", pady=10, padx=10)
        self.comments_frame.grid_columnconfigure(0, weight=1)

       # Ρύθμιση χρωμάτων για το Treeview για να υποστηρίζει σωστά το Dark Mode
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

        # Μπάρα κύλισης για τα σχόλια
        self.scrollbar = ttk.Scrollbar(self.comments_frame, orient="vertical", command=self.tree_comments.yview)
        self.tree_comments.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_comments.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        #περιοχή αξιολόγησης
        self.lbl_your_rating = ctk.CTkLabel(self, text="Η αξιολόγησή σου:", font=("arial", 12, "bold"))
        self.lbl_your_rating.grid(row=6, column=0, pady=(20, 5))

        #Μενού επιλογής (Combobox) από 1 έως 5. Το state="readonly" δεν αφήνει τον χρήστη να πληκτρολογήσει γράμματα
        self.combo_rating = ttk.Combobox(self, values=["1", "2", "3", "4", "5"], state="readonly")
        self.combo_rating.grid(row=7, column=0, pady=5)

        self.lbl_comment = ctk.CTkLabel(self, text="Σχόλιο:", font=("arial", 11))
        self.lbl_comment.grid(row=8, column=0, pady=(10, 0))

        # Textbox ώστε ο χρήστης να μπορεί να γράψει παράγραφο
        self.text_comment = ctk.CTkTextbox(self, height=80, width=400)
        self.text_comment.grid(row=9, column=0, pady=5, padx=10)

        self.save_button = ctk.CTkButton(self, text="Αποθήκευση", command=self.handle_save, fg_color="#4CAF50", hover_color="#45a049", text_color="white")
        self.save_button.grid(row=10, column=0, pady=15)

        #Φόρτωση παλιών σχολίων στον πίνακα
        print("--- DEBUG RATINGS DATA ---")
        for r in self.ratings:
            print("DATA TYPE CHECK:", type(r), "->", r)
            
            # Έλεγχος Α: Αν τα δεδομένα ήρθαν ως Λεξικό
            if isinstance(r, dict):
                rating_val = r.get('rating', 0)
                username = r.get('username', 'Άγνωστος')
                # Δοκιμάζουμε και 'comments' και 'comment' για ασφάλεια
                comment_text = r.get('comments', r.get('comment', ''))

            # Έλεγχος Β: Αν τα δεδομένα ήρθαν ως Λίστα ή Πλειάδα με απευθείας ερώτημα SQL
            elif isinstance(r, (list, tuple)):
                rating_val = r[2] if len(r) > 2 else 0
                username = f"Χρήστης #{r[1]}" if len(r) > 1 else "Άγνωστος"
                comment_text = r[3] if len(r) > 3 else ''
            # Αν τα δεδομένα δεν είναι τίποτα από τα παραπάνω,, αγνοούμε και πάμε στο επόμενο
            else:
                continue
            # Μορφοποίηση και εισαγωγή στον πίνακα
            display_text = f"👤 {username}      |     ⭐ {rating_val}/5:  {comment_text}"
            self.tree_comments.insert("", "end", values=(display_text,))

    def handle_save(self):
        #Παίρνουμε τα δεδομένα από το combobox και το Textbox
        rating = self.combo_rating.get()
        comment = self.text_comment.get("1.0", "end").strip() #To "1.0" σημαίνει ότι ξεκινάει από τη γραμμή 0, χαρακτήρας 1, μέχρι το τέλος

        # Υποχρεωτικός έλεγχος για βαθμολογία
        if not rating:
            messagebox.showwarning("Προσοχή", "Παρακαλώ επιλέξτε βαθμολογία!")
            return
            
        book_id = self.book.get('book_id')
        
        # --- ΕΛΕΓΧΟΣ ΣΥΝΕΔΡΙΑΣ (SESSION CHECK) ---
        # Ελέγχουμε αν υπάρχει το αντικείμενο 'current_user' στο master (στο κεντρικό παράθυρο)
        # Αυτό αποτρέπει την προσθήκη σχολίων αν ο χρήστης δεν έχει κάνει Login.

        if not hasattr(self.master, 'current_user') or not self.master.current_user:
            messagebox.showerror("Σφάλμα", "Δεν βρέθηκε ενεργή συνεδρία χρήστη. Παρακαλώ συνδεθείτε ξανά.")
            return
            
        user_id = self.master.current_user.get('id')
        # Επιπλέον έλεγχος ασφαλείας για σωστό ID
        if not user_id:
            messagebox.showerror("Σφάλμα", "Το ID του χρήστη δεν είναι έγκυρο. Η αποθήκευση ακυρώθηκε.")
            return
        # Προσπάθεια αποθήκευσης μέσω του Rating Service
        try:
            save_rating(user_id, book_id, int(rating), comment)
            messagebox.showinfo("Επιτυχία", "Η αξιολόγησή σου αποθηκεύτηκε!")
            # Καθαρίζουμε το κουτάκι του σχολίου μετά την επιτυχή αποθήκευση
            self.text_comment.delete("1.0", "end")
            
            # Αν περάστηκε συνάρτηση on_save από το main_window, την καλούμε για ανανέωση
            if self.on_save:
                self.on_save()

        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Δεν μπόρεσε να αποθηκευτεί: {e}")

    def go_back(self):
        #Καταστρέφουμε αυτό το frame
        print("Επιστροφή στην αρχική οθόνη!")
        self.destroy()
        #Καλούμε την show_main_screen() του γονέα (αν υπάρχει) για να ξαναφέρει τα βιβλία μπροστά
        if hasattr(self.master, 'show_main_screen'):
            self.master.show_main_screen()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    test_book = {"book": {"book_id": 1, "title": "Test Book", "authors": "Test Author"}}
    def test_refresh(): print("Refresh callback triggered!")
    app = BookDetailsWindow(root, book_data=test_book, on_save=test_refresh)
    root.mainloop()