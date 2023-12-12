from app import db, ma
from marshmallow import fields

# Authors Model
class Author(db.Model):
    # Table name
    __tablename__ = "authors"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    surname = db.Column(db.String, nullable=False)
    given_names = db.Column(db.String)
    # Relationships
    book_authors = db.relationship("BookAuthor", back_populates="author", cascade="all, delete-orphan")

class AuthorSchema(ma.Schema):
    
    class Meta:
        ordered = True
        fields = ("id", "surname", "given_names")