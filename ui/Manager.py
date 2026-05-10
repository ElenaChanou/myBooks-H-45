import tkinter as tk
from tkinter import messagebox
from add_book_view import AddBookScreen
from book_details_view import BookDetailsScreen
from login_view import LoginScreen
from main_view import MainScreen
from db import Database_Manager 


class ScreenManager:
    '''Διαχειρίζεται την εναλλαγή των Frames-Οθόνων, προσφέροντας γραφική ανεξαρτησία 
    στις επιμέρους οθόνες και κεντρικό έλεγχο της πλοήγησης της εφαρμογής.'''

    def __init__(self, root):
        # Αρχικοποίηση του root και διαμόρφωση του παραθύρου
        self.root = root
        self.root.geometry("900x750")
        self.root.title("Εφαρμογή myBooks")
        self.db_manager = Database_Manager('myBooks') # Δημιουργούμε τον διαχειριστή της βάσης δεδομένων
        
        self.current_user = None # Πληροφορίες για τον τρέχοντα χρήστη
        
        # Frame όπου θα γίνεται η εμφάνιση-εναλλαγή των οθονών
        self.window = tk.Frame(self.root)
        self.window.pack(fill="both", expand=True)

        # Αρχικοποίηση των οθονών της εφαρμογής, περνάμε το self.window(Tkinter Frame) και το self(Manager) για να έχουν πρόσβαση στις μεθόδους του Manager)
        self.login_screen = LoginScreen(self.window, self)
        self.main_screen = MainScreen(self.window, self)
        self.add_book_screen = AddBookScreen(self.window, self)
        self.book_details_screen = BookDetailsScreen(self.window, self)

        self.screens = [self.login_screen, self.main_screen, self.book_details_screen, self.add_book_screen]
        self.show_login()

    def clear_screen(self):
        for screen in self.screens:
            screen.pack_forget()
        
    def show_login(self):
        self.clear_screen()
        self.login_screen.pack(fill="both", expand=True)

    def show_main(self):
        self.clear_screen()
        self.main_screen.pack(fill="both", expand=True)
        # Ανανέωση του πίνακα με τα βιβλία κάθε φορά που εμφανίζεται η κύρια οθόνη
        self.main_screen.load_top_books()

    def show_book_details(self, book_id):
        self.clear_screen()
        self.book_details_screen.pack(fill="both", expand=True)
        # Ενεργοποιημένο για να φορτώνει τα σωστά δεδομένα
        self.book_details_screen.load_book_info(book_id)

    def show_add(self):
        self.clear_screen()
        self.add_book_screen.pack(fill="both", expand=True)
        #self.add_book_screen.clear_entries()

    def handle_add_new_book(self, book_data):
        try:
            new_book_id = self.db_manager.add_book(book_data)
            return new_book_id
        except Exception as e:
            print(f"Error adding book: {e}")
            messagebox.showerror("Σφάλμα", f"Αποτυχία προσθήκης βιβλίου:\n{e}")
            return None 
        
    def handle_add_rating(self, book_id, rating, comment):
        user_id = self.current_user
        try:
            success = self.db_manager.upsert_rating(
                user_id=user_id, 
                book_id=book_id, 
                rating=rating, 
                comments=comment
            )
            return success
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης αξιολόγησης:\n{e}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenManager(root)
    root.mainloop()