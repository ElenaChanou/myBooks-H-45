import tkinter as tk
from tkinter import messagebox
from add_book_view import AddBookScreen
from book_details_view import BookDetailsScreen
from login_view import LoginScreen
from main_view import  MainScreen


class ScreenManager:
    '''Ο ScreenManager είναι ο διαχειριστής(γονιός). Εκτελεί την εναλλαγή των οθονών(Frames) μέσα σε ένα window.
    Μας εξυπηρετεί για να μπορεί η κάθε οθόνη(παιδί) να είναι γραφικά ανεξάρτητη, να χρειάζεται μόνο να
    σχεδιάσει το περιεχόμενο της μέσα στο παράθυρο και να μην ενδιαφέρεται για το πως θα εμφανίζονται οι οθόνες και τις ενναλαγές
    μεταξύ τους, αλλα να μπορει να έχει επικοινωνία και να καλεί τον manager για αυτόν τον σκοπό'''

    def __init__(self,root):
        #ΕΔΩ ΕΧΟΥΜΕ ΤΟ ΒΑΣΙΚΟ ΠΑΡΑΘΥΡΟ ΤΟΥ UI
        self.root = root
        self.root.geometry("700x550")
        self.root.title("Εφαρμογή myBooks")
        
        #ΕΔΩ ΕΧΟΥΜΕ ΕΝΑ ΒΑΣΙΚΟ FRAME ΠΟΥ ΘΑ ΠΙΑΝΕΙ ΟΛΗ ΤΗΝ ΟΘΟΝΗ 
        #ΚΑΙ ΘΑ ΜΠΟΡΟΥΜΕ ΝΑ ΕΝΑΛΛΑΣΟΥΜΕ ΤΟ ΠΕΡΙΕΧΟΜΕΝΟ ΔΗΛΑΔΗ ΤΟ ΠΟΙΑ ΟΘΟΝΗ ΘΑ ΕΜΦΑΝΙΖΕΤΑΙ
        self.window = tk.Frame(self.root)
        self.window.pack(fill="both", expand=True)

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
        self.login_screen.pack(fill="both", expand= "True")
    def show_main(self):
        self.clear_screen()
        self.main_screen.pack(fill="both", expand= "True")
    def show_book_details(self):
        self.clear_screen()
        self.book_details_screen.pack(fill="both", expand= "True")
    def show_add(self):
        self.clear_screen()
        self.add_book_screen.pack(fill="both", expand= "True")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenManager(root)
    root.mainloop()
