from app import db, ma
from marshmallow import fields

# Groups Model
class Group(db.Model):
    # Table name
    __tablename__ = "groups"
    # PK
    id = db.Column(db.Integer, primary_key=True)
    # Attributes
    rname = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    # Relationships
    users_groups = db.relationship("UserGroup", back_populates="group")

class GroupSchema(ma.Schema):
    users = fields.Nested("UserGroupSchema", many=True, only=["user"])
    class Meta:
        ordered = True
        fields = ("id", "name", "password", "users")
        load_only = ("password")