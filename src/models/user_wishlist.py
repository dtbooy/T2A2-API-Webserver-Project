from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf

QUALITIES = ["any", "fair", "good", "mint"]

# users_groups table Model
class UserWishlist(db.Model):
    # Table name
    __tablename__ = 'users_wishlists'
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    quality = db.Column(db.String, default="any")
    # FKs
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        "books.id"), nullable=False)
    # Relationships
    user = db.relationship("User", back_populates="users_wishlists")
    book = db.relationship("Book", back_populates="users_wishlists")

# Users_Groups Schema
class UserWishlistSchema(ma.Schema):
    user = fields.Nested("UserSchema", exclude=["password", "is_admin"])
    book = fields.Pluck("BookSchema", "title")
    quality = fields.String(validate=OneOf(QUALITIES))
    class Meta:
        ordered = True
        fields = ('id', 'user_id', 'book_id')