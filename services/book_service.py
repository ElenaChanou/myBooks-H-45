import os
import sys

# Βοηθάει την Python να βρει τον φάκελο db
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db.db import Database_Manager

# Δημιουργούμε ένα instance της βάσης
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
    
    # Στη βάση σου η μέθοδος λέγεται get_ratings
    ratings = db.get_ratings(book_id)

    return {
        "book": book,
        "ratings": ratings,
    }


def popular_books(limit=10):
    """Επιστρέφει τα πιο δημοφιλή βιβλία βάσει avg_rate."""
    all_books = db.get_all_books_with_stats()

    # Ταξινόμηση με βάση το 'avg_rate' (έτσι λέγεται το πεδίο στο db.py)
    sorted_books = sorted(
        all_books,
        key=lambda x: (x.get('avg_rate') is not None, x.get('avg_rate') or 0),
        reverse=True
    )
    
    return sorted_books[:limit]


def unread_popular_books(user_id, limit=10):
    """Επιστρέφει δημοφιλή βιβλία που ο χρήστης δεν έχει αξιολογήσει ακόμα."""
    popular = popular_books(limit=100)
    
    # Παίρνουμε τα IDs των βιβλίων που έχει ήδη αξιολογήσει ο χρήστης
    user_ratings = db.get_ratings_by_user(user_id)
    rated_ids = {r['book_id'] for r in user_ratings} 

    # Φιλτράρισμα (το πεδίο λέγεται 'book_id' στη βάση)
    unread = [book for book in popular if book['book_id'] not in rated_ids]

    return unread[:limit]