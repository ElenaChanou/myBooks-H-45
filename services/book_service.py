import os
import sys



from db.db import (
    get_all_books_with_stats,
    search_books as db_search_books,
    get_book,
    get_ratings_for_book,
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