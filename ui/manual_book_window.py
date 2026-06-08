import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Φέρνουμε έτοιμο το αντικείμενο της db μέσω του service
from services.book_service import db

class ManualBookWindow(ctk.CTkToplevel):
    
    def __init__ (self, parent):
        super().__init__(parent)
        
        self.title("Χειροκίνητη Προσθήκη Βιβλίου")
        self.geometry("500x700")
        
        # Αρχικοποιούμε το μονοπάτι του εξωφύλλου ως κενό
        self.cover_path = None
        
        # grab_set(): Κλειδώνει το από πίσω παράθυρο.
        # Ο χρήστης δεν μπορεί να κάνει κλικ αλλού μέχρι να κλείσει το πάνω.
        self.grab_set()
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Φτιάχνουμε ένα κεντρικό "κουτί" που θα κάτσει ακριβώς στη μέση (expand=True)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True)

        # 2. Το weight το δίνουμε στο container για να στοιχιστούν τα πεδία όμορφα στο κέντρο του
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        # Πεδία εισαγωγής δεδομένων
       
      
        self.label_title = ctk.CTkLabel(self.main_container, text="Τίτλος *", font=("arial", 12, "italic"))
        self.label_title.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_title = ctk.CTkEntry(self.main_container, placeholder_text="Τίτλος Βιβλίου")
        self.entry_title.grid(row=0, column=1, padx=10, pady=10)

        self.label_author = ctk.CTkLabel(self.main_container, text="Συγγραφέας *", font=("arial", 12, "italic"))
        self.label_author.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.entry_author = ctk.CTkEntry(self.main_container, placeholder_text="Όνομα Συγγραφέα")
        self.entry_author.grid(row=1, column=1, padx=10, pady=10)

        self.label_year = ctk.CTkLabel(self.main_container, text="Έτος *", font=("arial", 12, "italic"))
        self.label_year.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.entry_year = ctk.CTkEntry(self.main_container, placeholder_text="Έτος συγγραφής")
        self.entry_year.grid(row=2, column=1, padx=10, pady=10)

        self.label_isbn = ctk.CTkLabel(self.main_container, text="ISBN", font=("arial", 12, "italic"))
        self.label_isbn.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.entry_isbn = ctk.CTkEntry(self.main_container, placeholder_text="Εισάγετε ISBN")
        self.entry_isbn.grid(row=3, column=1, padx=10, pady=10)

        self.label_desc = ctk.CTkLabel(self.main_container, text="Περιγραφή*", font=("arial", 12, "italic"))
       
        self.label_desc.grid(row=4, column=0, padx=10, pady=10, sticky="ne")
        
        
        self.textbox_desc = ctk.CTkTextbox(self.main_container, height=100)
        self.textbox_desc.grid(row=4, column=1, padx=10, pady=10)

        # Επιλογή εξωφύλλου
        self.button_upload = ctk.CTkButton(self.main_container, text="Επιλογή εξωφύλλου", command=self.choose_cover)
        self.button_upload.grid(row=5, column=0, padx=10, pady=10)

        # Το label που θα φιλοξενεί την εικόνα. Αρχικά δείχνει μόνο κείμενο.
        self.image_label = ctk.CTkLabel(self.main_container, text="[Δεν επιλέχθηκε εικόνα]")
        self.image_label.grid(row=5, column=1, padx=10, pady=10)

        # Αποθήκευση/Ακύρωση
        self.save_button = ctk.CTkButton(self.main_container, text="Αποθήκευση", command=self.save_book)
        self.save_button.grid(row=6, column=1, padx=10, pady=10)

        self.cancel_button = ctk.CTkButton(self.main_container, text="Ακύρωση", command=self.cancel)
        self.cancel_button.grid(row=6, column=0, padx=10, pady=10)


    def choose_cover(self):
        """Ανοίγει τον File Explorer για να επιλέξει ο χρήστης εικόνα εξωφύλλου"""
        # 1. Ανοίγουμε το παράθυρο επιλογής αρχείου
        filename = filedialog.askopenfilename(
            title="Επιλογή Εξωφύλλου",
            # Φίλτρο: Λέμε στον υπολογιστή να δείχνει ΜΟΝΟ αρχεία εικόνας
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

        # 2. Αν ο χρήστης επέλεξε πράγματι ένα αρχείο (δεν πάτησε "Ακύρωση")
        if filename:
            print("Επιλέχθηκε το αρχείο:", filename)
            
            # Αποθηκεύουμε το μονοπάτι στη μνήμη του αντικειμένου για να το σώσουμε στη βάση αργότερα
            self.cover_path = filename
            
            # Α. Ανοίγουμε την εικόνα από τον δίσκο χρησιμοποιώντας την Pillow
            pil_image = Image.open(filename)
            
            # Β. Την κάνουμε resize  για να χωράει στο UI 
            pil_image_resized = pil_image.resize((120, 180))
            
            # Γ. Μετατρέπουμε την εικόνα της Pillow σε αντικείμενο CTkImage που δέχεται το CustomTkinter
            self.ctk_image = ctk.CTkImage(light_image=pil_image_resized, dark_image=pil_image_resized, size=(120, 180))
            
            # Δ. Ενημερώνουμε την ταμπέλα (label) που φτιάξαμε πριν:
            # Σβήνουμε το κείμενο "[Δεν επιλέχθηκε εικόνα]" και της αναθέτουμε την εικόνα!
            self.image_label.configure(text="", image=self.ctk_image)

    def cancel(self):
        """Κλείνει το παράθυρο χωρίς να αποθηκεύσει τίποτα (επιστροφή)"""
        self.destroy()

    def save_book(self):
        """Ελέγχει τα δεδομένα και αποθηκεύει το βιβλίο στη Βάση Δεδομένων"""
        # 1. Ανάγνωση δεδομένων 
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        year = self.entry_year.get().strip()
        isbn = self.entry_isbn.get().strip() # Το ISBN δεν είναι υποχρεωτικό
        
       
        # Το "0.0" σημαίνει γραμμή 0 χαρακτήρας 0. Το "end" σημαίνει μέχρι το τέλος.
        desc = self.textbox_desc.get("0.0", "end").strip()

        # 2. Έλεγχος υποχρεωτικών πεδίων
        # Αν έστω και ένα από τα υποχρεωτικά είναι κενό (δηλαδή if not...):
        if not title or not author or not year or not desc:
            print("ΜΠΗΚΕ ΣΤΟ IF: Κάποιο πεδίο είναι κενό!") 
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα υποχρεωτικά πεδία (*).")
            return  # Σταματάει τη συνάρτηση εδώ! Δεν προχωράει προς τη βάση.

        print("--- Στοιχεία Προς Αποθήκευση ---")
        print(f"Τίτλος: {title}")
        print(f"Συγγραφέας: {author}")
        
        # 3. Δημιουργούμε το λεξικό με τα δεδομένα του βιβλίου, όπως ακριβώς τα περιμένει η βάση
        book_data = {
            "title": title,
            "authors": author,      
            "year": year,
            "isbn": isbn if isbn else None,
            "description": desc,
            "cover_img": self.cover_path if self.cover_path else None  
        }
        

        # 4. Προσπάθεια αποθήκευσης στη βάση
        try:
            # Καλούμε την πραγματική μέθοδο της βάσης μέσω του εγκέφαλου db για να σωθεί το βιβλίο
            new_book_id = db.add_book(book_data)
            
            # Αν η βάση επέστρεψε το νέο ID επιτυχώς
            if new_book_id:
                messagebox.showinfo("Επιτυχία", f"Το βιβλίο '{title}' αποθηκεύτηκε με επιτυχία!")
                
                # Ενημερώνουμε την κεντρική οθόνη να ξαναδιαβάσει τη βάση για να εμφανιστεί το νέο βιβλίο
                # Ελέγχουμε με hasattr αν το παράθυρο που μας άνοιξε (master) έχει λειτουργία ανανέωσης
                if hasattr(self.master, 'on_add_success') and self.master.on_add_success:
                    self.master.on_add_success()
                elif hasattr(self.master, 'refresh_books_list'):
                    self.master.refresh_books_list()
                
                # Κλείνουμε το παράθυρο αφού η αποθήκευση ήταν επιτυχής
                self.destroy()  
            else:
                messagebox.showerror("Σφάλμα", "Αποτυχία αποθήκευσης του βιβλίου στη βάση δεδομένων.")
                
        except Exception as e:
            # Αν κάτι "σκάσει" (π.χ. πρόβλημα με τη βάση SQLite), πετάμε μήνυμα στον χρήστη αντί να κρασάρει
            messagebox.showerror("Σφάλμα", f"Προέκυψε πρόβλημα κατά την αποθήκευση: {e}")


if __name__ == "__main__":
    # --- ΚΩΔΙΚΑΣ ΜΟΝΟ ΓΙΑ ΤΕΣΤΙΝΓΚ ---
    # Φτιάχνουμε ένα αόρατο/μικρό βασικό παράθυρο-γονιό για να πατήσει πάνω του το δικό μας
    app = ctk.CTk()
    app.geometry("10x10") 
    
    # Ανοίγουμε το παράθυρο προσθήκης
    window = ManualBookWindow(app)
    
    # Ξεκινάμε την εφαρμογή
    app.mainloop()