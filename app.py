from app import db, create_app, DB_NAME
import os

app = create_app()

if not os.path.exists(DB_NAME):
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
