import urllib.request
import urllib.parse
import urllib.error
import json
import os
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


def search_google_books(query):

    base_url = "https://www.googleapis.com/books/v1/volumes"

    search_query = f"intitle:{query}" #Αναζήτηση ακριβώς με τίτλο στα μέταδεδομένα(καλύτερα αποτελέσματα-μικρότερο εύρος αναζήτησης)
    params = {
        'q': search_query,
        'maxResults': 10,
        'printType': 'books',
        'orderBy': 'relevance',
        'projection': 'full',
        'key': API_KEY
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url) as response:

            data = json.loads(response.read().decode('utf-8'))

            if 'items' not in data:
                return []

            books_found = []
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})

                # Οι συγγραφείς μπορεί να είναι μια λίστα, οπότε την μετατρέπουμε σε string
                authors_list = volume_info.get('authors', None)
                authors = ", ".join(authors_list) if authors_list else 'Unknown'

                # extract only the year from publishedDate (e.g. "1949-06-08" -> "1949")
                published_date = volume_info.get('publishedDate', None)
                year = published_date[:4] if published_date else None

                # industryIdentifiers Eίναι μια λίστα από λεξικά, θα αναζητήσουμε το ISBN_13
                identifiers = volume_info.get('industryIdentifiers', [])
                isbn = None
                for identifier in identifiers:
                    if identifier.get('type') == 'ISBN_13':
                        isbn = identifier.get('identifier', None)
                        break

                books_found.append({
                    'title': volume_info.get('title', None),
                    'authors': authors,
                    'year': year,
                    'isbn': isbn,
                    'description': volume_info.get('description', ''),
                    'cover_url': volume_info.get('imageLinks', {}).get('thumbnail', None),
                    'volume_id': item.get('id', None)
                })

            return books_found
    except urllib.error.HTTPError as error:
        print(f"HTTP Σφάλμα: {error.code} - {error.reason}")
        return []
    except Exception as error:
        print(f"Σφάλμα κατά την επικοινωνία με την API: {error}")
        return []
