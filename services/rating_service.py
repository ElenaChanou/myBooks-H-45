from db.db import Database_Manager
# Global μεταβλητή για να κρατάμε τη σύνδεση με τη βάση (Singleton Pattern)

_db = None


def _get_db():
    """
    Βοηθητική συνάρτηση που επιστρέφει τη σύνδεση με τη βάση.
    Αν δεν υπάρχει ήδη, τη δημιουργεί. Αν υπάρχει, επιστρέφει την ίδια.
    """
    global _db
    if _db is None:
        _db = Database_Manager("myBooks")
    return _db


def save_rating(user_id: int, book_id: int, rating: int, comment: str) -> bool:

    """
    Ελέγχει τα δεδομένα και αποθηκεύει ή ανανεώνει τη βαθμολογία ενός χρήστη για ένα βιβλίο.
    """
    # 1. Έλεγχος εγκυρότητας της βαθμολογίας (πρέπει να είναι ακέραιος από 1 έως 5)
    
    if type(rating) is not int or not (1 <= rating <= 5):
        raise ValueError("Η βαθμολογία πρέπει να είναι 1-5")

    # Παίρνουμε το instance της βάσης
    db = _get_db()

    # 2. Έλεγχος αν το βιβλίο υπάρχει όντως στη βάση πριν αφήσουμε τον χρήστη να ψηφίσει
    if db.get_book(book_id) is None:
        raise ValueError("Το βιβλίο δεν υπάρχει")

    # 3. Κλήση της upsert_rating (κάνει INSERT αν είναι νέα, ή UPDATE αν ο χρήστης αλλάζει παλιά βαθμολογία)
    return db.upsert_rating(user_id, book_id, rating, comment)