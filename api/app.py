import logging as logger
from flask import Blueprint, jsonify, request
import pandas as pd
from .GoodReadsGraph import BuildGraph

main = Blueprint('main', __name__)
logger.debug("App starting")

BigGraph, titles_dict = BuildGraph()
logger.debug("Graph is built service")

books = pd.read_csv("api/data/goodbooks-10k-master/books.csv")

output_URL = ""
output_URL2 = ""
output_URL1 = ""
ids = []
titles = []
seperator = ";"

@main.route('/input_book', methods=['POST'])
def input_book():
    logger.debug("Starting service")
    _book = request.get_json()
    # Extract the title from our JSON
    _book_title = str(_book["title"])
    logger.debug("book: ", _book_title)
    # The dictionary created during graph construction and the object for the book is created.
    # It is this object that is passed to the function and NOT the string.
    try:
        _book_object = titles_dict[_book_title.lower()]["Book"]
        logger.debug(_book_object)
        # The parameter N below specifies the number of books to be fetched.
        book_list = BigGraph.book2book(_book_object, N=5)

        # Here we are trying to capture all of the books recommended through the graph into a string.
        # Every individual book will be of the format "bookName,isbn"
        # Every "book" entity is separated by a ";" as "book1;book2"
        # The same pattern is used in the js file to retrieve the details
        global output_URL, seperator
        output_URL = ""
        titles = []
        for i in book_list:
            titles.append(str(i.title) + "," + str(i.isbn))
        output_URL = ";".join(titles)
        return "Done", 201
    except Exception as e:
        logger.warning("Encountered exception: ", e)
        return "Error", 400

# This function actually returns the list of books to the react.
@main.route('/novel_novel', methods=['GET'])
def novel_novel():
    logger.debug("GET method returning output_url")
    return jsonify({"original_title": output_URL}), 200