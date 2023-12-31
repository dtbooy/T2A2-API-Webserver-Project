from app import db, ma
from marshmallow import fields

# users_groups table Model
class UserBook(db.Model):
    # Table name
    __tablename__ = "users_books"
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    # FKs
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id", ondelete='CASCADE'), nullable=False)
    # Relationships
    user = db.relationship("User", back_populates="owned_books")
    book = db.relationship("Book", back_populates="users_books")

# Users_Groups Schema
class UserBookSchema(ma.Schema):
    user = fields.Nested("UserSchema", exclude=["password", "is_admin"])
    book = fields.Nested("BookSchema")
    class Meta:
        ordered = True
        fields = ("id", "user_id", "book_id", "user", "book")