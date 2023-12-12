from app import db, bcrypt
from models.group import Group, GroupSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, abort
from datetime import timedelta
from controllers.auth_controller import is_admin, is_group_or_admin

groups = Blueprint("groups", __name__, url_prefix="/groups")

# READ: ALL GROUPS
@groups.route("/", methods=["GET"])
@jwt_required()
def get_groups():
    # Only administrators can access groups lists
    is_admin()
    # Database query: return all groups
    stmt = db.select(Group)
    groups = db.session.scalars(stmt)
    return GroupSchema(many=True).dump(groups)

# READ: SINGLE GROUP
@groups.route("/<int:group_id>", methods=["GET"])
@jwt_required()
def get_group(group_id):
    # Only administrator or user in group_id can access group
    is_group_or_admin(group_id)
    # Database query: return group with group_id
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)

    return GroupSchema().dump(group)