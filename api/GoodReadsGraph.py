import pandas as pd
import numpy as np

class Graph(object):
    def __init__(self, reads):
        # Edges in our graph
        self.reads = reads

    def book2book(self, input_Book, N=3 , debug=False):
        """
        Returns a list of N books recommended to the user using the database
        Params:
            1. self: the object
            2. input_book: the book input by the user based on which recommendations are given
            3. N: the number of books which are to be recommended.
        """
        # returns the popularity index of the book which was calculated during the building of the graph
        def _sort_tuple(tuple_val):
            return tuple_val[1]

        out_recs = []
        for i in range(N):
            _reader_list = input_Book.reader_list
            _len_rl = len(_reader_list)
            _rand_User = _reader_list[np.random.randint(_len_rl)]
            _list = [(book, book.popularity, rating) for book, rating in _rand_User.shelf
                    if rating > 4] 
            _list = sorted(_list, key=_sort_tuple, reverse=True)
            book, popularity, rating = _list[0]
            out_recs.append(book)

        return out_recs

class User(object):
    def __init__(self,user_id):
        self.user_id = user_id
        self.shelf = [] # Books read
        self.author_list = [] # Authors read

class Book(object):
    def __init__(self, book_id, original_title, isbn, Author, ratings_5, popularity, image_url):
        self.book_id = book_id
        self.title = original_title
        self.isbn = isbn
        self.author = Author
        self.author_id = Author.author_id
        self.ratings_5 = ratings_5 # Number of people that rated the book a 5
        self.popularity = popularity # What fraction of ratings does this book have?+
        self.image_url = image_url
        self.reader_list = [] #Users that read the book

    def add_reader(self,User):
        if User not in self.reader_list:
            self.reader_list.append(User) # User read this book

class Author(object):
    def __init__(self, author_id):
            self.author_id = author_id
            self.reader_list = [] #People who read the book

    def add_reader(self,User):
        if User not in self.reader_list:
            self.reader_list.append(User) # User read this book

# This class finally connects all the three classes above
class Read(object):
    def __init__(self, User, Book, Author, rating=None):
        if Book not in User.shelf:
            User.shelf.append((Book, rating)) # User read this book and rated it.
        if Author not in User.author_list:
            User.author_list.append(Author)

        self.user = User
        self.book = Book
        self.author = Author
        self.rating = rating # Optional

        Book.add_reader(User)
        Author.add_reader(User)


def BuildGraph():
    uir = pd.read_csv("api/data/goodbooks-10k-master/ratings.csv")
    books = pd.read_csv("api/data/goodbooks-10k-master/books.csv")

    # Drop nan values from the "title" and "isbn" column in books.csv
    books = books[books['original_title'].notnull()]
    books = books[books['isbn'].notnull()]
    
    books = books[(books["language_code"] == "eng") | (books["language_code"] == "en-US")]
    books["author_id"] = (books["authors"].astype("category")).cat.codes # Gives us an index

    # The below line has a metric for judging the popularity of a book. 
    # The formula used to judge the popularity is: "The ratio of the number of ratings of a book to 
    # the total number of ratings given to all the books"
    books["popularity_ratings"] = np.array(books["ratings_count"])/np.sum(books["ratings_count"])

    uir = pd.merge(uir, books[["book_id", "original_title", "isbn",
                               "author_id","popularity_ratings","ratings_5", "image_url"]], on=["book_id"])

    # Creating a dataframe for all the authors
    unique_authors = uir[["author_id"]].drop_duplicates()
    unique_authors["Author"] = [Author(aid) for aid in unique_authors["author_id"]]
    unique_authors = unique_authors.set_index("author_id", drop=True)

    
    # Doing the same for the users:
    unique_users = uir[["user_id"]].drop_duplicates()
    unique_users["User"] = [User(uid) for uid in unique_users["user_id"]]
    unique_users = unique_users.set_index("user_id", drop=True)

    # Converting the above two dataframes to provide better access rate to the details
    user_dict = unique_users.to_dict("index")
    author_dict =  unique_authors.to_dict("index")

    unique_books = uir[["book_id", "original_title", "isbn", "author_id", "ratings_5", "popularity_ratings",
                        "image_url"]].drop_duplicates()
    unique_books["Book"] = [Book(bid, ot, isbn, author_dict[aid]["Author"], rat, pop, url) for bid, ot, isbn, aid, rat, pop, url
                            in unique_books[
                                ["book_id", "original_title", "isbn", "author_id", "ratings_5", "popularity_ratings", "image_url"]].values]

    # Building a similar dictionary now for books
    _unique_books = unique_books.set_index("book_id", drop=True)
    _unique_books = _unique_books.drop(["author_id", "ratings_5", "popularity_ratings", "image_url"],
                                       axis=1) 
    book_dict = _unique_books.to_dict("index")

    
    _unique_titles = unique_books.copy()
    _unique_titles["original_title"] = _unique_titles["original_title"].str.lower()
    _unique_titles = _unique_titles.drop(["author_id", "book_id", "ratings_5", "popularity_ratings", "image_url"], axis=1)
    _unique_titles = _unique_titles.drop_duplicates("original_title").dropna()
    _unique_titles = _unique_titles.set_index("original_title", drop=True)
    titles_dict = _unique_titles.to_dict("index")

    # Assemble everything accumulated above to form the graph
    read_list = [Read(user_dict[u]["User"], book_dict[b]["Book"], author_dict[a]["Author"], rating=int(r))
               for u, b, a, r in uir[["user_id","book_id","author_id", "rating"]].values]

    BigGraph = Graph(read_list)

    return BigGraph, titles_dict