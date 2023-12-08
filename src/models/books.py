from app import db, ma
from marshmallow import fields

# Books Model
class Book(db.Model):
    # Table name
    __tablename__ = "book"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    title = db.Column(db.String, nullable=False)
    catagory = db.Column(db.String)
    series = db.Colum(db.String)
    # Relationships
    works = db.relationship("Work", back_populates="book")
    isbns = db.relationship("Isbn", back_populates="book")
    bookshelves = db.relationship("Bookshelf", back_populates="books")
    wishlists = db.relationship("Wishlist", back_populates="books")

class UserSchema(ma.Schema):
    isbns = fields.Nested("IsbnSchema", many=True, exclude=["book"])
    class Meta:
        ordered = True
        fields = ("id", "title", "series", "isbns")