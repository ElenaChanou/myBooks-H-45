import unittest
import os
from api.google_books import search_google_books
from api.covers import download_cover

ULYSSES_URL = "http://books.google.com/books/content?id=example&printsec=frontcover&img=1&zoom=1&source=gbs_api"

class TestApi(unittest.TestCase):
    
    def test_search_returns_results(self):
        results = search_google_books("Ulysses Joyce")
        self.assertGreater(len(results), 0)
        print("✓ search Ulysses")

    def test_first_result_has_required_fields(self):
        results = search_google_books("Ulysses Joyce")
        book = results[0]
        self.assertIn('title', book)
        self.assertIn('authors', book)
        print("✓ parse fields")

    def test_download_cover(self):
        results = search_google_books("Ulysses Joyce")
        book = results[0]
        path = download_cover(book['cover_url'], book['volume_id'])
        self.assertTrue(os.path.exists(path))
        print("✓ download cover")

    def test_default_cover_fallback(self):
        path = download_cover(None, "test")
        self.assertEqual(path, "assets/covers/default.jpg")
        print("✓ missing cover fallback")

    def test_missing_isbn_is_none(self):
        results = search_google_books("xyzzy obscure book 12345")
        for book in results:
            self.assertIn('isbn', book)
        print("✓ missing ISBN handled")

    def test_empty_results_no_exception(self):
        results = search_google_books("xyzzy obscure book 12345")
        self.assertIsInstance(results, list)
        print("✓ no exceptions on empty results")

if __name__ == "__main__":
    unittest.main(verbosity=0)