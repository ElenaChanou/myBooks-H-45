import sqlite3

def database_myBooks():
    # ΔΗΜΙΟΥΡΓΙΑ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ myBooks
    connection = sqlite3.connect("myBooks.db")

    # ΕΝΕΡΓΟΠΟΙΗΣΗ ΤΩΝ ΞΕΝΩΝ ΚΛΕΙΔΙΩΝ(FOREIGN KEYS)
    connection.execute("PRAGMA foreign_keys = ON")

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
    connection.close()

def user_registration(username, password):
    
    connection = sqlite3.connect("myBooks.db")
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
    
    finally:
        # ΣΤΟ ΤΕΛΟΣ ΚΛΕΙΝΕΙ Η ΣΥΝΔΕΣΗ ΜΕ ΤΗΝ ΒΑΣΗ
        connection.close()


