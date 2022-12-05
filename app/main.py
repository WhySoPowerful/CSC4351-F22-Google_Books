from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models import Books
import requests


main = Blueprint("main", __name__)

base_url = "https://www.googleapis.com/books/v1"


@main.route("/home", methods=["POST", "GET"])
@login_required
def index():
    books = []
    book_images = []    

    book_list = Books.query.filter(Books.user_id == current_user.id).all()
    for book in book_list:
        books.append(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author
            }
        )
        book_images.append(book.thumbnail_link)


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
                    "id": data["items"][i]["id"],
                    "title": data["items"][i]["volumeInfo"]["title"],
                    "description": data["items"][i]["volumeInfo"]["description"].split(".")[0]
                    if "description" in data["items"][i]["volumeInfo"]
                    else None,
                    "author": data["items"][i]["volumeInfo"]["authors"][0]
                    if "authors" in data["items"][i]["volumeInfo"]
                    else None,
                    "thumbnail": data["items"][i]["volumeInfo"]["imageLinks"]["thumbnail"] if "imageLinks" in data["items"][i]["volumeInfo"] else None,
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

# Add to favourites
@main.route("/add/<book_id>")
@login_required
def add(book_id):
    check_book = Books.query.filter(Books.book_id == book_id).first()
    if check_book:
        flash(f"'{check_book.title}' is already favorited")
        return (redirect(url_for("main.index")))

    response = requests.get(f"{base_url}/volumes/{book_id}")
    data = response.json()

    title = data["volumeInfo"]["title"]
    description = data["volumeInfo"]["description"].split(".")[0] if "description" in data["volumeInfo"] else None
    author = data["volumeInfo"]["authors"][0] if "authors" in data["volumeInfo"] else None
    thumbnail = data["volumeInfo"]["imageLinks"]["thumbnail"] if "imageLinks" in data["volumeInfo"] else None

    try:
        new_book = Books(book_id=book_id, title=title, author=author, description=description, thumbnail_link=thumbnail, user_id=current_user.id)
        new_book.insert()
        message = f"Successfully added '{title}' to favorites"
    except:
        message = f"Failed to add '{title}' to favorites"
        abort(500)
    finally:
        flash(message)

    return redirect(url_for("main.index"))

# Remove from favourites
@main.route("/remove/<int:book_id>")
@login_required
def remove(book_id):
    book = Books.query.get(book_id)
    if not book:
        abort(404)

    try:
        book.delete()
        message = f"Removed '{book.title}' from favorites"
    except:
        message = f"Failed to remove '{book.title}' from favorites"
        abort(500)
    finally:
        flash(message)

    return redirect(url_for("main.index"))
