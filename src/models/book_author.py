from app import db, ma
from marshmallow import fields

# Works table
class BookAuthor(db.Model):
    # Table name
    __tablename__ = "works"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # FKs
    author_id = db.Column(db.Integer, db.ForeignKey(
        "authors.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id"), nullable=False)
    # Relationships
    author = db.relationship("Author", back_populates="authors")
    book = db.relationship("Book", back_populates="authors")

# Works Schema
class BookAuthorSchema(ma.Schema):
    author = fields.Nested("AuthorSchema")
    book = fields.Pluck("BookSchema", "title")
    class Meta:
        ordered = True
        fields = ("id", "author_id", "book_id", "author")
        