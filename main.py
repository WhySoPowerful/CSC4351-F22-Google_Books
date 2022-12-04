from flask import Flask, render_template

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"


@app.route("/")
def index():
    books = [
        "The Little Life",
        "The Warmth of Other Suns",
        "The Idiot",
        "The Great Gatsby",
        "Will My Cat Eat My Eyeballs?",
    ]

    book_images = [
        "https://upload.wikimedia.org/wikipedia/en/9/94/A_Little_LIfe.jpg",
        "https://images1.penguinrandomhouse.com/cover/9780679763888",
        "https://kbimages1-a.akamaihd.net/f02b167e-e66b-46e1-8bb3-4fe05b2ea588/353/569/90/False/the-idiot-202.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg/440px-The_Great_Gatsby_Cover_1925_Retouched.jpg",
        "https://prodimage.images-bn.com/lf?set=key%5Bresolve.pixelRatio%5D,value%5B1%5D&set=key%5Bresolve.width%5D,value%5B600%5D&set=key%5Bresolve.height%5D,value%5B10000%5D&set=key%5Bresolve.imageFit%5D,value%5Bcontainerwidth%5D&set=key%5Bresolve.allowImageUpscaling%5D,value%5B0%5D&set=key%5Bresolve.format%5D,value%5Bwebp%5D&source=url%5Bhttps://prodimage.images-bn.com/pimages/9780393358490_p0_v1_s600x595.jpg%5D&scale=options%5Blimit%5D,size%5B600x10000%5D&sink=format%5Bwebp%5D",
    ]

    return render_template(
        "index.html",
        books=books,
        length_of_books=len(books),
        book_images=book_images,
        length_of_images=len(book_images),
    )

app.run(use_reloader = True, debug = True)