from flask import Flask, render_template, request
import requests

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

base_url = "https://www.googleapis.com/books/v1"


@app.route("/", methods=["POST", "GET"])
def index():
    book_ids = [
        "Lf99BAAAQBAJ",
        "dt6JDQAAQBAJ",
        "SfeuDwAAQBAJ",
        "3IAUEAAAQBAJ",
        "CPOPDwAAQBAJ",
    ]
    books = []
    book_images = []

    for id in book_ids:
        response = requests.get(f"{base_url}/volumes/{id}")
        data = response.json()

        books.append(data["volumeInfo"]["title"])
        book_images.append(data["volumeInfo"]["imageLinks"]["thumbnail"])

    if request.method == "GET":

        return render_template(
            "index.html",
            books=books,
            length_of_books=len(books),
            book_images=book_images,
            length_of_images=len(book_images),
        )

    elif request.method == "POST":
        search_term = request.form.get("search")
        results = []
        response = requests.get(f"{base_url}/volumes?q={search_term}&maxResults=5")
        data = response.json()

        for i in range(5):
            results.append(
                {
                    "title": data["items"][i]["volumeInfo"]["title"],
                    "subtitle": data["items"][i]["volumeInfo"]["subtitle"]
                    if "subtitle" in data["items"][i]["volumeInfo"]
                    else None,
                    "author": data["items"][i]["volumeInfo"]["authors"][0]
                    if "authors" in data["items"][i]["volumeInfo"]
                    else None,
                    "thumbnail": data["items"][i]["volumeInfo"]["imageLinks"][
                        "thumbnail"
                    ],
                }
            )

        return render_template(
            "index.html",
            books=books,
            length_of_books=len(books),
            book_images=book_images,
            length_of_images=len(book_images),
            results=results,
            search_term=search_term,
        )


app.run(use_reloader=True, debug=True)
