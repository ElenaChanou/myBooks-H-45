from api.google_books import search_google_books
from api.covers import download_cover

# Κάνουμε import την κλάση από το db.py που βρίσκεται στο root
from db.db import Database_Manager

db_manager = Database_Manager("myBooks")

def search_books_online(query):
    """
    Καλεί το API (Google Books) για αναζήτηση βιβλίων βάσει του query 
    και επιστρέφει τη λίστα αποτελεσμάτων ως έχει.
    """
    return search_google_books(query)


def import_online_book(book_dict):
    """
    Δέχεται τα δεδομένα ενός βιβλίου από το API, κατεβάζει τοπικά το εξώφυλλο,
    το προσθέτει στο λεξικό και το αποθηκεύει στη βάση δεδομένων.
    """
    cover_url = book_dict.get("cover_url")
    volume_id = book_dict.get("volume_id")
    
    # Ορίζουμε το path της default εικόνας σε μια μεταβλητή για ευκολία
    default_cover_path = "assets/covers/default.jpg"

    # Κατέβασμα του εξωφύλλου και αποθήκευση του τοπικού path
    if cover_url and volume_id:
        local_path = download_cover(cover_url, volume_id)
        # Αν το κατέβασμα πετύχει, βάζουμε το local_path, αλλιώς τη default
        book_dict["cover_img"] = local_path if local_path else default_cover_path
    else:
        # Αν το API δεν έστειλε καν URL εξωφύλλου, βάζουμε κατευθείαν τη default
        book_dict["cover_img"] = default_cover_path 

    # Αποθήκευση του βιβλίου στη βάση χρησιμοποιώντας την κλάση σου
    book_id = db_manager.add_book(book_dict)
    
    return book_id