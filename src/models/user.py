from app import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# Users Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    groups = db.relationship("UserGroup", back_populates="user", cascade="all, delete-orphan")
    owned_books = db.relationship("UserBook", back_populates="user", cascade="all, delete-orphan")
    users_wishlists = db.relationship("UserWishlist", back_populates="user", cascade="all, delete-orphan")

class UserSchema(ma.Schema):
    groups = fields.Pluck("UserGroupSchema", "group", many=True)
    password = fields.String(validate=Length(min=6)) 
    owned_books = fields.Nested("UserBookSchema", many=True, only=["book"])
    class Meta:
        ordered = True
        fields = ('id', 'username', 'password', "email", "is_admin", "groups", "owned_books")