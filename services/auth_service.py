import hashlib
import sys
import os

# Βοηθάει την Python να βρει τον φάκελο db
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db.db import Database_Manager

# Δημιουργούμε ένα instance του Database_Manager για να μιλήσουμε στη βάση
db = Database_Manager("myBooks")

def hash_password(password: str) -> str:
    """
    Δέχεται plaintext string, επιστρέφει SHA-256 hex digest.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login(username: str, password: str) -> dict | None:
    """
    Ελέγχει credentials και επιστρέφει user dict ή None.
    """
    # Χρησιμοποιούμε τη δική σου μέθοδο find_user από το db.py
    user_id = db.find_user(username, password)
    
    if user_id is not None:
        # Αν το login είναι επιτυχές, επιστρέφουμε το dictionary 
        return {"id": user_id, "username": username}
    
    return None