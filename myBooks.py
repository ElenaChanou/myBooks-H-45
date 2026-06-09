import sys
import os
import customtkinter as ctk

# Προσθήκη του τρέχοντος φακέλου στο path για να μην έχουμε θέματα με τα imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db import Database_Manager
from ui.login_window import LoginFrame
from ui.main_window import MainFrame
from services import auth_service


class MyBooksApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Βασικές ρυθμίσεις του παραθύρου
        self.title("myBooks - Κεντρικό Σύστημα")
        self.geometry("1400x1000")
        
        # 1. Αρχικοποίηση της Βάσης Δεδομένων
        # Σύνδεση με τη βάση (ο Database_Manager φτιάχνει τα tables αυτόματα στο init)
        self.db = Database_Manager("myBooks")
        
        # Μεταβλητή για το session του χρήστη (αποθηκεύει id και username)
        self.current_user = None
        self.current_frame = None
        
        # 2. Εκκίνηση της εφαρμογής με το Login Window
        self.show_login_screen()

    def show_login_screen(self):
        """Καθαρίζει την οθόνη και εμφανίζει το Login."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = LoginFrame(self, controller=self)
        self.current_frame.pack(fill="both", expand=True)

    def handle_auth(self, username, password):
        """Καλείται από το LoginFrame. Χρησιμοποιεί το auth_service για έλεγχο."""
        user_session = auth_service.login(username, password)
        
        if user_session:
            self.current_user = user_session  # Κράτα τα στοιχεία του χρήστη στη μνήμη
            self.show_main_screen()             # Προχωράμε στην αρχική οθόνη
            return True                        
        else:
            return False

    def show_main_screen(self):
        """Κλείνει το Login και ανοίγει το Main Window περνώντας το session."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = MainFrame(self, controller=self)
        self.current_frame.pack(fill="both", expand=True)
        
        # Αν έχουμε ενεργό χρήστη, άλλαξε το welcome label με το όνομά του
        if self.current_user:
            self.current_frame.welcome_label.configure(
                text=f"Καλώς ήρθες, {self.current_user['username']}!"
            )
            
        

if __name__ == "__main__":
    # Ρύθμιση εμφάνισης 
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Εκτέλεση της εφαρμογής
    app = MyBooksApp()
    app.mainloop()