import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class AddBookScreen(tk.Frame):
    '''Η κλάση AddBookScreen είναι ενα Tkinter Frame...'''
    def __init__(self, parent, manager):
        #ΚΑΛΟΥΜΕ ΤΟΝ CONSTRUCTOR ΤΗΣ ΓΟΝΙΚΗΣ ΚΛΑΣΗΣ (tk.Frame) ΓΙΑ ΝΑ ΕΧΟΥΜΕ ΟΛΗ ΤΗ ΛΕΙΤΟΥΡΓΙΚΟΤΗΤΑ ΕΝΟΣ FRAME
        super().__init__(parent)
        #ΑΠΟΘΗΚΕΥΟΜΕ ΤΟΝ ΔΙΑΧΕΙΡΙΣΤΗ (Manager) ΓΙΑ ΝΑ ΤΟΝ ΕΧΕΙ ΤΟ ΑΝΤΙΚΕΙΜΕΝΟ ΣΤΗ ΜΝΗΜΗ ΤΟΥ ΚΑΙ ΝΑ ΤΟΥ ΔΙΝΕΙ ΕΝΤΟΛΕΣ ΑΡΓΟΤΕΡΑ
        self.manager = manager 

        tk.Label(self, text = "Προσθήκη Βιβλίου", font=("Courier", 16)).pack(pady=20)

        tk.Label(self, text="Τίτλος:").pack()
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.pack(pady=5)

        tk.Label(self, text="Συγγραφέας:").pack()
        self.author_entry = tk.Entry(self, width=40)
        self.author_entry.pack(pady=5)

        tk.Label(self, text="Έτος:").pack()
        self.year_entry = tk.Entry(self, width=40)
        self.year_entry.pack(pady=5)
        
        tk.Label(self, text="Βαθμολογία:", font=("Courier", 10, "bold")).pack(pady=(20, 5))

        self.rating_combo = ttk.Combobox(self, values = [1, 2, 3, 4, 5], state = "readonly", width=5)
        self.rating_combo.pack(pady=5)

        tk.Label(self, text = "Σχόλια:").pack(pady=(10, 5))

        # Text Widget: 4 γραμμές
        self.comment_text = tk.Text(self, height=4, width=40)
        self.comment_text.pack(pady=5)

        # Button: Αποθήκευση
        self.save_button = tk.Button(self, text= "Αποθήκευση", bg ="yellow", command=self.process_save)
        self.save_button.pack(pady=15)

        self.MainButton = tk.Button(self, text = "Αρχική", bg ="lightgray", command = manager.show_main)
        self.MainButton.pack(pady=10)


    def process_save(self):
        # ΑΠΟΘΗΚΕΥΟΥΜΕ ΤΙΣ ΤΙΜΕΣ ΠΟΥ ΕΧΟΥΜΕ ΣΤΑ ΠΕΔΙΑ ENTRY ΣΕ ΜΕΤΑΒΛΗΤΕΣ
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_combo.get()
        comment = self.comment_text.get("1.0", tk.END).strip()


        if not title or not author:
            messagebox.showwarning("Προσοχή!", "Συμπλήρωσε τα βασικά πεδία (Τίτλος, Συγγραφέας)")
            return
        if not rating:
            messagebox.showwarning("Προσοχή!", "Επίλεξε βαθμολογία")
            return
        
        rating = int(rating) #Μετατρέπουμε την βαθμολογία σε ακέραιο για να την στείλουμε στον manager
        

        # 3. ΦΤΙΑΧΝΟΥΜΕ ΕΝΑ ΛΕΞΙΚΟ ΜΕ ΤΑ ΔΕΔΟΜΕΝΑ ΠΟΥ ΘΑ ΣΤΕΙΛΟΥΜΕ ΣΤΟΝ MANAGER
        # Η ΜΕΘΟΔΟΣ handle_add_new_book ΠΡΕΠΕΙ ΝΑ ΔΕΧΕΤΑΙ ΕΝΑ ΛΕΞΙΚΟ ΜΕ ΤΟΥΣ ΚΛΕΙΔΙΑ 'title', 'authors', 'year'
        new_book_data = {
            'title': title,
            'authors': author,
            'year': year
        }

        # ΚΑΛΟΥΜΕ ΤΗΝ ΜΕΘΟΔΟ ΤΟΥ MANAGER ΓΙΑ ΝΑ ΠΡΟΣΘΕΣΟΥΜΕ ΤΟ ΒΙΒΛΙΟ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ΚΑΙ ΝΑ ΠΑΡΟΥΜΕ ΤΟ ID ΤΟΥ ΝΕΟΥ ΒΙΒΛΙΟΥ
        book_id = self.manager.handle_add_new_book(new_book_data)

        if book_id:
            # ΚΑΛΟΥΜΕ ΤΗΝ ΜΕΘΟΔΟ handle_add_rating ΓΙΑ ΝΑ ΠΡΟΣΘΕΣΟΥΜΕ ΤΗΝ ΑΞΙΟΛΟΓΗΣΗ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ
            
            rating_success = self.manager.handle_add_rating(book_id, rating, comment)
            if rating_success: 
                messagebox.showinfo("Επιτυχία!", "Το βιβλίο καταχωρήθηκε με επιτυχία!")
            else:
                messagebox.showerror("Σφάλμα!", "Κάτι πήγε στραβά κατά την προσθήκη της αξιολόγησης. Δοκίμασε ξανά.")
            # ΚΑΘΑΡΙΖΟΥΜΕ ΤΑ ΠΕΔΙΑ ΓΙΑ ΝΑ ΕΙΝΑΙ ΕΤΟΙΜΑ ΓΙΑ ΝΕΑ ΚΑΤΑΧΩΡΗΣΗ 
            self.clear_fields()
        else:
            messagebox.showerror("Σφάλμα!", "Κάτι πήγε στραβά κατά την προσθήκη του βιβλίου. Δοκίμασε ξανά.")

   

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_combo.set('')
        self.comment_text.delete("1.0", tk.END)