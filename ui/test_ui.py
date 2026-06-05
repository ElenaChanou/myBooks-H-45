import customtkinter as ctk
from login_window import LoginFrame
from main_window import MainFrame

class DummyController(ctk.CTk):
    """
    Αυτός είναι ένας ψεύτικος κεντρικός Manager ΜΟΝΟ για το testing του UI (#20).
    Αντικαθιστά το appUI ώστε να μην υπάρχουν conflicts με τους συναδέλφους.
    """
    def __init__(self):
        super().__init__()
        self.title("UI Testing Environment - Issue #20")
        self.geometry("900x700")

        # Ξεκινάμε δείχνοντας το Login Window
        self.current_frame = LoginFrame(self, self)
        self.current_frame.pack(fill="both", expand=True)

    def show_main_screen(self):
        # Κρύβουμε το login και δείχνουμε το κεντρικό παράθυρο
        self.current_frame.pack_forget()
        
        # Το ονομάζουμε main_frame για να το βρίσκει το login!
        self.main_frame = MainFrame(self, self)
        self.main_frame.pack(fill="both", expand=True)
        
        self.current_frame = self.main_frame

    def show_login_screen(self):
        # Κρύβουμε το κεντρικό και γυρνάμε στο login (για το κουμπί Αποσύνδεση)
        self.current_frame.pack_forget()
        self.current_frame = LoginFrame(self, self)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = DummyController()
    app.mainloop()