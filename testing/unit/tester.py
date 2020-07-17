import unittest
import requests

class Test(unittest.TestCase):
    def test_input_book_valid(self):
        input_book = "a game of thrones"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 201)

    def test_novel_novel_valid(self):
        r = requests.get("http://127.0.0.1:5000/novel_novel")
        self.assertEqual(r.status_code, 200)
        self.assertIn("original_title", r.json())

    def test_input_book_invalid(self):
        input_book = "the way i am"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 400)
    
    def test_input_book_all_caps(self):
        input_book = "A GAME OF THRONES"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 201)

    def test_input_book_all_nums(self):
        input_book = "94646854163"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 400)

    def test_input_book_spl_chars(self):
        input_book = "as $ Tawe"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 400)

    def test_input_book_num_char_valid(self):
        input_book = "1776"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 201)

    def test_input_book_num_splchar_valid(self):
        input_book = "New Moon (Twilight, #2)"
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 201)

    def test_input_book_empty(self):
        input_book = ""
        json = {
            "title": input_book
        }
        r = requests.post("http://127.0.0.1:5000/input_book", json=json)
        self.assertEqual(r.status_code, 400)

unittest.main()