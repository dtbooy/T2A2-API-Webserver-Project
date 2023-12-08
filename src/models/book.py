#----------------------------------------------------------------------|---|
from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

CATEGORIES = [
    "art and music", "Australiana", "biography", "children's books", 
    "computers", "cooking", "economics", "gardening", "fiction", 
    "health", "history", "hobbies", "humour and religion", 
    "languages other than English", "literature and classics", 
    "philosophy", "reference", "science", "science fiction & fantasy", "sport", 
    "travel"
    ]

# Books Model
class Book(db.Model):
    # Table name
    __tablename__ = "books"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    series = db.Column(db.String)    
    # Relationships
    works = db.relationship("Work", back_populates="book", cascade="all, delete-orphan")
    isbns = db.relationship("Isbn", back_populates="book", cascade="all, delete-orphan")
    users_books = db.relationship("UserBook", back_populates="book", cascade="all, delete-orphan")
    users_wishlists = db.relationship("UserWishlist", back_populates="book", cascade="all, delete-orphan")

class BookSchema(ma.Schema):
    isbns = fields.Nested("IsbnSchema", many=True, only=["isbn"])
    category = fields.String(validate=OneOf(CATEGORIES))
    class Meta:
        ordered = True
        fields = ("id", "title", "series", "isbns")