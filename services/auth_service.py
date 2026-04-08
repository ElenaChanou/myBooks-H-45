import hashlib   # built-in βιβλιοθήκη για κρυπτογράφηση
import sys 
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from db.db import get_user_by_username

def hash_password(password: str) -> str:
    """
    Δέχεται plaintext string, επιστρέφει SHA-256 hex digest.
    Χρησιμοποιείται και για τη δημιουργία demo users στο db.py
    ώστε τα hashes να είναι συμβατά.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login(username: str, password: str) -> dict | None:
    """
    Ελέγχει credentials και επιστρέφει user dict ή None.

    Returns:
        {"id": int, "username": str}  αν το login είναι επιτυχές
        None                          αν ο χρήστης δεν υπάρχει ή λάθος password
    """
    user = get_user_by_username(username)
    
    if user is None:
        return None
    
    if hash_password(password) == user["password"]:
        return {"id": user["id"], "username": user["username"]}
    
    return None