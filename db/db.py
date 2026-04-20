import sqlite3
import hashlib
import os


class Database_Manager:

    def __init__(self,db_name):
        self.db_name = db_name
        self.execute_schema()

    def create_connection(self):
        connection = sqlite3.connect(f"{self.db_name}.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        return connection


    def execute_schema(self):
       
       with self.create_connection() as connection:
            # ΔΗΜΙΟΥΡΓΙΑ ΑΝΤΙΚΕΙΜΕΝΟΥ ΚΕΡΣΟΡΑ(cursor)
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
                authors TEXT,
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

            connection.commit()

    
            

    def user_registration(self, username, password):
    
        with self.create_connection() as connection:
            cursor = connection.cursor()
            try:
                new_user_insert = "INSERT INTO USERS (username, password) VALUES (?, ?)"
                cursor.execute(new_user_insert,(username, password))#, (username, hashed_password))
                connection.commit()
                return True
            except sqlite3.IntegrityError:
                # ΕΔΩ ΘΑ ΜΠΕΙ ΤΟ ΠΡΟΓΡΑΜΜΑ ΑΝ ΕΠΙΧΕΙΡΗΣΕΙ ΚΑΠΟΙΟΣ ΝΑ ΧΡΗΣΙΜΟΠΟΙΗΣΕΙ ΕΝΑ username ΠΟΥ ΧΡΗΣΙΜΟΠΟΙΕΙΤΑΙ ΗΔΗ
                print(f"ΠΡΟΕΚΥΨΕ ΣΦΑΛΜΑ: {username} ΥΠΑΡΧΕΙ ΗΔΗ ΧΡΗΣΤΗΣ ΜΕ ΑΥΤΟ ΤΟ username")
                return False
            except Exception as fail:
                print(f"ΑΠΟΤΥΧΙΑ: {fail}")
                return False
    
    def find_user(self,username, password):
        with self.create_connection() as connection:
            cursor = connection.cursor()

            search_query = "SELECT user_id from USERS WHERE username = ? AND password = ?"
            cursor.execute(search_query,(username, password))

            user = cursor.fetchone()
            #ΕΠΙΣΤΡΕΦΕΙ ΤΟ user_id Ή None
            if user:
                return user[0] 
            else:
                return None
            
    def add_book(self, book_dict) :
        
        title = book_dict.get('title', None)
        authors = book_dict.get('authors', None)
        year = book_dict.get('year', None)
        isbn = book_dict.get('isbn', None)
        description = book_dict.get('description', None)
        cover_img = book_dict.get('cover_img', None)
        volume_id = book_dict.get('volume_id', None)

        with self.create_connection() as connection:
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
                return cursor.lastrowid
            except Exception as fail:
                print(f"ΑΠΟΤΥΧΙΑ ΕΙΣΑΓΩΓΗΣ: {fail}")
                return None
               
    def get_ratings(self, book_id):
        with self.create_connection() as connection:
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
            
    def upsert_rating(self, user_id, book_id, rating, comments):
    
        if rating < 1 or rating > 5:
            print("ΕΙΣΑΓΕΤΑΙ ΤΙΜΗ ΑΠΟ 1-5.")
            return False

        with self.create_connection() as connection:
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
            except Exception as fail:
                print(f"ΣΦΑΛΜΑ ΚΑΤΑ ΤΗΝ ΒΑΘΜΟΛΟΓΗΣΗ: {fail}")
                return False
    
                    
    def search_books(self, query):
        """
        Η συνάρτηση κάνει αναζήτηση βιβλίων με βάση τον τίτλο, συγγραφέα ή ISBN 
        και αν το πεδίο αναζήτησης είναι κενό επιστρέφει όλα τα βιβλία.
        """
        with self.create_connection() as connection:
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


    def get_book(self, book_id):
        '''Η συνάρτηση επιστρέφει ενα λεξικό με τα αποθηκευμένα στοιχεία γιά το βιβλίο, διαφορετικά επιστρέφει None'''
        with self.create_connection() as connection:
                
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
                
    def get_all_books_with_stats(self):
        '''Η ΣΥΝΑΡΤΗΣΗ ΜΑΣ ΕΠΙΣΤΡΕΦΕΙ ΤΟ ΣΥΝΟΛΟ ΤΩΝ ΒΙΒΛΙΩΝ ΜΕ ΤΟΝ ΜΕΣΟ ΟΡΟ ΤΩΝ ΑΞΙΟΛΟΓΗΣΕΩΝ
        ΚΑΙ ΤΟΝ ΑΡΙΘΜΟ ΑΥΤΩΝ.
        '''
        with self.create_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            try:

                books_stats_query = '''
                SELECT BOOKS.*, 
                ROUND(ANG(RATINGS.rating) AS avg_rate,
                COUNT (RATINGS.rating) AS total_rates,
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
    
