import urllib.request
import urllib.parse
import json


def search_books(query, max_results=5):

    # Vasiko url apo to google books API
    base_url = "https://www.googleapis.com/books/v1/volumes"

    # parametroi pou tha xrhsimopoihsoume gia thn anazhthsh vivliwn
    params = {
        'q': query,
        'maxResults': max_results,
        'printType': 'books',
        'projection': 'lite'  # me authn thn parametrw glutwnoume xrono kathws dinei mono ths vasikes plhrofories
    }

    # Metaroph se url (se morfh pou diavazei to web(kena metatrepontai se %20))
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"

    try:
        # Kaloume to API kai elegxoume ama to response apo thn selida den vgazei htpps errors kai vgazei 200(OK)
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                # Diavazei ta raw data se json morfh kai ta metatrepei se utf-8 wste na mporoume na ta diavasoume
                data = json.loads(response.read().decode('utf-8'))

                # an den vrethoune vivlia []
                if 'items' not in data:
                    return []

                # Dhmiourgia listas pou tha apothikeutoun oi plhrofories tou vivliou
                books_found = []

                # loop pou pernaei kathe apotelesma pou mas edwse to api wste na apothikeusw ta info pou thelw
                for item in data['items']:

                    # To api ths google mas exei steilei ena leksiko me data kai mesa sto leksiko auto uparxei
                    # h lista items. Mesa se auth einai apothikeumena ta apotelesmata tou search pou kaname
                    # dhladh to id twn vilviwn kai o tupos(Books).Mesa sthn items uparxei to leksiko volumeInfo
                    # to opoio periexei plhrofories opws authors,title,publishedDate kai image_links ktlp


                    # pernw ta stoixeia me .get kai ta apothikeuw se metavlhtes analogws me to poies plhrofories
                    # epileksoume oti tha exoume.Se periptwsh pou leipei mia plhroforia vazw default values (p.x
                    # Άγνωστος Τίτλος)
                    volume_info = item.get('volumeInfo', {})
                    title = volume_info.get('title', 'Άγνωστος Τίτλος')

                    authors_list = volume_info.get('authors', ['Άγνωστος Συγγραφέας'])
                    authors = ", ".join(authors_list)

                    published_date = volume_info.get('publishedDate', 'Άγνωστη Ημερομηνία')
                    description = volume_info.get('description', 'Δεν υπάρχει διαθέσιμη περιγραφή.')

                    # edw pernw to URL tou ekswfulou
                    image_links = volume_info.get('imageLinks', {})
                    cover_url = image_links.get('thumbnail', '')

                    # apothikeuw ths plhrofories tou vivliou se ena leksiko
                    book_data = {
                        'title': title,
                        'authors': authors,
                        'published_date': published_date,
                        'description': description,
                        'cover_url': cover_url
                    }
                    # vazw to leksiko mesa sthn lista books_data pou dhmiourghsa prin
                    books_found.append(book_data)

                return books_found
            else:
                print(f"Σφάλμα API: Κωδικός {response.status}")
                return []

    except Exception as e:
        print(f"Προέκυψε σφάλμα κατά την επικοινωνία με το API: {e}")
        return []


