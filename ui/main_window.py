from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Βιβλιοθήκη - Κεντρική Οθόνη")
        self.master.geometry("800x600")

        #Μεταφέρω εδώ τα widgets της αναζήτησης γιατί έχω μοιράσει τον υπόλοιπο χώρο στον πίνακα
        #στον πίνακα και το taskbar

        self.label_search= tk.Label(self.master, text="Αναζήτηση", font=("Arial", 12, "bold"))
        self.label_search.pack(pady=5)
        
        self.entry_search= tk.Entry(self.master, font=("Arial", 12))
        self.entry_search.pack(pady=5)
        self.entry_search.bind("<Return>", self.handle_search)

        
        self.search_button= tk.Button(self.master, text="Αναζήτηση", command= self.handle_search, font= ("Arial", 12, "italic"))
        self.search_button.pack(pady=10)
        
         
        #Δημιουργία πλειάδας για το σχέδιο του πίνακα με 6 στήλες()
        self.columns = ("id", "title", "author", "year", "avg_rate", "total_rates")
        #Δημιορυργία Treeview πίνακα
        self.tree = ttk.Treeview(self.master, columns = self.columns, show="headings")
        
        
        #Δημιουργία scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="top", fill="both", expand=True)


        #Δημιοργία τίτλων πρώτης σειράς στηλών
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text = "Τίτλος")
        self.tree.heading("author", text = "Συγγραφέας")
        self.tree.heading("year", text = "Χρονολογία")
        self.tree.heading("avg_rate", text = "Μέση βαθμολογία")
        self.tree.heading("total_rates", text = "Αξιολογήσεις")


        #Ρύθμιση πλάτους στηλών με τη μέθοδο column
        self.tree.column("id", width=30, anchor="center")
        self.tree.column("title", width=200, anchor="w")
        self.tree.column("author", width=150, anchor="w")
        self.tree.column("year", width=60, anchor="center")
        self.tree.column("avg_rate", width=50, anchor="center")
        self.tree.column("total_rates", width=80, anchor="center")


        #Δημιουργία frame κάτω για αναζήτηση online --ΠΕΔΙΟ ΚΟΥΜΠΙΩΝ--
        self.footer_frame = tk.Frame(self.master)
        self.footer_frame.pack(pady=20)

        #Add book. Αργότερα θα φτιαχτεί μια νέα συνάρτηση που θα ανοίγει τη φόρμα προσθήκης και θα καλείται με το κουμπί addBook
        self.addΒook_button =tk.Button (self.footer_frame, text = "Προσθήκη Βιβλίου", command=self.online_search, font = ("Arial" , 10, "italic") )
        self.addΒook_button.pack(side="left", padx=10)
        #placeholder προς το παρόν. θα μπει command που θα παίρνει τα δημοφιλή από μέθοδο βάσης
        self.popularBook_button =tk.Button(self.footer_frame, text = "Δημοφιλή", font = ("Arial" , 10, "italic"), command=lambda: print("Δημοφιλή βιβλία κουμπί"))
        self.popularBook_button.pack(side="left", padx=10)
        #placeholder προς το παρόν. θα μπει command που θα παίρνει τα αδιάβαστα από μέθοδο βάσης
        self.unreadBook_button =tk.Button(self.footer_frame, text = "Δημοφιλή αδιάβαστα", font = ("Arial" , 10, "italic"), command=lambda: print("Δημοφιλή αδιάβαστα κουμπί"))
        self.unreadBook_button.pack(side="left", padx=10)
        #καλεί τη μέθοδο open_details, η οποία θα παίρνει το ID και θα εμφανίζει τις λεπτομέρειες από τη βάση
        self.bookDetails_button=tk.Button(self.footer_frame, text ="Λεπτομέρειες", command=self.open_details, font = ("Arial" , 10, "italic") )
        self.bookDetails_button.pack(side="left", padx=10)


        #Δοκιμαστικά δεδομένα σε λεξικά μέσα σε λίστα. θα αντικατασταθούν με τα δεδομένα της βάσης
        self.books_data = [
                          {"id": 1, "title": "Όπλα, μικρόβια και ατσάλι", "author": "Jared Diamond", "year": "1997", "avg_rate": "4.6", "total_rates": "2000"},
                          {"id": 2, "title": "Big Bang", "author": "Simon Singh", "year": "2005", "avg_rate": "4.6", "total_rates": "1500"},
                          {"id": 3, "title": "Στα μυστικά του Βάλτου", "author": "Πηνελόπη Δέλτα", "year": "1937", "avg_rate": "4.8", "total_rates": "10000"},
                          {"id": 4, "title": "Ένα παιδί μετράει τ΄ άστρα", "author": "Μενέλαος Λουντέμης", "year": "1956", "avg_rate": "4.8", "total_rates": "7000"},
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
        

    #Συνάρτηση προσθήκης βιβλίου από το διαδίκτυο. Προς το παρόν δοκιμαστικά ένα print.
    def online_search(self):
        print(" Άνοιγμα παραθύρου online αναζήτησης")







if __name__ == "__main__":
    root = tk.Tk()           
    app = MainWindow(root)   
    root.mainloop()        



