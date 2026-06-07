import customtkinter as ctk
from ui.manual_book_window import ManualBookWindow
from services.import_service import search_books_online, import_online_book
from tkinter import messagebox

class AddBookWindow(ctk.CTkToplevel):
    def __init__(self,parent, on_add_success=None):
        super().__init__(parent)

        # Αποθηκεύουμε τη συνάρτηση ανανέωσης του κεντρικού παραθύρου (callback)
        # Θα την καλέσουμε στο τέλος για να εμφανιστεί το νέο βιβλίο στον πίνακα.
        self.on_add_success = on_add_success

        self.title("Προσθήκη Βιβλίου")
        self.geometry("800x800")
        # Το grab_set() κλειδώνει το από πίσω παράθυρο, 
        # ώστε ο χρήστης να πρέπει υποχρεωτικά να κλείσει πρώτα αυτό το βοηθητικό παραθυρο
        self.grab_set()
        # Αρχικοποίηση άδειας λίστας για την προσωρινή αποθήκευση των αποτελεσμάτων (έως 10)
        self.current_results = []
        
        # Σχεδίαση στοιχείων οθόνης
        self.create_widgets()
        
    def create_widgets(self):
        # 1. φτιάχνουμε ένα κεντρικό κουτί(frame) και του λέμε να πιάσει όλο το διαθέσιμο χώρο (expand=True)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(expand=True)

        # 2. Το weight τώρα το δίνουμε στο container, όχι στο self
        # Μοιράζουμε το χώρο ομοιόμορφα στις στήλες 0 και 1 (weight=1) για σωστή στοίχιση
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=1)

        #Στοιχεία αναζήτησης
        self.label_add_book=ctk.CTkLabel(self.main_container, text="Στοιχεία Αναζήτησης", font=("arial", 12, "bold"))
        self.label_add_book.grid(row=0, column=0, padx=5)
            
        self.entry_title = ctk.CTkEntry(self.main_container, placeholder_text="Τίτλος Βιβλίου", font=("arial", 12))
        self.entry_title.grid(row=1, column = 0, padx=5, pady=(10,5))
            
        self.entry_author = ctk.CTkEntry(self.main_container, placeholder_text="Συγγραφέας...")
        self.entry_author.grid(row=2, column = 0, padx=5, pady=(10,5))
        
        # Κουμπί που καλεί τη συνάρτηση search_and_add όταν πατηθεί
        self.button_search_add = ctk.CTkButton(self.main_container, text="Αναζήτηση και Προσθήκη", command = self.search_and_add)
        self.button_search_add.grid(row=3, column = 0, padx=5, pady=(10,5))
       
        #ΔΥΝΑΜΙΚΟ ΜΕΝΟΥ ΕΠΙΛΟΓΗΣ (Κρυφό στην αρχή)
        #Προσθήκη label και dropdown για να επιλέξει ο χρήστης ένα από τα αποτελέσματα
        self.label_dropdown = ctk.CTkLabel(self.main_container, text = "Επιλέξτε το σωστό βιβλίο:")
        self.option_menu = ctk.CTkOptionMenu(self.main_container, values=[], command=self.on_book_selected, width=250)

        #ΝΕΟ κουμπί για χειροκίνητη εισαγωγή 
        self.button_manual = ctk.CTkButton(self.main_container, text="Χειροκίνητη Προσθήκη", command=self.open_manual_window, fg_color="#6c757d", hover_color="#5a6268")
        self.button_manual.grid(row=6, column=0, padx=5, pady=(20,5))
    
    def search_and_add(self):
        # 1. Παίρνουμε Τίτλο και Συγγραφέα και τα ενώνουμε σε ένα query, κόβωντας τα περιττά κενά(strip)
        input_title = self.entry_title.get().strip()
        input_author = self.entry_author.get().strip()
        query = f"{input_title} {input_author}".strip()
        
        # Αν το πεδίο είναι εντελώς άδειο, βγάζουμε μήνυμα και σταματάμε την εκτέλεση (return)
        if not query:
            messagebox.showwarning("Προσοχή", "Παρακαλώ εισάγετε έναν όρο αναζήτησης.")
            return

        print(f"--- Ψάχνω στο ίντερνετ για: {query} ---")

        # Κλήση στο API μέσω του Backend (Import Service)
        results = search_books_online(query)
        # Ελέγχουμε αν το API επέστρεψε αποτελέσματα
        if not results:
            print(f"Το βιβλίο '{query}' ΔΕΝ βρέθηκε. Αυτόματο άνοιγμα χειροκίνητης...")
            # Καθαρίζουμε τα παλιά dropdown αν υπήρχαν
            self.label_dropdown.grid_forget()
            self.option_menu.grid_forget()
            
            messagebox.showinfo("Δεν βρέθηκε", "Δεν βρέθηκαν αποτελέσματα online. Παρακαλώ προσθέστε το βιβλίο χειροκίνητα.")
            
            # Αυτόματη μετάβαση στη χειροκίνητη προσθήκη
            self.open_manual_window()
        else:
            # Κρατάμε 10 αποτελέσματα στη μνήμη
            self.current_results = results[:10]
            print(f"Επιτυχία! Βρέθηκαν {len(results)} αποτελέσματα στο ίντερνετ.")
            
            # Αρχικοποίηση άδειας λίστας για να γεμίσουμε τις επιλογές του μενού
            dropdown_options = []
            
            # Βάζουμε enumerate για να έχουμε το 'i' (αρίθμηση)
            # enumerate: Μας δίνει τον αριθμό σειράς (i) και το περιεχόμενο (book) ταυτόχρονα
            for i, book in enumerate(self.current_results):
                # Χρήση.get() για ασφάλεια. Αν δεν υπάρχει κλειδί 'title', επιστρέφει το default.
                title = book.get('title', 'Άγνωστος Τίτλος')
                author = book.get('authors', '')
                if isinstance(author, list):
                    author = ", ".join(author)
                elif not author:
                    author = "Άγνωστος Συγγραφέας"
                
                # Προσθέτουμε αρίθμηση (i+1) για να ξεχωρίζουν τα ολόιδια βιβλία μεταξύ τους
                dropdown_options.append(f"{i + 1}. {title} - {author}")
            
            #Τροφοδοτούμε το μενού με τη λίστα και του βάζουμε την αρχική ετικέτα
            self.option_menu.configure(values=dropdown_options)
            self.option_menu.set("--- Κάντε μια επιλογή ---")
           
            # Εμφάνιση μενού και  ταμπέλας του στην οθόνη (grid)
            self.label_dropdown.grid(row=4, column=0, pady=(15,5))
            self.option_menu.grid(row=5, column=0, pady=5)
            
    def on_book_selected(self, choice):
        # Αν ο χρήστης κάνει κλικ στον αρχικό τίτλο του μενού, δεν κάνει καμία ενέργεια
        if choice == "--- Κάντε μια επιλογή ---":
            return
            
        # 1. Βρίσκουμε σε ποια θέση (0, 1, 2, 3) της λίστας αντιστοιχεί αυτό που πάτησε
        selected_index = self.option_menu._values.index(choice)
        
        # 2. Τραβάμε ολόκληρο το βιβλίο από τη "μνήμη"  χρησιμοποιώντας αυτή τη θέση
        selected_book = self.current_results[selected_index]
        
        print(f"Ο χρήστης επέλεξε το: {selected_book.get('title')}")


        # Αδειάζουμε τα κουτάκια (από τη θέση 0 έως το τέλος) και εισάγουμε τα νέα δεδομένα
        self.entry_title.delete(0, "end")
        self.entry_title.insert(0, selected_book.get('title',""))

        self.entry_author.delete(0, "end")
        self.entry_author.insert(0, selected_book.get('authors',""))
       
        # Προσπαθούμε να σώσουμε το επιλεγμένο βιβλίο στη βάση
        try:
            book_id=import_online_book(selected_book)
            print("Αποθηκεύτηκε επιτυχώς το βιβλίο με ID:", book_id)
            # Μετά την επιτυχή αποθήκευση, κρύβουμε ξανά το μενού επιλογής
            self.label_dropdown.grid_forget()
            self.option_menu.grid_forget()
            # Αν υπάρχει συνάρτηση ανανέωσης από το main_window, την καλούμε για να δείξει το νέο βιβλίο
            if self.on_add_success:
                self.on_add_success()
        except Exception as e:
            print(f"Σφάλμα κατά την αποθήκευση: {e}")

    def open_manual_window(self):
        # Κρύβουμε τα αποτελέσματα αν υπήρχαν
        self.label_dropdown.grid_forget()
        self.option_menu.grid_forget()
        # Ανοίγουμε το παράθυρο χειροκίνητης καταχώρησης. 
        # Περνάμε το self ως parent για να καταλάβει ότι ανήκει σε αυτό το παράθυρο.
        ManualBookWindow(self)


if __name__ == "__main__":
    # Φτιάχνουμε ένα αόρατο/μικρό βασικό παράθυρο-γονιό για να πατήσει πάνω του το δικό μας
    app = ctk.CTk()
    app.geometry("10x10") 
    
    # Ανοίγουμε το παράθυρο προσθήκης
    window = AddBookWindow(app)
    
    # Ξεκινάμε την εφαρμογή
    app.mainloop()