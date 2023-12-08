#----------------------------------------------------------------------|---|
from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

CATEGORIES = [
    "art and music", "Australiana", "biography", "children's books", 
    "computers", "cooking", "economics", "gardening", "fiction", 
    "health", "history", "hobbies", "humour and religion", 
    "languages other than English", "literature and classics", 
    "philosophy", "reference", "science", "science fiction", "sport", 
    "travel"
    ]

# Books Model
class Book(db.Model):
    # Table name
    __tablename__ = "book"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    series = db.Colum(db.String)    
    # Relationships
    works = db.relationship("Work", back_populates="book")
    isbns = db.relationship("Isbn", back_populates="book")
    bookshelves = db.relationship("Bookshelf", back_populates="books")
    wishlists = db.relationship("Wishlist", back_populates="books")

class BookSchema(ma.Schema):
    isbns = fields.Nested("IsbnSchema", many=True, only=["isbn"])
    category = fields.String(validate=OneOf(CATEGORIES))
    class Meta:
        ordered = True
        fields = ("id", "title", "series", "isbns")