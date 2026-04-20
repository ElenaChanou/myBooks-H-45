import tkinter as tk

class LoginWindow:
    def __init__(self, master):
        self.master = master

        self.master.title("Βιβλιοθήκη - Είσοδος")
        self.master.geometry("400x300")

        myfont = ("Arial", 12,"bold")

        self.label_user = tk.Label(self.master, text = "Όνομα Χρήστη:", font=myfont)
        self.label_user.pack(pady=10)

        self.entry_user = tk.Entry(self.master)
        self.entry_user.pack(pady=5)


        self.label_password = tk.Label(self.master, text="Κωδικός πρόσβασης", font=("Arial", 12))
        self.label_password.pack(pady=5)

        self.entry_password = tk.Entry(self.master, font=("Arial", 12), show="*")
        self.entry_password.pack(pady=5)

        self.login_button = tk.Button(self.master, text= "Είσοδος", command = self.handle_login, font=myfont)
        self.login_button.pack(pady=20)

        self.error_label=tk.Label(self.master, text="", fg = "red", font= ("Arial",14))
        self.error_label.pack(pady=5)


    def handle_login(self):
        username= self.entry_user.get()
        password= self.entry_password.get()

        print(f"--- Προσπάθεια Σύνδεσης ---")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("-"*20)


#Δοκιμή με admin και 1234
        if username == "admin" and password =="1234":
            print("--- Επιτυχής Σύνδεση ---")
            print(f"User: {username}")
            print(f"Pass: {password}")
            print("-----------------------")
            
            self.master.destroy()
        else:
            print("--- Αποτυχία Σύνδεσης ---")
            print(f"Δοκιμή με User: {username} και Pass: {password}")
            print("-------------------------") 

             # Ενημέρωση του κόκκινου label στην οθόνη
            self.error_label.config(text="Λάθος username ή κωδικός!")
            # Καθαρισμός του πεδίου κωδικού για την επόμενη προσπάθεια
            self.entry_password.delete(0, tk.END)

root = tk.Tk()
app = LoginWindow(root)
root.mainloop()