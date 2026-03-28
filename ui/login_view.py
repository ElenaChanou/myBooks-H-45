import tkinter as tk
from tkinter import messagebox


class Main_Screen:
    '''
    ΕΙΝΑΙ ΕΝΑ ΑΠΛΟ ΠΑΡΑΘΥΡΟ ΑΡΓΟΤΕΡΑ ΘΑ ΓΙΝΕΙ ΑΝΑΠΤΥΞΗ ΣΤΟ main_view.py
    '''

    def __init__(self, root, username):
        self.root = root
        self.root.title(f"{username} books")
        self.root.geometry("600x400")

        #ΤΟ FRAME ΠΟΥ ΘΑ ΠΕΡΙΕΧΕΙ ΟΤΙ ΓΡΑΨΟΥΜΕ
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=40)
        
        tk.Label(self.frame, text = f"Welcome ,{username}", font=("Courier", 16, "bold")).pack(pady=20)

        tk.Button(self.frame, text = "Logout", command = self.root.quit, bg = 'blue', fg = 'white').pack(pady=20)


class Login_Screen:
    def __init__(self, root):
        self.root = root 
        #ΤΙΤΛΟΣ ΚΑΙ ΜΕΓΕΘΟΣ ΟΘΟΝΗΣ
        self.root.title("myBooks")
        self.root.geometry("500x550")

        #ΤΟ FRAME ΠΟΥ ΘΑ ΠΕΡΙΕΧΕΙ ΟΤΙ ΓΡΑΨΟΥΜΕ
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=15)

        #Η ΣΥΝΑΡΤΗΣΗ ΘΑ ΦΤΙΑΞΕΙ ΤΟ ΠΕΡΙΒΑΛΛΟΝ ΤΟΥ FRAME
        self.setup_frame()

    def setup_frame(self):
        tk.Label(self.frame, text = "Welocme to myBooks app", font = ("Courier", 14, "bold")).pack(pady=15)
        
        #ΤΑ ΠΕΔΙΑ ΠΟΥ ΘΑ ΠΛΗΚΤΡΟΛΟΓΕΙ Ο ΧΡΗΣΤΗΣ
        tk.Label(self.frame, text = "Username: ").pack()
        self.ent_username = tk.Entry(self.frame)
        self.ent_username.pack(pady=5)

        tk.Label(self.frame, text = "Password: ").pack()
        self.ent_password = tk.Entry(self.frame, show='*')
        self.ent_password.pack(pady=5)

        #ΤΑ ΚΟΥΜΠΙΑ ΓΙΑ ΤΗΝ ΕΙΣΟΔΟ ΚΑΙ ΕΓΓΡΑΦΗ
        tk.Button(self.frame, text = "Sign in", command = self.login_ui).pack(pady=10)
        tk.Button(self.frame, text = "Sign up", command = self.registration_ui).pack(pady=5)  

        

    def login_ui(self):
        username = self.ent_username.get()
        password = self.ent_password.get()

        #ΑΝ ΔΕΝ ΕΓΡΑΨΕ Ο ΧΡΗΣΤΗΣ ΤΠΤ
        if username == "" or password == "":
            messagebox.showwaring("Try again")
            return

        #ΕΔΩ ΘΑ ΓΙΝΕΙ Η ΣΥΝΔΕΣΗ ΜΕ ΤΗΝ ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΗΝ ΕΙΣΟΔΟ ΧΡΗΣΤΗ ΣΤΟ BACKEND ΓΙΑ ΤΩΡΑ ΘΑ ΒΑΛΟΥΜΕ ΜΙΑ ΜΕΤΑΒΛΗΤΗ 
        validate_user = True

        if validate_user:
            messagebox.showinfo("Login succesful", f"Welcome {username}")
            self.frame.destroy()

            # -> ΑΦΟΥ ΚΛΕΙΣΟΥΜΕ ΤΟ ΠΑΡΑΘΥΡΟ ΕΔΩ ΘΑ ΚΑΛΕΙΤΕ ΜΙΑ ΑΛΛΗ ΟΘΟΝΗ Η MAIN
            Main_Screen(self.root, username)
            

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


if __name__ == "__main__":
    root = tk.Tk()
    test = Login_Screen(root)
    root.mainloop()



