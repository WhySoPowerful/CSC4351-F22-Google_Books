from flask import Flask, render_template
import requests

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

base_url = "https://www.googleapis.com/books/v1"

@app.route("/")
def index():
    book_ids = ["Lf99BAAAQBAJ", "dt6JDQAAQBAJ", "SfeuDwAAQBAJ", "3IAUEAAAQBAJ", "CPOPDwAAQBAJ"]
    books = []
    book_images = []

    for id in book_ids:
        response = requests.get(f"{base_url}/volumes/{id}")
        data = response.json()

        books.append(data["volumeInfo"]["title"])
        book_images.append(data["volumeInfo"]["imageLinks"]["thumbnail"])


    return render_template(
        "index.html",
        books=books,
        length_of_books=len(books),
        book_images=book_images,
        length_of_images=len(book_images),
    )

app.run(use_reloader = True, debug = True)