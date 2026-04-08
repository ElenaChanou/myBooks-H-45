import tkinter as tk
from tkinter import messagebox



class LoginScreen(tk.Frame):
    '''Η κλάση LoginScreen είναι ενα Tkinter Frame. Είναι η πρώτη οθόνη που βλέπει ο χρήστης
    όταν θέλει να κάνει σύνδεση/εγγραφή και θα περιέχει τα κατάλληλα γραφικα στοιχεία '''
    
    def __init__(self, parent, manager):
        super().__init__(parent)
        #ΑΠΟΘΗΚΕΥΟΜΕ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ (Manager) ΓΙΑ ΝΑ ΤΟΝ ΕΧΕΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΣΤΗ ΜΝΗΜΗ ΤΟΥ ΚΑΙ ΝΑ ΤΟΥ ΔΙΝΕΙ ΕΝΤΟΛΕΣ ΑΡΓΟΤΕΡΑ
        self.manager = manager 
        # self.auth_service = AuthService()  Φέρνουμε τη λογική του Authentication

        #Η ΣΥΝΑΡΤΗΣΗ ΘΑ ΦΤΙΑΞΕΙ ΤΟ ΠΕΡΙΒΑΛΛΟΝ 
        self.setup_frame()

    def setup_frame(self):
        container = tk.Frame(self)
        container.pack(expand=True)

        tk.Label(container, text = "Welocme to myBooks app", font = ("Courier", 14, "bold")).pack(pady=20)
        
        #ΤΑ ΠΕΔΙΑ ΠΟΥ ΘΑ ΠΛΗΚΤΡΟΛΟΓΕΙ Ο ΧΡΗΣΤΗΣ
        tk.Label(container, text = "Username: ").pack()
        self.ent_username = tk.Entry(container)
        self.ent_username.pack(pady=5)

        tk.Label(container, text = "Password: ").pack()
        self.ent_password = tk.Entry(container, show='*')
        self.ent_password.pack(pady=5)

        #ΤΑ ΚΟΥΜΠΙΑ ΓΙΑ ΤΗΝ ΕΙΣΟΔΟ ΚΑΙ ΕΓΓΡΑΦΗ
        button_frame = tk.Frame(container)
        button_frame.pack(pady=20)
        Sign_in_button = tk.Button(button_frame, text = "Sign in", command = self.login_ui).pack(side="left", padx=10)
        Sign_up_button = tk.Button(button_frame, text = "Sign up", command = self.registration_ui).pack(side="left", padx=10)

        

    def login_ui(self):
        username = self.ent_username.get()
        password = self.ent_password.get()

        #ΑΝ ΔΕΝ ΕΓΡΑΨΕ Ο ΧΡΗΣΤΗΣ ΤΠΤ
        if username == "" or password == "":
            messagebox.showwarning("Try again")
            return

        #ΕΔΩ ΘΑ ΓΙΝΕΙ Η ΣΥΝΔΕΣΗ ΜΕ ΤΗΝ ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΗΝ ΕΙΣΟΔΟ ΧΡΗΣΤΗ ΣΤΟ BACKEND ΓΙΑ ΤΩΡΑ ΘΑ ΒΑΛΟΥΜΕ ΜΙΑ ΜΕΤΑΒΛΗΤΗ 
        validate_user = True

        if validate_user:
            messagebox.showinfo("Login succesful", f"Welcome")
            self.ent_username.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)
            self.manager.show_main()
        else:
            messagebox.showerror("Try again wrong username or password")
            self.ent_password.delete(0, tk.END)


    def registration_ui(self):
        username = self.ent_username.get()
        password = self.ent_password.get()

        #ΑΝ ΔΕΝ ΕΓΡΑΨΕ Ο ΧΡΗΣΤΗΣ ΤΠΤ
        if username == "" or password == "":
            messagebox.showwarning("Try again")
            return

        #ΕΔΩ ΘΑ ΓΙΝΕΙ Η ΣΥΝΔΕΣΗ ΜΕ ΤΗ ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΗΝ ΕΓΓΡΑΦΗ ΤΟΥ ΧΡΗΣΤΗ ΣΤΟ BACKEND ΓΙΑ ΤΩΡΑ ΘΑ ΒΑΛΟΥΜΕ ΜΙΑ ΜΕΤΑΒΛΗΤΗ
        registrated_user = True

        if registrated_user:
            messagebox.showinfo("Registration is complete, try signing in ", f"{username}")
            self.ent_username.delete(0, tk.END)
            self.ent_password.delete(0, tk.END)

        else:
            messagebox.showerror("Try again (username or password)")
            self.ent_password.delete(0, tk.END)





