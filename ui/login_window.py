import tkinter as tk
import customtkinter as ctk
from services.auth_service import login
from db.db import Database_Manager

# Φτιάχνουμε ένα αντικείμενο για να μιλάμε στη βάση "myBooks"
db_manager = Database_Manager("myBooks")

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller = controller

         # --- ΝΕΟ: Κεντρικό Container που κάθεται ακριβώς στη μέση ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        #self.master.title("Βιβλιοθήκη - Είσοδος")
        #self.master. geometry("400x300")
       
        
        myfont = ("Arial", 12,"bold")

        self.label_user = ctk.CTkLabel(self.main_container, text = "Όνομα Χρήστη:", font=myfont)
        self.label_user.grid(row=0, column=0, padx=10,pady=(40,10), sticky="e")

        self.entry_user = ctk.CTkEntry(self.main_container, font=("arial", 12))
        self.entry_user.grid(row=0, column=1, padx=10,pady=(40,10), sticky="w")


        self.label_password = ctk.CTkLabel(self.main_container, text="Κωδικός πρόσβασης", font=("Arial", 12))
        self.label_password.grid(row=1, column=0, padx=10,pady=(40,10), sticky="e")

        self.entry_password = ctk.CTkEntry(self.main_container, font=("Arial", 12), show="*")
        self.entry_password.grid(row=1, column=1, padx=10,pady=10, sticky="w")

        self.login_button = ctk.CTkButton(self.main_container, text= "Είσοδος", command = self.handle_login, font=myfont)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.register_button = ctk.CTkButton(self.main_container, text = "Εγγραφή Νέου Χρήστη", command= self.open_register_window, font = ("Arial", 10, "underline"), text_color= "lightblue", fg_color="transparent")
        self.register_button.grid(row=3, column=0, columnspan=2,pady=5)

        self.error_label= ctk.CTkLabel(self.main_container, text="", text_color= "red", font= ("Arial",14))
        self.error_label.grid(row=4, column=0,columnspan=2, pady=5)


    def handle_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_password.get().strip()

        print(f"--- Προσπάθεια Σύνδεσης ---")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print("-" * 20)
        # 1. Καλώ  το backend για να ελέγξει τα στοιχεία στη βάση
        
        user_data = login(username, password)
        
        # Δοκιμή με admin και 1234
        #if username == "admin" and password == "1234":
         #   print("--- Επιτυχής Σύνδεση ---")

        #2. Έλεγχος απάντησης
        
        if user_data: 

            #αν επιστρέψει λεξικό, η σύνδεση πέτυχε
            print("--- Επιτυχής Σύνδεση ---")
            # Καθαρίζει τυχόν παλιό μήνυμα λάθους
            self.error_label.configure(text="")
            # Ανοίγει το Main Window
            self.controller.show_main_screen() 
            
            # Αλλάζουμε το κείμενο με το πραγματικό username που  έφερε η βάση
            actual_username = user_data["username"]
            self.controller.main_frame.welcome_label.configure(text=f"Καλώς ήρθες, {actual_username}")
            
        else:
            # Αν επιστρέψει None, η σύνδεση απέτυχε
            print("--- Αποτυχία Σύνδεσης ---")
            print(f"Αποτυχημένη δοκιμή με User: {username}")
            print("-------------------------") 

            # Ενημέρωση του κόκκινου label στην οθόνη
            self.error_label.configure(text="Λάθος username ή κωδικός!")
            # Καθαρισμός του πεδίου κωδικού για την επόμενη προσπάθεια
            self.entry_password.delete(0, tk.END)

    def open_register_window(self):
        #Νέο πράθυρο πάνω από τη login
        reg_window= ctk.CTkToplevel(self)
        reg_window.title("Νέα εγγραφή")
        reg_window.geometry("300x300")
        reg_window.grab_set()
        reg_window.focus()

        ctk.CTkLabel(reg_window, text= "Επιλέξτε Username: ", font = ("Arial",11)).pack(pady= (20, 5))
        entry_new_user = ctk.CTkEntry(reg_window, font =('Arial', 12))
        entry_new_user.pack(pady=5)

        ctk.CTkLabel(reg_window, text= "Επιλέξτε Password: ", font = ("Arial",11)).pack(pady= 5)
        entry_new_pass = ctk.CTkEntry(reg_window, font =('Arial', 12), show="*")
        entry_new_pass.pack(pady=5)

        def save_new_user():

            new_u = entry_new_user.get().strip()
            new_p = entry_new_pass.get().strip()
            
            # Έλεγχος αν άφησε κενά τα πεδία
            if not new_u or not new_p:
                print("Σφάλμα: Πρέπει να συμπληρωθούν και τα δύο πεδία!")
                return
            
            # ΕΔΩ: Εκτύπωση για δοκιμή και πάσσα προς βάση
            print("\n--- ΑΙΤΗΜΑ ΝΕΑΣ ΕΓΓΡΑΦΗΣ ---")
            print(f"Username: {new_u}")
            print(f"Password: {new_p}")
            
            #Καλούμε τη συνάρτηση της βάσης 
            success = db_manager.user_registration(new_u, new_p)
            #Ελέγχουμε αν η εγγραφή πέτυχε
            if success:
                print("Η εγγραφή ολοκληρώθηκε με επιτυχία στη βάση!")
                print("----------------------------\n")
                reg_window.destroy() # Κλείνει το μικρό παράθυρο μόνο αν ειναι επιτυχής η εγγραφη
            else:
                print("Αποτυχία εγγραφής! Ίσως το username υπάρχει ήδη.")
                print("----------------------------\n")

        #  το κουμπί που κάθεται έξω από τη συνάρτηση
        save_button = ctk.CTkButton(reg_window, text="Ολοκλήρωση!", command = save_new_user, font =("Arial", 11, "bold"), fg_color = "#4caf50", text_color="white")
        save_button.pack(pady=20)





if __name__== "__main__":
    root = tk.Tk()
    app = LoginFrame(root,root)
    app.pack(fill="both", expand = True)
    root.mainloop()
