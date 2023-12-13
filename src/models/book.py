#----------------------------------------------------------------------|---|
from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

CATEGORIES = [
    "art", "australiana", "biography", "children", "computers", "cooking", 
    "gardening", "fantasy", "fiction", "health", "history", "hobbies", "humour", 
    "literature", "philosophy", "reference", "scifi", "sport", 
    "travel"
    ]

# Books Model
class Book(db.Model):
    # Table name
    __tablename__ = "books"
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    series = db.Column(db.String)    
    # Relationships
    authors = db.relationship("BookAuthor", back_populates="book", cascade="all, delete-orphan")
    isbns = db.relationship("Isbn", back_populates="book", cascade="all, delete-orphan")
    users_books = db.relationship("UserBook", back_populates="book", cascade="all, delete-orphan")
    wanted_books = db.relationship("WantedBook", back_populates="book", cascade="all, delete-orphan")

class BookSchema(ma.Schema):
    # Relationship fields
    isbns = fields.Pluck("IsbnSchema", "isbn", many=True)
    authors = fields.Pluck("BookAuthorSchema", "author", many=True)
    # Validators
    category = fields.String(validate=OneOf(CATEGORIES))
    class Meta:
        ordered = True
        fields = ("id", "title", "category", "series", "isbns", "authors")


