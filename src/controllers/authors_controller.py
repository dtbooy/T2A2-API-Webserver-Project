from app import db 
from models.author import Author, AuthorSchema
from flask_jwt_extended import jwt_required 
from flask import Blueprint, request
from controllers.auth_controller import is_admin

authors = Blueprint("authors", __name__, url_prefix="/authors")

# GET ALL AUTHORS
@authors.route("/", methods=["GET"])
@jwt_required()
def get_authors():
    # DB search - return all authors from author table
    stmt = db.select(Author)
    authors = db.session.scalars(stmt)
    return AuthorSchema(many=True).dump(authors), 200

# CREATE: ADD AUTHOR
@authors.route("/", methods=["POST"])
@jwt_required()
def add_author():
    # Verify user credentials - only admin can add author
    is_admin()
    # input data required = [surname] optional = [given_names]
    # Load author data through schema
    author_info = AuthorSchema(exclude=["id"]).load(request.json)
    # Check Author isn't already in database
    stmt = db.select(Author).where(Author.surname == author_info["surname"], Author.given_name == author_info.get("given_name"), None)
    check = db.session.scalar(stmt)
    if check:
        return {"error": f"Author already exists, id={check.id}"}, 400

    # Add Author to DB
    author = Author(
        surname = author_info["surname"],
        given_name = author_info.get("given_name")
    )
    db.session.add(author)
    db.session.commit()

    return AuthorSchema().dump(author), 201

# UPDATE AUTHOR
@authors.route("/<int:author_id>", methods=["PATCH, PUT"])
@jwt_required()
def add_author(author_id):
    # Verify user credentials - only admin can update author
    is_admin()
    # input data required = [] optional = [surname, given_names]
    # Load author data through schema
    author_info = AuthorSchema(exclude=["id"]).load(request.json)
    # Check Author exists
    stmt = db.select(Author).where(Author.id == author_id)
    author = db.session.scalar(stmt)
    if not author:
        return {"error": "Author not found"}, 400

    # Add Author to DB
    author.surname = author_info.get("surname"),
    author.given_name = author_info.get("given_name")
    db.session.commit()
    return AuthorSchema().dump(author), 200

# DELETE AUTHOR
@authors.route("/<int:author_id>", methods=["DELETE"])
@jwt_required()
def delete_author(author_id):
    # Verify user credentials - only admin can remove authors
    is_admin()
    # DB Search for Author ID (ensure author exists to delete)
    stmt = db.select(Author).where(Author.id == author_id)
    author = db.session.scalar(stmt)
    # Return 404 error if author not in database
    if not author:
         return {"error": "Author not found"}, 404
    db.session.delete(author)
    db.session.commit()
    return {}, 204