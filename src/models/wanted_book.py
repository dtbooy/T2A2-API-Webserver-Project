from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

QUALITIES = ["any", "fair", "good", "mint"]

# users_groups table Model
class WantedBook(db.Model):
    # Table name
    __tablename__ = "wantedbooks"
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String, default="any")
    # FKs
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id"), nullable=False)
    # Relationships
    user = db.relationship("User", back_populates="wanted_books")
    book = db.relationship("Book", back_populates="wanted_books")

# Users_Groups Schema
class WantedBookSchema(ma.Schema):
    user = fields.Nested("UserSchema", exclude=["password", "is_admin"])
    book = fields.Pluck("BookSchema", "title")
    quality = fields.String(validate=OneOf(QUALITIES))
    class Meta:
        ordered = True
        fields = ("id", "user_id", "book_id", "quality", "user", "book")