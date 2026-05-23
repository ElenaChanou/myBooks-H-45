import os
import sys



from db.db import (
    get_all_books_with_stats,
    search_books as db_search_books,
    get_book,
    get_ratings_for_book,
    get_user_ratings,
)


def list_all_books() -> list:

    # Επιστρέφει όλα τα βιβλία με στατιστικά (avg_rating, rating_count).
    return get_all_books_with_stats()





def search_books(query: str) -> list:
   
#    Ψάχνει βιβλία με βάση τίτλο, συγγραφέα ή ISBN.
#     Αν query είναι κενό → επιστρέφει όλα τα βιβλία.
    return db_search_books(query)

def get_book_details(book_id:  int) -> dict | None:

    """
    Επιστρέφει στοιχεία βιβλίου + λίστα αξιολογήσεων.
 
    Returns:
        {
            "book":    { id, title, authors, year, ... },
            "ratings": [ { username, rating, comment }, ... ]
        }
        None  αν το βιβλίο δεν βρεθεί
    """

    book = get_book(book_id)

    if book is None:
        return None
    
    ratings = get_ratings_for_book(book_id)


    return {
        "book": book,
        "ratings": ratings,
    }

def popular_books(limit=10):
    # Επιστρέφει τα πιο δημοφιλή βιβλία βάσει avg_rating.
    # Τα βιβλία χωρίς βαθμολογία μπαίνουν στο τέλος.

    all_books = get_all_books_with_stats()

    # Ταξινόμηση: 
    # 1ο κριτήριο: Αν έχει rating (True/1) ή όχι (False/0) -> στέλνει τα None στο τέλος
    # 2ο κριτήριο: Η τιμή του avg_rating
    sorted_books = sorted(
        all_books,
        key=lambda x: (x.get('avg_rating') is not None, x.get('avg_rating') or 0),
        reverse=True
    )
    
    return sorted_books[:limit]


def unread_popular_books(user_id, limit=10):
   
    # Επιστρέφει δημοφιλή βιβλία που ο χρήστης δεν έχει αξιολογήσει ακόμα.
    # 1. Παίρνουμε τα δημοφιλή (χωρίς μικρό limit αρχικά για να έχουμε περιθώριο φιλτραρίσματος)

    popular = popular_books(limit=100)
    # 2. Παίρνουμε τα IDs των βιβλίων που έχει ήδη αξιολογήσει ο χρήστης
    # Υποθέτουμε ότι η get_user_ratings επιστρέφει λίστα από dicts με 'book_id

    user_ratings = get_user_ratings(user_id)
    rated_ids = {r['book_id'] for r in user_ratings} # Set για ταχύτητα αναζήτησης

    # 3. Φιλτράρισμα
    unread = [book for book in popular if book['id'] not in rated_ids]

    return unread[:limit]
    