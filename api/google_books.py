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
    



        