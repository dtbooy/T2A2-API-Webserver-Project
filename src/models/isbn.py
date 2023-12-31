from app import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# ISBN table model
class Isbn(db.Model):
    # Table name
    __tablename__ = "isbns"
    # PK
    isbn = db.Column(db.String(13), primary_key=True, autoincrement=False)
    # FK
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id", ondelete='CASCADE'), nullable=False)
    # Relationships
    book = db.relationship("Book", back_populates="isbns")

class IsbnSchema(ma.Schema):
    book = fields.Nested("BookSchema", exclude=["isbns"])
    isbn = fields.String(validate=Length(max=13)) 
    class Meta:
        ordered = True
        fields = ("isbn", "book_id", "book")

