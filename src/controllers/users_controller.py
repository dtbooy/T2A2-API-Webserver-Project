from app import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from flask import Blueprint, request
from datetime import timedelta

auth = Blueprint("auth", __name__, url_prefix="/auth")

# Auth routes
@auth.route("/login", methods=["POST"])
def auth_login():
    # request.json is the post data
    login = UserSchema(exclude=["id"]).load(request.json)
    # pull user details from the database
    stmt = db.select(User).where(User.username==login["username"])
    user = db.session.scalar(stmt)
    # Check username & password
    if not user or not bcrypt.check_password_hash(user.password, login["password"]):
        return {"Error": "Username or password invalid"}, 412

    token = create_access_token(user.id, expires_delta=timedelta(hours=1))
    return {"Username" : user.username, "Token" : token}, 200

@auth.route("/register", methods=["POST"])
def auth_register():
    # get user info
    user_info = UserSchema().load(request.json)
    # Check adequate password length
    if len(user_info["password"]) <= 8:
        return {"Error": "Password must be at least 8 characters"}, 400
    
    # check if user exists
    stmt = db.select(User).where(User.username==user_info["username"])
    exist = db.session.scalar(stmt)
    if exist:
        return {"Error": "Username exists"}, 400
    
    # Add new user to db
    db.session.add(
        User(
            username=user_info["username"],
            password=bcrypt.generate_password_hash(user_info["password"]).decode("utf-8")
        )
    )
    db.session.commit()
    # check the name is in the db
    user = db.session.scalar(db.select(User).where(User.username==user_info["username"]))
    # create a token for the new user 
    token = create_access_token(user.id, expires_delta=timedelta(hours=1))
    return {"Username" : user.username, "Token" : token}, 201

@auth.route("/", methods=["GET"])
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=["password"]).dump(users)