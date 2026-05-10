import sqlite3
import hashlib
import os


class Database_Manager:

    # Εκκίνηση της βάσης δεδομένων 
    def __init__(self,db_name:str) -> None:
        self.db_name = db_name
        self.execute_schema()

    # Άνοιγμα σύνδεσης με τη βάση δεδομένων και ενεργοποίηση των foreign keys
    def create_connection(self)-> sqlite3.Connection:

        connection = sqlite3.connect(f"{self.db_name}.db")
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    # Δημιουργία των πινάκων USERS, BOOKS και RATINGS αν δεν υπάρχουν ήδη
    def execute_schema(self)-> None:
       connection = self.create_connection()
       # Χρήση try-except-finally για να διαχειριστούμε τυχόν σφάλματα και να εξασφαλίσουμε ότι η σύνδεση θα κλείνει κανονικα.
       try:
           with connection:
                cursor = connection.cursor()
                # ΔΗΜΙΟΥΡΓΙΑ ΠΙΝΑΚΑ ΧΡΗΣΤΩΝ USERS
                create_table_users = '''CREATE TABLE IF NOT EXISTS USERS
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    )'''
                cursor.execute(create_table_users) 

                # ΔΗΜΙΟΥΡΓΙΑ ΠΙΝΑΚΑ BOOKS
                create_table_books = '''CREATE TABLE IF NOT EXISTS BOOKS
                    (book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    year TEXT,
                    isbn TEXT,
                    description TEXT,
                    cover_img TEXT,
                    volume_id TEXT)'''
                cursor.execute(create_table_books)

                #ΔΗΜΙΟΥΡΓΙΑ ΠΙΝΑΚΑ RATINGS
                create_table_ratings ='''CREATE TABLE IF NOT EXISTS RATINGS
                    (rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    comments TEXT,
                    rating INTEGER CHECK (rating>=1 AND rating<=5),
                    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
                    FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
                    UNIQUE(user_id,book_id)
                    )'''
                cursor.execute(create_table_ratings)

       except Exception as fail:
            print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΔΗΜΙΟΥΡΓΙΑ ΤΩΝ ΠΙΝΑΚΩΝ: {fail}")
       finally:
            # Κλέινουμε κάθε φορά τη σύνδεση για να μην έχουμε προβλήματα με κλειδώματα ή διαρροές πόρων.
            connection.close()

    # Θέλουμε όλες τις CRUD λειτουργίες (CREATE, READ, UPDATE, DELETE) για χρήστες, βιβλία και αξιολογήσεις.
    # CREATE(user_registration, add_book):
    def user_registration(self, username:str, password:str) -> bool:
        connection = self.create_connection()
        try:
             with connection:
                cursor = connection.cursor()
                new_user_insert = "INSERT INTO USERS (username, password) VALUES (?, ?)"
                cursor.execute(new_user_insert,(username, password))#, (username, hashed_password))
                connection.commit()
                return True
        except Exception as fail:
            print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΕΓΓΡΑΦΗ ΤΟΥ ΧΡΗΣΤΗ: {fail}")
            return False
        finally:
            connection.close()  

    def add_book(self, book_dict: dict) -> int | None:

        connection = self.create_connection()
        
        title = book_dict.get('title', None)
        authors = book_dict.get('authors', None)
        year = book_dict.get('year', None)
        isbn = book_dict.get('isbn', None)
        description = book_dict.get('description', None)
        cover_img = book_dict.get('cover_img', None)
        volume_id = book_dict.get('volume_id', None)

        try:
            with connection:
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT book_id FROM BOOKS WHERE title = ? and authors = ?",(title, authors))
                    book_exists = cursor.fetchone()
                    if book_exists:
                        print("ΤΟ ΒΙΒΛΙΟ ΕΧΕΙ ΗΔΗ ΚΑΤΑΧΩΡΗΘΕΙ ΣΤΗΝ ΒΑΣΗ")
                        return book_exists[0]
                
                    insert_query = "INSERT INTO BOOKS(title, authors, year, isbn, description, cover_img, volume_id) VALUES(?, ?, ?, ?, ?, ?, ?)"
                    cursor.execute(insert_query,(title, authors,year, isbn, description, cover_img, volume_id))

                    connection.commit()
                    return cursor.lastrowid # Το ID του βιβλίου 
                except Exception as fail:
                    print(f"ΑΠΟΤΥΧΙΑ ΕΙΣΑΓΩΓΗΣ: {fail}")
                    return None
        finally:
            connection.close()

    # READ(find_user, get_book, search_books, get_all_books_with_stats, get_ratings):
    def find_user(self,username:str, password:str)-> int | None:
        connection = self.create_connection()
        try:             
            with connection:
                cursor = connection.cursor()

                search_query = "SELECT user_id from USERS WHERE username = ? AND password = ?"
                cursor.execute(search_query,(username, password))

                user = cursor.fetchone()
                #ΕΠΙΣΤΡΕΦΕΙ ΤΟ user_id Ή None
            if user:
                return user[0] 
            else:
                return None
        finally:
            connection.close()

    def get_book(self, book_id: int) -> dict | None:
        '''Η συνάρτηση επιστρέφει ενα λεξικό με τα αποθηκευμένα στοιχεία γιά το βιβλίο, διαφορετικά επιστρέφει None'''
        connection = self.create_connection()
        try:
            with connection:
                connection.row_factory = sqlite3.Row #Με αυτό τον τρόπο μας επιστέφει τις εγγραφές σαν λεξικό και με τα πεδία τους αντι σε πλειάδες(γλυτώνουμε το index).
                cursor = connection.cursor()
                try:
                    cursor.execute("SELECT * FROM BOOKS WHERE book_id = ?", (book_id,))
                    row = cursor.fetchone()

                    if row:
                        return dict(row)
                    else:
                        return None
                    
                except Exception as fail:
                    print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΑΝΑΚΤΗΣΗ: {fail}")
                    return None
        finally:
            connection.close()
    
    def get_ratings(self, book_id: int)-> list[dict]:
        connection = self.create_connection()
        try:
            with connection:
                # Μετατρέπει σε λεξικό τις εγγραφές
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                try:
                    query = '''
                            SELECT USERS.username, RATINGS.rating, RATINGS.comments
                            FROM RATINGS
                            JOIN USERS ON RATINGS.user_id = USERS.user_id 
                            WHERE RATINGS.book_id = ?
                            '''
                    cursor.execute(query, (book_id,))
                    rows = cursor.fetchall()

                    return[dict(row) for row in rows]
                except Exception as fail:
                    print(f"ΑΠΟΤΥΧΙΑ ΑΝΑΚΤΗΣΗΣ : {fail}")
                    return []
        finally:
            connection.close()

    def search_books(self, query: str)-> list[dict]:
        """
        Η συνάρτηση κάνει αναζήτηση βιβλίων με βάση τον τίτλο, συγγραφέα ή ISBN 
        και αν το πεδίο αναζήτησης είναι κενό επιστρέφει όλα τα βιβλία.
        """
        connection = self.create_connection()
        try:
            with connection:
                # Ρυθμίζουμε το row_factory για να πάρουμε τα αποτελέσματα σε λεξικό.
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                try:
                    # Αν ο χρήστης δεν πληκτρολογήσει τίποτα επιστρέφει όλες τις εγγραφές
                    if not query or query.strip() == "":
                        cursor.execute("SELECT * FROM BOOKS")
                    else:
                        # Αναζήτησ με %{}% LIKE
                        search_term = f"%{query}%"
                        search_sql = """
                            SELECT * FROM BOOKS 
                            WHERE title LIKE ? OR authors LIKE ? OR isbn LIKE ?
                        """
                        # Περνάμε το search_term σε κάθε πεδίο
                        cursor.execute(search_sql, (search_term, search_term, search_term))

                    rows = cursor.fetchall()
                    #Επιστρέφουμε το αποτέλεσμα σε κανονικό λεξικό της Python
                    return [dict(row) for row in rows]
            
                except Exception as fail:
                    print(f"Σφάλμα κατά την αναζήτηση: {fail}")
                return []
        finally:
            connection.close()

    def get_all_books_with_stats(self)-> list[dict]:
        '''Η ΣΥΝΑΡΤΗΣΗ ΜΑΣ ΕΠΙΣΤΡΕΦΕΙ ΤΟ ΣΥΝΟΛΟ ΤΩΝ ΒΙΒΛΙΩΝ ΜΕ ΤΟΝ ΜΕΣΟ ΟΡΟ ΤΩΝ ΑΞΙΟΛΟΓΗΣΕΩΝ
        ΚΑΙ ΤΟΝ ΑΡΙΘΜΟ ΑΥΤΩΝ.
        '''
        connection = self.create_connection()
        try:
            with connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                try:
                    books_stats_query = '''
                    SELECT BOOKS.*, 
                    ROUND(AVG(RATINGS.rating), 2) AS avg_rate,
                    COUNT(RATINGS.rating) AS total_rates
                    FROM BOOKS
                    LEFT JOIN RATINGS ON BOOKS.book_id = RATINGS.book_id
                    GROUP BY BOOKS.book_id'''
                
                    cursor.execute(books_stats_query)
                    rows = cursor.fetchall()
                    all_book_stats = [] # ΑΡΧΙΚΟΠΟΙΗΣ ΛΙΣΤΑΣ

                    for row in rows:
                        all_book_stats.append(dict(row))
                    return all_book_stats
                
                except Exception as fail:
                    print(f"ΣΦΑΛΜΑ ΕΥΡΕΣΗΣ ΣΤΑΤΙΣΤΙΚΩΝ: {fail}")
                    return []
        finally:
            connection.close()  
    
    # UPDATE (Upsert λειτουργεί και για insert και για update).
    def upsert_rating(self, user_id: int, book_id: int, rating: int, comments: str)-> bool:

        connection = self.create_connection()  
        if rating < 1 or rating > 5:
            print("ΕΙΣΑΓΕΤΑΙ ΤΙΜΗ ΑΠΟ 1-5.")
            return False
        try:
            with connection:
                cursor = connection.cursor()
                try:
                    query = "SELECT * FROM RATINGS WHERE user_id = ? AND book_id=?"
                    cursor.execute(query,(user_id, book_id))

                    rating_exists = cursor.fetchone()    

                    if rating_exists:
                        update_query = '''
                        UPDATE RATINGS SET rating = ?, comments = ?
                        WHERE user_id = ? AND book_id = ?'''
                    
                        cursor.execute(update_query,(rating, comments, user_id, book_id))
                
                    else:
                        insert_query = '''
                        INSERT INTO RATINGS(user_id, book_id, rating, comments)
                        VALUES (?,?,?,?)'''
                        cursor.execute(insert_query,(user_id, book_id, rating, comments))

                    connection.commit()
                    return True
                except sqlite3.IntegrityError as Error:
                    print(f"ΠΡΟΕΚΥΨΕ ΑΚΕΡΑΙΟΤΗΤΑΣ: {Error}")
                return False
        finally:
            connection.close()

    # DELETE:
    def delete_book(self, book_id: int)-> bool:
        #Διαγραφή βιλίων και των αξιολογήσεων τους.
        connection = self.create_connection()
        
        try:
            with connection: 
                cursor = connection.cursor()
                #  Αναζήτηση του βιβλίου για να επιβεβαιώσουμε ότι υπάρχει πριν προσπαθήσουμε να το διαγράψουμε.
                cursor.execute("SELECT * FROM BOOKS WHERE book_id = ?", (book_id,))
                book_to_delete = cursor.fetchone()
                if not book_to_delete:
                    print(f"ΠΛΗΡΟΦΟΡΙΑ: Δεν βρέθηκε βιβλίο με ID {book_id}.")
                    return False
                # Διαγραφή των αξιολογήσεων που σχετίζονται με το βιβλίο για να διατηρηθεί η ακεραιότητα των δεδομένων (Foreign Keys).
                cursor.execute("DELETE FROM RATINGS WHERE book_id = ?", (book_id,))
                # Διαγραφή του βιβλίου από τον πίνακα BOOKS
                cursor.execute("DELETE FROM BOOKS WHERE book_id = ?", (book_id,))
                
                return False
                    
        except Exception as fail:
            print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗ ΔΙΑΓΡΑΦΗ: {fail}")
            return False
            
        finally:
            connection.close()

    def delete_user(self, user_id: int)-> bool:
    #Διαγράφει τον χρήστη και όλες τις αξιολογήσεις του για να διατηρηθεί η ακεραιότητα των δεδομένων.
        connection = self.create_connection()
        
        try:
            with connection: # Transaction starts
                cursor = connection.cursor()
                # Αναζήτηση του χρήστη για να επιβεβαιώσουμε ότι υπάρχει πριν προσπαθήσουμε να τον διαγράψουμε.
                cursor.execute("SELECT * FROM USERS WHERE user_id = ?", (user_id,))
                user_to_delete = cursor.fetchone()
                if not user_to_delete:
                    print(f"ΠΛΗΡΟΦΟΡΙΑ: Δεν βρέθηκε χρήστης με ID {user_id}.")
                    return False    
                # Διαγραφή των αξιολογήσεων που σχετίζονται με το χρήστη για να διατηρηθεί η ακεραιότητα των δεδομένων (Foreign Keys).
                cursor.execute("DELETE FROM RATINGS WHERE user_id = ?", (user_id,))
                # Διαγραφή του χρήστη από τον πίνακα USERS
                cursor.execute("DELETE FROM USERS WHERE user_id = ?", (user_id,))
                
                return True
                    
        except Exception as fail:
            print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗ ΔΙΑΓΡΑΦΗ ΧΡΗΣΤΗ: {fail}")
            return False
            
        finally:
            connection.close()

    def delete_rating(self, user_id: int, book_id: int)-> bool:
        #Διαγραφή μίας αξιολόγησης με βάση το user_id και book_id, καθώς αυτά τα δύο πεδία είναι μοναδικά μαζί (UNIQUE(user_id, book_id)).
        connection = self.create_connection()
        
        try:
            with connection: 
                cursor = connection.cursor()
                #Ευρεση της αξιολόγησης για να επιβεβαιώσουμε ότι υπάρχει πριν προσπαθήσουμε να την διαγράψουμε.
                cursor.execute("SELECT * FROM RATINGS WHERE user_id = ? AND book_id = ?", (user_id, book_id))
                rating_to_delete = cursor.fetchone()

                if not rating_to_delete:
                    print(f"ΠΛΗΡΟΦΟΡΙΑ: Δεν βρέθηκε αξιολόγηση με ID χρήστη {user_id} και ID βιβλίου {book_id}.")
                    return False
                
                cursor.execute(
                    "DELETE FROM RATINGS WHERE user_id = ? AND book_id = ?", 
                    (user_id, book_id))
                return True
                    
        except Exception as fail:
            print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗ ΔΙΑΓΡΑΦΗ ΑΞΙΟΛΟΓΗΣΗΣ: {fail}")
            return False
            
        finally:
            connection.close()
    
