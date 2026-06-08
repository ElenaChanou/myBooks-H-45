import tkinter as tk
import customtkinter as ctk

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        # Αρχικοποιούμε το Frame. Το parent είναι το κεντρικό παράθυρο.
        super().__init__(parent)
        
        # Αποθηκεύουμε τον controller (δηλαδή το myBooks.py, το κεντρικό App).
        # Τον χρειαζόμαστε για να του στέλνουμε αιτήματα, όπως "έλεγξε αυτόν τον κωδικό".
        self.controller = controller

        # Κεντρικό Container που κάθεται ακριβώς στη μέση
        # Φτιάχνουμε ένα διάφανο frame (fg_color="transparent") για να βάλουμε μέσα τα πεδία.
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        
        # Χρησιμοποιούμε place αντί για pack/grid για να το κεντράρουμε απόλυτα!
        # relx=0.5 και rely=0.5 σημαίνει "πήγαινε στο 50% του πλάτους και του ύψους της οθόνης".
        # anchor="center" σημαίνει ότι το κέντρο αυτού του κουτιού θα καρφιτσωθεί σε αυτό το 50%.
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Ορισμός μια κοινής γραμματοσειρά
        myfont = ("Arial", 12, "bold")

        # Στοιχείας σύνδεσης. Πεδία και ετικέτες
        self.label_user = ctk.CTkLabel(self.main_container, text="Όνομα Χρήστη:", font=myfont)
        # sticky="e": σπρώχνει το κείμενο να κολλήσει στα δεξιά του κελιού του
        self.label_user.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_user = ctk.CTkEntry(self.main_container, font=("Arial", 12), width=200)
        # sticky="w", σπρώχνει το κουτάκι να κολλήσει στα αριστερά του κελιού του
        self.entry_user.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.label_password = ctk.CTkLabel(self.main_container, text="Κωδικός πρόσβασης:", font=myfont)
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Το show="*" κρύβει τους χαρακτήρες που πληκτρολογεί ο χρήστης για ασφάλεια
        self.entry_password = ctk.CTkEntry(self.main_container, font=("Arial", 12), show="*", width=200)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Κουμπιά
        self.login_button = ctk.CTkButton(self.main_container, text="Είσοδος", command=self.handle_login, font=myfont, width=150)
        # columnspan=2: Κάνει το κουμπί να πιάνει και τις δύο στήλες για να κεντραριστεί ομοιόμορφα από κάτω
        self.login_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))
        
        # Κουμπί εγγραφής που μοιάζει με σύνδεσμο
        self.register_button = ctk.CTkButton(self.main_container, text="Εγγραφή Νέου Χρήστη", command=self.open_register_window, font=("Arial", 10, "underline"), text_color="lightblue", fg_color="transparent")
        self.register_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Ετικέτα για την εμφάνιση μηνυμάτων λάθους ή επιτυχίας. Αρχικά είναι κενή ("")
        self.error_label = ctk.CTkLabel(self.main_container, text="", text_color="red", font=("Arial", 14))
        self.error_label.grid(row=4, column=0, columnspan=2, pady=5)


    def handle_login(self):
        # Διαβάζουμε τι έγραψε ο χρήστης στα κουτάκια
        username = self.entry_user.get()
        password = self.entry_password.get()

        print(f"--- Προσπάθεια Σύνδεσης: {username} ---")

        # Ζητάμε από τον controller (κεντρική εφαρμογή) να κάνει τον έλεγχο στη βάση.
        # Θα μας επιστρέψει True αν τα στοιχεία είναι σωστά, αλλιώς False.
        success = self.controller.handle_auth(username, password)

        if not success:
            print("--- Αποτυχία Σύνδεσης ---")
            # Εμφανίζουμε το μήνυμα λάθους
            self.error_label.configure(text="Λάθος username ή κωδικός!", text_color="red")
            # Καθαρίζουμε μόνο το πεδίο του κωδικού (από τη θέση 0 έως το τέλος: tk.END)
            self.entry_password.delete(0, tk.END) 


    def open_register_window(self):
        # CTkToplevel: Δημιουργεί ένα νέο, ανεξάρτητο popup παράθυρο  πάνω από το login
        reg_window = ctk.CTkToplevel(self)
        reg_window.title("Νέα εγγραφή")
        reg_window.geometry("300x300")
        
        # grab_set(): Απαγορεύει στον χρήστη να κάνει κλικ στο από πίσω παράθυρο μέχρι να κλείσει αυτό!
        reg_window.grab_set()
        # focus(): Φέρνει το παράθυρο αυτόματα στο προσκήνιο
        reg_window.focus()

        # Τα γραφικά του νέου παραθύρου 
        ctk.CTkLabel(reg_window, text="Επιλέξτε Username: ", font=("Arial", 11)).pack(pady=(20, 5))
        entry_new_user = ctk.CTkEntry(reg_window, font=('Arial', 12))
        entry_new_user.pack(pady=5)

        ctk.CTkLabel(reg_window, text="Επιλέξτε Password: ", font=("Arial", 11)).pack(pady=5)
        entry_new_pass = ctk.CTkEntry(reg_window, font=('Arial', 12), show="*")
        entry_new_pass.pack(pady=5)

        # Nested function που ζει μόνο μέσα στην open_register_window
        # Έτσι έχει άμεση πρόσβαση στα entry_new_user και entry_new_pass χωρίς να τα κάνουμε self
        def save_new_user():
            # Παίρνουμε τα στοιχεία και κόβουμε τα κενά αριστερά/δεξιά (strip)
            new_u = entry_new_user.get().strip()
            new_p = entry_new_pass.get().strip()

            # Έλεγχος αν άφησε κάποιο πεδίο άδειο
            if not new_u or not new_p:
                print("Σφάλμα: Πρέπει να συμπληρωθούν και τα δύο πεδία!")
                return
            
            # Επικοινωνούμε απευθείας με τον Database Manager μέσω του controller για εγγραφή
            success = self.controller.db.user_registration(new_u, new_p)
            
            if success:
                print(f"--- ΕΠΙΤΥΧΗΣ ΕΓΓΡΑΦΗ: {new_u} ---")
                # Γράφουμε μήνυμα επιτυχίας στο ΑΡΧΙΚΟ παράθυρο (login_frame)
                self.error_label.configure(text="Επιτυχής εγγραφή! Μπορείς να συνδεθείς.", text_color="green")
                # Κλείνουμε το popup εγγραφής
                reg_window.destroy()
            else:
                print("Σφάλμα εγγραφής (π.χ. το username υπάρχει ήδη).")
                self.error_label.configure(text="Το όνομα χρήστη υπάρχει ήδη!", text_color="red")
                reg_window.destroy()

        # Το κουμπί που καλεί την ένθετη συνάρτηση save_new_user
        save_button = ctk.CTkButton(reg_window, text="Ολοκλήρωση!", command=save_new_user, font=("Arial", 11, "bold"), fg_color="#4caf50", text_color="white")
        save_button.pack(pady=20)


if __name__ == "__main__":
    # --- ΚΩΔΙΚΑΣ ΜΟΝΟ ΓΙΑ ΤΕΣΤΙΝΓΚ ---
    root = tk.Tk()
    
    # Περνάμε το root και ως parent και ως "εικονικό" controller για να ανοίξει
    app = LoginFrame(root, root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()