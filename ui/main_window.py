from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from book_details_window import BookDetailsWindow
import customtkinter as ctk
from add_book_window import AddBookWindow


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.controller=controller
        #self.master = master
        #self.master.title("Βιβλιοθήκη - Κεντρική Οθόνη")
        #self.master.geometry("800x600")

        #Μεταφέρω εδώ τα widgets της αναζήτησης γιατί έχω μοιράσει τον υπόλοιπο χώρο στον πίνακα
        #στον πίνακα και το taskbar

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.search_frame=ctk.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, pady=10, sticky="ew")
        self.search_frame.grid_columnconfigure(3, weight=1)
        ####

        self.label_search= ctk.CTkLabel(self.search_frame, text="Αναζήτηση", font=("Arial", 12, "bold"))
        self.label_search.grid(row=0, column=0, padx=5)
        
        self.entry_search= ctk.CTkEntry(self.search_frame, font=("Arial", 12))
        self.entry_search.grid(row=0, column=1, padx=5)
        self.entry_search.bind("<Return>", self.handle_search)

        
        self.search_button= ctk.CTkButton(self.search_frame, text="Αναζήτηση", command= self.handle_search, font= ("Arial", 12, "italic"))
        self.search_button.grid(row=0, column=2, padx=5)
        
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, sticky="nsew" ,padx=20)

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        #Δημιουργία πλειάδας για το σχέδιο του πίνακα με 6 στήλες()
        self.columns = ("id", "title", "author", "year", "avg_rate", "total_rates")

        #Ρύθμιση στυλ dark mode για το πίνακα
        style=ttk.Style()
        style.theme_use("default")

        #Xρώματα για το σώμα του πίνακα
        style.configure("Treeview", background="#2b2b2b", 
                                    foreground="white",
                                    rowheight=30,
                                    fieldbackground="#2b2b2b",
                                    borderwidth=0)
        #Χρώμα κατά την επιλογή του βιβλίου
        style.map('Treeview', background=[('selected', '#1f538d')])

        #Χρώμα για επικεφαλίδα
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        font=("arial", 11, "bold"),
                        borderwidth=0)
        style.map("Treeview.Heading", background=[('active', '#3c3f41')])

        #Δημιορυργία Treeview πίνακα
        self.tree = ttk.Treeview(self.tree_frame, columns = self.columns, show="headings")
        
        
        #Δημιουργία scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        #Τοποθετώ τον πίνακα και τη μπάρα στο tree_frame
        self.tree.grid(row=0,column=0,sticky="nsew")
        self.scrollbar.grid(row=0,column=1,sticky="ns")

       # self.scrollbar.pack(side="right", fill="y")
        #self.tree.pack(side="top", fill="both", expand=True)


        #Δημιοργία τίτλων πρώτης σειράς στηλών
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text = "Τίτλος")
        self.tree.heading("author", text = "Συγγραφέας")
        self.tree.heading("year", text = "Χρονολογία")
        self.tree.heading("avg_rate", text = "Μέση βαθμολογία")
        self.tree.heading("total_rates", text = "Αξιολογήσεις")


        #Ρύθμιση πλάτους στηλών με τη μέθοδο column
        self.tree.column("id", width=30, anchor="center")
        self.tree.column("title", width=220, anchor="center")
        self.tree.column("author", width=180, anchor="center")
        self.tree.column("year", width=100, anchor="center")
        self.tree.column("avg_rate", width=200, anchor="center")
        self.tree.column("total_rates", width=100, anchor="center")


        # Δημιουργία frame κάτω για αναζήτηση online --ΠΕΔΙΟ ΚΟΥΜΠΙΩΝ--
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent") 
        self.footer_frame.grid(row=2, column=0, pady=20, sticky="ew") 
        
        # Λέμε στις 4 στήλες των κουμπιών να μοιραστούν τον χώρο ίσα (weight=1)
        self.footer_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        

        #Add book. Αργότερα θα φτιαχτεί μια νέα συνάρτηση που θα ανοίγει τη φόρμα προσθήκης και θα καλείται με το κουμπί addBook
        #Μέσα στο footer βάζω τα κουμπιά στη σειρά (στηλες 0,1,2,3)

        self.addBook_button =ctk.CTkButton (self.footer_frame, text = "Προσθήκη Βιβλίου", command=self.open_add_book, font = ("Arial" , 10, "italic") )
        self.addBook_button.grid(row=0,column=0, padx=10, pady=20)

        #placeholder προς το παρόν. θα μπει command που θα παίρνει τα δημοφιλή από μέθοδο βάσης
        self.popularBook_button =ctk.CTkButton(self.footer_frame, text = "Δημοφιλή", font = ("Arial" , 10, "italic"), command=lambda: print("Δημοφιλή βιβλία κουμπί"))
        self.popularBook_button.grid(row=0,column=1,padx=10, pady=10)

        #placeholder προς το παρόν. θα μπει command που θα παίρνει τα αδιάβαστα από μέθοδο βάσης
        self.unreadBook_button =ctk.CTkButton(self.footer_frame, text = "Δημοφιλή αδιάβαστα", font = ("Arial" , 10, "italic"), command=lambda: print("Δημοφιλή αδιάβαστα κουμπί"))
        self.unreadBook_button.grid(row=0,column=2,padx =10,pady=10)

        #καλεί τη μέθοδο open_details, η οποία θα παίρνει το ID και θα εμφανίζει τις λεπτομέρειες από τη βάση
        self.bookDetails_button=ctk.CTkButton(self.footer_frame, text ="Λεπτομέρειες", command=self.open_details, font = ("Arial" , 10, "italic"), fg_color = "#28a745", hover_color="#218838")
        self.bookDetails_button.grid(row=0,column=3,padx =10,pady=10)

        self.logout_button = ctk.CTkButton(self.search_frame, text="Αποσύνδεση", command=self.controller.show_login_screen)
        self.logout_button.grid(row=0, column=5,padx=10, pady=10)

        self.welcome_label=ctk.CTkLabel(self.search_frame, text= "Καλώς ήρθες!", font=("Arial", 12), text_color="gray" )
        self.welcome_label.grid(row=0, column=4, padx=10,pady=10)


        #Δοκιμαστικά δεδομένα σε λεξικά μέσα σε λίστα. θα αντικατασταθούν με τα δεδομένα της βάσης
        self.books_data = [
                          {"id": 1, "title": "Όπλα, μικρόβια και ατσάλι", "author": "Jared Diamond", "year": "1997", "avg_rate": "4.6", "total_rates": "2000"},
                          {"id": 2, "title": "Big Bang", "author": "Simon Singh", "year": "2005", "avg_rate": "4.6", "total_rates": "1500"},
                          {"id": 3, "title": "Στα μυστικά του Βάλτου", "author": "Πηνελόπη Δέλτα", "year": "1937", "avg_rate": "4.8", "total_rates": "10000"},
                          {"id": 4, "title": "Ένα παιδί μετράει τ΄ άστρα", "author": "Μενέλαος Λουντέμης", "year": "1956", "avg_rate": "4.8", "total_rates": "7000", "cover_url": "https://covers.openlibrary.org/b/id/8225261-L.jpg"},
                          {"id": 5, "title": "Ο καπετάν Μιχάλης", "author": "Νίκος Καζαντζάκης", "year": "1953", "avg_rate": "4.9", "total_rates": "9200"},
                          {"id": 6, "title": "Η μεγάλη χίμαιρα", "author": "Μ.Καραγάτσης", "year": "1936", "avg_rate": "4.6", "total_rates": "6850"}
                        ]
        #εδώ θα γίνει η σύνδεση με τη συνάρτηση της βάσης
        self.update_table(self.books_data)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)
        
    def update_table(self,data):

        #Καθαρισμός υπαρχόντων αντικειμένων
        for item in self.tree.get_children():
            self.tree.delete(item)


        #Γέμισμα για κάθε λεξικό με την προσωρινή παράμετρο data που παίρνει τη λίστα self.books_data
        #Η self.books.data περνάει ως data και στο for παίρνει το κάθε λεξικό και περνάει στη μεταβλητή book
        #Με το end εισαγωγουμε στο τέλος το νέο βιβλίο
        for book in data:
            self.tree.insert("", "end", values=(
                book["id"],
                book["title"],
                book["author"],
                book["year"],
                book["avg_rate"],
                book["total_rates"]
            ))
    
    def on_item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_data = self.tree.item(selected_item)['values']
            print(f"Επιλέχθηκε: {item_data}")

    def handle_search(self, event=None):
        #μετατρέπουμε το κείμενο από το entry σε μικρά με το lower()
        query = self.entry_search.get().lower()
        

        #προστασία αν πατηθείτο search χωρίς κείμενο
        if not query:
            self.update_table(self.books_data)
            return
        
    
        print(f"Αναζήτηση για: {query}")
    
        #Προσωρινή λίστα για αποθήκευση όσων ταιριάζουν
        filtered_books = []
        for book in self.books_data:
             #Έλεγχος αν η λέξη της ααζήτησης υπάρχει σε τίτλο ή συγγραφέα
            if query in book["title"].lower() or query in book["author"].lower():
                filtered_books.append(book)#Λίστα αποτελεσμάτων αν ικανοποιείται το if

        self.update_table(filtered_books)#κλήση της update_table με τα φιλτραρισμένα βιβλία

    def open_details(self):
        selected_item = self.tree.selection() #με τη μέθοδο seelectio() ρωτάμε ποιο στοιχείο επέλεξε ο χρήστης

        if not selected_item:
            messagebox.showwarning("Προσοχή", "\nΕπίλεξε βιβλίο")# αν η πλειάδα είναι άδεια, δηλαδή δεν επιλέξει κάτι  ο χρήστης
        else:#παίρνουμε την επιλογή, όλα τα δεδομένα και παίρνουμε το πρωτο στοιχείο ID
            item_data = self.tree.item(selected_item)['values']
            book_id = item_data[0]
            print(f"Άνοιγμα λεπτομερειών για το βιβλίο με ID: {book_id}")
            book_to_open = next(b for b in self.books_data if b["id"]==book_id)
           
           
            #ΝΕΟΣ ΚΩΔΙΚΑΣ ΓΙΑ ΕΝΑΛΛΑΓΗ ΣΕΛΙΔΑΣ (FRAME) ---
            self.pack_forget() # 1. Κρύβουμε το τρέχον παράθυρο (Main Window)
            
            #  Φορτώνουμε τις λεπτομέρειες και τις περνάμε στον Controller
             #Σύνδεση με την class BookDetails
            self.details_frame = BookDetailsWindow(master=self.controller, book_data=book_to_open, on_save=self.refresh_books_list)
            self.details_frame.pack(fill="both", expand=True) 


    def open_add_book(self):
        AddBookWindow(self)
        
    

    #Μηχανισμός διαγραφής για να μην φαίνονται διπλά τα βιβλία μετά τη φόρτωση
    def refresh_books_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    #ξαναγεμίζουμε τον πίνακα από τη λίστα self.books_data προς το παρόν
        for book in self.books_data:
            self.tree.insert("","end", values=(book["id"], book.get("title",""), book.get("author",""), book.get("year",""), book.get("avg_rate", 0), book.get("total_rates",0)))
        print("Ο πίνακας καθαρίστηκε και ενημερώθηκε")










if __name__ == "__main__":
    #ψεύτικος manager για να παρακάμπτει τη show_login_screen που βρίσκεται στον manager
    class DummyController:
        def show_login_screen(self):
            print("To κουμπί αποσύνδεσης πατήθηκε!(Test mode)")
    root = tk.Tk()
    dummy_manager = DummyController()
    app = MainFrame(root, dummy_manager) #ο ψεύτικος controller στην θέση της παραμέτρου controller που περιμένει η MainFrame
    app.pack(fill="both", expand=True)
    root.mainloop()



