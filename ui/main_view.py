import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MainScreen(tk.Frame):

    def __init__(self, parent, manager):
        #ΚΑΛΟΥΜΕ ΤΟΝ CONSTRUCTOR ΤΗΣ ΓΟΝΙΚΗΣ ΚΛΑΣΗΣ (tk.Frame) ΓΙΑ ΝΑ ΕΧΟΥΜΕ ΟΛΗ ΤΗ ΛΕΙΤΟΥΡΓΙΚΟΤΗΤΑ ΕΝΟΣ FRAME
        super().__init__(parent)
        self.manager = manager 
        
        # Ετικέτα
        self.label_search = tk.Label(self, text="Αναζήτηση Βιβλίου", font=("Arial", 12, "bold"))
        self.label_search.pack(pady=5)
        
        # Πεδίο αναζήτησης και κουμπί
        self.entry_search = tk.Entry(self, font=("Arial", 12))
        self.entry_search.pack(pady=5)
        self.entry_search.bind("<Return>", self.handle_search)
        
        # Κουμπί αναζήτησης
        self.search_button = tk.Button(self, text="Αναζήτηση", command=self.handle_search, font=("Arial", 12, "italic"))
        self.search_button.pack(pady=5)
         
        # Προσθήκη πίνακα (Treeview) για εμφάνιση των δημοφιλέστερων βιβλίων στο main screen
        # Μορφοποίηση του πίνακα με στήλες για τίτλο, συγγραφέα, έτος, μέση βαθμολογία και πλήθος αξιολογήσεων
        self.table_title = tk.Label(self, text="Λίστα Βιβλίων: Κορυφαία Βιβλία", font=("Arial", 11, "italic"), fg="gray")
        self.table_title.pack(pady=(10, 0))

        self.columns = ("id", "title", "author", "year", "avg_rate", "total_rates")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="top", fill="both", expand=True, padx=20, pady=5)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Τίτλος")
        self.tree.heading("author", text="Συγγραφέας")
        self.tree.heading("year", text="Χρονολογία")
        self.tree.heading("avg_rate", text="Μέση βαθμολογία")
        self.tree.heading("total_rates", text="Αξιολογήσεις")

        self.tree.column("id", width=30, anchor="center")
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("author", width=150, anchor="w")
        self.tree.column("year", width=60, anchor="center")
        self.tree.column("avg_rate", width=50, anchor="center")
        self.tree.column("total_rates", width=80, anchor="center")

        # --- FOOTER & ΚΟΥΜΠΙΑ ---
        self.footer_frame = tk.Frame(self)
        self.footer_frame.pack(pady=10)
        
        # Κρατήσαμε μόνο το κουμπί των λεπτομερειών στο κέντρο
        self.bookDetails_button = tk.Button(self.footer_frame, text="Προβολή Λεπτομερειών", command=self.open_details, bg="blue", fg='white', width=20)
        self.bookDetails_button.pack(side="left", padx=10)

        self.Add_book_button = tk.Button(self, text="Προσθήκη βιβλίου", command=self.manager.show_add, bg='blue', fg='white', width=20)
        self.Add_book_button.pack(side="right", pady=15, padx=20)

        self.Logout_button = tk.Button(self, text="Αποσύνδεση", command=self.manager.show_login, bg='blue', fg='white', width=20)
        self.Logout_button.pack(side="left", pady=15, padx=20)

        self.load_top_books()

    def load_top_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        self.table_title.config(text="Λίστα Βιβλίων: Κορυφαία Βιβλία")

        try:
            all_books = self.manager.db_manager.get_all_books_with_stats()
            
            # Ταξινομούμε τα βιβλία με βάση τη βαθμολογία (όπως συζητήσαμε πριν)
            top_books = sorted(all_books, key=lambda b: b['avg_rate'] or 0, reverse=True)
            
            # Εισαγωγή των Top 10 στον πίνακα
            for book in top_books[:10]:
                self.tree.insert("", "end", values=(
                    book['book_id'], 
                    book['title'], 
                    book['authors'], 
                    book['year'], 
                    book['avg_rate'], 
                    book['total_rates']
                ))
        except AttributeError:
            print("Πληροφορία: Η σύνδεση με τη βάση (self.manager.db) δεν είναι ακόμα έτοιμη.")

    def handle_search(self, event=None):
        query = self.entry_search.get().strip()
        
        if query:
            self.table_title.config(text=f'Αποτελέσματα Αναζήτησης: "{query}"')
            
            # 1. Καθαρισμός του πίνακα (Clear the Treeview)
            for row in self.tree.get_children():
                self.tree.delete(row)
                
            # 2. Αναζήτηση στη βάση δεδομένων
            try:
                # Προϋποθέτει ότι υπάρχει η μέθοδος search_books στην κλάση Database_Manager
                search_results = self.manager.db_manager.search_books(query)
                
                # 3. Εισαγωγή των αποτελεσμάτων στον πίνακα
                for book in search_results:
                    self.tree.insert("", "end", values=(
                        book['book_id'], 
                        book['title'], 
                        book['author'], 
                        book['year'], 
                        f"{book['avg_rate']:.1f}" if book['avg_rate'] else "N/A", 
                        book['total_rates']
                    ))
            except Exception as e:
                messagebox.showerror("Σφάλμα Αναζήτησης", f"Υπήρξε πρόβλημα κατά την αναζήτηση:\n{e}")
        else:
            self.load_top_books()

    def open_details(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Προσοχή", "Παρακαλώ επιλέξτε ένα βιβλίο από τη λίστα για να δείτε λεπτομέρειες.")
            return
        
        item_data = self.tree.item(selected_item[0])
        book_id = item_data['values'][0]
        
        print(f"Άνοιγμα λεπτομερειών για το βιβλίο με ID: {book_id}")
        self.manager.show_book_details(book_id)