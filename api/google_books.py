import urllib.request
import urllib.parse
import json
import os
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")


def search_google_books(query):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,
        'maxResults': 10,
        'printType': 'books',
        'projection': 'full',
        'key': API_KEY
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                print(f"API error: {response.status}")
                return []

            data = json.loads(response.read().decode('utf-8'))

            if 'items' not in data:
                return []

            books_found = []
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})

                # authors is a list, join into a single string
                authors_list = volume_info.get('authors', None)
                authors = ", ".join(authors_list) if authors_list else 'Unknown'

                # extract only the year from publishedDate (e.g. "1949-06-08" -> "1949")
                published_date = volume_info.get('publishedDate', None)
                year = published_date[:4] if published_date else None

                # industryIdentifiers is a list of dicts, find the ISBN_13 entry
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

    except Exception as e:
        print(f"Error communicating with API: {e}")
        return []