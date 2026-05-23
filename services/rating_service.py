from db.db import Database_Manager

_db = None


def _get_db():
    global _db
    if _db is None:
        _db = Database_Manager("myBooks")
    return _db


def save_rating(user_id: int, book_id: int, rating: int, comment: str) -> bool:
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        raise ValueError("Η βαθμολογία πρέπει να είναι 1-5")

    db = _get_db()

    if db.get_book(book_id) is None:
        raise ValueError("Το βιβλίο δεν υπάρχει")

    db.upsert_rating(user_id, book_id, rating, comment)
    return True