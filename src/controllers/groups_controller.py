from app import db, bcrypt
from models.group import Group, GroupSchema
from models.user_group import UserGroup, UserGroupSchema
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, abort
from datetime import timedelta
from controllers.auth_controller import is_admin, is_group_or_admin, is_user_or_admin, is_user_group_admin_or_admin

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
    return GroupSchema(many=True, exclude=["password"]).dump(groups)

# READ: SINGLE GROUP
@groups.route("/<int:group_id>", methods=["GET"])
@jwt_required()
def get_group(group_id):
    # Only administrator or user in group_id can access group
    is_group_or_admin(group_id)
    # Database query: return group with group_id
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    if not group:
        return {"error" : "Group not found"}, 404
    return GroupSchema(exclude=["password"]).dump(group)

# CREATE GROUP
@groups.route("/", methods=["POST"])
@jwt_required()
def create_group():
    # Required fields = [name, admin_id] optional fields=[password]
    group_info = GroupSchema(only=["name", "password", "admin_id"]).load(request.json)
    
    # Search DB for group with same name
    stmt = db.select(Group).where(Group.name==group_info["name"])
    group = db.session.scalar(stmt)
    if group:
        return {"Error": "Group exists with that name"}, 400
    
    # Create Group Object
    group =  Group()
    group.name=group_info["name"]
    if group_info.get("password", None):
        group.password=bcrypt.generate_password_hash(group_info["password"]).decode("utf-8"),

    # return User record with id stored in admin_id
    stmt = db.select(User).where(User.id==group_info.get("admin_id", None))
    admin_user = db.session.scalar(stmt)
    if admin_user:
        group.admin_id=group_info["admin_id"]
    else:
        group.admin_id=get_jwt_identity()

    # Add new Group to session and flush
    db.session.add(group)
    db.session.flush()

    # Add group creator as member of new group
    member = UserGroup(
        user_id=get_jwt_identity(),
        group_id=group.id
    )
    db.session.add(member)
    db.session.commit()
    # return 201 created and Group details
    return GroupSchema(exclude=["password"]).dump(group), 201

# DELETE GROUP
@groups.route("/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_group(group_id):
    # Database query: return group with id <group_id>
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)

    # Only administrator or group admin user can delete group
    is_user_or_admin(group.admin_id)

    # Ensure book exists
    if not group:
        return {"Error": "Group not found"}, 404
    # delete group from database & commit
    db.session.delete(group)
    db.session.commit()
    # return empty body & 204 No Content response to confirm delete
    return {}, 204

# UPDATE GROUP
@groups.route("/<int:group_id>", methods=["PATCH", "PUT"])
@jwt_required()
def update_group(group_id):
    # fields [name, password, admin_id]
    # Confirm group exists
    # Database query: return group with group_id
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    if not group:
        return {"Error": "Group not found"}, 404
    # Validate Authority: Only administrator or group admin user can change group details
    is_user_or_admin(group.admin_id)
    # Validate updated group info through schema 
    group_info = GroupSchema(exclude=["id"]).load(request.json)
    
    # If updated group name provided, update group name (If changed)
    if group_info.get("name", None) and group_info.get("name", None) != group.name:
        # Validate new group name unique
        # Search DB for group with new group name
        stmt = db.select(Group).where(Group.name==group_info["name"])
        group_name = db.session.scalar(stmt)
        # Return Error if group name taken
        if group_name:
            return {"Error": "Group exists with that name"}, 400
        group.name = group_info.get("name", group.name) 
    
    # If updated group admin_id provided update group_admin
    if group_info.get("admin_id", None):
        # DB Search: check provided user <admin_id> is a member of group <group_id> 
        stmt = db.select(UserGroup).where(UserGroup.user_id == group_info["admin_id"], UserGroup.group_id == group_id)
        admin = db.session.scalar(stmt)
        # Only update if user exists and is member of group
        if admin:
            group.admin_id = group_info.get("admin_id", group.admin_id)

    # update password
    if group_info.get("password", None):
        group.password = bcrypt.generate_password_hash(group_info["password"]).decode("utf-8")

    db.session.commit()
    # exclude password hash in json return
    return GroupSchema(exclude=["password", "users"]).dump(group), 200

# JOIN GROUP
@groups.route("/<int:group_id>", methods=["POST"])
@jwt_required()
def join_group(group_id):
    # Check if already a member (db lookup UserGroup for matching user/group entry)
    stmt = db.select(UserGroup).where(UserGroup.group_id == group_id, UserGroup.user_id == get_jwt_identity())
    member = db.session.scalar(stmt)
    if member:
        return {"error" : "User already member of this group"}, 400

    join_info = GroupSchema(only=["password"]).load(request.json)
    # Database query: return group with group_id
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    # Check group exists
    if not group:
        # return 401 (Unauthorised error) if invalid password
        return {"error": "Group not found"}, 404
    # check password hash matches
    if group.password and not bcrypt.check_password_hash(group.password, join_info["password"]):
        return {"error": "Invalid passphrase to join group"}, 401
    # Add member to group (insert user_id/Group_id pair into user_groups table)
    member = UserGroup(
        user_id=get_jwt_identity(),
        group_id=group_id
    )
    db.session.add(member)
    db.session.commit()

    # Return group listing
    stmt = db.select(Group).filter_by(id=group_id)
    group = db.session.scalar(stmt)
    return GroupSchema(exclude=["password"]).dump(group), 201

# REMOVE GROUP MEMBER
@groups.route("/<int:group_id>/members/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_member(group_id, user_id):
    # Admin, group admin or <user_id> can remove <user_id> from group
    is_user_group_admin_or_admin(user_id, group_id) 
    # Database query: return user_group pair with <group_id> & <user_id>
    stmt = db.select(UserGroup).where(UserGroup.user_id == user_id, UserGroup.group_id==group_id)
    user_group = db.session.scalar(stmt)
    # Ensure user group pair exists
    if not user_group:
        return {"Error": "User not found in Group"}, 404
    # delete user_group pair from database & commit
    db.session.delete(user_group)
    db.session.commit()

    # Check if group has any other members - if not DELETE
    # Database query: return user_group pairs with <group_id> 
    stmt = db.select(UserGroup).where(UserGroup.group_id==group_id)
    group_users = db.session.scalar(stmt)
    # if group users is empty - no members exist - delete
    if not group_users:
        # return Group with id stored in group_id
        stmt = db.select(Group).where(Group.id==group_id)
        group = db.session.scalar(stmt)
        db.session.delete(group)
        db.commit()

    # Return empty body & 204 No Content response to confirm delete
    return {}, 204

from models.wanted_book import WantedBook

# GET ALL BOOKS GROUP USERS WANT
@groups.route("/<int:group_id>/wanted-books", methods=["GET"])
@jwt_required()
def get_group_books(group_id):
    # Only members can see booklist
    is_group_or_admin(group_id)
    # output wanted_books where User_id in (user_groups.userid (where usergroup == group)
    # Return All Users in Group with id stored in sgroup id 
    stmt = db.select(User).join(UserGroup).join(Group).where(Group.id == group_id)
    users = db.session.scalars(stmt)
    # return each Users username and wanted books
    return UserSchema(only =["username", "wanted_books"], many=True).dump(users)
