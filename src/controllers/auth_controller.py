from app import db, bcrypt
from flask import Blueprint, request, abort
from models.user import User, UserSchema
from models.user_group import UserGroup
from models.group import Group
from flask_jwt_extended import create_access_token, get_jwt_identity
from datetime import timedelta

auth = Blueprint("auth", __name__)

# Auth routes
# LOGIN
@auth.route("/login", methods=["POST"])
def auth_login():
    # Load username & password from request.json
    login = UserSchema(only=["username", "password"]).load(request.json)
    # Pull user details from the database
    stmt = db.select(User).filter_by(username=login["username"])
    user = db.session.scalar(stmt)
    # Check username exists & password hash matches
    if not user or not bcrypt.check_password_hash(user.password, login["password"]):
        # return 401 (Unauthorised error) if invalid username / password
        return {"Error": "Username or password invalid"}, 401

    # Create JWT token for user session
    token = create_access_token(user.id, expires_delta=timedelta(hours=1))
    return {"Username" : user.username, "Token" : token}, 200

# CREATE USER
@auth.route("/register", methods=["POST"])
def auth_register():
    # Load user details from request.json. exclude: id (autogenerated) & is_admin 
    # (can only be set by existing admin).
    # Required fields = [username, password]
    user_info = UserSchema(only=["username", "password", "email"]).load(request.json)
    
    # check if user exists
    stmt = db.select(User).where(User.username==user_info["username"])
    user = db.session.scalar(stmt)
    if user:
        return {"Error": "Username exists"}, 400
    
    user =  User(
        username=user_info["username"],
        password=bcrypt.generate_password_hash(user_info["password"]).decode("utf8"),
        email = user_info.get("email", None)
    )
    # Add new user to db
    db.session.add(user)
    db.session.commit()
    # create a token for the new user 
    token = create_access_token(user.id, expires_delta=timedelta(hours=1))
    return {"ID": user.id, "Username" : user.username, "Email" : user.email, "Token" : token}, 201

# AUTH FUNCTIONS
# CHECK IF USER HAS ADMINISTRATOR ACCESS
def is_admin():
    user_id = get_jwt_identity()
    # Database query: return user with the user id stored in user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # If user does not exist or is not an administrator, abort
    if not user or not user.is_admin:
        abort(403, description="Unauthorised - Admin privilages required to perform this action")

# CHECK IF USER IS ADMIN OR ACCESSING OWN DATA
def is_user_or_admin(id):
    auth_id = get_jwt_identity()
    # Database query: return user with the user id stored in auth_id
    stmt = db.select(User).filter_by(id=auth_id)
    user = db.session.scalar(stmt)
    # Make sure it is in the database
    if not user or not (auth_id == id or user.is_admin):
        abort(403, description="Unauthorised: Access denied")

def is_group_or_admin(group_id):
    # Database query: return user with the user id stored in auth_id
    stmt = db.select(User).where(User.id == get_jwt_identity(), User.is_admin == True)
    user = db.session.scalar(stmt)
    stmt = db.select(UserGroup).where(UserGroup.group_id == group_id, UserGroup.user_id == get_jwt_identity())
    member = db.session.scalar(stmt)
    #Make sure it is in the database
    if not member and not user:
        abort(403, description="Unauthorised: Access denied")

def is_user_group_admin_or_admin(user_id, group_id):
    # Database query: return user with the user id stored in auth_id
    auth_id =get_jwt_identity()
    stmt = db.select(User).where(User.id == auth_id, User.is_admin == True)
    user = db.session.scalar(stmt)
    stmt = db.select(Group).where(Group.id == group_id)
    group = db.session.scalar(stmt)
    #Make sure it is in the database
    if not (auth_id == user_id or auth_id == group.admin_id or user):
        abort(403, description="Unauthorised: Access denied")