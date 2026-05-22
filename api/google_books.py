import requests
import sqlite3
from db import Database_Manager

class myBooksAPI:
    def __init__(self,db_name = 'myBooks'):
        self.search_books_url = "https://www.googleapis.com/books/v1/volumes"
        self.db_manager = Database_Manager(db_name)

    def execute_search(self, search_query, results=5):

        search_parameters = {'q': search_query, 'maxResults': results, 'printType': 'books'}
        custom_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        try:
            #Αποστολή αιτήματος GET σύμφωνα με το http πρωτόκολλο
            response = requests.get(self.search_books_url, search_parameters, headers=custom_headers)
            response.raise_for_status()

            requested_data = response.json()

            if 'items' not in requested_data:
                return []
            
            api_books = []

            for item in requested_data['items']:
                volume_id = item.get('id','')
                info = item.get('volumeInfo',{})
                title = info.get('title', '')
                authors_list = info.get('authors', 'Άγνώστου Συγγραφέα')
                authors = ", ".join(authors_list)
                year = info.get('publishedDate','')[:4]
                cover_img = info.get('imageLinks', {}).get('thumbnail','')
                description = info.get('description','')

                # Παίρνουμε τη λίστα με τους κωδικούς (αν δεν υπάρχει, επιστρέφει κενή λίστα [])
                identifiers_list = info.get('industryIdentifiers', [])
                # Αν η λίστα έχει έστω και ένα στοιχείο, παίρνουμε το 'identifier' του πρώτου στοιχείου (θέση 0)
                if identifiers_list:
                    isbn = identifiers_list[0].get('identifier', '')
                else:
                    isbn = ''

                data = {
                    'title': title,
                    'authors': authors,
                    'year': year,
                    'isbn': isbn,
                    'description': description,
                    'cover_img': cover_img,
                    'volume_id': volume_id
                }
                api_books.append(data)
            return api_books
        except requests.exceptions.RequestException as request_failure:
                print(f"ΣΦΑΛΜΑ : {request_failure}")
                return []

    def save_books(self,search_query, results = 5):
        found_books = self.execute_search(search_query, results)
        saved_books_ids = []
        for book in found_books:
            book_id = self.db_manager.add_book(book)
            if book_id is not None:
                saved_books_ids.append(book_id)
        return saved_books_ids
    


 

def test_everything():
    import sqlite3 # Το κάνουμε import εδώ για τη δοκιμή
    print("=== ΞΕΚΙΝΑΕΙ Η ΔΟΚΙΜΗ ===")
    
    print("[1] Αρχικοποίηση API και Βάσης Δεδομένων...")
    api = myBooksAPI(db_name='myBooks')
    
    search_term = "Lord of the Rings Tolkien"
    print(f"\n[2] Αναζήτηση και αποθήκευση για: '{search_term}'...")
    
    saved_ids = api.save_books(search_term, results=3)
    print(f"-> Επιστράφηκαν τα IDs: {saved_ids}")
    
    print("\n[3] Ανάγνωση απευθείας από τη βάση δεδομένων για επιβεβαίωση...")
    conn = sqlite3.connect("myBooks.db")
    cursor = conn.cursor()
    
    # Διαβάζουμε από τον πίνακα BOOKS
    cursor.execute("SELECT book_id, title, authors, year FROM BOOKS")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]} | Τίτλος: {row[1]} | Συγγραφέας: {row[2]} | Έτος: {row[3]}")
        
    conn.close()
    print("\n=== Η ΔΟΚΙΜΗ ΟΛΟΚΛΗΡΩΘΗΚΕ ΕΠΙΤΥΧΩΣ! ===")

# Προσοχή: Το if κολλάει εντελώς αριστερά!
if __name__ == "__main__":
    test_everything()
 
 

'''1. Τι είναι ένα API (Γενικά)
API σημαίνει Application Programming Interface (Διεπαφή Προγραμματισμού Εφαρμογών). Στην ουσία, είναι ένας "μεσάζοντας" που επιτρέπει σε δύο διαφορετικά προγράμματα να επικοινωνήσουν.

Το κλασικό παράδειγμα του εστιατορίου:

Εσύ (Ο Πελάτης / Η Python Εφαρμογή σου): Κάθεσαι στο τραπέζι και ξέρεις τι θέλεις να φας (π.χ. δεδομένα για ένα βιβλίο). Δεν μπορείς όμως να πας μόνος σου στην κουζίνα να το φτιάξεις.

Η Κουζίνα (Ο Server / Η Βάση της Google): Έχει όλα τα υλικά (τα δεδομένα) και ξέρει πώς να τα μαγειρέψει, αλλά περιμένει παραγγελίες.

Το Γκαρσόνι (Το API): Παίρνει την παραγγελία σου (το Request), την πηγαίνει στην κουζίνα, και σου επιστρέφει το έτοιμο πιάτο (το Response).

Το API έχει ένα συγκεκριμένο "μενού" (κανόνες) για το τι μπορείς να του ζητήσεις και πώς ακριβώς πρέπει να το ζητήσεις.

2. Πώς "μιλάνε" τα Web APIs (Η Γλώσσα του HTTP)
Τα περισσότερα APIs (όπως το Google Books) είναι RESTful Web APIs. Αυτό σημαίνει ότι χρησιμοποιούν τους κανόνες του ίντερνετ (πρωτόκολλο HTTP). Για να συνεργαστείς μαζί τους, πρέπει να ξέρεις τρία βασικά πράγματα:

Α. Τα "Ρήματα" (HTTP Methods):
Όταν κάνεις ένα αίτημα, πρέπει να πεις στο API τι θέλεις να κάνει:

GET: "Φέρε μου δεδομένα" (Αυτό κάνεις τώρα για να βρεις βιβλία. Είναι μόνο για ανάγνωση).

POST: "Σου στέλνω νέα δεδομένα για να τα αποθηκεύσεις" (π.χ. όταν κάνεις εγγραφή σε ένα site).

PUT / PATCH: "Άλλαξε/Ενημέρωσε αυτά τα δεδομένα".

DELETE: "Διέγραψε αυτά τα δεδομένα".

Β. Τους "Κωδικούς Κατάστασης" (Status Codes):
Όταν το API σου απαντάει, το πρώτο πράγμα που σου στέλνει είναι ένας τριψήφιος αριθμός που σου λέει πώς πήγε η φάση:

200 OK: Όλα πήγαν τέλεια, ορίστε τα δεδομένα σου!

400 Bad Request: Ζήτησες κάτι λάθος (π.χ. έβαλες λάθος παραμέτρους).

401 / 403: Δεν έχεις άδεια (π.χ. χρειάζεται API Key/Κωδικός και δεν τον έβαλες).

404 Not Found: Το endpoint ή τα δεδομένα δεν βρέθηκαν.

500 Internal Server Error: Κάτι χάλασε στον server της Google (δεν φταις εσύ).

Γ. Τα Δεδομένα (JSON):
Όταν το API σου επιστρέφει πληροφορίες, συνήθως τις στέλνει σε μορφή JSON (JavaScript Object Notation). 
Είναι ένα κείμενο που μοιάζει εκπληκτικά πολύ με τα λεξικά (dictionaries) και τις λίστες της Python.

3. Η Python και η Βιβλιοθήκη requests
Εδώ μπαίνει στο παιχνίδι η requests. 
Είναι μια βιβλιοθήκη που αναλαμβάνει να κρύψει όλη την πολυπλοκότητα του ίντερνετ και να σε αφήσει να γράψεις απλό κώδικα Python.

Να πώς μεταφράζει η requests αυτά που είπαμε παραπάνω:

Το Request:
Αντί να γράφεις πολύπλοκα δίκτυα, λες απλά requests.get(url, params=...). 
Αυτό αυτόματα "χτίζει" ένα σωστό HTTP GET αίτημα.
Η παράμετρος params είναι εξαιρετική γιατί αναλαμβάνει 
να βάλει τα ?q=python&maxResults=5 στο τέλος του URL αυτόματα, αντικαθιστώντας τα κενά με %20 (url encoding).

Ο Έλεγχος των Σφαλμάτων:
Αντί να ελέγχεις χειροκίνητα αν ο κωδικός είναι 200, 404 ή 500, 
χρησιμοποιείς το response.raise_for_status(). Αν ο κωδικός δεν είναι 200 (δηλαδή κάτι πήγε στραβά),
 αυτή η γραμμή θα πετάξει ένα Exception στην Python και θα σε στείλει κατευθείαν στο except block σου. 
 Είναι σωτήριο για να μην κρασάρει σιωπηλά το πρόγραμμα!

Η Μετατροπή των Δεδομένων:
Η απάντηση έρχεται ως απλό κείμενο JSON. 
Η μαγική μέθοδος response.json() παίρνει αυτό το κείμενο και το μετατρέπει κατευθείαν σε Python dictionary.
 Έτσι, μπορείς αμέσως να γράψεις data['items'][0]['volumeInfo']['title'] για να πάρεις τον τίτλο.

4. Χρυσοί κανόνες για Πανεπιστημιακές (και μη) Εργασίες με APIs
Ποτέ μην εμπιστεύεσαι τυφλά το API (Defensive Programming):
Τα APIs συχνά αλλάζουν τη δομή τους ή λείπουν πεδία. Ένα βιβλίο μπορεί να μην έχει συγγραφέα ή εξώφυλλο. 
Πάντα να χρησιμοποιείς τη μέθοδο .get('κλειδί', 'προεπιλεγμένη_τιμή')
 στα λεξικά (όπως κάναμε στον κώδικά μας) αντί για το κλασικό λεξικό['κλειδί'], για να γλιτώσεις τα KeyError.

Πάντα να βάζεις Timeout:
Αν πέσει το ίντερνετ ή κολλήσει ο server, η requests.get() χωρίς timeout μπορεί να περιμένει για... πάντα,
 "παγώνοντας" την εφαρμογή σου. Πάντα να βάζεις timeout=10 (δευτερόλεπτα).

Όρια Χρήσης (Rate Limiting):
Τα δημόσια APIs έχουν όρια (π.χ. "μέχρι 100 αιτήματα το λεπτό"). 
Αν βάλεις την requests.get() μέσα σε ένα τεράστιο for loop χωρίς παύσεις (time.sleep()), 
η Google θα σε μπλοκάρει προσωρινά επιστρέφοντας σφάλμα 429 Too Many Requests.

Θα ήθελες να δούμε πώς μπορείς να τεστάρεις και να δεις τη μορφή των δεδομένων ενός API 
(όπως αυτό του Google Books) κατευθείαν μέσα από τον browser σου, χωρίς να γράψεις ούτε μια γραμμή κώδικα;'''
            



        