import tkinter as tk
from tkinter import messagebox


class LoginScreen(tk.Frame):
    '''Η κλάση LoginScreen είναι ενα Tkinter Frame. Είναι η πρώτη οθόνη που βλέπει ο χρήστης
    όταν θέλει να κάνει σύνδεση/εγγραφή και θα περιέχει τα κατάλληλα γραφικα στοιχεία '''
    
    def __init__(self, parent, manager):
        #ΚΑΛΟΥΜΕ ΤΟΝ CONSTRUCTOR ΤΗΣ ΓΟΝΙΚΗΣ ΚΛΑΣΗΣ (tk.Frame) ΓΙΑ ΝΑ ΕΧΟΥΜΕ ΟΛΗ ΤΗ ΛΕΙΤΟΥΡΓΙΚΟΤΗΤΑ ΕΝΟΣ FRAME
        super().__init__(parent)
        #ΑΠΟΘΗΚΕΥΟΜΕ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ (Manager) ΓΙΑ ΝΑ ΤΟΝ ΕΧΕΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΣΤΗ ΜΝΗΜΗ ΤΟΥ ΚΑΙ ΝΑ ΤΟΥ ΔΙΝΕΙ ΕΝΤΟΛΕΣ ΑΡΓΟΤΕΡΑ
        self.manager = manager 

        #Η ΣΥΝΑΡΤΗΣΗ ΘΑ ΦΤΙΑΞΕΙ ΤΟ ΠΕΡΙΒΑΛΛΟΝ 
        self.setup_frame()

    def setup_frame(self):
        
        tk.Label(self, text = "Καλώς ήρθες στην myBooks app", font = ("Courier", 14, "bold")).pack(pady=20)
        
        #ΤΑ ΠΕΔΙΑ ΠΟΥ ΘΑ ΠΛΗΚΤΡΟΛΟΓΕΙ Ο ΧΡΗΣΤΗΣ
        tk.Label(self, text = "Username: ").pack()
        self.ent_username = tk.Entry(self)
        self.ent_username.pack(pady=5)

        tk.Label(self, text = "Password:").pack()
        self.ent_password = tk.Entry(self, show='*')
        self.ent_password.pack(pady=5)

        #ΤΑ ΚΟΥΜΠΙΑ ΓΙΑ ΕΙΣΟΔΟ ΚΑΙ ΕΓΓΡΑΦΗ MΕΣΑ ΣΕ ΕΝΑ FRAME ΞΕΧΩΡΙΣΤΟ 
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        Sign_in_button = tk.Button(button_frame, text = "Είσοδος", command = self.login_ui)
        Sign_in_button.pack(side="left", padx = 10)
        
        Sign_up_button = tk.Button(button_frame, text = "Εγγραφή", command = self.registration_ui)
        Sign_up_button.pack(side="left", padx = 10)

    def login_ui(self):
        username = self.ent_username.get()
        password = self.ent_password.get()

        #ΑΝ ΔΕΝ ΕΓΡΑΨΕ Ο ΧΡΗΣΤΗΣ ΤΠΤ
        if username == "" or password == "":
            messagebox.showwarning("Ξαναπροσπάθησε! ", "Συμπλήρωσε όλα τα πεδία.")
            return
 
        #ΕΔΩ ΚΑΛΟΥΜΕ ΤΗΝ ΣΥΝΑΡΤΗΣΗ find_user ΤΟΥ Database_Manager
        user_id = self.manager.db_manager.find_user(username, password) 

        if user_id is not None:
            messagebox.showinfo("Επιτυχής σύνδεση", f"Καλώς ήρθες, {username}")
            self.manager.current_user = user_id  # Αποθήκευση του user_id του τρέχοντος χρήστη στον manager για μελλοντική χρήση
            self.ent_username.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
            self.manager.show_main()
        else:
            messagebox.showerror("Σφάλμα", "Λάθος όνομα χρήστη ή κωδικός. Ξαναπροσπάθησε!")
            self.ent_password.delete(0, tk.END)


    def registration_ui(self):
        username = self.ent_username.get()
        password = self.ent_password.get()

        #ΑΝ ΔΕΝ ΣΥΜΠΛΗΡΩΣΕ Ο ΧΡΗΣΤΗΣ ΕΝΑ ΑΠΟ ΤΑ ΠΕΔΙΑ
        if username == "" or password == "":
            messagebox.showwarning("Ξαναπροσπάθησε!", "Συμπλήρωσε όλα τα πεδία.")
            return
        #ΕΔΩ ΚΑΛΟΥΜΕ ΤΗΝ ΣΥΝΑΡΤΗΣΗ user_registration ΤΟΥ Database_Manager   
        registrated_user = self.manager.db_manager.user_registration(username, password) 

        if registrated_user:
            messagebox.showinfo("Εγγραφή ολοκληρώθηκε!", f"Μπορείτε να συνδεθείτε! {username}")
            self.ent_username.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
        else:
            messagebox.showerror("Σφάλμα", "Αυτό το όνομα χρήστη χρησιμοποιείται ήδη, ξαναπροσπάθησε.")
            self.ent_password.delete(0, tk.END)




