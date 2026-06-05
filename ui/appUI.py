import sys
import os
# Αυτό λέει στην Python να βλέπει και τον κεντρικό φάκελο του project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
import customtkinter as ctk
from login_window import LoginFrame
from main_window import MainFrame 
from add_book_window import AddBookWindow

class AppController():
    def __init__(self, root):
        self.root=root
        root.title("Διαχείριση Βιβλιοθήκης")
        self.login_frame = LoginFrame(self.root,self)
        self.main_frame = MainFrame(self.root, self)
        self.show_login_screen()

    def show_login_screen(self):
        self.main_frame.pack_forget()
        self.login_frame.pack(fill = "both", expand= True)

    def show_main_screen(self):#η συνάστηση που καλείται αν είναι σωστός ο κωδικός
        self.main_frame.pack(fill= "both", expand= True)
        self.login_frame.pack_forget()
    
   


if __name__== "__main__":
    root=ctk.CTk() 

    root.geometry("900x700")
       
    app=AppController(root)
    root.mainloop()