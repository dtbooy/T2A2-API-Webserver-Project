from app import db, ma
from marshmallow import fields

# users_groups table Model
class UserGroup(db.Model):
    # Table name
    __tablename__ = 'users_groups'
    # Attributes
    id = db.Column(db.Integer, primary_key=True)
    # FKs
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=False)
    # Relationships
    user = db.relationship("User", back_populates="groups")
    group = db.relationship("Group", back_populates="users")

# Users_Groups Schema
class UserGroupSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["id", "username"])
    group = fields.Pluck("GroupSchema", "name")
    class Meta:
        ordered = True
        fields = ('id', 'user_id', 'group_id', "user", "group")