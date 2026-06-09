import os
import sys

# Βοηθάει την Python να βρει τον φάκελο db
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db.db import Database_Manager

# Αρχικοποίηση του manager για τις κλήσεις στη βάση
db = Database_Manager("myBooks")


def list_all_books() -> list:
    """Επιστρέφει όλα τα βιβλία με στατιστικά (avg_rate, total_rates)."""
    return db.get_all_books_with_stats()


def search_books(query: str) -> list:
    """
    Ψάχνει βιβλία με βάση τίτλο, συγγραφέα ή ISBN.
    Αν query είναι κενό → επιστρέφει όλα τα βιβλία.
    """
    return db.search_books(query)


def get_book_details(book_id: int) -> dict | None:
    """
    Επιστρέφει στοιχεία βιβλίου + λίστα αξιολογήσεων.
    """
    book = db.get_book(book_id)

    if book is None:
        return None
    
 # Τραβάμε τα ratings από τη βάση χρησιμοποιώντας τη μέθοδο get_ratings
    ratings = db.get_ratings(book_id)

    return {
        "book": book,
        "ratings": ratings,
    }


def popular_books(limit=10):
    """Επιστρέφει τα πιο δημοφιλή βιβλία βάσει avg_rate."""
    all_books = db.get_all_books_with_stats()

        # Ταξινόμηση: βάζουμε πρώτα όσα έχουν score, αποφεύγοντας τα None για να μην κρασάρει
    sorted_books = sorted(
        all_books,
        key=lambda x: (x.get('avg_rate') is not None, x.get('avg_rate') or 0),
        reverse=True
    )
    
    return sorted_books[:limit]


def unread_popular_books(user_id, limit=10):
    """Επιστρέφει δημοφιλή βιβλία που ο χρήστης δεν έχει αξιολογήσει ακόμα."""
    popular = popular_books(limit=100)
    
     # Χρήση getattr για ασφάλεια σε περίπτωση που αλλάξει το όνομα της μεθόδου στη βάση
    user_ratings = getattr(db, "get_user_ratings", lambda uid: [])(user_id)

   
# Καθαρίζουμε τα δεδομένα για να απομονώσουμε τα book IDs που έχουν ήδη βαθμολογηθεί
    rated_ids = set()
    for r in user_ratings:
        if not isinstance(r, dict):
            continue
        if 'book_id' in r:
            rated_ids.add(r['book_id'])
        elif 'book' in r and isinstance(r['book'], dict) and 'id' in r['book']:
            rated_ids.add(r['book']['id'])
        elif 'book' in r and isinstance(r['book'], int):
            rated_ids.add(r['book'])

 # Κρατάμε μόνο τα βιβλία που το 'book_id' τους ΔΕΝ είναι στα rated_ids
    unread = [book for book in popular if book['book_id'] not in rated_ids]

    return unread[:limit]


def delete_book(book_id: int) -> bool:
        """Επικοινωνεί με τη βάση για τη διαγραφή του βιβλίου."""
        return db.delete_book(book_id)

    