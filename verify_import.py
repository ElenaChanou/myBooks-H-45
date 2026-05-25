from services.import_service import search_books_online, import_online_book
from db.db import Database_Manager

db = Database_Manager("myBooks")

print("1. Γίνεται αναζήτηση στο Google Books API...")
results = search_books_online("Ulysses Joyce")

if results:
    print(f"   Βρέθηκε το βιβλίο: {results[0].get('title')}")
    
    print("\n2. Γίνεται εισαγωγή στη βάση (και κατέβασμα εξωφύλλου)...")
    book_id = import_online_book(results[0])
    print(f"   Το βιβλίο πήρε book_id: {book_id}")
    
    print("\n3. Ανάκτηση από τη βάση για επιβεβαίωση...")
    book = db.get_book(book_id)
    if book:
        print(f"   Επιτυχία! Τίτλος στη DB: {book['title']}")
        print(f"   Path εξωφύλλου στη DB: {book['cover_img']}")
    else:
        print("   Σφάλμα: Το βιβλίο δεν βρέθηκε στη βάση.")
else:
    print("   Σφάλμα: Δεν ήρθαν αποτελέσματα από το API.")