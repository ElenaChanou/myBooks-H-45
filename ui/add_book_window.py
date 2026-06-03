import customtkinter as ctk
from ui.manual_book_window import ManualBookWindow
from services.import_service import search_books_online, import_online_book

class AddBookWindow(ctk.CTkToplevel):
    def __init__(self,parent, on_add_success=None):
        super().__init__(parent)

        # Αποθηκεύουμε τη συνάρτηση ανανέωσης για να τη χρησιμοποιήσουμε στο τέλος
        self.on_add_success = on_add_success

        self.title("Προσθήκη Βιβλίου")
        self.geometry("500x800")
        self.grab_set()
        #προσθήκη λίστας με τα 4 πρώτα αποτελέσματα
        self.current_results = []
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

        #Προσθήκη label και dropdown για να επιλέξει ο χρήστης ένα από τα τέσσερα βιβλία
        self.label_dropdown = ctk.CTkLabel(self.main_container, text = "Επιλέξτε το σωστό βιβλίο:")
        self.option_menu = ctk.CTkOptionMenu(self.main_container, values=[], command=self.on_book_selected, width=250)

    
    def search_and_add(self):
        title = self.entry_title.get().strip()
        
        # Αν ο χρήστης δεν έγραψε τίποτα, μην κάνεις τίποτα
        if not title:
            return

        print(f"--- Ψάχνω στο ίντερνετ για: {title} ---")
        
        # ΚΑΛΟΥΜΕ ΤΟ ΠΡΑΓΜΑΤΙΚΟ BACKEND ΑΝΤΙ ΓΙΑ ΤΗΝ ΕΙΚΟΝΙΚΗ ΒΑΣΗ
        results = search_books_online(title)

        if results:
            self.current_results=results[:4]
            print(f"Επιτυχία! Βρέθηκαν {len(results)} αποτελέσματα στο ίντερνετ.")
            
            #θα χρησιμοποιήσουμε το .get(). Αυτό λέει στην Python: να φερει  τον συγγραφέα, αλλά αν δεν υπάρχει να μην κρασάρει απλά θα τυπώνει 'Άγνωστος'".
            
            dropdown_options = []
            for book in self.current_results:
                title = book.get('title', 'Αγνωστος συγγραφέας')
                author = book.get('authors', 'Άγνωστος Συγγραφέας')
                print(f"ΒΡΕΘΗΚΕ: {title} - {author}")
                dropdown_options.append(f"{title} ({author})")
            #Με το configure ταΐζουμε το κρυφό μας μενού με τη λίστα που μόλις φτιάξαμε. Το set του βάζει έναν προεπιλεγμένο τίτλο. Τέλος, οι εντολές grid παίρνουν το μενού και την ταμπέλα του από την "αφάνεια" και τα καρφιτσώνουν στην οθόνη.
            self.option_menu.configure(values=dropdown_options)
            self.option_menu.set("---Κάντε μια επιλογή---")
            ## Εμφανίζουμε το μενού στην οθόνη ΜΟΝΟ εφόσον βρέθηκαν βιβλία και το γεμίσαμε.
            self.label_dropdown.grid(row=4, column=0, pady=(15,5))
            self.option_menu.grid(row=5, column=0, pady=5)

            # Στο μέλλον, εδώ θα καλούμε την import_online_book για αποθήκευση
            
        else:
            print(f"Το βιβλίο '{title}' ΔΕΝ βρέθηκε. Άνοιγμα χειροκίνητης εισαγωγής...")
            #Αν ο χρήστης είχε ψάξει πριν κάτι σωστό (και το μενού ήταν ανοιχτό), και μετά ψάξει κάτι λάθος, δεν θέλουμε να βλέπει το παλιό μενού. Το grid_forget() είναι το αντίθετο του grid(): το εξαφανίζει από την οθόνη.
            self.label_dropdown.grid_forget()
            self.option_menu.grid_forget
            ManualBookWindow(self)

    def on_book_selected(self, choice):
        # Αν ο χρήστης κάνει κλικ στον αρχικό τίτλο του μενού, μην κάνεις τίποτα
        if choice == "--- Κάντε μια επιλογή ---":
            return
            
        # 1. Βρίσκουμε σε ποια θέση (0, 1, 2, 3) της λίστας αντιστοιχεί αυτό που πάτησε
        selected_index = self.option_menu._values.index(choice)
        
        # 2. Τραβάμε ολόκληρο το βιβλίο από τη "μνήμη" μας χρησιμοποιώντας αυτή τη θέση
        selected_book = self.current_results[selected_index]
        
        print(f"Ο χρήστης επέλεξε το: {selected_book.get('title')}")

        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, selected_book.get('title',""))

        self.entry_author.delete(0, "end")
        self.entry_author.insert(0, selected_book.get('title',""))

        try:
            book_id=import_online_book(selected_book)
            print("Αποθηκεύτηκε επιτυχώς το βιβλίο με ID:", book_id)
            self.label_dropdown.grid_forget()
            self.option_menu.grid_forget()
            #Ενημέρωση του κεντρικού να ξαναδιαβάσει τη βάση
            if self.on_add_success:
                self.on_add_success()
        except Exception as e:
            print(f"Σφάλμα κατά την αποθήκευση: {e}")



if __name__ == "__main__":
    # Φτιάχνουμε ένα αόρατο/μικρό βασικό παράθυρο-γονιό για να πατήσει πάνω του το δικό μας
    app = ctk.CTk()
    app.geometry("10x10") 
    
    # Ανοίγουμε το παράθυρο προσθήκης
    window = AddBookWindow(app)
    
    # Ξεκινάμε την εφαρμογή
    app.mainloop()