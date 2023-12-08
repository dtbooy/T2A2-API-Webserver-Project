from app import db, ma
from marshmallow import fields

# Users Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # user_groups = db.relationship("UserGroup", back_populates="user")

class UserSchema(ma.Schema):
    # user_groups = fields.Pluck("UserGroupSchema", "name")
    class Meta:
        ordered = True
        fields = ('id', 'username', 'password', "reviews")