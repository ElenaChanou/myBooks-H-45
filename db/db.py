import sqlite3


class Database_Manager:

    def __init__(self,db_name):
        self.db_name = db_name
        self.db_tables()

    def create_connection(self):
        connection = sqlite3.connect(f"{self.db_name}.db")
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        return connection


    def db_tables(self):
       
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
                author TEXT,
                description TEXT,
                cover_img TEXT)'''
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
            

    def user_registration(self,username, password):
    
        with self.create_connection() as connection:
            cursor = connection.cursor()
    
            try:

                new_user_insert = "INSERT INTO USERS (username, password) VALUES (?, ?)"
                cursor.execute(new_user_insert,(username, password))
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
            
    def add_book(self,title, author, description, cover_img):
        with self.create_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT book_id FROM BOOKS WHERE title = ? and author = ?",(title, author))
                book_exists = cursor.fetchone()
                if book_exists:
                    print("ΤΟ ΒΙΒΛΙΟ ΕΧΕΙ ΗΔΗ ΚΑΤΑΧΩΡΗΘΕΙ ΣΤΗΝ ΒΑΣΗ")
                    return book_exists[0]
                
                insert_query = "INSERT INTO BOOKS(title, author, description, cover_img) VALUES(?, ?, ?, ?)"
                cursor.execute(insert_query,(title, author, description, cover_img))

                connection.commit()
                return cursor.lastrowid
            except Exception as fail:
                print(f"ΑΠΟΤΥΧΙΑ ΕΙΣΑΓΩΓΗΣ: {fail}")
                return None

    def add_rating(self,user_id, book_id, comments, rating):
        if (rating < 1 or rating > 5):
                print("ΒΑΘΜΟΛΟΓΙΑ ΠΡΕΠΕΙ ΝΑ ΕΙΝΑΙ 1-5 ")
                return False
            
        with self.create_connection() as connection:
            cursor = connection.cursor()

           
            try:
                cursor.execute("SELECT rate_id FROM RATINGS WHERE user_id = ? AND book_id = ?",(user_id,book_id))
                rating_exists = cursor.fetchone()
                
                if rating_exists:
                    update_query = "UPDATE RATINGS SET comments = ?, rating = ? WHERE user_id = ? AND book_id = ?"
                    cursor.execute(update_query,(comments, rating, user_id, book_id))
                    print("ΕΠΙΤΥΧΗΣ ΕΝΗΜΕΡΩΣΗ ΚΑΤΑΧΩΡΗΣΗΣ")
                else:
                    insert_query = "INSERT INTO RATINGS(user_id, book_id, comments, rating) VALUES (?, ?, ?, ?)"
                    cursor.execute(insert_query,(user_id, book_id, comments, rating))
                    print("ΕΠΙΤΥΧΗΣ ΑΞΙΟΛΟΓΗ ΒΙΒΛΙΟΥ")
                    
                connection.commit()
                return True
            except sqlite3.IntegrityError as Error:
                print(f"ΠΡΟΕΚΥΨΕ ΑΚΕΡΑΙΟΤΗΤΑΣ: {Error}")
                return False
            except Exception as fail:
                print(f"ΑΠΟΤΥΧΙΑ: {fail}")
                return False
        

            

if __name__== "__main__":

    db_name = 'myBooks'
    myBooks_db = Database_Manager(db_name)
    
    
