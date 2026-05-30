import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import os
from tkinter import messagebox
import customtkinter as ctk
#from api_man import load_image_from_url


class BookDetailsWindow(ctk.CTkFrame):
    def __init__(self,master, book_data, on_save):#αλλαγή στο μέλλον θα μπει μια παράμετρος book_data που θα λαβάνει από το main_window
        #Αρχικοποίηση ως frame
        super().__init__(master, fg_color="transparent")
        self.book = book_data
        self.on_save = on_save

       
        
        #----ΠΡΟΣΩΡΙΝΑ DEMO DATA----
        #To self.book θα παίρνει από το book_data
        #self.book = {"title": "Η μεγάλη χίμαιρα",
                     #"authors": "Μ.Καραγάτσης",
                     #"cover_path": None}
        #τα ratings θα έρχονται από το api
        self.ratings = [
            {"username": "Giannis", "rating": 5, "comment": "Εξαιρετικό!"},
            {"username": "Vasilis", "rating": 4, "comment": "Αρκετά καλό"}
        ]
        self.create_widgets()

    def create_widgets(self):

        self.grid_columnconfigure(0, weight=1)

        #κουμπί επιστροφής
        self.btn_back = ctk.CTkButton(self, text="< Επιστροφή", width=100, command=self.go_back, fg_color="gray40", hover_color="gray30")
        self.btn_back.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        #Δημιουργία widgets τίτλος και συγγραφέας
        self.label_title=ctk.CTkLabel(self, text=self.book["title"], font=("arial", 18,"bold"))
        self.label_title.grid(row=1, column=0, pady=(10, 15))

        self.label_authors=ctk.CTkLabel(self, text=f"Συγγραφέας:{self.book['author']}", font= ("Arial", 12))
        self.label_authors.grid(row=2, column=0,pady=5)

        print("--- ΔΕΔΟΜΕΝΑ ΠΟΥ ΕΦΤΑΣΑΝ ΣΤΙΣ ΛΕΠΤΟΜΕΡΕΙΕΣ ---")
        print(self.book)
        #Το cover_path θα περιέχει την πλήρη διαδρομή τοπικά ή URL
        path = self.book.get("cover_path")
        url = self.book.get("cover_url")


        #Έλγχος αν υπάρχει διαδρομή  και αρχείο για να μην κρασάρει
        #if path and os.path.exists(path):
          #  try:
          #      img= Image.open(path)
          #      img= img.resize((150, 220))
          #      self.photo = ImageTk.PhotoImage(img)
          #      self.label_cover = ctk.CTkLabel(self, image=self.photo)
          #  except Exception:#έλεγχος αν η εικονα υπάρχει αλλά είναι κατεσταμμέν
          #      self.label_cover = ctk.CTkLabel(self, text="Σφάλμα δόρτωσης εικόνας", text_color="red")

        #else: #Αν το αρχείο δεν υπάρχει
           # self.label_cover = ctk.CTkLabel(self, text = "Το εξώφυλλο δεν βρέθηκε", font=("arial", 12, "italic"), width=150, height=220, fg_color="gray20", corner_radius=10)
        
       
        #if url:
            #pil_img = load_image_from_url(url)
            #if pil_img != None:

            #    self.photo=ctk.CTkImage(light_image=pil_img, size=(150,220))
                
             #   self.label_cover = ctk.CTkLabel(self, text="", image=self.photo)

            #else:
             #   self.label_cover = ctk.CTkLabel(self,text="Σφάλμα Φόρωσης", text_color="red")
        #else:    
        
         #   self.label_cover = ctk.CTkLabel(self, text="Το εξώφυλλο δεν βρέθηκε", fg_color="transparent")
        # --- ΠΡΟΣΘΕΤΟΥΜΕ ΑΥΤΗ ΤΗ ΓΡΑΜΜΗ (Προσωρινό Mock για το UI Test) ---
        self.label_cover = ctk.CTkLabel(self, text="Το εξώφυλλο δεν βρέθηκε\n(UI Test)", fg_color="gray20", width=150, height=220, corner_radius=10)
        
        self.label_cover.grid(row=3, column=0,pady=10)

        self.comments_frame=ctk.CTkFrame(self,fg_color="transparent")
        self.comments_frame.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)
        self.comments_frame.grid_columnconfigure(0,weight=1)


        #Λίστα σχολίων Treeview
        self.tree_comments= ttk.Treeview(self.comments_frame,columns="comment", show="headings", height=5 )
        self.tree_comments.heading("comment", text="Σχόλια Χρηστών")
        self.tree_comments.column("comment", width=400, anchor="w")

        self.scrollbar=ttk.Scrollbar(self.comments_frame, orient="vertical", command=self.tree_comments.yview)
       
        self.tree_comments.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree_comments.grid(row=0, column=0, pady=10, padx=10, sticky="nsew" )

        ctk.CTkLabel(self, text="Η αξιολόγησή σου:", font= ("arial", 12, "bold")).grid(pady=(20,5))

        self.combo_rating=ttk.Combobox(self, values=[1, 2, 3, 4, 5], state="readonly")
        self.combo_rating.grid(row=6, column = 0, pady=5)

        ctk.CTkLabel(self, text="Σχόλιο:", font=("arial", 11)).grid(row=7, column=0,pady=(10,0))

        self.text_comment = ctk.CTkTextbox(self, height=80, width=400)
        self.text_comment.grid(row=8, column=0, pady=5, padx=10)

        self.save_button=ctk.CTkButton(self, text="Αποθήκευση", command=self.handle_save, fg_color="#4CAF50", hover_color="#45a049", text_color="white")
        self.save_button.grid(row=9, column =0, pady=15)

        #Φόρτωση σχολίων από Demo Data
        for r in self.ratings:
            display_text = f"⭐ {r['rating']}/5 - {r['username']}: {r['comment']}"
            self.tree_comments.insert("", "end", values=(display_text,))

    def handle_save(self):
        #Διαβάζει από την Combobox
        rating=self.combo_rating.get()

        #Διαβάζει από την text_comment το σχόλιο του χρήστη
        comment=self.text_comment.get("1.0", tk.END).strip()

        #Έλεγχος αν δενέχει επιλεγεί  rating
        if not rating:
            messagebox.showwarning("Προσοχή","Παρακαλώ επιλέξτε βαθμολογία!")
            return
        print(f"Αποθήκευση: rating={rating}, comment={comment}")
        messagebox.showinfo("Επιτυχία", "Η αξιολόγησή σου αποθηκεύτηκε!")

        self.on_save()
        self.go_back() # Χρησιμοποιούμε τη go_back για να κλείσει το frame

    def go_back(self):
        print("Επιστροφή στην αρχική οθόνη!")
        self.destroy() # Καταστρέφει το Frame των λεπτομερειών
        
        # ο Controller (master) θα ξαναδείξει το Main Screen
        self.master.show_main_screen()

if __name__ == "__main__":
    # Μικρό test για να βλέπεις αν τρέχει μόνο του ως Frame
    root = ctk.CTk()
    root.geometry("500x800")
    
    # 1. Φτιάχνουμε ένα ψεύτικο λεξικό για το τεστ
    test_book = {"id": 1, "title": "Test Book", "author": "Test Author", "cover_url": ""}
    
    # 2. Φτιάχνουμε μια ψεύτικη συνάρτηση για το on_save
    def test_refresh(): print("Refresh callback triggered!")

    # 3. Φορτώνουμε το Frame και το κάνουμε pack στο root
    app = BookDetailsWindow(root, book_data=test_book, on_save=test_refresh)
    app.pack(fill="both", expand=True)
    
    root.mainloop()