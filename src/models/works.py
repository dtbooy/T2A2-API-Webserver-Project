from app import db, ma
from marshmallow import fields

# Works table
class Work(db.Model):
    # Table name
    __tablename__ = 'works'
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    # FKs
    author_id = db.Column(db.Integer, db.ForeignKey(
        "authors.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id"), nullable=False)
    # Relationships
    author = db.relationship("Author", back_populates="works")
    book = db.relationship("Book", back_populates="works")

# Works Schema
class WorkSchema(ma.Schema):
    # author = fields.Nested("AuthorSchema", exclude=["works"])
    # book = fields.Pluck("BookSchema", "title")
    class Meta:
        ordered = True
        fields = ('id', 'author_id', 'book_id')
        