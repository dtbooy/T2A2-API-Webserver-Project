from app import db, ma
from marshmallow import fields

# Users Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    users_groups = db.relationship("UserGroup", back_populates="user", cascade="all, delete-orphan")
    users_books = db.relationship("UserBook", back_populates="user", cascade="all, delete-orphan")
    users_wishlists = db.relationship("UserWishlist", back_populates="user", cascade="all, delete-orphan")

class UserSchema(ma.Schema):
    user_groups = fields.Pluck("UserGroupSchema", "group")
    class Meta:
        ordered = True
        fields = ('id', 'username', 'password', "is_admin")