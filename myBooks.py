import sys
import os
import customtkinter as ctk


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db import Database_Manager
from ui.login_window import LoginFrame
from ui.main_window import MainFrame
from services import auth_service
# Μπορείς να κάνεις import και τα υπόλοιπα services όταν χρειαστεί
# from services import book_service, import_service, rating_service

class MyBooksApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("myBooks - Κεντρικό Σύστημα")
        self.geometry("1200x800")
        
        # 1. Αρχικοποίηση της Βάσης Δεδομένων
        # Η κλάση Database_Manager τρέχει αυτόματα την execute_schema() κατά το __init__
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
            self.current_user = user_session  # Αποθήκευση του dict {id, username}
            self.show_main_screen()
            return True
        else:
            return False

    def show_main_screen(self):
        """Κλείνει το Login και ανοίγει το Main Window περνώντας το session."""
        if self.current_frame is not None:
            self.current_frame.destroy()
            
        self.current_frame = MainFrame(self, controller=self)
        self.current_frame.pack(fill="both", expand=True)
        
        # Ενημέρωση του UI με τα πραγματικά δεδομένα του χρήστη
        if self.current_user:
            self.current_frame.welcome_label.configure(
                text=f"Καλώς ήρθες, {self.current_user['username']}!"
            )
            
        # ΕΔΩ: Μελλοντικά θα φορτώνεις τα δεδομένα από το book_service αντί για τη hardcoded λίστα
        # books_data = book_service.list_all_books()
        # self.current_frame.update_table(books_data)

if __name__ == "__main__":
    # Ρύθμιση εμφάνισης (προαιρετικά)
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Εκτέλεση της εφαρμογής
    app = MyBooksApp()
    app.mainloop()