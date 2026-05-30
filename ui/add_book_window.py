import customtkinter as ctk
from manual_book_window import ManualBookWindow
from services.import_service import search_books_online, import_online_book

class AddBookWindow(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)

        self.title("Προσθήκη Βιβλίου")
        self.geometry("500x800")
        self.grab_set()
        self.create_widgets()
        
    def create_widgets(self):
        #αλλαγή # 1. φτιάχνουμε ένα κεντρικό "κουτί" και του λέμε να κάτσει ακριβώς στη μέση (expand=True)
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

    def search_and_add(self):
        #title = self.entry_title.get().strip().lower()
        
        #author = self.entry_author.get().strip().lower()

        #print(title, author)

        title = self.entry_title.get().strip().lower()
        author = self.entry_author.get().strip().lower()
       
        #Έλεγχος αν τα πεδία είναι κενά
        if not title:
            print("Παρακαλώ συμπληρώστε τουλάχιστον τον τίτλο.")
            return

        # Εικονική "βάση" για να τεστάρουμε τη λογική μας
        #mock_api_results = ["1984", "ο μικρος πριγκιπας"]
        #αντικατασταση mock dατα με ερωτηση στο api(internet)
        query = f"{title} {author}".strip()
        api_results= search_books_online(query)#κληση api

        if api_results:
            #Βρήκαμε κάτι. Παίρνουμε το 1ο αποτέλεσμα
            first_book = api_results[0]
            print(f"Βρέθηκε το βιβλίο: {first_book.get('title')}. Γίνεται αποθήκευση...")
            
            #καλώ τη βιβλιοθήκη για να το σώσει
            new_id = import_online_book(first_book)

            if new_id:
                print(f"Επιτυχία! Το βιβλίο αποθηκεύτηκε με ID: {new_id}")
                self.destroy()  # Κλείνει αυτόματα το παράθυρο
            else:
                print("Σφάλμα: Δεν μπόρεσε να αποθηκευτεί στη βάση.")

        else:
            # Δεν βρέθηκε τίποτα στο ίντερνετ
            print("Το βιβλίο ΔΕΝ βρέθηκε. Άνοιγμα χειροκίνητης εισαγωγής...")
            
            ManualBookWindow(self) # Η  γραμμή που ανοίγει το νέο  παράθυρο
           
          

if __name__ == "__main__":
    # Φτιάχνουμε ένα αόρατο/μικρό βασικό παράθυρο-γονιό για να πατήσει πάνω του δοκιμαστικα
    app = ctk.CTk()
    app.geometry("10x10") 
    
    # Ανοίγουμε το παράθυρο προσθήκης
    window = AddBookWindow(app)
    
    # Ξεκινάμε την εφαρμογή
    app.mainloop()