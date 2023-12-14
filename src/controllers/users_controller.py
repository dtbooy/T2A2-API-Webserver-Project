from app import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, abort
from controllers.owned_books_controller import owned_books
from controllers.wanted_books_controller import wanted_books
from controllers.auth_controller import is_admin, is_user_or_admin

users = Blueprint("users", __name__, url_prefix="/users")
users.register_blueprint(owned_books)
users.register_blueprint(wanted_books)

# READ: ALL USERS
@users.route("/", methods=["GET"])
@jwt_required()
def get_users():
    # Only administrators can access user lists
    is_admin()
    # Database query: return all users
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    # exclude password hash in json Return
    return UserSchema(many=True, only=["id", "username", "email", "groups"]).dump(users)

# READ: SINGLE USER
@users.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    # Only administrator or <user_id> can access <user_id>
    is_user_or_admin(user_id)
    # Database query: return user with user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # exclude password hash in json Return
    if not user:
        abort(404, "user does not exist")
    return UserSchema(only=["id", "username", "email", "groups"]).dump(user)

# UPDATE: USER
@users.route("/<int:user_id>", methods=["PATCH", "PUT"])
@jwt_required()
def update_user(user_id):
    # Only administrator or <user_id> can change <user_id> details
    is_user_or_admin(user_id)
    
    # Database query: return user with user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        return {"Error": "User not found"}, 404
    # validate updated user info through schema 
    user_info = UserSchema(only=["password", "email"]).load(request.json)
    
    user.email = user_info.get("email", user.email)
    if user_info.get("password", None):
        user.password = bcrypt.generate_password_hash(user_info["password"])

    # exclude password hash in json return
    return UserSchema(only=["id", "username", "email"]).dump(user), 200

# DELETE: SINGLE USER
@users.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    # Only administrator or <user_id> can delete <user_id>
    is_user_or_admin(user_id)
    # Database query: return user with the user id user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Ensure user exists
    if not user:
        abort(404, description= "User doesn't exist")
    # delete user from database & commit
    db.session.delete(user)
    db.session.commit()
    # return empty body & 204 No Content response
    return {}, 204

