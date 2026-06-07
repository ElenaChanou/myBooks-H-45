from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from ui.book_details_window import BookDetailsWindow
import customtkinter as ctk
from ui.add_book_window import AddBookWindow

# Εισαγωγή όλων των απαραίτητων λειτουργιών (Services) που επικοινωνούν με τη Βάση Δεδομένων
from services.book_service import list_all_books, get_book_details
from services.book_service import popular_books, unread_popular_books, delete_book 

class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Ο controller (κεντρική εφαρμογή myBooks) χρειάζεται για να αλλάζουμε οθόνες 
        # (π.χ. επιστροφή στο login) και για να ξέρουμε ποιος χρήστης είναι συνδεδεμένος.
        self.controller = controller
        
        # gRID Παραθύρου
        # Ρυθμίζουμε το κεντρικό πλέγμα (Grid). 
        # Το weight=1 στη γραμμή 1 σημαίνει ότι ο πίνακας (treeview) θα παίρνει όλον τον διαθέσιμο χώρο 
        # αν μεγαλώσουμε το παράθυρο, αφήνοντας σταθερά τα κουμπιά πάνω και κάτω.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Πάνω μέρος. πεδία αναζητησης και αποσύνδεσης
        self.search_frame = ctk.CTkFrame(self)
        # sticky="ew": Απλώνεται από αριστερά (West) έως δεξιά (East)
        self.search_frame.grid(row=0, column=0, pady=10, sticky="ew") 
        # Δίνουμε weight στη στήλη 3 για να σπρώξει το κουμπί αποσύνδεσης και το καλωσόρισμα τέρμα δεξιά
        self.search_frame.grid_columnconfigure(3, weight=1)
        
        self.label_search = ctk.CTkLabel(self.search_frame, text="Αναζήτηση", font=("Arial", 12, "bold"))
        self.label_search.grid(row=0, column=0, padx=5)
        
        self.entry_search = ctk.CTkEntry(self.search_frame, font=("Arial", 12))
        self.entry_search.grid(row=0, column=1, padx=5)
        # bind("<Return>"): Επιτρέπει στον χρήστη να πατήσει το πλήκτρο "Enter" για να ψάξει, αντί να πατάει το κουμπί
        self.entry_search.bind("<Return>", self.handle_search)
        
        self.search_button = ctk.CTkButton(self.search_frame, text="Αναζήτηση", command=self.handle_search, font=("Arial", 12, "italic"))
        self.search_button.grid(row=0, column=2, padx=5)
        
        # Ετικέτα καλωσορίσματος και Κουμπί Αποσύνδεσης (Μπαίνουν τέρμα δεξιά)
        self.welcome_label = ctk.CTkLabel(self.search_frame, text="Καλώς ήρθες!", font=("Arial", 12), text_color="gray" )
        self.welcome_label.grid(row=0, column=4, padx=10, pady=10)

        self.logout_button = ctk.CTkButton(self.search_frame, text="Αποσύνδεση", command=self.controller.show_login_screen)
        self.logout_button.grid(row=0, column=5, padx=10, pady=10)

        # Κνετρικό μέρος
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, sticky="nsew", padx=20)

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Δημιουργία πλειάδας (tuple) για τις 6 στήλες του πίνακα
        self.columns = ("id", "title", "author", "year", "avg_rate", "total_rates")

        # Ρύθμιση στυλ (Dark Mode) για τον πίνακα (το Treeview είναι από το κλασικό tkinter/ttk)
        style = ttk.Style()
        style.theme_use("default")

        # Χρώματα για το σώμα του πίνακα
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#2b2b2b",
                        borderwidth=0)
                        
        # Χρώμα που παίρνει η γραμμή όταν την επιλέγει ο χρήστης
        style.map('Treeview', background=[('selected', '#1f538d')])

        # Χρώμα για τις επικεφαλίδες των στηλών
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        font=("arial", 11, "bold"),
                        borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3c3f41')])

        # Δημιουργία του αντικειμένου Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show="headings")
        
        # Δημιουργία μπάρας κύλισης (Scrollbar) και σύνδεσή της με τον πίνακα (yview)
        self.scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Τοποθέτηση του πίνακα και της μπάρας στο Frame τους
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Δημιουργία των τίτλων (Επικεφαλίδες)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Τίτλος")
        self.tree.heading("author", text="Συγγραφέας")
        self.tree.heading("year", text="Χρονολογία")
        self.tree.heading("avg_rate", text="Μέση βαθμολογία")
        self.tree.heading("total_rates", text="Αξιολογήσεις")

        # Ρύθμιση πλάτους στηλών και στοίχισης (anchor="center" για κεντράρισμα κειμένου)
        self.tree.column("id", width=30, anchor="center")
        self.tree.column("title", width=220, anchor="center")
        self.tree.column("author", width=180, anchor="center")
        self.tree.column("year", width=100, anchor="center")
        self.tree.column("avg_rate", width=200, anchor="center")
        self.tree.column("total_rates", width=100, anchor="center")

        # Κάτω μέρος με κουμπιά ενεργειών
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent") 
        self.footer_frame.grid(row=2, column=0, pady=20, sticky="ew") 
        
        # Λέμε στις 5 στήλες των κουμπιών να μοιραστούν τον χώρο ίσα (weight=1) για να απλωθούν όμορφα
        self.footer_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.addBook_button = ctk.CTkButton(self.footer_frame, text="Προσθήκη Βιβλίου", command=self.open_add_book, font=("Arial", 10, "italic"))
        self.addBook_button.grid(row=0, column=0, padx=10, pady=20)

        self.popularBook_button = ctk.CTkButton(self.footer_frame, text="Δημοφιλή", font=("Arial", 10, "italic"), command=self.handle_popular)
        self.popularBook_button.grid(row=0, column=1, padx=10, pady=10)

        self.unreadBook_button = ctk.CTkButton(self.footer_frame, text="Δημοφιλή αδιάβαστα", font=("Arial", 10, "italic"), command=self.handle_popular_unread)
        self.unreadBook_button.grid(row=0, column=2, padx=10, pady=10)

        # Κουμπί που ανοίγει τις λεπτομέρειες του βιβλίου
        self.bookDetails_button = ctk.CTkButton(self.footer_frame, text="Λεπτομέρειες", command=self.open_details, font=("Arial", 10, "italic"), fg_color="#28a745", hover_color="#218838")
        self.bookDetails_button.grid(row=0, column=3, padx=10, pady=10)

        self.deleteBook_button = ctk.CTkButton(self.footer_frame, text="Διαγραφή", command=self.handle_delete_book, font=("Arial", 10, "italic"), fg_color="#dc3545", hover_color="#c82333")
        self.deleteBook_button.grid(row=0, column=4, padx=10, pady=10)

        # Αρχικοποίηση δεδομένων
        self.refresh_books_list() # Κατεβάζει τα βιβλία με το που ανοίγει η οθόνη
        
        # Συνδέουμε ένα "γεγονός" (Event): Όποτε ο χρήστης κάνει κλικ σε μια γραμμή, τρέχει η on_item_selected
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.selected_book_id = None
    
    def update_table(self, data):
        """Καθαρίζει τον πίνακα και τον γεμίζει ξανά με τα νέα δεδομένα (data)"""
        # 1. Καθαρισμός υπαρχόντων αντικειμένων (για να μην φαίνονται διπλά)
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 2. Ασφαλής εισαγωγή με get() ώστε να μην κρασάρει το πρόγραμμα αν λείπει κάποιο κλειδί από το λεξικό
        for book in data:
            self.tree.insert("", "end", values=(
                book.get("book_id", book.get("id", "")), # Ψάχνει είτε book_id είτε id
                book.get("title", "Άγνωστος Τίτλος"),
                book.get("authors", book.get("author", "")), # Ψάχνει είτε authors είτε author
                book.get("year", ""),
                book.get("avg_rate", 0),
                book.get("total_rates", 0)
            ))
    
    def on_item_selected(self, event):
        """Εκτελείται όταν ο χρήστης κάνει κλικ σε μια γραμμή του πίνακα"""
        selected_item = self.tree.selection()
        if selected_item:
            item_data = self.tree.item(selected_item)['values']
            # Αποθηκεύουμε το ID (πρώτη στήλη, άρα θέση [0]) του επιλεγμένου βιβλίου
            self.selected_book_id = item_data[0]
            print(f"Επιλέχθηκε το βιβλίο με ID: {self.selected_book_id}")

    def handle_search(self, event=None):
        """Φιλτράρει τα βιβλία ανάλογα με το τι έγραψε ο χρήστης"""
        query = self.entry_search.get().lower().strip()
        
        # Καλούμε τη βάση για να πάρουμε τη λίστα με όλα τα πραγματικά βιβλία
        all_books = list_all_books()

        # Αν το πεδίο είναι άδειο, δείξε πάλι όλα τα βιβλία
        if not query:
            self.update_table(all_books)
            return
        
        print(f"Αναζήτηση για: {query}")
    
        filtered_books = []
        for book in all_books:
            # Παίρνουμε τίτλο και συγγραφέα με ασφάλεια
            title = book.get("title", "").lower()
            author = book.get("authors", "").lower()
            
            # Έλεγχος αν η λέξη της αναζήτησης υπάρχει μέσα στον τίτλο ή στον συγγραφέα
            if query in title or query in author:
                filtered_books.append(book)

        # Ενημερώνουμε τον πίνακα μόνο με τα αποτελέσματα που ταίριαξαν
        self.update_table(filtered_books)

    def handle_popular(self):
        """Φέρνει τα 10 κορυφαία βιβλία (Top 10) από το Service"""
        books = popular_books(limit=10)
        self.update_table(books) 

    def handle_popular_unread(self):
        """Φέρνει τα 10 κορυφαία που δεν έχει διαβάσει (ούτε βαθμολογήσει) ο τρέχων χρήστης"""
        # Παίρνουμε το ID του συνδεδεμένου χρήστη από τον controller
        user_id = self.controller.current_user.get('id')
        books = unread_popular_books(user_id, limit=10)
        self.update_table(books)

    def open_details(self):
        """Ανοίγει την οθόνη με τις λεπτομέρειες του βιβλίου και τα σχόλια"""
        # Ρωτάμε το Treeview ποιο στοιχείο έχει επιλέξει ο χρήστης
        selected_item = self.tree.selection() 

        # Αν η πλειάδα είναι άδεια (δεν επέλεξε κάτι)
        if not selected_item:
            messagebox.showwarning("Προσοχή", "Επίλεξε ένα βιβλίο πρώτα!")
        else:
            # Παίρνουμε τα δεδομένα και απομονώνουμε το ID
            item_data = self.tree.item(selected_item)['values']
            book_id = item_data[0]
            print(f"Άνοιγμα λεπτομερειών για το βιβλίο με ID: {book_id}")
            
            # Ζητάμε τα πλήρη δεδομένα (συμπεριλαμβανομένων εξωφύλλων και σχολίων) από το Service
            book_to_open = get_book_details(book_id)
            
            #Μηχανισμός εναλλαγής σελίδας
            # 1. Κρύβουμε το τρέχον παράθυρο (Main Window) χωρίς να το διαγράψουμε εντελώς
            self.pack_forget() 
            
            # 2. Φορτώνουμε τις λεπτομέρειες στο ίδιο κεντρικό παράθυρο (controller)
            # Δίνουμε την refresh_books_list ως on_save για να ανανεωθούν τα δεδομένα όταν κλείσει
            self.details_frame = BookDetailsWindow(master=self.controller, book_data=book_to_open, on_save=self.refresh_books_list)
            self.details_frame.pack(fill="both", expand=True) 

    def handle_delete_book(self):
        """Διαγράφει το επιλεγμένο βιβλίο και τις αξιολογήσεις του οριστικά"""
        selected_item = self.tree.selection()

        # Έλεγχος αν δεν έχει επιλεγεί κάτι
        if not selected_item:
            messagebox.showwarning("Προσοχή", "Επίλεξε ένα βιβλίο για διαγραφή.")
            return

        # Παίρνουμε τα δεδομένα της επιλεγμένης γραμμής
        item_data = self.tree.item(selected_item)['values']
        book_id = item_data[0]
        book_title = item_data[1]

        #  παράθυρο επιβεβαίωσης δαγραφής
        confirm = messagebox.askyesno(
            "Επιβεβαίωση Διαγραφής", 
            f"Είσαι σίγουρος ότι θέλεις να διαγράψεις το βιβλίο:\n\n'{book_title}';\n\n(Θα διαγραφούν οριστικά και οι αξιολογήσεις του)"
        )

        # Αν ο χρήστης πατήσει ναι = (True)
        if confirm:
            try:
                # Καλούμε το Service για τη διαγραφή
                success = delete_book(book_id)

                if success:
                    messagebox.showinfo("Επιτυχία", "Το βιβλίο διαγράφηκε επιτυχώς!")
                    # Ανανεώνουμε τον πίνακα για να εξαφανιστεί το βιβλίο οπτικά αμέσως
                    self.refresh_books_list()
                else:
                    messagebox.showerror("Σφάλμα", "Το βιβλίο δεν μπόρεσε να διαγραφεί.")
                    
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Προέκυψε πρόβλημα: {e}")

    def open_add_book(self):
        """Ανοίγει το παράθυρο αναζήτησης και προσθήκης νέου βιβλίου (API)"""
        AddBookWindow(self, on_add_success=self.refresh_books_list)
        
    def refresh_books_list(self):
        """Διαβάζει ξανά τα βιβλία από τη βάση και ενημερώνει την οθόνη"""
        # 1. Ο  μηχανισμός καθαρισμού για να μη φαίνονται διπλά
        # μέσα στην update_table, αλλά καλούμε τη Βάση για να πάρουμε τα πιο φρέσκα δεδομένα!
        books_data = list_all_books()
        
        # 2. Τα στέλνουμε στην update_table για να τα σχεδιάσει σωστά
        self.update_table(books_data)
        print("Ο πίνακας ενημερώθηκε με τα τελευταία δεδομένα από τη Βάση!")


if __name__ == "__main__":
    # --- ΚΩΔΙΚΑΣ ΜΟΝΟ ΓΙΑ ΤΕΣΤΙΝΓΚ ΤΟΥ MAIN WINDOW ---
    # Διορθώθηκε ώστε να φορτώνει το MainFrame και όχι το BookDetailsWindow
    
    root = ctk.CTk()
    root.geometry("1000x600")
    root.title("Τεστ Κεντρικού Παραθύρου")
    
    # Φτιάχνουμε έναν ψεύτικο "controller" class για να μην κρασάρει το πρόγραμμα όταν ψάχνει το current_user
    class FakeController(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.current_user = {"id": 1, "username": "test_user"}
            
        def show_login_screen(self):
            print("Επιστροφή στο Login!")
            
    test_controller = FakeController()
    
    # Εκκίνηση του Frame
    app = MainFrame(parent=test_controller, controller=test_controller)
    app.pack(fill="both", expand=True)
    
    test_controller.mainloop()