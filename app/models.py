from app import db, login_manager
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Books(db.Model):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    book_id = Column(String(20), nullable=False)
    title = Column(String(100), nullable=False)
    author = Column(String(50))
    description = Column(String(500))
    thumbnail_link = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __init__(self, book_id, title, author, description, thumbnail_link, user_id):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.thumbnail_link = thumbnail_link
        self.user_id = user_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
class Users(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(10), nullable=False)
    password = Column(String(500), nullable=False)
    books = relationship("Books", cascade="all, delete-orphan", backref=backref("user"))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
