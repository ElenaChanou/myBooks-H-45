import tkinter as tk
from tkinter import messagebox
from add_book_view import AddBookScreen
from book_details_view import BookDetailsScreen
from login_view import LoginScreen
from main_view import  MainScreen
from db import Database_Manager 


class ScreenManager:
    '''Ο ScreenManager είναι ο διαχειριστής(γονιός). Εκτελεί την εναλλαγή των οθονών(Frames) μέσα σε ένα window.
    Μας εξυπηρετεί για να μπορεί η κάθε οθόνη(παιδί) να είναι γραφικά ανεξάρτητη, να χρειάζεται μόνο να
    σχεδιάσει το περιεχόμενο της μέσα στο παράθυρο και να μην ενδιαφέρεται για το πως θα εμφανίζονται οι οθόνες και τις ενναλαγές
    μεταξύ τους, αλλα να μπορει να έχει επικοινωνία και να καλεί τον manager για αυτόν τον σκοπό'''

    def __init__(self,root):
        #ΕΔΩ ΕΧΟΥΜΕ ΤΟ ΒΑΣΙΚΟ ΠΑΡΑΘΥΡΟ ΤΟΥ UI
        self.root = root
        self.root.geometry("900x750")
        self.root.title("Εφαρμογή myBooks")
        self.db_manager = Database_Manager('myBooks') #Δημιουργούμε τον διαχειριστή της βάσης δεδομένων για να τον έχουμε διαθέσιμο σε όλο το UI
        
        self.current_user = None #Θα χρησιμοποιηθεί για να κρατάμε πληροφορίες για τον τρέχοντα χρήστη που έχει συνδεθεί, π.χ. username, user_id κλπ. Αυτό θα μας βοηθήσει να φιλτράρουμε τα βιβλία και τις αξιολογήσεις που εμφανίζονται ανάλογα με τον χρήστη.
        
        #ΕΔΩ ΕΧΟΥΜΕ ΕΝΑ ΒΑΣΙΚΟ FRAME ΠΟΥ ΘΑ ΠΙΑΝΕΙ ΟΛΗ ΤΗΝ ΟΘΟΝΗ 
        #ΚΑΙ ΘΑ ΜΠΟΡΟΥΜΕ ΝΑ ΕΝΑΛΛΑΣΟΥΜΕ ΤΟ ΠΕΡΙΕΧΟΜΕΝΟ ΔΗΛΑΔΗ ΤΟ ΠΟΙΑ ΟΘΟΝΗ ΘΑ ΕΜΦΑΝΙΖΕΤΑΙ
        self.window = tk.Frame(self.root)
        self.window.pack(fill= "both", expand=True)

        #ΕΔΩ ΑΡΧΙΚΟΠΟΙΟΥΜΕ ΤΙΣ ΟΘΟΝΕΣ ΜΑΣ ΚΑΙ ΠΕΡΝΑΜΕ ΚΑΙ ΤΟΝ ScreenManager ΓΙΑ ΝΑ ΚΑΝΕΙ ΤΗΝ ΔΙΑΧΕΙΡΙΣΗ

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
        self.login_screen.pack(fill = "both", expand = True)
    def show_main(self):
        self.clear_screen()
        self.main_screen.pack(fill = "both", expand = True)
        #Ανανέωση του πίνακα με τα βιβλία κάθε φορά που εμφανίζεται η κύρια οθόνη, για να βλέπει ο χρήστης τα πιο πρόσφατα δεδομένα
        self.main_screen.load_top_books()

    def show_book_details(self, book_id):
        self.clear_screen()
        self.book_details_screen.pack(fill="both", expand = True)
        #self.book_details_screen.load_book_info(book_id)
    def show_add(self):
        self.clear_screen()
        self.add_book_screen.pack(fill="both", expand= True)
        #self.add_book_screen.clear_entries()

    def handle_add_new_book(self, book_data):
        try:
            new_book_id = self.db_manager.add_book(book_data)
            return new_book_id
        except Exception as e:
            print(f"Error adding book: {e}")
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
            print(f"Error adding rating: {e}")
            return False
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenManager(root)
    root.mainloop()

