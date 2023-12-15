from app import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# Users Model
class User(db.Model):
    # Table name
    __tablename__ = "users"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    # Relationships
    groups = db.relationship("UserGroup", back_populates="user", cascade="all, delete-orphan")
    owned_books = db.relationship("UserBook", back_populates="user", cascade="all, delete-orphan")
    wanted_books = db.relationship("WantedBook", back_populates="user", cascade="all, delete-orphan")

class UserSchema(ma.Schema):
    groups = fields.Pluck("UserGroupSchema", "group", many=True)
    password = fields.String(validate=Length(min=6)) 
    owned_books = fields.Pluck("UserBookSchema", "book", many=True)
    wanted_books = fields.Nested("WantedBookSchema", only=["book","quality"], many=True)
    class Meta:
        ordered = True
        fields = ("id", "username", "password", "email", "is_admin", "groups", "owned_books", "wanted_books")