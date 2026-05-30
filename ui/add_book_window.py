import customtkinter as ctk
from ui.manual_book_window import ManualBookWindow
from services.import_service import search_books_online

class AddBookWindow(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.title("Προσθήκη Βιβλίου")
        self.geometry("500x800")
        self.grab_set()
        self.create_widgets()
        
    def create_widgets(self):
        # 1. φτιάχνουμε ένα κεντρικό "κουτί" και του λέμε να κάτσει ακριβώς στη μέση (expand=True)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True)

        # 2. Το weight τώρα το δίνουμε στο container, όχι στο self
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        self.label_add_book=ctk.CTkLabel(self.main_container, text="Στοιχεία Αναζήτησης", font=("arial", 12, "bold"))
        self.label_add_book.grid(row=0, column=0, padx=5)
            
        self.entry_title = ctk.CTkEntry(self.main_container, placeholder_text="Τίτλος Βιβλίου", font=("arial", 12))
        self.entry_title.grid(row=1, column = 0, padx=5, pady=(10,5))
            
        self.entry_author = ctk.CTkEntry(self.main_container, placeholder_text="Συγγραφέας...")
        self.entry_author.grid(row=2, column = 0, padx=5, pady=(10,5))
            
        self.button_search_add = ctk.CTkButton(self.main_container, text="Αναζήτηση και Προσθήκη", command = self.search_and_add)
        self.button_search_add.grid(row=3, column = 0, padx=5, pady=(10,5))

    # --- Η συνάρτηση ήρθε πιο αριστερά, στην ίδια ευθεία με το create_widgets ---
    def search_and_add(self):
        title = self.entry_title.get().strip()
        
        # Αν ο χρήστης δεν έγραψε τίποτα, μην κάνεις τίποτα
        if not title:
            return

        print(f"--- Ψάχνω στο ίντερνετ για: {title} ---")
        
        # ΚΑΛΟΥΜΕ ΤΟ ΠΡΑΓΜΑΤΙΚΟ BACKEND ΑΝΤΙ ΓΙΑ ΤΗΝ ΕΙΚΟΝΙΚΗ ΒΑΣΗ
        results = search_books_online(title)

        if results:
            print(f"Επιτυχία! Βρέθηκαν {len(results)} αποτελέσματα στο ίντερνετ.")
            # Εκτυπώνουμε το πρώτο αποτέλεσμα για να δούμε αν δουλεύει
            print("ΠΡΩΤΟ ΑΠΟΤΕΛΕΣΜΑ:", results[0]['title'], "-", results[0]['authors'])
            
            # Στο μέλλον, εδώ θα καλούμε την import_online_book για αποθήκευση
        else:
            print(f"Το βιβλίο '{title}' ΔΕΝ βρέθηκε. Άνοιγμα χειροκίνητης εισαγωγής...")
            ManualBookWindow(self)

if __name__ == "__main__":
    # Φτιάχνουμε ένα αόρατο/μικρό βασικό παράθυρο-γονιό για να πατήσει πάνω του το δικό μας
    app = ctk.CTk()
    app.geometry("10x10") 
    
    # Ανοίγουμε το παράθυρο προσθήκης
    window = AddBookWindow(app)
    
    # Ξεκινάμε την εφαρμογή
    app.mainloop()