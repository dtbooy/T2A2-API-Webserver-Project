from app import db, ma
from marshmallow import fields

# Groups Model
class Group(db.Model):
    # Table name
    __tablename__ = "groups"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Relationships
    users = db.relationship("UserGroup", back_populates="group", cascade="all, delete-orphan")
    # admin = db.relationship("")

class GroupSchema(ma.Schema):
    users = fields.Pluck("UserGroupSchema", "user", many=True)

    class Meta:
        ordered = True
        fields = ("id", "name", "users", "password")

