import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ManualBookWindow(ctk.CTkToplevel):
    
    def __init__ (self,parent):
        super().__init__(parent)
        
        self.title("Χειροκίνητη Προσθήκη Βιβλίου")
        self.geometry("500x700")
        self.cover_path = None
        self.grab_set()
        self.create_widgets()

    def create_widgets(self):
        # 1. αλλαγή φτιάχνουμε ένα κεντρικό "κουτί" και του λέμε να κάτσει ακριβώς στη μέση (expand=True)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True)

        # 2. Το weight τώρα το δίνουμε στο container όχι στο self
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

       
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

        self.entry_isbn = ctk.CTkEntry(self.main_container, placeholder_text="Εισάγετε ISBN ")
        self.entry_isbn.grid(row=3, column=1, padx=10, pady=10)

        self.label_desc = ctk.CTkLabel(self.main_container, text="Περιγραφή*", font=("arial", 12, "italic"))
        self.label_desc.grid(row=4, column=0, padx=10, pady=10, sticky="ne")
        
        self.textbox_desc = ctk.CTkTextbox(self.main_container, height = 100)
        self.textbox_desc.grid(row=4, column=1, padx=10, pady=10)

        #Κουμπί για ανέβασμα εικόνας
        self.button_upload = ctk.CTkButton(self.main_container, text = "Επιλογή εξωφύλλου", command=self.choose_cover)
        self.button_upload.grid(row=5, column=0, padx=10, pady=10)

        #To label που θα φιλοξενεί την εικόνα. Προσωρινά κείμενο
        self.image_label= ctk.CTkLabel(self.main_container,text="[Δεν επιλέχθηκε εικόνα]")
        self.image_label.grid(row=5, column=1,padx=10,pady=10)

        self.save_button=ctk.CTkButton(self.main_container, text="Αποθήκευση", command=self.save_book)
        self.save_button.grid(row=6, column=1, padx=10,pady=10)

        self.cancel_button=ctk.CTkButton(self.main_container, text="Ακύρωση", command=self.cancel)
        self.cancel_button.grid(row=6,column=0,padx=10,pady=10)





    def choose_cover(self):
        # 1. Ανοίγουμε το παράθυρο επιλογής αρχείου (χρησιμοποιούμε το filedialog που κάναμε import)
        filename = filedialog.askopenfilename(
            title="Επιλογή Εξωφύλλου",
            # Λέμε στον υπολογιστή να δείχνει μόνο αρχεία εικόνας
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

        # 2. Αν ο χρήστης επέλεξε πράγματι ένα αρχείο (δεν πάτησε "Ακύρωση")
        if filename:
            print("Επιλέχθηκε το αρχείο:", filename)
            
            
            
            # Α. Ανοίγουμε την εικόνα από το δίσκο
            pil_image = Image.open(filename)
            
            # Β. Την κάνουμε resize (αλλαγή μεγέθους) για να χωράει  στο παράθυρό 
            # (π.χ. 120 πλάτος, 180 ύψος)
            pil_image_resized = pil_image.resize((120, 180))
            
            # Γ. Μετατρέπουμε την εικόνα της Pillow σε εικόνα που καταλαβαίνει το CustomTkinter
            self.ctk_image = ctk.CTkImage(light_image=pil_image_resized, dark_image=pil_image_resized, size=(120, 180))
            
            # Δ. Ενημερώνουμε το generic label που φτιάξαμε πριν:
            # Σβήνουμε το κείμενο "[Δεν επιλέχθηκε εικόνα]" και βάζουμε την εικόνα!
            self.image_label.configure(text="", image=self.ctk_image)

    def cancel(self):#συνάρτηση ακύρωσης κλείνει παράθρο και μας γυρνάει πίσω
        self.destroy()

    def save_book(self):
      
        # 1. Ανάγνωση δεδομένων (Το .strip() καθαρίζει τα άχρηστα κενά στην αρχή και στο τέλος)
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        year = self.entry_year.get().strip()
        isbn = self.entry_isbn.get().strip() # Το ISBN δεν είναι υποχρεωτικό, αλλά το διαβάζουμε
        
        # ΠΡΟΣΟΧΗ: Το Textbox διαβάζεται διαφορετικά από τα Entry! 
        # Το "0.0", "end" σημαίνει "διάβασε τα πάντα από την αρχή ως το τέλος".
        desc = self.textbox_desc.get("0.0", "end").strip()

        # 2. Έλεγχος υποχρεωτικών πεδίων
        # Αν έστω και ένα από τα υποχρεωτικά είναι κενό (δηλαδή if not...):
        if not title or not author or not year or not desc:
            print("ΜΠΗΚΕ ΣΤΟ IF: Κάποιο πεδίο είναι κενό!") #  αυτό για τεστ
            messagebox.showerror("Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα υποχρεωτικά πεδία (*).")
            return  # Σταματάει τη συνάρτηση εδώ! Δεν προχωράει παρακάτω.

        # 3. Προσωρινή εκτύπωση για δοκιμή (αργότερα εδώ θα μπει η κλήση για τη βάση δεδομένων)
        print("--- Στοιχεία Προς Αποθήκευση ---")
        print(f"Τίτλος: {title}")
        print(f"Συγγραφέας: {author}")
        print(f"Έτος: {year}")
        print(f"ISBN: {isbn}")
        print(f"Περιγραφή: {desc}")
        print(f"Εξώφυλλο (Path): {self.cover_path}")

        #Εδώ θα μπει η συνάρτηση του Backend
        # π.χ. database.save_new_book(title, author, year, isbn, desc, self.cover_path)

        # Εμφάνιση μηνύματος επιτυχίας
        messagebox.showinfo("Επιτυχία", f"Το βιβλίο '{title}' προστέθηκε με επιτυχία!")
        
        # Κλείσιμο του παραθύρου μετά την αποθήκευση
        self.destroy()


if __name__ == "__main__":
    # Φτιάχνουμε ένα αόρατο/μικρό βασικό παράθυρο-γονιό για να πατήσει πάνω του το δικό μας
    app = ctk.CTk()
    app.geometry("10x10") 
    
    # Ανοίγουμε το παράθυρο προσθήκης
    window = ManualBookWindow(app)
    
    # Ξεκινάμε την εφαρμογή
    app.mainloop()



